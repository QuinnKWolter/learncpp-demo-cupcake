"""Native C++ adapter for trusted collaborators, with bounded execution resources.

This is not an adversarial-code sandbox. See docs/DEPLOYMENT.md for its trust boundary.
"""
from pathlib import Path
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path(os.environ.get('CUPCAKE_RUNTIME_DIR', ROOT / '.runtime'))
REPORTS = Path(os.environ.get('CUPCAKE_REPORT_DIR', ROOT / 'research'))
LOCAL_COMPILER=ROOT/'.tools/gcc/mingw64/bin/g++.exe'
COMPILER = os.environ.get('CUPCAKE_CXX') or (str(LOCAL_COMPILER) if LOCAL_COMPILER.exists() else shutil.which('g++'))
STANDARD='c++23'
MAX_OUTPUT = 128 * 1024

@contextmanager
def compilation_directory():
    RUNTIME.mkdir(parents=True,exist_ok=True)
    directory=Path(tempfile.mkdtemp(prefix='cpp-',dir=RUNTIME)).resolve()
    try:yield directory
    finally:
        # Windows may retain an executable handle briefly after process termination.
        if not directory.is_relative_to(RUNTIME.resolve()):raise RuntimeError('Unexpected cleanup path.')
        for attempt in range(10):
            try:
                shutil.rmtree(directory)
                break
            except OSError as error:
                # Antivirus/indexing can briefly hold a file or make rmdir observe
                # a not-yet-empty directory after Windows reports process exit.
                if not isinstance(error, PermissionError) and getattr(error,'winerror',None)!=145:
                    raise
                if attempt==9:print('Temporary compiler files retained for later cleanup:',directory)
                else:time.sleep(.1)

def source_text(task):
    source = task.get('source', {})
    if not isinstance(source, dict) or len(source) != 1:
        raise ValueError('The local demo requires one embedded main.cpp source.')
    return next(iter(source.values()))

def locate(source, location):
    """Resolve the snippet/nth/context subset used by this course, against original source."""
    snippet = str(location['snippet'])
    matches = list(re.finditer(re.escape(snippet), source))
    context = location.get('context')
    if context:
        spans = [(m.start(), m.end()) for m in re.finditer(re.escape(str(context)), source)]
        matches = [m for m in matches if any(a <= m.start() and m.end() <= b for a,b in spans)]
    index = location.get('nth', 1) - 1
    if not matches or index >= len(matches):
        raise ValueError(f'Unresolved code location: {snippet!r}')
    m = matches[index]
    return m.start(), m.end()

def materialize(task, payload=None):
    payload = payload or {}
    source = source_text(task)
    kind = task['pedagogy']['activity']
    elements = [e for e in task.get('elements', []) if e['type'] in ('blank','block','editable','parameter')]
    changes = []
    selections = payload.get('selections')
    answers = payload.get('answers')
    for i, element in enumerate(elements):
        start, end = locate(source, element['location'])
        text = source[start:end]
        if kind in ('code-completion','parsons-puzzles'):
            if kind == 'parsons-puzzles' and answers is not None:
                text = answers[i] if i < len(answers) else ''
                # The native viewer returns de-indented block text.
                indent = len(source[start:end]) - len(source[start:end].lstrip(' '))
                lines = str(text).splitlines()
                if lines and not lines[0].startswith(' '):
                    text = '\n'.join(' ' * indent + line for line in lines)
            else:
                choices = element['choices']
                selected = next(j for j,c in enumerate(choices) if c['role'] == 'solution') if selections is None else selections[i]
                if not isinstance(selected, int) or selected < 0 or selected >= len(choices):
                    raise ValueError('Choose an option for every blank/block.')
                text = choices[selected]['snippet']
        elif kind == 'free-coding' and answers is not None:
            text = answers[i] if i < len(answers) else ''
        elif kind == 'parameterized-code-tracing':
            index = 0 if selections is None else selections[i]
            if not isinstance(index, int) or index < 0 or index >= len(element['values']):
                raise ValueError('Invalid parameter selection.')
            text = str(element['values'][index])
        if not isinstance(text, str) or len(text) > 60000:
            raise ValueError('Invalid answer text.')
        changes.append((start,end,text))
    for start,end,text in sorted(changes, reverse=True):
        source = source[:start] + text + source[end:]
    return source

