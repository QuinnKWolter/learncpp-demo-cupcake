"""Build all seven native Cupcake types from reviewed C++23 teaching sources."""
from pathlib import Path
import json
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
from course_data import MODULES,CAPSTONES
from execution import run_source,locate

TYPES=['worked-example','macro-visualization','parsons-puzzles','code-completion','multiple-choice-question','parameterized-code-tracing','free-coding']
LABELS=['Worked example','Step through','Arrange code','Fill gaps','Explain why','Predict output','Write code']
INSTRUCTIONS={
 'worked-example':['Read the small program and guess its result.','Click an underlined piece of code or its ? marker to open the explanation.','Compare your reasoning with the sample run, then mark the example reviewed when ready.'],
 'macro-visualization':['This is a guided diagram for one fixed program, not a live debugger.','Use Step forward (the single right arrow) to advance; Undo goes back one state and Move to begin returns to the start.','The highlight marks the line just explained. The state labels summarize what changed; read the sentence below the diagram before advancing.'],
 'parsons-puzzles':['Move complete blocks from Options into the empty program slots. Each block is used once.','The surrounding code is supplied; only the marked slots need blocks. C++ indentation is handled for you.','When every slot is filled, choose Check Answer. If needed, move a block again and check a new arrangement.'],
 'code-completion':['Click the marked gap in the program to open its choices.','Choose the code that fits the stated goal, then choose Check Answer to try the completed program.','Click a checked gap again to read why that choice works or fails. Hints below are available before you submit.'],
 'multiple-choice-question':['Read the question and choose one explanation.','Choose Check Answer to see feedback about that idea.','Use Try Again for another attempt; the answer positions may be shuffled.'],
 'parameterized-code-tracing':['Read the actual values shown in your program; they may differ on a later attempt.','Predict every output line, preserving word order and spaces between values. Type output, not C++ code.','Check Answer runs that displayed variant and compares its output with your prediction. Try Again starts another attempt and may change the starting values.'],
 'free-coding':['The marked regions are yours to edit. The other lines supply input, output, or a definition you can read.','Use the input/output examples below to understand the task; write one rule that handles them all.','Check Answer builds and tests your code. Read the first build error, or compare a failed case’s input and expected output. Drafts save after a short pause while you edit.']}

class LiteralDumper(yaml.SafeDumper):pass
def represent_str(dumper,value):return dumper.represent_scalar('tag:yaml.org,2002:str',value,style='|' if '\n' in value else None)
LiteralDumper.add_representer(str,represent_str)
def save_yaml(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.dump(data,Dumper=LiteralDumper,sort_keys=False,allow_unicode=True,width=105),encoding='utf-8')
def input_lines(text):return text.removesuffix('\n').split('\n') if text else []
def base(m,kind,title,index):
    return {'$schema':f'https://adapt2.sis.pitt.edu/cupcake/schemas/{kind}/0.1.0','license':'MIT','locale':'en-US',
            'id':f'cpp23-v2-{m["slug"]}-{kind}','title':title,'description':'Practice '+m['title'].lower()+'.',
            'pedagogy':dict(activity=kind,difficulty='novice' if index<=10 else 'intermediate',
                            prereq_topics=MODULES[index-2]['topics'] if 1<index<=20 else [],topics=m['topics'])}
def source_fields(source,includes=None):
    fields=dict(runtime=dict(language='cpp',version='23'),source={'main.cpp':source})
    if includes:fields['includes']=includes
    return fields
def cases(items,purposes=None,hints=None):
    return [dict(title=t,visible=True,stdin=input_lines(s),stdout=o,
                 feedback=dict(on_pass=[(purposes[i] if purposes else 'This run matches the requested result.')],
                               on_fail=[(purposes[i]+' ' if purposes else '')+(hints[0] if hints else 'Trace the supplied inputs through your chosen steps, then compare the result.')]))
            for i,(t,s,o) in enumerate(items)]
