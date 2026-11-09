// A deliberately small, escaped renderer for the headings, lists, and code fences
// used by our authored lesson notes. No raw HTML is accepted.
export const escape=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const inline=text=>escape(text).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
export function renderMarkdown(text){
 const lines=String(text||'').split('\n');let html='',paragraph=[],list=[],fence=null,code=[];
 const flush=()=>{if(paragraph.length){html+=`<p>${inline(paragraph.join(' '))}</p>`;paragraph=[];}if(list.length){html+='<ul>'+list.map(s=>`<li>${inline(s)}</li>`).join('')+'</ul>';list=[];}};
 for(const line of lines){
  if(line.startsWith('```')){if(fence!==null){html+=`<pre tabindex="0"><code>${escape(code.join('\n'))}</code></pre>`;fence=null;code=[];}else{flush();fence=line.slice(3);}continue;}
  if(fence!==null){code.push(line);continue;}
  if(/^#{1,4} /.test(line)){flush();html+=`<h3>${inline(line.replace(/^#+ /,''))}</h3>`;}
  else if(/^- /.test(line)){if(paragraph.length)flush();list.push(line.slice(2));}
  else if(!line.trim())flush();
  else{if(list.length)flush();paragraph.push(line.trim());}
 }
 flush();return html;
}