def invoke(command, cwd, stdin='', timeout=10):
    """Bound child resources and clean up the process group, including exited parents.

    A file for stdin avoids blocking the watchdog when a program never reads input.
    Linux limits run in a separate launcher (preexec_fn is unsafe in HTTP threads).
    """
    with tempfile.TemporaryFile() as inp, tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        inp.write(stdin.encode());inp.seek(0)
        environment=os.environ.copy()
        if COMPILER:environment['PATH']=str(Path(COMPILER).parent)+os.pathsep+environment.get('PATH','')
        if sys.platform == 'linux':
            command=[sys.executable,str(ROOT/'tools/limit_process.py'),str(timeout),*map(str,command)]
        process = subprocess.Popen(command, cwd=cwd, stdin=inp, stdout=out, stderr=err,env=environment,
                                   start_new_session=os.name != 'nt',
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        deadline=time.monotonic()+timeout
        timed_out=False;output_limited=False
        while process.poll() is None:
            if time.monotonic()>deadline:timed_out=True;break
            if os.fstat(out.fileno()).st_size+os.fstat(err.fileno()).st_size>MAX_OUTPUT:
                output_limited=True;break
            try:process.wait(timeout=.03)
            except subprocess.TimeoutExpired:pass
        if os.name != 'nt':
            # Also reap descendants left behind by a parent that already exited.
            try:os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        elif timed_out or output_limited:
            if os.name == 'nt':
                subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'], capture_output=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()
        output_limited=output_limited or os.fstat(out.fileno()).st_size+os.fstat(err.fileno()).st_size>MAX_OUTPUT
        out.seek(0); err.seek(0)
        stdout, stderr = out.read(MAX_OUTPUT).decode('utf-8',errors='replace'), err.read(MAX_OUTPUT).decode('utf-8',errors='replace')
        return dict(stdout=stdout.replace('\r\n','\n'), stderr=stderr.replace('\r\n','\n'),
                    exitCode=process.returncode, timedOut=timed_out, outputLimited=output_limited)

def run_source(source, cases, includes=None):
    if not COMPILER:
        raise RuntimeError('g++ not found. Set CUPCAKE_CXX to the compiler executable.')
    with compilation_directory() as cwd:
        (cwd/'main.cpp').write_text(source,encoding='utf-8')
        for name, content in (includes or {}).items():
            if not re.fullmatch(r'[A-Za-z0-9_.-]+\.(hpp|h)',name):
                raise ValueError('Only embedded header basenames are supported.')
            (cwd/name).write_text(content,encoding='utf-8')
        executable = cwd/('program.exe' if os.name == 'nt' else 'program')
        compiled = invoke([COMPILER,'-std='+STANDARD,'-Wall','-Wextra','-pedantic-errors','-Werror=return-type','-O0','main.cpp','-o',str(executable)],cwd,timeout=30)
        results=[]
        for case in cases:
            stdin = case.get('stdin', [])
            stdin = '\n'.join(str(x) for x in stdin) + ('\n' if stdin else '') if isinstance(stdin,list) else stdin
            result = compiled.copy() if compiled['exitCode'] != 0 or compiled['timedOut'] or compiled['outputLimited'] else invoke([str(executable)],cwd,stdin,timeout=3)
            if compiled['exitCode'] != 0:
                result['stderr'] = 'Compilation failed:\n' + result['stderr']
            if result['timedOut']:
                result['stderr'] += '\nExecution time limit exceeded.'
            if result['outputLimited']:
                result['stderr'] += '\nOutput limit exceeded.'
            expected = case.get('stdout','')
            result.update(title=case.get('title','Run'), type='testcase', stdin=case.get('stdin',[]),
                          expected=expected, visible=case.get('visible',True), console=result['stdout'],
                          passed=result['exitCode']==0 and not result['timedOut'] and not result['outputLimited'] and result['stdout'].strip()==expected.strip())
            results.append(result)
        return results

def execute(task,payload=None):
    cases = task.get('testcases') or task.get('executions') or [dict(title='Run',stdin=[],stdout='')]
    return run_source(materialize(task,payload),cases,task.get('includes'))
