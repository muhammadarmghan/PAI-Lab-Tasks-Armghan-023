const form = document.getElementById('chat-form');
const messages = document.getElementById('messages');

function appendMessage(text, who='bot'){
  const d = document.createElement('div');
  d.className = 'msg ' + who;
  if(who === 'bot'){
    // render simple menu items or plain text
    try{
      const obj = JSON.parse(text);
      if(obj.intent === 'menu'){
        obj.menu.forEach(it => {
          const row = document.createElement('div'); row.className='menu-item';
          row.innerHTML = `<div>${it.name}</div><div class="meta">${it.price}</div>`;
          messages.appendChild(row);
        });
        return;
      }
      if(obj.intent === 'reservation'){
        d.innerText = `Reservations available: ${obj.available} — Next: ${obj.next_available}`;
      } else if(obj.intent === 'order'){
        d.innerText = obj.status ? `Order ${obj.order_no}: ${obj.status}` : obj.message || JSON.stringify(obj);
      } else if(obj.intent === 'fallback'){
        d.innerText = obj.message;
      } else {
        d.innerText = JSON.stringify(obj);
      }
    }catch(e){
      d.innerText = text;
    }
  } else {
    d.innerText = text;
  }
  messages.appendChild(d);
}

form.addEventListener('submit', async (ev)=>{
  ev.preventDefault();
  const q = document.getElementById('query').value.trim();
  if(!q) return;
  appendMessage(q, 'user');
  document.getElementById('query').value='';
  appendMessage('...', 'bot');
  const botPlaceholder = messages.lastChild;
  try{
    const res = await fetch('/api/query', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({query: q})});
    const data = await res.json();
    // replace placeholder
    messages.removeChild(botPlaceholder);
    appendMessage(JSON.stringify(data), 'bot');
  }catch(err){
    messages.removeChild(botPlaceholder);
    appendMessage('Server error: '+err.message,'bot');
  }
  messages.scrollTop = messages.scrollHeight;
});
