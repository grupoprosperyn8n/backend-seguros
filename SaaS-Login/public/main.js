const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const messageEl = document.getElementById('message');

// URL del Webhook de Login de n8n
const N8N_LOGIN_WEBHOOK_URL = 'https://primary-production-0abcf.up.railway.app/webhook/login-v2'; 

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Reset message
    messageEl.classList.add('hidden');
    messageEl.classList.remove('error');
    
    // Loading state
    loginBtn.classList.add('loading');
    loginBtn.disabled = true;

    try {
        const response = await fetch(N8N_LOGIN_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            messageEl.textContent = "Acceso concedido. Redirigiendo...";
            messageEl.classList.remove('hidden');
            messageEl.style.color = "#10b981";
            
            // Save email for the portal to use to fetch user details
            localStorage.setItem('saasUserEmail', email);

            // Redirect to the portal
            setTimeout(() => {
                window.location.href = 'welcome.html';
            }, 1000);
        } else {
            throw new Error(data.error || 'Credenciales inválidas');
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