def editable_elements(source,regions,prompts):
    spans=[];elements=[]
    for region,prompt in zip(regions,prompts):
        assert source.count(region)==1,(region,source)
        start,end=locate(source,dict(snippet=region));spans.append((start,end))
        indent=len(region)-len(region.lstrip(' '))
        elements.append(dict(type='editable',location=dict(snippet=region),placeholder=' '*indent+'// '+prompt))
    cursor=0
    for start,end in sorted(spans):
        if source[cursor:start].strip():elements.append(dict(type='locked',location=dict(snippet=source[cursor:start])))
        cursor=end
    if source[cursor:].strip():elements.append(dict(type='locked',location=dict(snippet=source[cursor:])))
    return elements
def compile_sample(source,stdin='',includes=None):
    r=run_source(source,[dict(title='Sample run',stdin=stdin,stdout='')],includes)[0]
    assert r['exitCode']==0 and not r['timedOut'],r
    return dict(title='Sample run',stdin=input_lines(stdin),stdout=r['stdout'],console=r['stdout'],status='pass')
def helper_note(m):
    if not m.get('includes'):return ''
    return '\n\n### The supplied header\n`geometry.hpp` announces `int rectanglePerimeter(int width, int height);` before the call. The complete definition is visible below `main`. The include guard keeps the announcement from being repeated. This file is supplied with the activity; you do not need to create it.'
def guide(kind,goal,hints=None,supporting=None,samples=None,**kw):
    return dict(goal=goal,instructions=INSTRUCTIONS[kind],hints=hints or [],supportingFiles=supporting or {},samples=samples or [],**kw)
def make_visualization(m,index):
    trace=m['tracing'];source=trace['source'];steps=[]
    names=list(dict.fromkeys(k for snap in trace['walkthrough'] for k in snap['state']))
    init=[['createFrame',0,'Guided C++23 state']]+[['createVariable',name] for name in names]
    init += [['setLine',2],['showText','Choose Step to begin. Follow the highlighted line, state labels, and explanation together.']]
    for snap in trace['walkthrough']:
        start,end=locate(source,dict(snippet=snap['snippet']))
        line=source[:start].count('\n')+1
        # Prefix actions run before the visible showText step. A trailing underscore
        # would run after the previous step, leaving its explanation one click behind.
        steps.append(['_setLine',line])
        for name,value in snap['state'].items():
            steps.extend([['_addValue',str(value),0,'int' if isinstance(value,int) else 'std::string'],['_assign',name]])
        steps.append(['showText',snap['note']])
    task=base(m,'macro-visualization',m['title']+' · step through',index)
    task.update(source_fields(source),statement='Follow one fixed version of this module’s program. '+trace['goal']+'\n\nUse Step to advance one explained state at a time. The highlighted line is the one just explained. These state labels are a teaching diagram, not the compiler’s physical memory layout. Predict output later gives you a changing version to solve yourself.',
                elements=[dict(settings=dict(code='top',heapHeight=10,stackHeight=220,width=900),init=init,steps=steps,lines=source.splitlines())])
    return task

