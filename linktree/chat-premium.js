// Configuración del Webhook de n8n
const N8N_CHAT_WEBHOOK = 'https://primary-production-0abcf.up.railway.app/webhook/chat-insurance';

// Elementos del DOM
const chatContainer = document.getElementById('chat-container-premium');
const chatMessages = document.getElementById('chat-messages-premium');
const chatInput = document.getElementById('chat-input-premium');
const sendBtn = document.getElementById('send-btn-premium');
const chatToggle = document.getElementById('chat-toggle-premium');
const closeBtn = document.getElementById('close-chat-premium');
const micBtn = document.getElementById('mic-btn-premium');
const attachBtn = document.getElementById('attach-btn-premium');
const fileInput = document.getElementById('file-input-premium');
const recordingOverlay = document.getElementById('recording-overlay-premium');
const recordingTimer = document.getElementById('recording-timer-premium');

// Estado de grabación
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let recordingInterval;
let recordingSeconds = 0;

// Lógica de apertura/cierre
function toggleChat() {
    chatContainer.classList.toggle('hidden');
    if (!chatContainer.classList.contains('hidden')) {
        chatInput.focus();
    }
}

if (chatToggle) chatToggle.addEventListener('click', toggleChat);
if (closeBtn) closeBtn.addEventListener('click', toggleChat);

window.openInsuranceChat = function() {
    chatContainer.classList.remove('hidden');
    chatInput.focus();
};

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-bubble', `${sender}-bubble`);
    
    const now = new Date();
    const timeStr = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');
    
    messageDiv.innerHTML = `
        <div class="bubble-content">${text}</div>
        <span class="bubble-time">${timeStr}</span>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Lógica de archivos
if (attachBtn) {
    attachBtn.addEventListener('click', () => fileInput.click());
}

if (fileInput) {
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            sendMessage(file);
            fileInput.value = ''; // Reset para permitir subir el mismo archivo
        }
    });
}

// Lógica de audio
if (micBtn) {
    micBtn.addEventListener('click', async () => {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    sendMessage(audioBlob, 'audio_message.webm');
                };

                // Activar Interfaz de Grabación
                recordingOverlay.classList.remove('hidden');
                chatInput.style.visibility = 'hidden';
                attachBtn.style.visibility = 'hidden';
                startTimer();

                mediaRecorder.start();
                isRecording = true;
                micBtn.classList.add('recording');
            } catch (err) {
                console.error("Error al acceder al micrófono:", err);
                addMessage("No pude acceder al micrófono. Por favor, revisa los permisos.", 'assistant');
            }
        } else {
            mediaRecorder.stop();
            isRecording = false;
            micBtn.classList.remove('recording');
            
            // Desactivar Interfaz de Grabación
            recordingOverlay.classList.add('hidden');
            chatInput.style.visibility = 'visible';
            attachBtn.style.visibility = 'visible';
            stopTimer();

            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    });
}

function startTimer() {
    recordingSeconds = 0;
    recordingTimer.textContent = "00:00";
    recordingInterval = setInterval(() => {
        recordingSeconds++;
        const mins = String(Math.floor(recordingSeconds / 60)).padStart(2, '0');
        const secs = String(recordingSeconds % 60).padStart(2, '0');
        recordingTimer.textContent = `${mins}:${secs}`;
    }, 1000);
}

function stopTimer() {
    clearInterval(recordingInterval);
}

async function sendMessage(file = null, fileName = null) {
    const text = chatInput.value.trim();
    if (!text && !file) return;

    chatInput.value = '';
    
    if (file) {
        if (file.type.startsWith('audio/') || (fileName && fileName.endsWith('.webm'))) {
            addMessage("🎤 Mensaje de voz enviado", 'user');
        } else {
            addMessage(`📎 Archivo enviado: ${file.name || fileName}`, 'user');
        }
    } else {
        addMessage(text, 'user');
    }

    const typingDiv = document.createElement('div');
    typingDiv.classList.add('chat-bubble', 'assistant-bubble', 'typing');
    typingDiv.innerHTML = `<div class="bubble-content">Sira está procesando...</div>`;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const formData = new FormData();
        formData.append('platform', 'web_premium');
        formData.append('timestamp', new Date().toISOString());
        
        if (file) {
            formData.append('file', file, fileName || file.name);
            if (text) formData.append('message', text);
        } else {
            formData.append('message', text);
        }

        const response = await fetch(N8N_CHAT_WEBHOOK, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        chatMessages.removeChild(typingDiv);
        
        if (data.output) {
            addMessage(data.output, 'assistant');
        } else {
            addMessage("Recibí tu archivo, permíteme revisarlo un momento.", 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        if (chatMessages.contains(typingDiv)) chatMessages.removeChild(typingDiv);
        addMessage("Vaya, parece que tengo un problema de conexión al procesar el archivo.", 'assistant');
    }
}

if (sendBtn) sendBtn.addEventListener('click', () => sendMessage());
if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}
