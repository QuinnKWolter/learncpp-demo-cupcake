"""Check the reviewed curriculum, all native schemas, C++23 programs, and interactions."""
from pathlib import Path
from itertools import permutations,product
import importlib
import json
import sys
import time
import yaml
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
from course_data import MODULES,CAPSTONES
from build_reviewed_course import TYPES
from execution import execute,locate,source_text,materialize,run_source,COMPILER,STANDARD,REPORTS

def main():
    started=time.time();checks=[];runs=0;variants=0;distractors=0;puzzles=0;visuals=0;groups=0
    # This compiles feature probes using the exact execution adapter/compiler.
    importlib.import_module('verify_cpp23')
    manifest=json.loads((ROOT/'web/course.json').read_text(encoding='utf-8'))
    assert manifest['language']=='C++23' and manifest['revision']==2
    assert len(manifest['modules'])==20
    for module,m in zip(manifest['modules'],MODULES):
        assert [a['type'] for a in module['activities']]==TYPES,module['slug']
        assert len(m['lesson'].split())>=250,m['slug']
        assert m['lesson'].count('### ')>=3,m['slug']
        assert len(m['case_purposes'])==len(m['cases'])
        assert len(m['region_prompts'])==1
        assert len(m['completion_goal'].split())>=12,m['slug']
        for activity in module['activities']:
            g=activity['guide'];assert len(g['instructions'])==3
            if activity['type'] in m['hints_by_type']:assert len(g['hints'])>=2
    entries=[a for m in manifest['modules'] for a in m['activities']]+manifest['capstones']
    files=sorted((ROOT/'course/activities').rglob('*.yaml'))
    assert len(entries)==len(files)==142
    teaching={a['id']:a['guide'] for a in entries};modules={m['slug']:m for m in MODULES}
    ids=set()
    for path in files:
        task=yaml.safe_load(path.read_text(encoding='utf-8'));kind=task['pedagogy']['activity'];g=teaching[task['id']]
        schema=json.loads((ROOT/'schemas'/f'{kind}_0.1.0.json').read_text(encoding='utf-8'))
        jsonschema.Draft7Validator(schema,format_checker=jsonschema.FormatChecker()).validate(task)
        assert task['id'] not in ids and task['id'].startswith('cpp23-v2-');ids.add(task['id'])
        assert 'C++17' not in json.dumps(task)
        if kind=='multiple-choice-question':
            assert sum(c['role']=='solution' for c in task['choices'])==1
            assert all(len(c['explanations'][0]['body'].split())>=7 for c in task['choices']),path
            checks.append(dict(file=path.relative_to(ROOT).as_posix(),kind=kind,schema=True));continue
        assert task['runtime']==dict(language='cpp',version='23'),path
        source=source_text(task)
        if kind=='code-completion':assert modules[path.parent.name]['completion_goal'] in task['statement']
        if kind=='macro-visualization':
            m=modules[path.parent.name];trace=m['tracing'];e=task['elements'][0]
            assert e['lines']==source.splitlines()
            assert len([s for s in e['steps'] if s[0]=='showText'])==len(trace['walkthrough'])
            allowed={'createFrame','createVariable','setLine','addValue','assign','showText'}
            assert all(s[0].strip('_') in allowed for s in e['init']+e['steps'])
            assert all(1<=s[1]<=len(e['lines']) for s in e['steps'] if s[0]=='_setLine')
            assert all(s[0]=='showText' or s[0].startswith('_') for s in e['steps'])
            assert str(trace['walkthrough'][-1]['state']['output'])==trace['output'].strip()
            out=run_source(source,[dict(title='Authored walkthrough result',stdin=trace.get('stdin',''),stdout=trace['output'])]);runs+=len(out)
            assert all(r['passed'] for r in out),(path,out)
            visuals+=1;checks.append(dict(file=path.relative_to(ROOT).as_posix(),kind=kind,schema=True,authoredStates=len(trace['walkthrough'])));print('OK '+path.parent.name+'/'+kind,flush=True);continue
        spans=[]
        for element in task.get('elements',[]):
            start,end=locate(source,element['location']);assert start<end
            if element['type'] in ('blank','block','editable','parameter'):spans.append((start,end))
            if element['type']=='block':
                assert start==0 or source[start-1]=='\n';assert end==len(source) or source[end]=='\n'
            if element['type'] in ('blank','block'):
                assert sum(c['role']=='solution' for c in element['choices'])==1
                assert next(c['snippet'] for c in element['choices'] if c['role']=='solution')==source[start:end]
        for (a,b),(c,d) in zip(sorted(spans),sorted(spans)[1:]):assert b<=c
        results=execute(task);runs+=len(results);assert results and all(r['passed'] for r in results),(path,results)
        if kind=='free-coding':
            answers=[e['location']['snippet'] for e in task['elements'] if e['type']=='editable']
            assert materialize(task,dict(answers=answers))==source
            blank=execute(task,dict(answers=['']*len(answers)));runs+=len(blank);assert not all(r['passed'] for r in blank),path
            assert len(g['samples'])==len(task['testcases']) and all(s['purpose'] for s in g['samples'])
        elif kind=='code-completion':
            elements=[e for e in task['elements'] if e['type']=='blank']
            for i,e in enumerate(elements):
                for j,c in enumerate(e['choices']):
                    if c['role']!='distractor':continue
                    selections=[next(k for k,c in enumerate(el['choices']) if c['role']=='solution') for el in elements];selections[i]=j
                    wrong=execute(task,dict(selections=selections));runs+=len(wrong);distractors+=1
                    assert not all(r['passed'] for r in wrong),(path,c)
        elif kind=='parsons-puzzles':
            puzzles+=1;blocks=[e for e in task['elements'] if e['type']=='block'];answers=[e['choices'][0]['snippet'].lstrip(' ') for e in blocks]
            native=execute(task,dict(answers=answers,selections=[0]*len(answers)));runs+=len(native);assert all(r['passed'] for r in native),(path,native)
            grouped={}
            for i,e in enumerate(blocks):
                if e.get('group'):grouped.setdefault(e['group'],[]).append(i)
            for members in grouped.values():
                alternate=answers.copy();values=[answers[i] for i in members][::-1]
                for i,value in zip(members,values):alternate[i]=value
                out=execute(task,dict(answers=alternate,selections=[0]*len(answers)));runs+=len(out);groups+=1
                assert all(r['passed'] for r in out),(path,'interchangeable blocks',out)
            wrong=answers.copy();wrong[0],wrong[-1]=wrong[-1],wrong[0]
            out=execute(task,dict(answers=wrong,selections=[0]*len(answers)));runs+=len(out)
            assert not all(r['passed'] for r in out),(path,'wrong dependency order accepted',out)
        elif kind=='parameterized-code-tracing':
            m=modules[path.parent.name];trace=m['tracing']
            for i,expected in enumerate(trace['expected']):
                result=execute(task,dict(selections=[i]));runs+=len(result);variants+=1
                assert result[0]['exitCode']==0 and result[0]['stdout'].strip()==expected.strip(),(path,i,expected,result)
        checks.append(dict(file=path.relative_to(ROOT).as_posix(),kind=kind,schema=True,referenceCases=len(results)))
        print('OK '+path.parent.name+'/'+kind,flush=True)
    # Real failures must remain failures under the new standard/toolchain.
    cases=[dict(title='Failure probe',stdin=[],stdout='expected\n')]
    bad=run_source('int main( {',cases)[0];assert not bad['passed'] and 'Compilation failed' in bad['stderr']
    wrong=run_source('#include <iostream>\nint main(){std::cout << "wrong";}',cases)[0];assert not wrong['passed']
    loop=run_source('int main(){volatile int keepRunning{1}; while(keepRunning){}}',cases)[0];assert loop['timedOut'] and not loop['passed']
    spam=run_source('#include <iostream>\nint main(){for(;;)std::cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\\n";}',cases)[0];assert spam['outputLimited'] and not spam['passed']
    report=dict(revision=2,standard=STANDARD,compiler=COMPILER,activities=len(files),schemasPassed=len(files),executedCases=runs,
                parameterVariants=variants,rejectedDistractors=distractors,puzzlesChecked=puzzles,allowedGroupPermutations=groups,
                authoredVisualizations=visuals,negativeChecks=['compilation failure','wrong output','execution timeout','output limit','blank starters','wrong puzzle dependencies'],seconds=round(time.time()-started,1),checks=checks)
    REPORTS.mkdir(parents=True,exist_ok=True)
    (REPORTS/'validation-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))

if __name__=='__main__':main()
