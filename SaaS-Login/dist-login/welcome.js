const N8N_PORTAL_WEBHOOK_URL = 'https://primary-production-0abcf.up.railway.app/webhook/portal-content-v2';

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Check Authentication
    const userEmail = localStorage.getItem('saasUserEmail');
    
    if (!userEmail) {
        // No session found, redirect to login
        window.location.href = 'index.html';
        return;
    }

    // Show initial loading state
    document.getElementById('user-name').textContent = 'Cargando...';
    document.getElementById('user-role').textContent = '...';

    try {
        // 2. Fetch User Data from n8n
        const response = await fetch(N8N_PORTAL_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail })
        });

        const userData = await response.json();

        if (!response.ok) {
            throw new Error(userData.error || 'Error al cargar perfil');
        }

        // 3. Populate User Info
        // Airtable fields: Rango, Estado, URL_Redireccion
        // n8n might return them as lowercase or exact match depending on the node settings.
        // We will try to be flexible.
        
        const role = userData.role || userData.Rango || userData.rango || 'Visitante';
        const name = userData.name || userEmail.split('@')[0]; // Simple name extraction
        const destinationUrl = userData.destinationUrl || userData.URL_Redireccion || userData.url_redireccion;
        const status = userData.status || userData.Estado || userData.estado || 'Pendiente';

        // Update UI
        document.getElementById('user-name').textContent = name;
        const roleBadge = document.getElementById('user-role');
        roleBadge.textContent = role;
        roleBadge.className = 'role-badge'; // reset
        roleBadge.classList.add(`role-${role.toLowerCase()}`);

        const quoteText = document.getElementById('quote-text');
        const heroSection = document.getElementById('hero-section');

        // Theme defaults
        let quote = "Bienvenido a tu espacio de trabajo.";
        let imageUrl = "";

        if (userData.theme) {
            quote = userData.theme.quote || quote;
            imageUrl = userData.theme.imageUrl || imageUrl;
        }

        quoteText.textContent = `"${quote}"`;
        if (imageUrl) {
            heroSection.style.backgroundImage = `url('${imageUrl}')`;
        }

        // 4. Handle Action Button
        const btnContainer = document.getElementById('access-btn-container');
        btnContainer.innerHTML = ''; // Clear loading

        if (status.toLowerCase() === 'activo' && destinationUrl) {
            const btn = document.createElement('a');
            btn.href = destinationUrl;
            btn.className = 'primary-action-btn';
            btn.target = '_blank';
            
            btn.innerHTML = `
                <span>Acceder a la Plataforma</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            `;
            btnContainer.appendChild(btn);
        } else if (status.toLowerCase() === 'pendiente') {
            btnContainer.innerHTML = `
                <div class="status-message pending">
                    <p><strong>Cuenta Pendiente de Aprobación</strong></p>
                    <p>Tu administrador está revisando tu solicitud. Por favor vuelve más tarde.</p>
                </div>
            `;
        } else {
             btnContainer.innerHTML = `
                <div class="status-message error">
                    <p><strong>Acceso Restringido</strong></p>
                    <p>Tu cuenta no está activa o no tienes una URL asignada.</p>
                </div>
            `;
        }

    } catch (error) {
        console.error("Portal Error:", error);
        document.getElementById('user-name').textContent = 'Error';
        document.getElementById('quote-text').textContent = "No se pudieron cargar tus datos.";
        
        const btnContainer = document.getElementById('access-btn-container');
        btnContainer.innerHTML = `
            <div class="status-message error">
                <p>Error de conexión: ${error.message}</p>
                <button onclick="window.location.reload()" class="retry-btn">Reintentar</button>
            </div>
        `;
    }

    // 5. Logout Logic
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('saasUserEmail');
        window.location.href = 'index.html';
    });
});
