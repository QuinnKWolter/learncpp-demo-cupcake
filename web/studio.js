const $ = id => document.getElementById(id);
import {escape,renderMarkdown} from '/lesson-markdown.js';
const KEY='cupcake-cpp23-studio-v2';
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{};}catch{return {};}}
let saved=load();saved.activities??={};saved.readings??={};saved.events??=[];
let course,currentModule,currentActivity;
const frame=$('activity');
function persist(){try{localStorage.setItem(KEY,JSON.stringify(saved));}catch{$('saveStatus').textContent='Browser storage is full or disabled. Export progress to keep your work.';}}
function allActivities(){return [...course.modules.flatMap(m=>m.activities),...course.capstones];}
function complete(activity){const p=saved.activities[activity.id];return p?.reviewed||p?.score===1;}
function updateProgress(){
 const all=allActivities(),n=all.filter(complete).length;
 $('progressText').textContent=`${n} / ${all.length} activities`; $('progressPercent').textContent=`${Math.round(100*n/all.length)}%`;
 $('progress').value=100*n/all.length;
 document.querySelectorAll('[data-activity]').forEach(b=>b.classList.toggle('complete',complete({id:b.dataset.activity})));
 $('messageCount').textContent=saved.events.length;
 const p=saved.activities[currentActivity?.id];
 $('resultStatus').textContent=p?.reviewed?'Walkthrough reviewed':p?.score!==undefined?`Last checked score: ${Math.round(p.score*100)}%`:'';
}
function renderModules(){
 const query=$('search').value.toLowerCase();$('modules').replaceChildren();
 for(const m of course.modules){
  if(![m.title,...m.topics].join(' ').toLowerCase().includes(query))continue;
  const a=document.createElement('a');a.href=`/?module=${m.slug}`;a.className='module'+(m.slug===currentModule?.slug?' active':'');
  a.innerHTML=`<span class="module-number">${String(m.number).padStart(2,'0')}</span><span>${escape(m.title)}</span>${m.activities.every(complete)?'<span class="done">✓</span>':''}`;
  a.onclick=e=>{e.preventDefault();openModule(m.slug);};$('modules').append(a);
 }
 for(const c of course.capstones){
  const a=document.createElement('a');a.href=`/?module=${c.slug}`;a.className='module capstone'+(c.slug===currentModule?.slug?' active':'');
  a.innerHTML=`<span class="module-number">◆</span><span>${escape(c.title)}</span>${complete(c)?'<span class="done">✓</span>':''}`;
  a.onclick=e=>{e.preventDefault();openModule(c.slug);};$('modules').append(a);
 }
}
function openModule(slug,activityId){
 const normal=course.modules.find(m=>m.slug===slug),cap=course.capstones.find(c=>c.slug===slug);
 currentModule=normal||(cap?{...cap,number:'PROJECT',activities:[{...cap,label:'Build & test'}],readings:course.modules[cap.after-1].readings}:course.modules[0]);
 $('chapter').textContent=`${normal?'MODULE '+String(currentModule.number).padStart(2,'0'):cap?'CAPSTONE':'MODULE 01'} / LEARNCPP ${currentModule.chapters}`;
 $('title').textContent=currentModule.title;
 $('subtitle').textContent=normal?'Understand the idea, follow an example, then make it your own.':`Integration project · recommended after module ${cap?.after||20}`;
 $('objectives').innerHTML=currentModule.objectives.map(t=>`<span class="objective">${escape(t)}</span>`).join('');
 $('notes').innerHTML=renderMarkdown(currentModule.lesson);
 $('readings').innerHTML=currentModule.readings.map(r=>`<a href="${r.url}" target="_blank" rel="noopener">${escape(r.title)} ↗</a>`).join('');
 $('readDone').checked=!!saved.readings[currentModule.slug];$('activityCount').textContent=`${currentModule.activities.length} activities`;
 $('activities').replaceChildren();
 currentModule.activities.forEach(a=>{const b=document.createElement('button');b.textContent=a.label;b.className='activity-tab';b.dataset.activity=a.id;b.onclick=()=>openActivity(a.id);$('activities').append(b);});
 renderModules();openActivity(activityId||currentModule.activities[0].id);
}
function openActivity(id){
 currentActivity=currentModule.activities.find(a=>a.id===id)||currentModule.activities[0];
 document.querySelectorAll('[data-activity]').forEach(b=>{b.classList.toggle('active',b.dataset.activity===currentActivity.id);b.setAttribute('aria-current',b.dataset.activity===currentActivity.id?'step':'false');});
 const url=`/activity.html?id=${encodeURIComponent(currentActivity.id)}&protocol=splice`;
 frame.src=url;
 $('yamlLink').href='/content/'+currentActivity.path;
 $('standalone').href=url;
 $('activityKind').textContent=currentActivity.type.replaceAll('-',' ').toUpperCase();
 $('markReviewed').hidden=!['worked-example','macro-visualization'].includes(currentActivity.type);
 $('markReviewed').textContent=currentActivity.type==='macro-visualization'?'Mark step-through reviewed':'Mark example reviewed';
 $('saveStatus').textContent='Your progress stays in this browser. Open the activity’s hints whenever you need a nudge; hints do not reduce your score.';
 history.replaceState(null,'',`/?module=${currentModule.slug}&activity=${currentActivity.id}`);
 saved.lastModule=currentModule.slug;saved.lastActivity=currentActivity.id;persist();updateProgress();
}
function log(direction,message){
 saved.events.push({time:new Date().toISOString(),direction,activity:currentActivity?.id,message});
 saved.events=saved.events.slice(-500);persist();renderMessages();
}
function renderMessages(){
 $('messageCount').textContent=saved.events.length;
 const counts={};for(const e of saved.events){const s=e.message.subject;counts[s]=(counts[s]||0)+1;}
 $('protocolStats').textContent=Object.entries(counts).map(([k,v])=>`${k}: ${v}`).join('  /  ');
 $('messages').textContent=saved.events.slice(-35).map(e=>`${e.time} ${e.direction} [${e.activity}]\n${JSON.stringify(e.message,null,2)}`).reverse().join('\n\n');
}
window.addEventListener('message',event=>{
 if(event.source!==frame.contentWindow||event.origin!==location.origin)return;
 const m=event.data;if(!m||typeof m!=='object'||typeof m.subject!=='string'||!currentActivity)return;
 if(!['SPLICE.getState','SPLICE.reportScoreAndState','SPLICE.sendEvent','lti.frameResize'].includes(m.subject)||typeof m.message_id!=='string')return;
 const declaredId=m.content_id||m.data?.activityId||m.data?.activity_id||m.state?.activityId||m.data?.queryParams?.id;
 if(declaredId&&declaredId!==currentActivity.id)return;
 log('← content',m);
 if(m.subject==='SPLICE.getState'){
  const p=saved.activities[currentActivity.id];const response={subject:'SPLICE.getState.response',message_id:m.message_id,state:p?.state??null,context_id:'cupcake-cpp-local-demo'};
  event.source.postMessage(response,event.origin);log('→ content',response);
 }else if(m.subject==='SPLICE.reportScoreAndState'){
  if(typeof m.score!=='number'||!Number.isFinite(m.score)||m.score<0||m.score>1)return;
  const old=saved.activities[currentActivity.id]||{};
  saved.activities[currentActivity.id]={...old,score:m.score,state:{...(old.state||{}),...(m.state||{}),score:m.score},updated:new Date().toISOString()};persist();updateProgress();renderModules();
 }else if(m.subject==='SPLICE.sendEvent'&&m.name==='studio.submission'){
  const old=saved.activities[currentActivity.id]||{};
  saved.activities[currentActivity.id]={...old,state:{...(old.state||{}),schemaVersion:2,activityId:currentActivity.id,submission:m.data?.submission,draft:m.data?.submission},updated:new Date().toISOString()};persist();
 }else if(m.subject==='SPLICE.sendEvent'&&m.name==='codeEdited'&&currentActivity.type==='free-coding'){
  const index=m.data?.regionIndex,text=m.data?.editedContent;
  if(Number.isInteger(index)&&index>=0&&index<40&&typeof text==='string'){
   const old=saved.activities[currentActivity.id]||{},answers=[...(old.state?.draft?.answers||[])];answers[index]=text;
   saved.activities[currentActivity.id]={...old,state:{...(old.state||{}),schemaVersion:2,activityId:currentActivity.id,draft:{answers}},updated:new Date().toISOString()};persist();
   $('saveStatus').textContent='Draft saved in this browser. You can return to this code later; Check Answer records a checked result.';
  }
 }else if(m.subject==='lti.frameResize'){
  if(!m.studio_document)return;
  if(Number.isFinite(m.height))frame.style.height=`${Math.max(350,Math.min(12000,Math.ceil(m.height)+40))}px`;
 }
});
function download(name,data){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
$('search').oninput=renderModules;
$('readDone').onchange=()=>{saved.readings[currentModule.slug]=$('readDone').checked;persist();};
$('markReviewed').onclick=()=>{const p=saved.activities[currentActivity.id]||{};saved.activities[currentActivity.id]={...p,reviewed:true,updated:new Date().toISOString()};persist();updateProgress();renderModules();};
$('protocolToggle').onclick=()=>{const open=$('inspector').hidden;$('inspector').hidden=!open;$('protocolToggle').setAttribute('aria-expanded',String(open));renderMessages();};
$('export').onclick=()=>download('cupcake-cpp-progress.json',{course:course.id,exported:new Date().toISOString(),...saved});
$('exportEvents').onclick=()=>download('cupcake-cpp-splice-events.json',saved.events);
$('copyEmbed').onclick=async()=>{const html=`<iframe src="${location.origin}/activity.html?id=${encodeURIComponent(currentActivity.id)}&protocol=splice" title="${currentActivity.title}" width="100%" height="800" style="border:0"></iframe>`;try{await navigator.clipboard.writeText(html);$('saveStatus').textContent='Iframe markup copied. The local server must be running on the viewing machine.';}catch{$('saveStatus').textContent=html;}};
$('nextActivity').onclick=()=>{const i=currentModule.activities.findIndex(a=>a.id===currentActivity.id);if(i+1<currentModule.activities.length)openActivity(currentModule.activities[i+1].id);else{const cap=course.capstones.find(c=>c.after===currentModule.number);if(cap)openModule(cap.slug);else{const n=typeof currentModule.number==='number'?currentModule.number:currentModule.after;openModule(course.modules[n]?.slug||course.modules[0].slug);}}};
try{const r=await fetch('/course.json');if(!r.ok)throw Error(`Course could not load (${r.status})`);course=await r.json();const params=new URLSearchParams(location.search);openModule(params.get('module')||saved.lastModule||course.modules[0].slug,params.get('activity')||saved.lastActivity);renderMessages();}catch(e){$('title').textContent='Unable to load the course';$('subtitle').textContent=e.message;}
