const chats = document.querySelector('.log')
const message = document.querySelector('#message')
const submitForm = document.querySelector('#submit-form')


const renderLogs = async (logs) => {
    chats.replaceChildren([])
    logs.forEach((log, i) => {
        const spanEl = document.createElement('span')
        spanEl.className = 'chat';
        spanEl.innerHTML = log[i];
        chats.appendChild(spanEl);
    });
}

const handleSubmit = async (e) => {
    e.preventDefault();
    const messageToSend = message.value;
    const body = new FormData();
    body.append('message', messageToSend)
    await fetch(`/chatroom`, {
        method: 'POST',
        body,
    }).then(res => res.json())
        .then(logs => renderLogs(logs))
}

submitForm.addEventListener('submit', handleSubmit)