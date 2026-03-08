const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const messageEl = document.getElementById('message');

const API_URL = 'https://web-production-2584d.up.railway.app/api/portal/login-password'; 

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dni = document.getElementById('dni').value.trim();
    const password = document.getElementById('password').value.trim();
    
    messageEl.classList.add('hidden');
    messageEl.classList.remove('error');
    loginBtn.classList.add('loading');
    loginBtn.disabled = true;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dni, password })
        });
        
        const data = await response.json();

        if (response.ok && data.valid) {
            messageEl.textContent = `¡Hola ${data.cliente.nombres}! Accediendo a tu portal...`;
            messageEl.classList.remove('hidden');
            messageEl.style.color = "#10b981";
            
            localStorage.setItem('saasUserDNI', dni);

            setTimeout(() => {
                window.location.href = 'portal.html';
            }, 1500);
        } else {
            throw new Error(data.message || 'Credenciales inválidas');
        }

    } catch (error) {
        messageEl.textContent = error.message;
        messageEl.classList.remove('hidden');
        messageEl.classList.add('error');
    } finally {
        loginBtn.classList.remove('loading');
        loginBtn.disabled = false;
    }
});