def build():
    manifest=dict(id='cupcake-cpp23-lab-v2',revision=2,title='C++ / Understand it. Try it. Explain it.',
                  subtitle='Guided C++23 practice following the LearnCpp reading sequence.',language='C++23',estimatedHours='40–60',
                  modules=[],capstones=[],source='https://www.learncpp.com/',activityTypes=TYPES)
    solutions={};review=[]
    for index,m in enumerate(MODULES,1):
        folder=ROOT/'course/activities'/m['slug']
        entry={k:m[k] for k in ['slug','title','chapters','readings','topics','objectives','lesson']}
        entry.update(number=index,activities=[],prerequisites=[MODULES[index-2]['slug']] if index>1 else [])
        def emit(kind,task,teaching):
            path=folder/(kind+'.yaml');save_yaml(path,task)
            entry['activities'].append(dict(id=task['id'],type=kind,label=LABELS[TYPES.index(kind)],title=task['title'],path=path.relative_to(ROOT).as_posix(),guide=teaching))
        sample=compile_sample(m['example'],m.get('example_input',''),m.get('includes'))
        kind='worked-example';task=base(m,kind,m['title']+' · worked example',index)
        task.update(source_fields(m['example'],m.get('includes')),statement='Read the small program and predict its result. Click the underlined pieces of code to see what each one contributes. Then compare your prediction with the sample run.'+helper_note(m),executions=[sample],
                    elements=[dict(type='explanation',location=dict(snippet=s),explanations=[dict(body=b)]) for s,b in m['explanations']])
        emit(kind,task,guide(kind,'Connect the written code with its purpose and the values it produces.',supporting=m.get('includes')))
        kind='macro-visualization';task=make_visualization(m,index)
        emit(kind,task,guide(kind,'Watch how the values change, one explained step at a time.',walkthrough=m['tracing']['walkthrough'],expectedOutput=m['tracing']['output']))
        kind='parsons-puzzles';p=m['puzzle'];sample_p=compile_sample(p['source'],p.get('stdin',''),m.get('includes') if index==2 else None)
        task=base(m,kind,m['title']+' · arrange code',index)
        elements=[]
        for i,b in enumerate(p['blocks']):
            block=dict(type='block',location=dict(snippet=b['snippet']),choices=[dict(snippet=b['snippet'],role='solution',indent=len(b['snippet'])-len(b['snippet'].lstrip(' ')),explanations=[dict(body=b['explanation'])])])
            group=p['groups'].get(i,p['groups'].get(str(i)))
            if group:block['group']=group
            elements.append(block)
        task.update(source_fields(p['source'],m.get('includes') if index==2 else None),statement=p['goal']+'\n\nMove whole blocks into the highlighted slots. The surrounding program is supplied. Blocks that prepare independent values can be placed in either order; blocks that use those values must follow their declarations.'+helper_note(m) if index==2 else p['goal']+'\n\nMove whole blocks into the highlighted slots. You do not need to edit their text. Prepare values before using them and print the requested final state.',hints=m['hints_by_type'][kind],elements=elements,
                    testcases=cases(p['cases'],hints=m['hints_by_type'][kind]) if p.get('cases') else [dict(title='Requested result',visible=True,stdin=sample_p['stdin'],stdout=sample_p['stdout'])])
        emit(kind,task,guide(kind,p['goal'],hints=m['hints_by_type'][kind],supporting=m.get('includes') if index==2 else None))
        kind='code-completion';task=base(m,kind,m['title']+' · fill gaps',index)
        statement=m['completion_goal']+' Choose the code for the marked gap that follows this rule.\n\n### Sample run'
        if sample['stdin']:statement+='\nInput:\n```text\n'+'\n'.join(sample['stdin'])+'\n```'
        statement+='\nOutput:\n```text\n'+sample['stdout'].rstrip()+'\n```'
        if m.get('completion_cases'):statement+='\nThe same rule must also handle the range endpoints and other inputs checked by the tests.'
        task.update(source_fields(m['example'],m.get('includes')),statement=statement+helper_note(m),hints=m['hints_by_type'][kind],
                    elements=[dict(type='blank',location=dict(snippet=m['blank']),choices=[dict(snippet=m['blank'],role='solution',explanations=[dict(body=m['completion_explanation'])])]+[dict(snippet=s,role='distractor',explanations=[dict(body=b)]) for s,b in m['wrong']])],
                    testcases=cases(m['completion_cases'],hints=m['hints_by_type'][kind]) if m.get('completion_cases') else [dict(title='Requested result',visible=True,stdin=sample['stdin'],stdout=sample['stdout'])])
        emit(kind,task,guide(kind,'Choose the missing step using the meaning of the calculation, then read its feedback.',hints=m['hints_by_type'][kind],supporting=m.get('includes')))
        kind='multiple-choice-question';task=base(m,kind,m['title']+' · explain why',index)
        task.update(question=m['question'],include_choices=len(m['choices']),hints=m['hints_by_type'][kind],choices=[dict(body=t,role='solution' if i==0 else 'distractor',explanations=[dict(body=b)]) for i,(t,b) in enumerate(m['choices'])])
        emit(kind,task,guide(kind,'Choose the explanation that matches how this C++ feature works.',hints=m['hints_by_type'][kind]))
        kind='parameterized-code-tracing';t=m['tracing'];task=base(m,kind,m['title']+' · predict output',index)
        location=dict(snippet=t['token'])
        if t.get('context'):location['context']=t['context']
        task.update(source_fields(t['source']),statement=t['goal']+'\n\nType the program’s output, not source code. Values may change between attempts, so start with the values actually displayed. Keep any spaces between printed values and any separate output lines.',hints=m['hints_by_type'][kind],
                    elements=[dict(type='parameter',location=location,values=t['values'])],testcases=[dict(title='First-variant author reference',visible=False,stdin=input_lines(t.get('stdin','')),stdout=t['expected'][0])])
        emit(kind,task,guide(kind,t['goal'],hints=m['hints_by_type'][kind],variantValues=t['values'],variantExpected=t['expected']))
        kind='free-coding';task=base(m,kind,m['title']+' · write code',index)
        task.update(source_fields(m['solution']),statement=m['task']+'\n\nEdit only the marked region. The other code is supplied for you to read and use. Check Answer tries the listed inputs; use their feedback to find which part of the rule needs another look.',hints=m['hints_by_type'][kind],elements=editable_elements(m['solution'],[m['editable']],m['region_prompts']),testcases=cases(m['cases'],m['case_purposes'],m['hints_by_type'][kind]))
        emit(kind,task,guide(kind,m['region_prompts'][0],hints=m['hints_by_type'][kind],samples=[dict(title=t,stdin=s,stdout=o,purpose=purpose) for (t,s,o),purpose in zip(m['cases'],m['case_purposes'])]))
        solutions[task['id']]=[m['editable']]
        manifest['modules'].append(entry)
        review.append(dict(module=m['slug'],activityTypes=TYPES,source=m['slug']+'.yaml',goals=m['objectives'],preparation=True,progressiveHints=True,distractorReasoning=True,supportingFiles=list(m.get('includes',{})),authoredTraceStates=len(m['tracing']['walkthrough']),testPurposes=len(m['case_purposes'])))
        print(f'Built {index:02d}: {m["title"]} (7 types)',flush=True)
    for project in CAPSTONES:
        kind='free-coding';task=base(project,kind,project['title'],project['after']);task['pedagogy']['difficulty']='advanced'
        task.update(source_fields(project['solution']),statement=project['task']+'\n\nThe two highlighted method/function bodies are yours to complete. Read the preparation notes and examples before editing; the surrounding program is supplied.',hints=project['hints'],
                    elements=editable_elements(project['solution'],[project['editable'],project['second_editable']],project['region_prompts']),testcases=cases(project['cases'],project['case_purposes'],project['hints']))
        path=ROOT/'course/activities'/project['slug']/'free-coding.yaml';save_yaml(path,task)
        manifest['capstones'].append(dict(id=task['id'],type=kind,slug=project['slug'],title=project['title'],after=project['after'],objectives=project['objectives'],chapters=project['chapters'],lesson=project['lesson'],path=path.relative_to(ROOT).as_posix(),guide=guide(kind,project['task'],hints=project['hints'],samples=[dict(title=t,stdin=s,stdout=o,purpose=purpose) for (t,s,o),purpose in zip(project['cases'],project['case_purposes'])])))
        solutions[task['id']]=[project['editable'],project['second_editable']]
    manifest['activityCount']=sum(len(m['activities']) for m in manifest['modules'])+len(manifest['capstones'])
    (ROOT/'web/course.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    save_yaml(ROOT/'course/course.yaml',manifest)
    (ROOT/'course/solutions.json').write_text(json.dumps(solutions,indent=2),encoding='utf-8')
    (ROOT/'research/editorial-review.json').write_text(json.dumps(dict(revision=2,standard='C++23',modules=review,projects=[p['slug'] for p in CAPSTONES]),indent=2),encoding='utf-8')
    lines=['# C++23 practice with Cupcake','','20 prepared modules, each with all seven native activity types, plus two integration projects.','']
    for m in manifest['modules']:
        lines += [f'## {m["number"]:02d}. {m["title"]}','',m['lesson'],'']
        lines += [f'- [{r["title"]}]({r["url"]})' for r in m['readings']]+['']
        lines += [f'- [{a["label"]}](activities/{m["slug"]}/{a["type"]}.yaml)' for a in m['activities']]+['']
    for c in manifest['capstones']:lines += [f'## {c["title"]}',f'After module {c["after"]}.','',c['lesson'],'',f'[Open project](activities/{c["slug"]}/free-coding.yaml)','']
    (ROOT/'course/README.md').write_text('\n'.join(lines),encoding='utf-8')
    print(f'Built {len(MODULES)} reviewed modules and {manifest["activityCount"]} activities.')

if __name__=='__main__':build()
