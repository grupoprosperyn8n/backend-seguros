const registerForm = document.getElementById('registerForm');
const registerBtn = document.getElementById('registerBtn');
const messageEl = document.getElementById('message');

const API_URL = 'https://web-production-2584d.up.railway.app/api/portal/register'; 

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dni = document.getElementById('dni').value.trim();
    const patente = document.getElementById('patente').value.trim();
    const password = document.getElementById('password').value.trim();
    
    messageEl.classList.add('hidden');
    messageEl.classList.remove('error');
    registerBtn.classList.add('loading');
    registerBtn.disabled = true;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dni, patente, password })
        });
        
        const data = await response.json();

        if (response.ok && data.valid) {
            messageEl.textContent = "¡Contraseña creada con éxito! Redirigiendo al Login...";
            messageEl.classList.remove('hidden');
            messageEl.style.color = "#10b981";
            
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else {
            throw new Error(data.message || 'No se pudo crear la contraseña');
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
