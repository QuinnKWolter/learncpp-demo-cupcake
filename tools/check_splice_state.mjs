// Focused host-message tests with synthetic inputs. This is not a browser UI test.
import {readFileSync,writeFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=readFileSync(new URL('../web/studio.js',import.meta.url),'utf8');
const start=source.indexOf("window.addEventListener('message',event=>{");
const end=source.indexOf('\nfunction download',start);
assert(start>=0&&end>start);
let handler;const responses=[],events=[],status={textContent:''};
const sender={postMessage:(message,origin)=>responses.push({message,origin})};
const saved={activities:{}};
let writes=0;
const context=vm.createContext({
 window:{addEventListener:(name,callback)=>{assert.equal(name,'message');handler=callback;}},
 location:{origin:'http://127.0.0.1:5173'},frame:{contentWindow:sender,style:{}},
 currentActivity:{id:'cpp23-v2-test-free-coding',type:'free-coding'},saved,
 log:(direction,message)=>events.push({direction,message}),persist:()=>writes++,
 updateProgress:()=>{},renderModules:()=>{},$:()=>status,Date,Number,Math,
});
vm.runInContext(source.slice(start,end),context);
const checks=[];
const send=(message,overrides={})=>handler({source:sender,origin:'http://127.0.0.1:5173',data:{message_id:'test-'+events.length,...message},...overrides});
send({subject:'SPLICE.sendEvent',name:'codeEdited',data:{regionIndex:0,editedContent:'return 4;'}},{origin:'https://unrelated.invalid'});
send({subject:'SPLICE.sendEvent',name:'codeEdited',data:{regionIndex:0,editedContent:'return 4;'}},{source:{}});
send({subject:'SPLICE.sendEvent',content_id:'other',name:'codeEdited',data:{regionIndex:0,editedContent:'return 4;'}});
assert.equal(writes,0);checks.push('Reject foreign origin, foreign iframe, and mismatched identity');
const id=context.currentActivity.id;
send({subject:'SPLICE.reportScoreAndState',score:1,state:{activityId:id,eventName:'answerChecked'}});
send({subject:'SPLICE.sendEvent',name:'codeEdited',data:{regionIndex:0,editedContent:'return width * height;'}});
send({subject:'SPLICE.sendEvent',name:'codeEdited',data:{regionIndex:1,editedContent:'return false;'}});
assert.equal(saved.activities[id].score,1);
assert.equal(saved.activities[id].state.draft.answers[0],'return width * height;');
assert.equal(saved.activities[id].state.draft.answers[1],'return false;');
checks.push('Save both draft regions without changing the last checked score');
send({subject:'SPLICE.getState',message_id:'correlated-state-request'});
assert.equal(responses.at(-1).message.message_id,'correlated-state-request');
assert.equal(responses.at(-1).message.state.draft.answers[1],'return false;');
assert.equal(responses.at(-1).origin,'http://127.0.0.1:5173');
checks.push('Return draft and checked state with the request correlation ID');
send({subject:'SPLICE.sendEvent',name:'studio.submission',data:{submission:{answers:['return 8;','return true;']}}});
send({subject:'SPLICE.reportScoreAndState',score:.5,state:{eventName:'answerChecked'}});
assert.equal(saved.activities[id].state.submission.answers[0],'return 8;');
assert.equal(saved.activities[id].state.draft.answers[1],'return true;');
assert.equal(saved.activities[id].score,.5);
checks.push('Keep checked code when a native score report has a different state shape');
send({subject:'SPLICE.reportScoreAndState',score:2,state:{}});
assert.equal(saved.activities[id].score,.5);
send({subject:'lti.frameResize',height:200});assert.equal(context.frame.style.height,undefined);
send({subject:'lti.frameResize',height:1400,studio_document:true});assert.equal(context.frame.style.height,'1440px');
checks.push('Reject invalid scores and use guidance-inclusive document resizing');
const before=writes;
send({subject:'SPLICE.sendEvent',name:'codeEdited',data:{regionIndex:-1,editedContent:'bad'}});
send({subject:'SPLICE.sendEvent',name:'codeEdited',data:{regionIndex:0,editedContent:42}});
assert.equal(writes,before);checks.push('Reject invalid draft region indices and non-text edits');
const report={kind:'synthetic message-handler integration checks',browserTest:false,passed:checks.length,checks};
writeFileSync(new URL('../research/splice-state-checks.json',import.meta.url),JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
