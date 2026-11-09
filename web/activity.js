// This adapter adds novice guidance and restoration. The server applies one pinned
// compatibility fix to the served free-coding control; the vendor files stay intact.
import {renderMarkdown} from '/lesson-markdown.js';
const id=new URLSearchParams(location.search).get('id');
const status=document.getElementById('launchStatus');
const embedded=window.parent!==window;
const parentOrigin=document.referrer?new URL(document.referrer).origin:null;
const uid=()=>crypto.randomUUID();
function send(subject,extra={}){if(embedded)window.parent.postMessage({subject,message_id:uid(),...extra},parentOrigin||'*');}
function getState(){
 if(!embedded){try{return Promise.resolve(JSON.parse(localStorage.getItem('cpp23-standalone-v2-'+id)));}catch{return Promise.resolve(null);}}
 return new Promise(resolve=>{
  const message_id=uid();let timer;
  const listener=event=>{
   if(event.source!==window.parent||(parentOrigin&&event.origin!==parentOrigin))return;
   if(event.data?.subject!=='SPLICE.getState.response'||event.data.message_id!==message_id)return;
   clearTimeout(timer);window.removeEventListener('message',listener);resolve(event.data.state??null);
  };
  window.addEventListener('message',listener);
  timer=setTimeout(()=>{window.removeEventListener('message',listener);resolve(null);},1500);
  window.parent.postMessage({subject:'SPLICE.getState',message_id,domain_id:'cupcake-cpp-studio',content_id:id},parentOrigin||'*');
 });
}
const originalFetch=window.fetch.bind(window);
// Prevent any upstream telemetry or execution request from leaving this local demo.
window.fetch=async(input,init)=>{
 const url=new URL(typeof input==='string'?input:input instanceof URL?input.toString():input.url,document.baseURI);
 if(url.pathname.endsWith('/api/v1/log')||url.pathname.endsWith('/log'))return new Response(null,{status:204});
 if(url.origin!==location.origin)throw new Error('The local course does not call remote services.');
 return originalFetch(input,init);
};
let currentState=null,activityKind='';
function element(tag,text,className){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(className)e.className=className;return e;}
function renderTeaching(teaching){
 const section=document.getElementById('teaching');section.replaceChildren();
 section.append(element('p',teaching.goal,'goal'));
 const how=element('details');how.open=true;how.append(element('summary','How this activity works'));
 const steps=element('ol');for(const text of teaching.instructions||[]){steps.append(element('li',!embedded?text.replace('Drafts save after a short pause while you edit.','Checked work saves in this view; use the course page for automatic draft saving.'):text));}how.append(steps);section.append(how);
 const hints=teaching.hints||[];
 if(hints.length){
  const box=element('details');box.open=true;box.append(element('summary','Need a nudge?'));
  box.append(element('p','Hints are available before you check an answer. Open one at a time; using them does not lower your score.','helper-note'));
  const content=element('div');content.setAttribute('aria-live','polite');const next=element('button','Show the first hint'),hide=element('button','Hide hints');hide.hidden=true;let count=0;
  next.onclick=()=>{const p=element('div',undefined,'hint');p.append(element('small',`Hint ${count+1} of ${hints.length}`));const text=element('div');text.innerHTML=renderMarkdown(hints[count]);p.append(text);content.append(p);count++;hide.hidden=false;next.textContent=count===hints.length?'All hints are open':'Show the next hint';next.disabled=count===hints.length;send('SPLICE.sendEvent',{name:'studio.hintOpened',data:{activityId:id,hintIndex:count-1}});};
  hide.onclick=()=>{content.replaceChildren();count=0;next.textContent='Show the first hint';next.disabled=false;hide.hidden=true;};
  box.append(content,next,hide);section.append(box);
 }
 for(const [name,source] of Object.entries(teaching.supportingFiles||{})){
  const file=element('details');file.open=true;file.append(element('summary','Supporting file: '+name));file.append(element('p','This file is supplied with the activity. It announces the function before main calls it; the calculation itself is visible in main.cpp below. You do not need to create or edit this header.','helper-note'));
  const pre=element('pre',source);pre.tabIndex=0;file.append(pre);section.append(file);
 }
 if(teaching.samples?.length){
  const examples=element('details');examples.append(element('summary',`Input and output examples · ${teaching.samples.length} checks`));examples.append(element('p','These examples explain the rule your code should follow. Your program should handle all of them, rather than printing a saved answer for one input.','helper-note'));
  for(const sample of teaching.samples){
   const card=element('div',undefined,'sample');card.append(element('h3',sample.title));const columns=element('div',undefined,'sample-columns');
   for(const [label,text] of [['Input',sample.stdin],['Expected output',sample.stdout]]){const c=element('div');c.append(element('small',label),element('pre',text===''?(label==='Input'?'(no input)':'(no output)'):text==='\n'&&label==='Input'?'(an empty input line)':text));columns.append(c);}card.append(columns,element('p',sample.purpose));examples.append(card);
  }section.append(examples);
 }
}
// Native components resize only their own content. Report our whole document,
// including guidance, expanded hints, and supporting files, as a SPLICE resize.
let resizeQueued=false,lastHeight=0;
const resize=()=>{if(!embedded||resizeQueued)return;resizeQueued=true;requestAnimationFrame(()=>{resizeQueued=false;const height=Math.ceil(document.body.getBoundingClientRect().height);if(height!==lastHeight){lastHeight=height;send('lti.frameResize',{height,width:document.documentElement.clientWidth,studio_document:true});}});};
new ResizeObserver(resize).observe(document.body);
const friendlyLabels={'STATEMENT':'Your task','QUESTION':'Think about this','PROGRAM':'Program','PROGRAM OUTPUT':'Example output','WHAT IS THE OUTPUT?':'What will this program print?','OPTIONS':'Available blocks'};
new MutationObserver(()=>{
 document.querySelectorAll('cupcake-activity-viewer h2').forEach(h=>{const label=friendlyLabels[h.textContent.trim().toUpperCase()];if(label&&h.textContent!==label)h.textContent=label;});
 document.querySelectorAll('cupcake-activity-viewer button').forEach(b=>{if(b.textContent.trim()==='Explain me why')b.textContent='Why this choice?';});resize();
 if(activityKind==='macro-visualization')document.querySelectorAll('.jsvee-stack > .jsvee-area-label').forEach(label=>{if(label.textContent==='Stack')label.textContent='Tracked values';});
}).observe(document.getElementById('viewer'),{childList:true,subtree:true,characterData:true});
const execute=async payload=>{
 const submission={};
 if(Array.isArray(payload.answers))submission.answers=payload.answers;
 if(Array.isArray(payload.selections))submission.selections=payload.selections;
 currentState={...(currentState||{}),schemaVersion:2,activityId:id,submission,draft:submission};
 if(embedded)send('SPLICE.sendEvent',{name:'studio.submission',data:{activityId:id,submission}});
 else localStorage.setItem('cpp23-standalone-v2-'+id,JSON.stringify(currentState));
 status.textContent='Building your C++23 program and trying the example inputs…';
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),50000);
 try{
  const response=await originalFetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json','X-Cupcake-Local':window.LOCAL_RUN_TOKEN},body:JSON.stringify({id,...submission}),signal:controller.signal});
  const data=await response.json();if(!response.ok)throw new Error(data.error||'Execution failed.');
  const passed=data.filter(r=>r.passed).length;
  const built=data.every(r=>r.exitCode===0&&!r.timedOut&&!r.outputLimited);
  status.textContent=!built?'The program could not finish a check. Read the first build or runtime message below, then try one small repair.':activityKind==='parameterized-code-tracing'
   ? 'The displayed program ran. Compare its result with your prediction below.'
   : `${passed} of ${data.length} checks match. ${passed===data.length?'Your rule works for these examples.':'Open a failed case below and compare what your code did with what that input needs.'} Checked work saved in this browser.`;
  return data;
 }catch(e){status.textContent=`Execution error: ${e.message}`;throw e;}finally{clearTimeout(timer);}
};
const bridge=Object.freeze({execute,run:execute});
Object.defineProperty(window,'CUPCAKE_EXECUTION_BRIDGE',{value:bridge});
Object.defineProperty(window,'cupcakeExecutionBridge',{value:bridge});
try{
 if(!id)throw new Error('Choose an activity from the course.');
 const [response,state,teachingResponse]=await Promise.all([originalFetch('/api/activity?id='+encodeURIComponent(id)),getState(),originalFetch('/api/teaching?id='+encodeURIComponent(id))]);
 if(!response.ok)throw new Error('Activity not found.');
 const activity=await response.json();currentState=state;activityKind=activity.pedagogy.activity;document.body.dataset.activityKind=activityKind;
 if(teachingResponse.ok)renderTeaching(await teachingResponse.json());
 document.title=activity.title+' · Cupcake';
 let restored=false;
 const savedAnswers=state?.draft?.answers||state?.submission?.answers;
 if(activity.pedagogy.activity==='free-coding'&&Array.isArray(savedAnswers)){
  activity.elements.filter(e=>e.type==='editable').forEach((e,i)=>{if(typeof savedAnswers[i]==='string'){e.placeholder=savedAnswers[i];restored=true;}});
 }
 const messages=[];
 if(restored)messages.push('Your saved code is back. You can keep editing or check it again.');
 if(typeof state?.score==='number')messages.push(`Previous checked score: ${Math.round(100*state.score)}%.`);
 if(!restored&&state?.submission)messages.push('Previous result is saved; choose the exercise options again for a new attempt.');
 messages.push('Runs with C++23.');status.textContent=messages.join(' ');
 await customElements.whenDefined('cupcake-activity-viewer');
 const viewer=document.getElementById('viewer');viewer.protocol='splice';viewer.yamlContent=JSON.stringify(activity);
 if(restored)send('SPLICE.sendEvent',{name:'studio.restored',data:{activityId:id,kind:'free-coding-draft'}});
}catch(e){status.textContent='Unable to open activity: '+e.message;}
