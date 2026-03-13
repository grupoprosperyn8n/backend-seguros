const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatToggle = document.getElementById('chat-toggle');
const chatContainer = document.getElementById('chat-container');
const closeChat = document.getElementById('close-chat');

// Lógica de apertura/cierre
function toggleChat() {
    chatContainer.classList.toggle('hidden');
    if (!chatContainer.classList.contains('hidden')) {
        userInput.focus();
        const badge = document.querySelector('.notification-badge');
        if (badge) badge.style.display = 'none';
    }
}

if (chatToggle) chatToggle.addEventListener('click', toggleChat);
if (closeChat) closeChat.addEventListener('click', toggleChat);

// Exponer función global para abrir desde el portal o linktree
window.openInsuranceChat = function() {
    if (chatContainer) {
        chatContainer.classList.remove('hidden');
        userInput.focus();
    } else {
        console.error('Chat container not found');
    }
};

// Configuración del Webhook de n8n
const N8N_WEBHOOK_URL = 'https://n8n-production-786d.up.railway.app/webhook/chat-insurance';

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    
    messageDiv.innerHTML = `
        <div class="bubble">
            ${text}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    userInput.value = '';
    addMessage(text, 'user');

    // Efecto de carga
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'assistant', 'typing');
    typingDiv.innerHTML = `<div class="bubble">Pensando...</div>`;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: text,
                platform: 'web',
                userId: 'user_temp_' + (localStorage.getItem('dni') || 'anonymous')
            })
        });

        const data = await response.json();
        chatMessages.removeChild(typingDiv);
        
        if (data.output) {
            addMessage(data.output, 'assistant');
        } else {
            addMessage("Lo siento, tuve un problema al procesar tu solicitud.", 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        if (chatMessages.contains(typingDiv)) chatMessages.removeChild(typingDiv);
        addMessage("Error de conexión con el servidor.", 'assistant');
    }
}

if (sendBtn) sendBtn.addEventListener('click', sendMessage);
if (userInput) userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
