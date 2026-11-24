import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { FileText, Mic, Send, Trash2, UploadCloud, Volume2 } from 'lucide-react';
import './styles.css';

const API = 'http://localhost:8000';
type Doc = { id:string; filename:string; chunks:number };
type Source = { filename:string; page:number|null; excerpt:string; score:number };
type Message = { role:'user'|'assistant'; text:string; sources?:Source[] };

function App() {
  const [docs,setDocs] = useState<Doc[]>([]); const [question,setQuestion] = useState('');
  const [messages,setMessages] = useState<Message[]>([]); const [busy,setBusy] = useState(false); const [recording,setRecording] = useState(false);
  const load = () => fetch(`${API}/api/documents`).then(r=>r.json()).then(setDocs);
  useEffect(()=>{ load(); },[]);
  async function upload(file:File) { const body=new FormData(); body.append('file',file); await fetch(`${API}/api/documents/upload`,{method:'POST',body}); load(); }
  async function ask() { if(!question.trim()||busy)return; const q=question; setQuestion(''); setMessages(m=>[...m,{role:'user',text:q}]); setBusy(true); const r=await fetch(`${API}/api/chat`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})}); const data=await r.json(); setMessages(m=>[...m,{role:'assistant',text:data.answer,sources:data.sources}]); setBusy(false); }
  async function remove(id:string){await fetch(`${API}/api/documents/${id}`,{method:'DELETE'});load();}
  return <div className="app"><aside><div className="brand"><div className="logo">V</div><div><strong>VoxKnowledge</strong><small>Voice-first document intelligence</small></div></div><label className="upload"><UploadCloud size={18}/> Add documents<input type="file" accept=".pdf,.txt,.md,.docx" onChange={e=>e.target.files?.[0]&&upload(e.target.files[0])}/></label><div className="section-title">Knowledge base <span>{docs.length}</span></div><div className="docs">{docs.map(d=><div className="doc" key={d.id}><FileText size={17}/><div><b>{d.filename}</b><small>{d.chunks} indexed chunks</small></div><button onClick={()=>remove(d.id)}><Trash2 size={15}/></button></div>)}{!docs.length&&<p className="muted">Upload a document to begin.</p>}</div></aside><main><header><div><p className="eyebrow">PERSONAL KNOWLEDGE SPACE</p><h1>Ask your documents<br/><em>anything.</em></h1></div><div className="status"><span/> Local RAG online</div></header><section className="chat">{!messages.length?<div className="empty"><div className="orb"><Volume2 size={27}/></div><h2>Your knowledge, in conversation.</h2><p>Upload a source, then ask a question. Every answer includes the passages it used.</p></div>:messages.map((m,i)=><div className={`message ${m.role}`} key={i}><div className="avatar">{m.role==='user'?'You':'V'}</div><div><p>{m.text}</p>{m.sources?.map((s,j)=><div className="source" key={j}><FileText size={14}/><span>{s.filename}{s.page?` · p. ${s.page}`:''}</span><small>{s.excerpt}</small></div>)}</div></div>)}</section><div className="composer"><button className={recording?'recording':''} onClick={()=>setRecording(!recording)}><Mic size={20}/></button><input value={question} onChange={e=>setQuestion(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()} placeholder={recording?'Listening…':'Ask about your knowledge base'} /><button className="send" onClick={ask} disabled={busy}><Send size={19}/></button></div><p className="hint">VoxKnowledge can make mistakes. Verify important information in the cited source.</p></main></div>
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
