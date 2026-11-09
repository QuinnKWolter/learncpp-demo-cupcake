import{Ia as p,Ja as o,Ka as d,La as f,Na as M,Oa as v,Pa as S,Qa as R,Ra as j,Sa as L,Ub as D,V as P,Vb as k,W as H,X as x,Xa as h,Y as w,Za as N,_b as Q,bc as q,da as F,hb as B,ia as c,ib as g,oa as _,pb as O,rb as W,sa as V,tb as z,ua as y,ub as $,vb as A,yb as G}from"./chunk-G6DDNVI7.js";function U(i,t){if(!i||!t||!t.snippet&&!t.pattern)return null;let{snippet:e,pattern:n,context:r,nth:a=1}=t,l=i,m=0;if(r){let s=i.indexOf(r);if(s===-1)return null;l=r,m=s}if(n)try{let s=new RegExp(n,"g"),u=null,b=0;for(;(u=s.exec(l))!==null;){if(b++,b===a)return{start:m+u.index,length:u[0].length};u[0].length===0&&s.lastIndex++}return null}catch{return null}if(e){let s=-1;for(let u=0;u<a;u++)if(s=l.indexOf(e,s+1),s===-1)return null;return{start:m+s,length:e.length}}return null}var E=class extends Q{toDOM(){let t=document.createElement("span");return t.className="cm-fold-gutter-ellipsis",t.innerHTML='<svg width="14" height="8" viewBox="0 0 16 8" fill="currentColor" style="display:inline-block; vertical-align:middle;"><circle cx="2.5" cy="4" r="1.75"/><circle cx="8" cy="4" r="1.75"/><circle cx="13.5" cy="4" r="1.75"/></svg>',t.title="Collapsed lines",t}},ue=q.of((i,t)=>t instanceof C?new E:null),C=class extends D{constructor(e,n,r){super();this.summary=e;this.lineCount=n;this.onToggle=r}summary;lineCount;onToggle;eq(e){return this.summary===e.summary&&this.lineCount===e.lineCount}toDOM(){let e=document.createElement("span");e.className="cm-fold-pill",e.title="Click to expand collapsed section";let n=document.createElement("span");n.className="cm-fold-icon",n.textContent="\u25B6",e.appendChild(n);let r=document.createElement("span");r.className="cm-fold-title",r.textContent=this.summary,e.appendChild(r);let a=document.createElement("span");return a.className="cm-fold-count",a.textContent=`(${this.lineCount} ${this.lineCount===1?"line":"lines"} collapsed \u2014 click to view)`,e.appendChild(a),e.onclick=l=>{l.stopPropagation(),l.preventDefault(),this.onToggle()},e}},T=class extends D{constructor(e,n){super();this.summary=e;this.onToggle=n}summary;onToggle;eq(e){return this.summary===e.summary}toDOM(){let e=document.createElement("div");e.className="cm-fold-expanded-header",e.title="Click to collapse section";let n=document.createElement("span");n.className="cm-fold-icon",n.textContent="\u25BC",e.appendChild(n);let r=document.createElement("span");r.className="cm-fold-title",r.textContent=this.summary,e.appendChild(r);let a=document.createElement("span");return a.className="cm-fold-hint",a.textContent="(click to collapse)",e.appendChild(a),e.onclick=l=>{l.stopPropagation(),l.preventDefault(),this.onToggle()},e}};function K(i,t,e,n){let r=[],a=[];(t||[]).forEach((l,m)=>{l?.type==="fold"&&l.location&&a.push({element:l,index:m})});for(let{element:l,index:m}of a){let s=U(i,l.location);if(!s)continue;let u=e[m]!==void 0?e[m]:l.collapsed!==!1,b=l.summary||"Collapsed Code";if(u){let J=i.substring(s.start,s.start+s.length).split(`
`).length;r.push(k.replace({widget:new C(b,J,()=>n(m)),block:!0,inclusive:!0}).range(s.start,s.start+s.length))}else r.push(k.widget({widget:new T(b,()=>n(m)),block:!0,side:-1}).range(s.start))}return r}function fe(i,t,e,n){let r=K(i,t,e,n);return r.sort((a,l)=>a.from-l.from||a.to-l.to),k.set(r)}var X=["previewFrame"],I=(i,t)=>({"bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-xs font-semibold":i,"text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100":t}),Z=i=>({"bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] dark:bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px]":i}),ee=(i,t)=>({width:i,height:t}),te=(i,t)=>({"rounded-2xl border-4 border-slate-700 dark:border-slate-600 shadow-xl":i,"rounded-xl border-3 border-slate-600 dark:border-slate-500 shadow-lg":t});function ne(i,t){i&1&&(o(0,"div",32),f(1,"div",33),d())}function ie(i,t){i&1&&(o(0,"div",34),f(1,"div",35),d())}function re(i,t){if(i&1){let e=M();o(0,"iframe",36,0),v("load",function(){P(e);let r=S();return H(r.onIframeLoad())}),d()}}function oe(i,t){i&1&&(o(0,"div",37)(1,"span",38),h(2,"\u21BB"),d(),o(3,"span"),h(4,"Loading preview..."),d()())}function le(i,t){if(i&1&&(o(0,"div",39),h(1),d()),i&2){let e=S();c(),N(" ",e.viewport==="mobile"?"375 \xD7 667 (Mobile)":"720 \xD7 960 (Tablet)"," ")}}var Y=class i{constructor(t,e){this.cdr=t;this.sanitizer=e}cdr;sanitizer;html="";css="";title="index.html";height="300px";previewFrame;viewport="desktop";rawDoc="";compiledSrcDoc="";isReloading=!1;ngAfterViewInit(){this.renderDocToIframe()}ngOnChanges(t){this.updatePreview()}onIframeLoad(){this.renderDocToIframe()}get tabTitle(){return this.title&&this.title!=="Live Web Preview"?this.title:this.html?"index.html":"style.css"}get displayPath(){return this.tabTitle.toLowerCase().replace(/\s+/g,"-")}setViewport(t){this.viewport=t,this.cdr.markForCheck()}get viewportWidth(){switch(this.viewport){case"mobile":return"375px";case"tablet":return"720px";default:return"100%"}}reloadPreview(){this.isReloading=!0,this.cdr.markForCheck(),setTimeout(()=>{this.isReloading=!1,this.cdr.markForCheck(),setTimeout(()=>this.renderDocToIframe(),0)},100)}renderDocToIframe(){if(!this.previewFrame?.nativeElement||!this.rawDoc)return;let t=this.previewFrame.nativeElement;try{let e=t.contentDocument||t.contentWindow?.document;e&&(e.open(),e.write(this.rawDoc),e.close())}catch{}}updatePreview(){let t=(this.html||"").trim(),e=(this.css||"").trim();!t&&e&&(t=`
<div class="bank-account" id="account-card">
  <div class="account-header">
    <h2 class="account-owner">Bob</h2>
  </div>
  <div class="account-transactions">
    <p class="transaction-deposit">Deposited 100</p>
    <p class="transaction-withdraw">Withdrew 50</p>
  </div>
  <div class="account-balance">
    <p class="balance-output">Balance: 250</p>
  </div>
  <div class="account-actions">
    <button class="btn btn-deposit" id="btn-deposit">Deposit 100</button>
    <button class="btn btn-withdraw" id="btn-withdraw">Withdraw 50</button>
  </div>
</div>`);let n=e;n&&!t.includes("<style")&&(t=`<style>
${n}
</style>
${t}`);let a=`<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
<style>
  *, *::before, *::after { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 16px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.5;
  }
  button {
    font-family: inherit;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background-color: #f8fafc;
    color: #0f172a;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
  }
  button:hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
  }
  input, select, textarea {
    font-family: inherit;
    font-size: 0.875rem;
    padding: 6px 10px;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
  }
</style>
</head>
<body>
  ${t}
</body>
</html>`;this.rawDoc=a,this.compiledSrcDoc=this.sanitizer.bypassSecurityTrustHtml(a),this.renderDocToIframe(),this.cdr.markForCheck()}static \u0275fac=function(e){return new(e||i)(_(O),_(G))};static \u0275cmp=V({type:i,selectors:[["app-html-preview"]],viewQuery:function(e,n){if(e&1&&R(X,5),e&2){let r;j(r=L())&&(n.previewFrame=r.first)}},inputs:{html:"html",css:"css",title:"title",height:"height"},features:[F],decls:40,vars:28,consts:[["previewFrame",""],[1,"border","border-slate-300","dark:border-slate-700/80","rounded-xl","overflow-hidden","bg-slate-100","dark:bg-slate-900","shadow-md","flex","flex-col","transition-all","text-xs"],[1,"bg-slate-200/90","dark:bg-slate-800","px-3","py-2","flex","items-center","justify-between","border-b","border-slate-300","dark:border-slate-700/80","select-none","gap-3"],[1,"flex","items-center","gap-1.5","shrink-0"],[1,"w-3","h-3","rounded-full","bg-rose-500/90","border","border-rose-600/40","inline-block","shadow-xs"],[1,"w-3","h-3","rounded-full","bg-amber-400/90","border","border-amber-500/40","inline-block","shadow-xs"],[1,"w-3","h-3","rounded-full","bg-emerald-500/90","border","border-emerald-600/40","inline-block","shadow-xs"],[1,"flex-1","flex","items-center","justify-start","gap-2","px-3","py-1.5","bg-white","dark:bg-slate-900","rounded-lg","border","border-slate-300","dark:border-slate-700","text-[11px]","text-slate-600","dark:text-slate-300","shadow-xs","max-w-xl"],["viewBox","0 0 24 24","fill","none","stroke","currentColor","stroke-width","2","stroke-linecap","round","stroke-linejoin","round",1,"w-3.5","h-3.5","text-emerald-500","shrink-0","block"],["x","3","y","11","width","18","height","11","rx","2","ry","2"],["d","M7 11V7a5 5 0 0 1 10 0v4"],[1,"font-mono","text-slate-700","dark:text-slate-200","truncate","leading-none","pt-[1px]"],[1,"flex","items-center","gap-1","shrink-0","bg-slate-300/80","dark:bg-slate-700/80","p-0.5","rounded-lg"],["type","button","title","Desktop View (100%)",1,"px-2","py-1","text-[11px]","rounded-md","transition-all","cursor-pointer","border-none","inline-flex","items-center","justify-center","gap-1.5",3,"click","ngClass"],["viewBox","0 0 24 24","fill","none","stroke","currentColor","stroke-width","2","stroke-linecap","round","stroke-linejoin","round",1,"w-3.5","h-3.5","shrink-0","block"],["x","2","y","3","width","20","height","14","rx","2","ry","2"],["x1","8","y1","21","x2","16","y2","21"],["x1","12","y1","17","x2","12","y2","21"],[1,"leading-none","pt-[1px]"],["type","button","title","Tablet View (720px)",1,"px-2","py-1","text-[11px]","rounded-md","transition-all","cursor-pointer","border-none","inline-flex","items-center","justify-center","gap-1.5",3,"click","ngClass"],["x","4","y","2","width","16","height","20","rx","2","ry","2"],["x1","12","y1","18","x2","12.01","y2","18"],["type","button","title","Mobile View (375px)",1,"px-2","py-1","text-[11px]","rounded-md","transition-all","cursor-pointer","border-none","inline-flex","items-center","justify-center","gap-1.5",3,"click","ngClass"],["x","5","y","2","width","14","height","20","rx","2","ry","2"],[1,"w-full","bg-slate-100/90","dark:bg-slate-950","flex","flex-col","justify-start","items-center","p-3","overflow-auto","min-h-[220px]",3,"ngClass"],[1,"bg-white","rounded-lg","shadow-md","overflow-hidden","transition-all","duration-300","border","border-slate-300/80","dark:border-slate-700/80","flex","flex-col",3,"ngStyle","ngClass"],["class","bg-slate-800 h-4 flex items-center justify-center shrink-0",4,"ngIf"],["class","bg-slate-800 h-3 flex items-center justify-center shrink-0",4,"ngIf"],[1,"w-full","flex-1","bg-white","relative"],["class","w-full h-full border-none block bg-white","sandbox","allow-scripts allow-same-origin","title","Live Browser Web Preview",3,"load",4,"ngIf"],["class","w-full h-full flex items-center justify-center bg-white/80 dark:bg-slate-900/80 text-slate-500 text-xs gap-2",4,"ngIf"],["class","mt-2 px-2 py-0.5 bg-slate-200/80 dark:bg-slate-800/80 text-slate-500 dark:text-slate-400 rounded text-[10px] font-mono select-none",4,"ngIf"],[1,"bg-slate-800","h-4","flex","items-center","justify-center","shrink-0"],[1,"w-12","h-1","bg-slate-600","rounded-full"],[1,"bg-slate-800","h-3","flex","items-center","justify-center","shrink-0"],[1,"w-1.5","h-1.5","bg-slate-600","rounded-full"],["sandbox","allow-scripts allow-same-origin","title","Live Browser Web Preview",1,"w-full","h-full","border-none","block","bg-white",3,"load"],[1,"w-full","h-full","flex","items-center","justify-center","bg-white/80","dark:bg-slate-900/80","text-slate-500","text-xs","gap-2"],[1,"animate-spin","text-sm"],[1,"mt-2","px-2","py-0.5","bg-slate-200/80","dark:bg-slate-800/80","text-slate-500","dark:text-slate-400","rounded","text-[10px]","font-mono","select-none"]],template:function(e,n){e&1&&(o(0,"div",1)(1,"div",2)(2,"div",3),f(3,"span",4)(4,"span",5)(5,"span",6),d(),o(6,"div",7),x(),o(7,"svg",8),f(8,"rect",9)(9,"path",10),d(),w(),o(10,"span",11),h(11,"https://localhost/preview"),d()(),o(12,"div",12)(13,"button",13),v("click",function(){return n.setViewport("desktop")}),x(),o(14,"svg",14),f(15,"rect",15)(16,"line",16)(17,"line",17),d(),w(),o(18,"span",18),h(19,"Desktop"),d()(),o(20,"button",19),v("click",function(){return n.setViewport("tablet")}),x(),o(21,"svg",14),f(22,"rect",20)(23,"line",21),d(),w(),o(24,"span",18),h(25,"Tablet"),d()(),o(26,"button",22),v("click",function(){return n.setViewport("mobile")}),x(),o(27,"svg",14),f(28,"rect",23)(29,"line",21),d(),w(),o(30,"span",18),h(31,"Mobile"),d()()()(),o(32,"div",24)(33,"div",25),y(34,ne,2,0,"div",26)(35,ie,2,0,"div",27),o(36,"div",28),y(37,re,2,0,"iframe",29)(38,oe,5,0,"div",30),d()(),y(39,le,2,1,"div",31),d()()),e&2&&(c(13),p("ngClass",g(11,I,n.viewport==="desktop",n.viewport!=="desktop")),c(7),p("ngClass",g(14,I,n.viewport==="tablet",n.viewport!=="tablet")),c(6),p("ngClass",g(17,I,n.viewport==="mobile",n.viewport!=="mobile")),c(6),p("ngClass",B(20,Z,n.viewport!=="desktop")),c(),p("ngStyle",g(22,ee,n.viewportWidth,n.height))("ngClass",g(25,te,n.viewport==="mobile",n.viewport==="tablet")),c(),p("ngIf",n.viewport==="mobile"),c(),p("ngIf",n.viewport==="tablet"),c(2),p("ngIf",!n.isReloading),c(),p("ngIf",n.isReloading),c(),p("ngIf",n.viewport!=="desktop"))},dependencies:[A,W,z,$],encapsulation:2,changeDetection:0})};export{U as a,ue as b,K as c,fe as d,Y as e};
