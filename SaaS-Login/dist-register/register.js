const registerForm = document.getElementById('registerForm');
const registerBtn = document.getElementById('registerBtn');
const messageEl = document.getElementById('message');

// URL del Webhook de Registro de n8n (Se actualizará en el siguiente paso)
// Placeholder for now
const N8N_REGISTER_WEBHOOK_URL = 'https://primary-production-0abcf.up.railway.app/webhook/register'; 

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const apellido = document.getElementById('apellido').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Reset message
    messageEl.classList.add('hidden');
    messageEl.classList.remove('error');
    messageEl.style.color = ""; // Reset success color

    if (password !== confirmPassword) {
        messageEl.textContent = "Las contraseñas no coinciden.";
        messageEl.classList.remove('hidden');
        messageEl.classList.add('error');
        return;
    }
    
    // Loading state
    registerBtn.classList.add('loading');
    registerBtn.disabled = true;

    try {
        const response = await fetch(N8N_REGISTER_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, apellido, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            messageEl.textContent = "Cuenta creada con éxito. Pendiente de activación.";
            messageEl.classList.remove('hidden');
            messageEl.style.color = "#10b981"; // Success green
            
            // Redirect to login after a delay
            setTimeout(() => {
                window.location.href = 'https://login-agentico-1770227340.surge.sh';
            }, 3000);
        } else {
            throw new Error(data.message || data.error || 'Error al crear la cuenta');
        }

    } catch (error) {
        messageEl.textContent = error.message;
        messageEl.classList.remove('hidden');
        messageEl.classList.add('error');
    } finally {
        registerBtn.classList.remove('loading');
        registerBtn.disabled = false;
    }
});
