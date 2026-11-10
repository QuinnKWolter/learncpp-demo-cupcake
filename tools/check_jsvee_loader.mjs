// Execute the actual served vendor loader against a small DOM stub, then fetch
// every generated URL. This tests runtime base concatenation, not string presence.
import assert from 'node:assert/strict';
import vm from 'node:vm';

const origin=process.argv[2]||'http://127.0.0.1:20700';
const prefix=process.env.CUPCAKE_BASE_PATH||'/learncpp-demo-cupcake';
async function text(path){const r=await fetch(origin+path);assert.equal(r.status,200,path);return r.text();}
const html=await text(prefix+'/activity.html');
const base=html.match(/<base href="([^"]+)"/)[1];
const source=await text(prefix+'/vendor/cupcake/chunk-PE6JJOUT.js');
const urls=[];
const document={
 querySelector(selector){return selector==='base'?{getAttribute:()=>base}:null;},
 createElement(tag){
  const attrs={};
  return {tag,setAttribute(name,value){attrs[name]=value;},
   get href(){return attrs.href;},set src(value){attrs.src=value;},get src(){return attrs.src;}};
 },
 head:{appendChild(element){urls.push({tag:element.tag,url:new URL(element.href||element.src,new URL(base,origin)).href});element.onload?.();}}
};
const styleStart=source.indexOf('loadStyle(t){');
const styleEnd=source.indexOf('}onResize=',styleStart)+1;
assert(styleStart>=0&&styleEnd>styleStart,'Pinned vendor style-loader anchor changed');
const style=vm.runInNewContext('({'+source.slice(styleStart,styleEnd)+'})',{document});
const styles=[...source.matchAll(/this\.loadStyle\("([^"]+)"\)/g)].map(m=>m[1]);
assert.equal(styles.length,2);
for(const path of styles)style.loadStyle(path);
const scriptAnchor='let t=e=>new Promise((i,o)=>{';
const scriptStart=source.indexOf(scriptAnchor)+6;
const scriptEnd=source.indexOf(';try{yield t(',scriptStart);
assert(scriptStart>=6&&scriptEnd>scriptStart,'Pinned vendor script-loader anchor changed');
const loadScript=vm.runInNewContext('('+source.slice(scriptStart,scriptEnd)+')',{document,Promise});
const scripts=[...source.slice(scriptEnd,scriptEnd+350).matchAll(/yield t\("([^"]+)"\)/g)].map(m=>m[1]);
assert.equal(scripts.length,3);
for(const path of scripts)await loadScript(path);
assert.equal(urls.length,5);
for(const {tag,url} of urls){
 const parsed=new URL(url);
 assert(parsed.pathname.startsWith(prefix+'/vendor/cupcake/lib/jsvee/'),url);
 assert.equal(parsed.pathname.split(prefix).length-1,1,'Deployment prefix occurs twice: '+url);
 const response=await fetch(url);
 assert.equal(response.status,200,url);
 assert.match(response.headers.get('content-type'),tag==='link'?/^text\/css\b/:/^(?:text|application)\/(?:java|ecma)script\b/,url);
 // CSS refers to these sibling images; test browser-style relative resolution too.
 if(tag==='link'){
  for(const match of (await response.text()).matchAll(/url\(["']?([^"')]+)["']?\)/g)){
   if(/^(?:https?:|data:)/.test(match[1]))continue;
   const asset=new URL(match[1],url),image=await fetch(asset);
   assert.equal(image.status,200,asset.href);
   await image.arrayBuffer();
  }
 }else await response.arrayBuffer();
}
console.log('Actual vendor JSVEE loaders passed: 2 stylesheets, 3 scripts, sibling images, one prefix and correct MIME types.');
