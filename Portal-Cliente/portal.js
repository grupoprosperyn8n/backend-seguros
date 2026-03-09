document.addEventListener('DOMContentLoaded', async () => {
    // 1. Verificar sesión
    const userDNI = localStorage.getItem('saasUserDNI');
    if (!userDNI) {
        window.location.href = 'index.html';
        return;
    }

    // 2. Constants & DOM
    const BACKEND_API = 'https://web-production-2584d.up.railway.app/api/portal/user-data';
    
    const ui = {
        nameDisplay: document.getElementById('user-display-name'),
        logoutBtn: document.getElementById('logoutBtn'),
        tabs: document.querySelectorAll('.tab-btn'),
        panes: document.querySelectorAll('.tab-pane'),
        loading: document.getElementById('loading-indicator'),
        contentArea: document.getElementById('content-area')
    };

    // 3. Navegación de tabs
    ui.tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            ui.tabs.forEach(t => t.classList.remove('active'));
            ui.panes.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            const pane = document.getElementById(`tab-${btn.dataset.target}`);
            if (pane) pane.classList.add('active');
        });
    });

    // 4. Logout
    ui.logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('saasUserDNI');
        window.location.href = 'index.html';
    });

    // 5. Fetch Data
    try {
        ui.nameDisplay.textContent = 'Cargando...';
        const res = await fetch(`${BACKEND_API}?dni=${encodeURIComponent(userDNI)}`);
        const result = await res.json();
        
        if (!res.ok || !result.valid) {
            throw new Error(result.message || 'Error cargando datos');
        }

        const data = result.data;
        
        if (data.perfil && data.perfil.nombres) {
            ui.nameDisplay.textContent = `${data.perfil.nombres} ${data.perfil.apellido || ''}`.trim();
        } else {
            ui.nameDisplay.textContent = 'Mi Cuenta';
        }

        // Renderizar todas las secciones
        renderPerfil(data.perfil);
        renderPolizas(data.polizas);
        renderGestiones(data.gestiones);
        renderAccidentes(data.accidentes);
        renderRoboOc(data.robo_oc);
        renderRoboIncendio(data.robo_incendio);

        ui.loading.classList.add('hidden');
        ui.contentArea.classList.remove('hidden');

    } catch (err) {
        console.error("Portal Error:", err);
        ui.loading.innerHTML = `
            <div class="status-message error">
                <p>${err.message}</p>
                <button onclick="window.location.reload()" class="action-btn">Reintentar</button>
            </div>`;
    }

    // ========================
    // Utilidades
    // ========================

    function formatDate(str) {
        if (!str) return '-';
        try {
            const d = new Date(str);
            return d.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' });
        } catch { return str; }
    }

    function formatDateTime(str) {
        if (!str) return '-';
        try {
            const d = new Date(str);
            return d.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' }) +
                   ' ' + d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
        } catch { return str; }
    }

    function strVal(v) {
        if (!v) return '';
        // Limpieza de strings técnicos detectados
        const clean = (val) => {
            const s = String(val);
            if (s === 'emptyDependency') return '';
            return s;
        };
        if (Array.isArray(v)) return v.map(clean).filter(Boolean).join(', ');
        return clean(v);
    }

    // Clase CSS de badge según texto — mapeo exacto al sistema del backend
    function badgeClass(text) {
        if (!text) return 'badge-gray';
        const s = strVal(text).toUpperCase().trim();
        // Verde
        if (/\bALTA$|\bALTAS\b|ACTIV|NO CULPABLE|POLIZA ACTIVADA|INCENDIO PARCIAL|ALTA PRODUCTO|EST[AÁ] CUBIERTO|RESUELVE/.test(s)) return 'badge-green';
        // Rojo
        if (/ANULD|ANULAC|BAJA|CON LESIONES|CULPABLE|ROBO TOTAL/.test(s)) return 'badge-red';
        // Amarillo
        if (/TRAMITE|PROCESO|ASESORADO|PENDIENTE|VER TENGO DUDAS|NO APLICA|ESPERA|ENDOSO|COBRANZA/.test(s)) return 'badge-yellow';
        // Naranja
        if (/VENCE|VTO|30 DI|7 DI|DERIVADO|ABOGADO|IMPRESIÓN|RETIRO|ENVIADA/.test(s)) return 'badge-orange';
        // Morado
        if (/INCENDIO TOTAL|SINIESTRO/.test(s)) return 'badge-purple';
        // Azul/celeste
        if (/SIN LESIONES|CONSULTA|COTIZACI|DENUNCIA/.test(s)) return 'badge-blue';
        // Gris
        if (/NUEVA|SIN VIG|SIN P[OÓ]LIZA|OTROS|NO REQUIERE|CRISTAL|PARABRISAS/.test(s)) return 'badge-gray';
        return 'badge-blue';
    }

    function makeBadge(text, cls) {
        if (!text) return '';
        const c = cls || badgeClass(text);
        return `<span class="badge ${c}">${strVal(text)}</span>`;
    }

    // Limpia el texto de análisis IA removiendo palabras técnicas internas
    function cleanIAText(raw) {
        if (!raw) return null;
        if (typeof raw === 'object') {
            const val = raw.value || raw.text || raw.content || Object.values(raw).find(v => typeof v === 'string' && v.length > 10);
            raw = val ? String(val) : JSON.stringify(raw);
        }
        if (typeof raw === 'string' && raw.trim().startsWith('{')) {
            try {
                const parsed = JSON.parse(raw);
                if (parsed.value) raw = String(parsed.value);
                else if (parsed.text) raw = String(parsed.text);
            } catch { /* usar como está */ }
        }
        // Eliminar palabras técnicas: state, generate, valve, value
        raw = raw.replace(/\b(state|generate|valve|value)\b/gi, '').replace(/\\n/g, '\n').replace(/\\t/g, ' ').trim();
        return raw.length > 2 ? raw : null;
    }

    function emptyState(msg) {
        const d = document.createElement('div');
        d.className = 'empty-state';
        d.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="2"/></svg>
            <p>${msg}</p>`;
        return d;
    }

    // ========================
    // PERFIL
    // Imagen ref:
    //   - 2 cards lado a lado: "Datos Personales" (NOMBRE/DNI/FECHA DE ALTA) | "Contacto" (EMAIL/TELEFONO/DIRECCIÓN)
    //   - Strip inferior: Total / Activas / Anuladas / En Trámite / Sin Vigencia / Sin Póliza / Vence 30 días / Vence 7 días
    // ========================
    function renderPerfil(perfil) {
        const pane = document.getElementById('tab-perfil');
        pane.innerHTML = '';
        const p = perfil || {};

        const total   = p.total_polizas       || 0;
        const activas = p.polizas_activas      || 0;
        const anulad  = p.polizas_anuladas     || 0;
        const tramite = p.polizas_tramite      || 0;
        const sinVig  = p.polizas_sin_vigencia || 0;
        const vence30 = p.vence_30dias         || 0;
        const vence7  = p.vence_7dias          || 0;

        const layout = document.createElement('div');
        layout.className = 'perfil-layout';

        // Strip de estadísticas — exactamente como el backend de Airtable
        const strip = document.createElement('div');
        strip.className = 'stats-strip';
        strip.innerHTML = `
            <div class="stat-badge stat-total">  <span class="stat-num">${total}</span>  <span class="stat-label">📊 Total</span></div>
            <div class="stat-badge stat-activa"> <span class="stat-num">${activas}</span> <span class="stat-label">✅ Activas</span></div>
            <div class="stat-badge stat-anulada"><span class="stat-num">${anulad}</span>  <span class="stat-label">❌ Anuladas</span></div>
            <div class="stat-badge stat-tramite"><span class="stat-num">${tramite}</span> <span class="stat-label">⏳ En Trámite</span></div>
            <div class="stat-badge stat-7dias">  <span class="stat-num">${sinVig}</span>  <span class="stat-label">🟣 Sin Vigencia</span></div>
            <div class="stat-badge stat-anulada"><span class="stat-num">0</span>          <span class="stat-label">🚫 Sin Póliza</span></div>
            <div class="stat-badge stat-30dias"> <span class="stat-num">${vence30}</span> <span class="stat-label">📆 Vence 30 días</span></div>
            <div class="stat-badge stat-semana"> <span class="stat-num">${vence7}</span>  <span class="stat-label">⚠️ Vence 7 días</span></div>
        `;
        layout.appendChild(strip);

        // Tarjeta: Datos Personales — NOMBRE, DNI, FECHA DE ALTA
        const cardLeft = document.createElement('div');
        cardLeft.className = 'data-card';
        cardLeft.innerHTML = `
            <div class="card-header"><div><p class="card-title">👤 Datos Personales</p></div></div>
            <div class="card-divider"></div>
            <div class="card-body">
                <div class="card-row"><span class="row-label">NOMBRE</span><span class="row-val">${(strVal(p.nombres) + ' ' + strVal(p.apellido)).trim() || '-'}</span></div>
                <div class="card-row"><span class="row-label">DNI</span><span class="row-val">${p.dni || '-'}</span></div>
                <div class="card-row"><span class="row-label">FECHA DE ALTA</span><span class="row-val">${formatDate(p.fecha_alta)}</span></div>
            </div>`;
        layout.appendChild(cardLeft);

        // Tarjeta: Contacto — EMAIL, TELÉFONO, DIRECCIÓN
        const cardRight = document.createElement('div');
        cardRight.className = 'data-card';
        cardRight.innerHTML = `
            <div class="card-header"><div><p class="card-title">✉️ Contacto</p></div></div>
            <div class="card-divider"></div>
            <div class="card-body">
                <div class="card-row"><span class="row-label">EMAIL</span><span class="row-val">${p.email || '-'}</span></div>
                <div class="card-row"><span class="row-label">TELÉFONO</span><span class="row-val">${p.telefono || '-'}</span></div>
                <div class="card-row"><span class="row-label">DIRECCIÓN</span><span class="row-val">${p.direccion || '-'}</span></div>
            </div>`;
        layout.appendChild(cardRight);

        pane.appendChild(layout);
    }

    // ========================
    // PÓLIZAS
    // Imagen ref:
    //   - N° póliza como título
    //   - Estado badge top-right: ALTA verde / ANULACION rojo / VENCE EN 30 DIAS naranja / VENCE EN 7 DIAS magenta
    //   - Campos inline: Vehículo | Cobertura (badge) | Vence
    //   - Borde izquierdo coloreado según estado
    // ========================
    function renderPolizas(polizas) {
        const pane = document.getElementById('tab-polizas');
        pane.innerHTML = '';
        if (!polizas || !polizas.length) { pane.appendChild(emptyState('No hay pólizas registradas.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'grid-column:1/-1;color:var(--white-70);font-size:.9rem;margin:0 0 4px;';
        hdr.textContent = `📄 ${polizas.length} póliza${polizas.length !== 1 ? 's' : ''}`;
        pane.appendChild(hdr);

        polizas.forEach(p => {
            const estado   = strVal(p['ESTADO DE LA POLIZA']) || strVal(p['ETIQUETA_POLIZA']) || 'SIN ESTADO';
            const patente  = strVal(p['PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES)']) || '-';
            const marca    = strVal(p['MARCA DEL VEHICULO']);
            const modelo   = strVal(p['MODELO DEL VEHICULO']);
            const vehiculo = [marca, modelo].filter(Boolean).join(' ') || '-';
            const cobert   = strVal(p['COBERTURA']);
            const vence    = strVal(p['FECHA VENCIMIENTO DE LA POLIZA']);
            const nPoliza  = strVal(p['N° DE POLIZA']) || strVal(p['ETIQUETA_POLIZA']) || 'Sin número';

            // Color borde izquierdo según estado
            let borderColor = 'var(--primary)';
            const eu = estado.toUpperCase();
            if (eu.includes('ALTA') || eu.includes('ACTIV')) borderColor = 'var(--color-activa)';
            else if (eu.includes('ANULD') || eu.includes('ANULAC')) borderColor = 'var(--color-anulada)';
            else if (eu.includes('30')) borderColor = 'var(--color-warning)';
            else if (eu.includes('7') || eu.includes('VENCE')) borderColor = '#ff2d78';

            const card = document.createElement('div');
            card.className = 'data-card';
            card.style.borderLeft = `4px solid ${borderColor}`;
            card.innerHTML = `
                <div class="card-header">
                    <div>
                        <h3 class="card-subtitle" style="font-size:1.2rem;font-weight:700;">${nPoliza}</h3>
                    </div>
                    <div class="badge-container">${makeBadge(estado)}</div>
                </div>
                <div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:8px;font-size:.78rem;color:var(--white-50);">
                    <span>Vehículo: <strong style="color:var(--white);">${vehiculo}</strong></span>
                    <span>Cobertura: ${cobert ? makeBadge(cobert, 'badge-orange') : '-'}</span>
                    <span>Vence: <strong style="color:var(--white);">${vence || '-'}</strong></span>
                </div>`;
            pane.appendChild(card);
        });
    }

    // ========================
    // GESTIONES
    // Imagen ref:
    //   - ID badge morado (ID_UNICO_GESTION) + estado badge top-right (NUEVA gris)
    //   - Tipo badge (ALTAS verde / ANULACIÓN rojo / CONSULTA azul / POLIZA ACTIVADA verde / DENUNCIA ROBO verde-azul / ...)
    //   - Motivo badge (COTIZACIÓN / ENDOSO naranja / ANULACIÓN rojo / NO APLICA amarillo / SINIESTRO oscuro / ...)
    //   - Campos: Fecha, Atendido por
    // ========================
    function renderGestiones(gestiones) {
        const pane = document.getElementById('tab-gestiones');
        pane.innerHTML = '';
        if (!gestiones || !gestiones.length) { pane.appendChild(emptyState('No hay gestiones registradas.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'grid-column:1/-1;color:var(--white-70);font-size:.9rem;margin:0 0 4px;';
        hdr.textContent = `📁 ${gestiones.length} gestión${gestiones.length !== 1 ? 'es' : ''}`;
        pane.appendChild(hdr);

        gestiones.forEach(g => {
            const idGestion = strVal(g['ID_UNICO_GESTION']);
            const tipo      = strVal(g['TIPO DE ATENCIÓN']);
            const motivo    = strVal(g['MOTIVOS DE LA CONSULTA']);
            const atendido  = strVal(g['ATENDIDO X']);
            const fecha     = strVal(g['FECHA DE CREACION']);
            // El estado de la gestión viene como "NUEVA", "PROCESADA", etc.
            const estadoGestion = strVal(g['ES CLIENTE']) || '';

            const card = document.createElement('div');
            card.className = 'data-card';
            card.innerHTML = `
                <div class="card-header">
                    <div>${idGestion ? `<span class="badge badge-purple" style="font-size:.7rem;margin-bottom:6px;display:inline-flex;gap:4px;">🪪 ${idGestion}</span>` : ''}</div>
                    ${estadoGestion ? `<div class="badge-container">${makeBadge(estadoGestion, 'badge-gray')}</div>` : ''}
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:6px;margin:6px 0;">
                    ${tipo   ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Tipo:</span>${makeBadge(tipo)}</div>`   : ''}
                    ${motivo ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Motivo:</span>${makeBadge(motivo)}</div>` : ''}
                </div>
                <div class="card-divider"></div>
                <div class="card-body">
                    <div class="card-row"><span class="row-label">Fecha</span><span class="row-val">${formatDateTime(fecha)}</span></div>
                    <div class="card-row"><span class="row-label">Atendido por</span><span class="row-val">${atendido || 'AGENTE IA'}</span></div>
                </div>`;
            pane.appendChild(card);
        });
    }

    // ========================
    // ACCIDENTES
    // Imagen ref:
    //   - Header pequeño: "Siniestro"
    //   - Tipo badge (SIN LESIONES azul claro / CON LESIONES rojo) + Culpa badge (NO CULPABLE verde / CULPABLE rojo / VER TENGO DUDAS naranja)
    //   - Sección IA contraíble individual por tarjeta
    //   - Tratam badge + Resoluc badge
    //   - Campos inline: Patente | Vehículo | Cobertura | Fecha | Atendido por | Póliza
    // ========================
    function renderAccidentes(accidentes) {
        const pane = document.getElementById('tab-accidentes');
        pane.innerHTML = '';
        if (!accidentes || !accidentes.length) { pane.appendChild(emptyState('No hay denuncias de accidente.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'grid-column:1/-1;color:var(--white-70);font-size:.9rem;margin:0 0 4px;';
        hdr.textContent = `🚗 ${accidentes.length} denuncia${accidentes.length !== 1 ? 's' : ''} de accidente`;
        pane.appendChild(hdr);

        let accIdx = 0;
        accidentes.forEach(a => {
            const tipo      = strVal(a['ATASCAMIENTO - CHOQUE -DAÑO - OTRO']) || strVal(a['TIPO DE ATENCIÓN']) || strVal(a['CLASIFICACIÓN']);
            const culpa     = strVal(a['CULPABILIDAD']);
            const tratam    = strVal(a['TRATAMIENTO']) || strVal(a['Tratamiento']);
            const resoluc   = strVal(a['TIPO DE RESOLUCION']) || strVal(a['Elegir Resolucion ']);
            const patente   = strVal(a['1) PATENTE DE SU VEHICULO']);
            const marca     = strVal(a['MARCA DEL VEHICULO Compilación (de N° POLIZA)']) || strVal(a['MARCA DEL VEHICULO']);
            const modelo    = strVal(a['MODELO DEL VEHICULO']) || strVal(a['MODELO DEL  VEHICULO']);
            const vehiculo  = [marca, modelo].filter(Boolean).join(' ');
            const cobertura = strVal(a['COBERTURA']);
            const fecha     = strVal(a['FECHA DE CREACION']);
            const atendido  = strVal(a['ATENDIDO X']);
            const poliza    = strVal(a['N° DE POLIZA']);
            const iaText    = cleanIAText(a['CULPABILIDAD IA']);

            // Colores específicos
            const tipoCls  = tipo && tipo.toUpperCase().includes('CON LESIONES') ? 'badge-red' : 'badge-blue';
            const culpaCls = !culpa ? '' :
                culpa.toUpperCase().includes('NO CULP') ? 'badge-green' :
                culpa.toUpperCase().includes('TENGO')   ? 'badge-yellow' : 'badge-red';

            const uid = `ia-acc-${accIdx++}`;
            const card = document.createElement('div');
            card.className = 'data-card';
            card.style.borderTop = '3px solid var(--color-warning)';
            card.innerHTML = `
                <p style="font-size:.72rem;color:var(--white-50);font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 6px;">Siniestro</p>
                <div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:8px;">
                    <div style="display:flex;flex-direction:column;gap:2px;">
                        <span style="font-size:.68rem;color:var(--white-50);">Tipo:</span>
                        ${tipo ? makeBadge(tipo, tipoCls) : '-'}
                    </div>
                    ${culpa ? `<div style="display:flex;flex-direction:column;gap:2px;">
                        <span style="font-size:.68rem;color:var(--white-50);">Culpa:</span>
                        ${makeBadge(culpa, culpaCls)}
                    </div>` : ''}
                </div>
                ${iaText ? `
                <details class="analyzer-details" id="${uid}">
                    <summary class="analyzer-label">🤖 IA: <span class="analyzer-toggle-icon">▼</span></summary>
                    <div class="analyzer-block">${iaText.replace(/\n/g, '<br>')}</div>
                </details>` : ''}
                ${(tratam || resoluc) ? `
                <div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0;">
                    ${tratam  ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Tratam:</span>${makeBadge(tratam, 'badge-yellow')}</div>` : ''}
                    ${resoluc ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Resoluc:</span>${makeBadge(resoluc, 'badge-green')}</div>`  : ''}
                </div>` : ''}
                <div class="card-divider"></div>
                <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:8px;font-size:.78rem;color:var(--white-50);">
                    ${patente   ? `<span>Patente: <strong style="color:var(--white)">${patente}</strong></span>`    : ''}
                    ${vehiculo  ? `<span>Vehículo: <strong style="color:var(--white)">${vehiculo}</strong></span>`  : ''}
                    ${cobertura ? `<span>Cobertura: <strong style="color:var(--white)">${cobertura}</strong></span>` : ''}
                    ${fecha     ? `<span>Fecha: <strong style="color:var(--white)">${formatDateTime(fecha)}</strong></span>` : ''}
                    ${atendido  ? `<span>Atendido por: <strong style="color:var(--white)">${atendido}</strong></span>` : ''}
                    ${poliza    ? `<span>Póliza: <strong style="color:var(--white)">${strVal(poliza)}</strong></span>` : ''}
                </div>`;
            pane.appendChild(card);
        });
    }

    // ========================
    // ROBO OC
    // Imagen ref:
    //   - Header pequeño: "Siniestro" + N° de siniestro
    //   - Daño badges (CLASIFICACIÓN DEL DAÑO): PARABRISAS gris oscuro / ROBO 1 RUEDA gris oscuro / CRISTAL azul
    //   - Alcance badge (ALCANCE DE COBERTURA): ESTÁ CUBIERTO azul
    //   - Tratam badge (TIPO DE ATENCIÓN): ESTA SIENDO ASESORADO-EN PROCESO amarillo
    //   - Orden badge (ORDEN PEDIDA A CIA): SI verde
    //   - Verif badge (VERIFICACION DE ORDEN): ENVIADA AL ASEGURADO naranja
    //   - Campos inline: Patente | Vehículo | Cobertura | Fecha | Atendido por | Póliza
    // ========================
    function renderRoboOc(robos) {
        const pane = document.getElementById('tab-robo_oc');
        pane.innerHTML = '';
        if (!robos || !robos.length) { pane.appendChild(emptyState('No hay denuncias de Robo OC.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'grid-column:1/-1;color:var(--white-70);font-size:.9rem;margin:0 0 4px;';
        hdr.textContent = `🛡️ ${robos.length} denuncia${robos.length !== 1 ? 's' : ''} de robo OC`;
        pane.appendChild(hdr);

        robos.forEach(r => {
            const nSiniestro = strVal(r['NUMERO DE SINIESTRO ']) || strVal(r['NUMERO']);
            const danyoRaw   = r['CLASIFICACIÓN DEL DAÑO'];
            const alcance    = strVal(r['ALCANCE DE COBERTURA']);
            const tratam     = strVal(r['TIPO DE ATENCIÓN']);
            const orden      = strVal(r['ORDEN PEDIDA A CIA']);
            const verif      = strVal(r['VERIFICACION DE ORDEN']);
            // Patente: campo compilado largo del join con POLIZAS → CLIENTES
            const patente    = strVal(r['PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES) Compilación (de N° POLIZA)'])
                            || strVal(r['PATENTE']);
            const marca      = strVal(r['MARCA DEL VEHICULO Compilación (de N° POLIZA)']);
            const modelo     = strVal(r['MODELO DEL VEHICULO']);
            const vehiculo   = [marca, modelo].filter(Boolean).join(' ');
            const cobertura  = strVal(r['COBERTURA']);
            const fecha      = strVal(r['FECHA DE CREACION']);
            const atendido   = strVal(r['ATENDIDO X']);
            const poliza     = strVal(r['N° DE POLIZA']);

            const danyos = Array.isArray(danyoRaw) ? danyoRaw : (danyoRaw ? [danyoRaw] : []);

            const card = document.createElement('div');
            card.className = 'data-card';
            card.style.borderTop = '3px solid var(--color-warning)';
            card.innerHTML = `
                <p style="font-size:.72rem;color:var(--white-50);font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 2px;">Siniestro</p>
                ${nSiniestro ? `<strong style="font-size:1.1rem;color:var(--white);display:block;margin-bottom:6px;">${nSiniestro}</strong>` : ''}
                <div style="display:flex;flex-wrap:wrap;gap:10px;margin:6px 0;">
                    ${danyos.length ? `<div style="display:flex;flex-direction:column;gap:2px;">
                        <span style="font-size:.68rem;color:var(--white-50);">Daño:</span>
                        <div style="display:flex;gap:4px;flex-wrap:wrap;">${danyos.map(d => makeBadge(d, 'badge-gray')).join('')}</div>
                    </div>` : ''}
                    ${alcance ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Alcance:</span>${makeBadge(alcance, 'badge-blue')}</div>` : ''}
                    ${tratam  ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Tratam:</span>${makeBadge(tratam, 'badge-yellow')}</div>` : ''}
                    ${orden   ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Orden:</span>${makeBadge(orden, 'badge-green')}</div>` : ''}
                    ${verif   ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Verif:</span>${makeBadge(verif, 'badge-orange')}</div>` : ''}
                </div>
                <div class="card-divider"></div>
                <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:8px;font-size:.78rem;color:var(--white-50);">
                    ${patente   ? `<span>Patente: <strong style="color:var(--white)">${patente}</strong></span>`    : ''}
                    ${vehiculo  ? `<span>Vehículo: <strong style="color:var(--white)">${vehiculo}</strong></span>`  : ''}
                    ${cobertura ? `<span>Cobertura: <strong style="color:var(--white)">${cobertura}</strong></span>` : ''}
                    ${fecha     ? `<span>Fecha: <strong style="color:var(--white)">${formatDateTime(fecha)}</strong></span>` : ''}
                    ${atendido  ? `<span>Atendido por: <strong style="color:var(--white)">${atendido}</strong></span>` : ''}
                    ${poliza    ? `<span>Póliza: <strong style="color:var(--white)">${strVal(poliza)}</strong></span>` : ''}
                </div>`;
            pane.appendChild(card);
        });
    }

    // ========================
    // ROBO/INCENDIO
    // Imagen ref:
    //   - ID badge morado (ID_UNICO_GESTION) + estado badge top-right (ANULADA rojo)
    //   - Tipo badge: ROBO TOTAL rojo / INCENDIO TOTAL gris oscuro (morado) / INCENDIO PARCIAL verde
    //   - Alcance badge (ALCANCE DE COBERTURA): ESTA CUBIERTO azul
    //   - Tratam badge: ESTA SIENDO ASESORADO verde / YA FUE CONTACTADO amarillo
    //   - Resoluc badge: DERIVADO AL GESTOR naranja / RESUELVE CON ABOGADO NUESTRO naranja
    //   - Campos: Fecha, Atendido por
    // ========================
    function renderRoboIncendio(robos) {
        const pane = document.getElementById('tab-robo_incendio');
        pane.innerHTML = '';
        if (!robos || !robos.length) { pane.appendChild(emptyState('No hay denuncias de Robo/Incendio.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'grid-column:1/-1;color:var(--white-70);font-size:.9rem;margin:0 0 4px;';
        hdr.textContent = `🔥 ${robos.length} denuncia${robos.length !== 1 ? 's' : ''} de robo/incendio`;
        pane.appendChild(hdr);

        robos.forEach(r => {
            const idReg    = strVal(r['ID_UNICO_GESTION']);
            const tipo     = strVal(r['TIPO DE ROBO / INCENDIO ']) || strVal(r['CLASIFICACIÓN DEL SINIESTRO']) || strVal(r['TIPO DE ATENCIÓN']);
            const alcance  = strVal(r['ALCANCE DE COBERTURA']);
            const tratam   = strVal(r['Tratamiento']) || strVal(r['TIPO DE ATENCIÓN']) || strVal(r['TRATAMIENTO']);
            const resoluc  = strVal(r['TIPO DE RESOLUCION']) || strVal(r['Elegir Resolucion ']);
            const fecha    = strVal(r['FECHA DE CREACION']);
            const atendido = strVal(r['ATENDIDO X']);
            const estado   = strVal(r['ES CLIENTE']);

            // Color tipo exacto
            let tipoCls = 'badge-gray';
            if (tipo) {
                const tu = tipo.toUpperCase();
                if (tu.includes('ROBO TOTAL')) tipoCls = 'badge-red';
                else if (tu.includes('INCENDIO TOTAL')) tipoCls = 'badge-purple';
                else if (tu.includes('INCENDIO PARCIAL')) tipoCls = 'badge-green';
            }

            const card = document.createElement('div');
            card.className = 'data-card';
            card.style.borderTop = '3px solid var(--color-employee)';
            card.innerHTML = `
                <div class="card-header">
                    <div>${idReg ? `<span class="badge badge-purple" style="font-size:.7rem;display:inline-flex;gap:4px;">🪪 ${idReg}</span>` : ''}</div>
                    ${estado ? `<div class="badge-container">${makeBadge(estado)}</div>` : ''}
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:10px;margin:8px 0;">
                    ${tipo    ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Tipo:</span>${makeBadge(tipo, tipoCls)}</div>` : ''}
                    ${alcance ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Alcance:</span>${makeBadge(alcance, 'badge-blue')}</div>` : ''}
                    ${tratam  ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Tratam:</span>${makeBadge(tratam, 'badge-green')}</div>` : ''}
                    ${resoluc ? `<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:.68rem;color:var(--white-50);">Resoluc:</span>${makeBadge(resoluc, 'badge-orange')}</div>` : ''}
                </div>
                <div class="card-divider"></div>
                <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:8px;font-size:.78rem;color:var(--white-50);">
                    ${fecha    ? `<span>Fecha: <strong style="color:var(--white)">${formatDateTime(fecha)}</strong></span>` : ''}
                    ${atendido ? `<span>Atendido por: <strong style="color:var(--white)">${atendido}</strong></span>` : ''}
                </div>`;
            pane.appendChild(card);
        });
    }
});
