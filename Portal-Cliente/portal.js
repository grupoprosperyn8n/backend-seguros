document.addEventListener('DOMContentLoaded', async () => {
    // 1. Verificar sesión
    const userDNI = localStorage.getItem('saasUserDNI');
    if (!userDNI) {
        window.location.href = 'index.html';
        return;
    }

    // Entorno Local de Alta Disponibilidad
    const BACKEND_API = 'https://web-production-2584d.up.railway.app/api/portal/user-data';
    
    const ui = {
        nameDisplay: document.getElementById('user-display-name'),
        logoutBtn: document.getElementById('logoutBtn'),
        tabs: document.querySelectorAll('.tab-btn'),
        panes: document.querySelectorAll('.tab-pane'),
        loading: document.getElementById('loading-indicator'),
        contentArea: document.getElementById('content-area'),
        // Nodos del Modal Global
        modal: {
            overlay: document.getElementById('portal-detail-modal'),
            closeBtn: document.getElementById('pdm-close'),
            title: document.getElementById('pdm-title'),
            body: document.getElementById('pdm-body')
        }
    };

    // Modal Logic
    function openModal(titleHTML, bodyHTML) {
        ui.modal.title.innerHTML = titleHTML;
        ui.modal.body.innerHTML = bodyHTML;
        ui.modal.overlay.classList.add('active');
    }
    function closeModal() {
        ui.modal.overlay.classList.remove('active');
        // Clear timeout/listeners if needed
        setTimeout(() => ui.modal.body.innerHTML = '', 300);
    }
    
    ui.modal.closeBtn.addEventListener('click', closeModal);
    ui.modal.overlay.addEventListener('click', (e) => {
        if (e.target === ui.modal.overlay) closeModal();
    });
    // Close on ESC mapping
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

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
        renderGestiones(data.gestiones, data.polizas);
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

    function resolvedAtendido(rec) {
        return (
            strVal(rec?.['ATENDIDO X']) ||
            strVal(rec?.['ATENDIDO X (from CLIENTES)']) ||
            strVal(rec?.['Atendido por']) ||
            strVal(rec?.['ATENDIDO POR']) ||
            ''
        );
    }

    function resolvedOficina(rec) {
        return (
            strVal(rec?.['OFICINAS']) ||
            strVal(rec?.['OFICINA']) ||
            strVal(rec?.['Oficina']) ||
            strVal(rec?.['OFICINAS (from CLIENTES)']) ||
            ''
        );
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
            
            // Extract Documentacion array from Airtable (list of attachments)
            const docArray = p['DOCUMENTACION'];
            let docButtonHTML = '';
            if (Array.isArray(docArray) && docArray.length > 0) {
                // Airtable objects hold URL in the .url property
                const docUrl = docArray[0].url;
                if (docUrl) {
                    docButtonHTML = `
                    <div style="margin-top: 12px; border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 12px;">
                        <a href="${docUrl}" target="_blank" class="btn-download-doc" title="Descargar PDF">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            Planilla de Póliza
                        </a>
                    </div>`;
                }
            }

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
                </div>
                ${docButtonHTML}
            `;
            pane.appendChild(card);
        });
    }

    // ========================
    // GESTIONES - LINEAL LIST
    // ========================
    function renderGestiones(gestiones, allPolizas = []) {
        const pane = document.getElementById('tab-gestiones');
        pane.innerHTML = '';
        pane.classList.add('list-mode');
        if (!gestiones || !gestiones.length) { pane.appendChild(emptyState('No hay gestiones registradas.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'color:var(--white-70);font-size:.9rem;margin:0 0 10px;';
        hdr.textContent = `📁 ${gestiones.length} gestión${gestiones.length !== 1 ? 'es' : ''}`;
        pane.appendChild(hdr);

        gestiones.forEach(g => {
            // 1. Vincular Póliza para obtener datos faltantes (Lookup/Rollup Cross-table)
            const idsPoliza = g['POLIZAS'] || [];
            const polId = Array.isArray(idsPoliza) ? idsPoliza[0] : idsPoliza;
            
            // Buscar la póliza en el set de datos ya cargado
            const polRecord = allPolizas.find(p => p.RECORD_ID === polId) || {};
            
            // Extracción de datos con fallback agresivo
            const idGestion   = strVal(g['ID_UNICO_GESTION']);
            const fechaCarga  = strVal(g['FECHA DE CREACION']);
            const motivo      = strVal(g['MOTIVOS DE LA CONSULTA']);
            const atendido    = resolvedAtendido(g) || '-';
            
            // Datos del Seguro (Buscando en Gestion y luego en Poliza)
            const nPoliza     = strVal(g['N° DE POLIZA']) || strVal(polRecord['N° DE POLIZA']) || strVal(polRecord['ETIQUETA_POLIZA']) || '-';
            
            // Fallback para Patente usando el nombre largo de Airtable si el corto falla
            const patente     = strVal(polRecord['PATENTE DEL VEHICULO']) || 
                                strVal(polRecord['PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES)']) || 
                                strVal(g['PATENTE DEL VEHICULO']) || '-';
            
            const compania    = strVal(polRecord['COMPANIA_RESOLVED']) || strVal(polRecord['NOMBRE (from COMPANIA LINK)']) || '-';
            const producto    = strVal(polRecord['PRODUCTO_RESOLVED']) || strVal(polRecord['NOMBRE PRODUCTO']) || '-';
            
            const oficina     = resolvedOficina(g) || '-';
            const detallarOtr = strVal(g['DETALLAR OTROS']) || '-';
            const formaPago   = strVal(g['FORMA DE PAGOS']) || '-';
            const vida        = strVal(g['VIDA']) || 'NO';
            const auxilio     = strVal(g['AUXILIOS']) || 'NO';
            const impPoliza   = strVal(g['IMPORTE']) ? `$${strVal(g['IMPORTE'])}` : '-';
            const impVida     = strVal(g['IMPORTE VIDA']) ? `$${strVal(g['IMPORTE VIDA'])}` : '-';
            const impAux      = strVal(g['IMPORTE AUX 24']) ? `$${strVal(g['IMPORTE AUX 24'])}` : '-';

            const row = document.createElement('div');
            row.className = 'glass-list-item';
            
            // LISTA: Fecha de Carga, Motivo, Producto, Patente (Estructura Fija)
            row.innerHTML = `
                <div class="list-item-main">
                    <p class="list-item-title" style="display:flex; align-items:center; gap:8px;">
                        ${idGestion ? `<span class="badge badge-purple" style="font-size:.65rem;">🪪 ${idGestion}</span>` : ''} 
                        <span style="color:var(--white-70); font-weight:400;">Motivo:</span> <strong>${motivo || '-'}</strong>
                    </p>
                    <div class="list-item-meta" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap:12px; margin-top:6px;">
                        <span>📅 <small style="color:var(--white-50);">Carga:</small> ${formatDate(fechaCarga)}</span>
                        <span>🚗 <small style="color:var(--white-50);">Patente:</small> ${patente}</span>
                        <span>📦 <small style="color:var(--white-50);">Producto:</small> ${producto}</span>
                    </div>
                </div>
            `;

            // MODAL: Estructura Fija con todos los campos
            row.addEventListener('click', () => {
                const title = `🪪 Gestión ${idGestion || ''}`;
                const body = `
                    <div class="modal-fixed-grid">
                        <section class="modal-fixed-section">
                            <h3 class="modal-section-title">Información de Gestión</h3>
                            <div class="modal-detail-row"><span class="modal-detail-label">ID Gestión</span><span class="modal-detail-value">${idGestion || '-'}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Fecha de Carga</span><span class="modal-detail-value">${formatDateTime(fechaCarga)}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Oficina</span><span class="modal-detail-value">${oficina}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Atendido por</span><span class="modal-detail-value" style="color:var(--primary-light);">${atendido || '-'}</span></div>
                        </section>

                        <section class="modal-fixed-section">
                            <h3 class="modal-section-title">Datos del Seguro</h3>
                            <div class="modal-detail-row"><span class="modal-detail-label">N° de Póliza</span><span class="modal-detail-value">${nPoliza}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Patente</span><span class="modal-detail-value">${patente}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Compañía</span><span class="modal-detail-value">${compania}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Tipo de Producto</span><span class="modal-detail-value">${makeBadge(producto, 'badge-blue')}</span></div>
                        </section>

                        <section class="modal-fixed-section">
                            <h3 class="modal-section-title">Consulta</h3>
                            <div class="modal-detail-row"><span class="modal-detail-label">Motivo de Consulta</span><span class="modal-detail-value">${makeBadge(motivo, 'badge-orange')}</span></div>
                            <div class="modal-detail-row"><span class="modal-detail-label">Detallar Otros</span><span class="modal-detail-value" style="font-style:italic; color:var(--white-70);">${detallarOtr}</span></div>
                        </section>

                        <section class="modal-fixed-section">
                            <h3 class="modal-section-title">Información Financiera</h3>
                            <div class="modal-detail-row"><span class="modal-detail-label">Forma de Pago</span><span class="modal-detail-value">${formaPago}</span></div>
                            <div class="modal-grid-3">
                                <div class="mini-card"><small>Importe Póliza</small><strong>${impPoliza}</strong></div>
                                <div class="mini-card"><small>Importe Vida</small><strong>${impVida}</strong></div>
                                <div class="mini-card"><small>Importe Auxilio</small><strong>${impAux}</strong></div>
                            </div>
                            <div class="modal-grid-2" style="margin-top:10px;">
                                <div class="mini-badge-row"><span>Vida</span> ${makeBadge(vida, vida.toUpperCase().includes('SI') ? 'badge-green' : 'badge-gray')}</div>
                                <div class="mini-badge-row"><span>Auxilio</span> ${makeBadge(auxilio, auxilio.toUpperCase().includes('SI') ? 'badge-green' : 'badge-gray')}</div>
                            </div>
                        </section>
                    </div>
                `;
                openModal(title, body);
            });

            pane.appendChild(row);
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
        pane.classList.add('list-mode');
        if (!accidentes || !accidentes.length) { pane.appendChild(emptyState('No hay denuncias de accidente.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'color:var(--white-70);font-size:.9rem;margin:0 0 10px;';
        hdr.textContent = `🚗 ${accidentes.length} denuncia${accidentes.length !== 1 ? 's' : ''} de accidente`;
        pane.appendChild(hdr);

        let accIdx = 0;
        accidentes.forEach(a => {
            const numSiniestro = strVal(a['NUMERO DE SINIESTRO']);
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
            const atendido  = resolvedAtendido(a);
            const poliza    = strVal(a['N° DE POLIZA']);
            const iaText    = cleanIAText(a['CULPABILIDAD IA']);

            // Colores específicos
            const tipoCls  = tipo && tipo.toUpperCase().includes('CON LESIONES') ? 'badge-red' : 'badge-blue';
            const culpaCls = !culpa ? '' :
                culpa.toUpperCase().includes('NO CULP') ? 'badge-green' :
                culpa.toUpperCase().includes('TENGO')   ? 'badge-yellow' : 'badge-red';

            const row = document.createElement('div');
            row.className = 'glass-list-item';
            
            row.innerHTML = `
                <div class="list-item-main">
                    <p class="list-item-title">
                        ${numSiniestro ? `<span class="badge badge-red" style="font-size:.65rem;">🚨 ${numSiniestro}</span>` : ''} 
                        Denuncia de Accidente
                    </p>
                    <div class="list-item-meta">
                        <span><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> ${formatDate(fecha)}</span>
                        <span>👥 ${atendido || 'Agente IA'}</span>
                    </div>
                </div>
                <div class="list-item-badges">
                    ${culpa ? makeBadge(culpa, culpaCls) : ''}
                    ${resoluc ? makeBadge(resoluc, 'badge-green') : ''}
                </div>
            `;

            row.addEventListener('click', () => {
                const title = `🚨 Accidente ${numSiniestro || ''}`;
                const body = `
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Fecha del Siniestro</span>
                        <span class="modal-detail-value">${formatDateTime(fecha)}</span>
                    </div>
                    
                    <h3 class="modal-section-title">Análisis de Caso</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Vehículo Involucrado</span>
                        <span class="modal-detail-value">${vehiculo || '-'} ${patente ? `(${patente})` : ''}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Tipo de Choque</span>
                        <span class="modal-detail-value">${tipo ? makeBadge(tipo, tipoCls) : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Culpabilidad Presunta</span>
                        <span class="modal-detail-value">${culpa ? makeBadge(culpa, culpaCls) : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Tratamiento</span>
                        <span class="modal-detail-value">${tratam ? makeBadge(tratam, 'badge-yellow') : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Resolución Final</span>
                        <span class="modal-detail-value">${resoluc ? makeBadge(resoluc, 'badge-green') : 'Pendiente'}</span>
                    </div>

                    ${iaText ? `
                    <h3 class="modal-section-title">Resumen Inteligencia Artificial</h3>
                    <div class="analyzer-block" style="margin-top:0;">${iaText.replace(/\n/g, '<br>')}</div>
                    ` : ''}
                    
                    <h3 class="modal-section-title">Seguimiento</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Asociado a Póliza</span>
                        <span class="modal-detail-value">${strVal(poliza) || '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Atendido por</span>
                        <span class="modal-detail-value" style="color:var(--primary-light);">${atendido || '-'}</span>
                    </div>
                `;
                openModal(title, body);
            });

            pane.appendChild(row);
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
        pane.classList.add('list-mode');
        if (!robos || !robos.length) { pane.appendChild(emptyState('No hay denuncias de Robo OC.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'color:var(--white-70);font-size:.9rem;margin:0 0 10px;';
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
            const atendido   = resolvedAtendido(r);
            const poliza     = strVal(r['N° DE POLIZA']);

            const danyos = Array.isArray(danyoRaw) ? danyoRaw : (danyoRaw ? [danyoRaw] : []);

            const row = document.createElement('div');
            row.className = 'glass-list-item';
            
            row.innerHTML = `
                <div class="list-item-main">
                    <p class="list-item-title">
                        ${nSiniestro ? `<span class="badge badge-blue" style="font-size:.65rem;">🔍 ${nSiniestro}</span>` : ''} 
                        Robo Parcial (OC)
                    </p>
                    <div class="list-item-meta">
                        <span><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> ${formatDate(fecha)}</span>
                        <span>👥 ${atendido || 'Agente IA'}</span>
                    </div>
                </div>
                <div class="list-item-badges">
                    ${tratam ? makeBadge(tratam, 'badge-yellow') : ''}
                    ${alcance ? makeBadge(alcance, 'badge-blue') : ''}
                </div>
            `;

            row.addEventListener('click', () => {
                const title = `🔍 Robo OC ${nSiniestro || ''}`;
                const body = `
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Fecha del Siniestro</span>
                        <span class="modal-detail-value">${formatDateTime(fecha)}</span>
                    </div>
                    
                    <h3 class="modal-section-title">Detalles del Hecho</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Vehículo</span>
                        <span class="modal-detail-value">${vehiculo || '-'} ${patente ? `(${patente})` : ''}</span>
                    </div>
                    ${danyos.length ? `
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Elementos Afectados</span>
                        <span class="modal-detail-value">${danyos.map(d => makeBadge(d, 'badge-gray')).join(' ')}</span>
                    </div>` : ''}
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Análisis de Cobertura</span>
                        <span class="modal-detail-value">${alcance ? makeBadge(alcance, 'badge-blue') : '-'}</span>
                    </div>

                    <h3 class="modal-section-title">Progreso de Gestión</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Estado</span>
                        <span class="modal-detail-value">${tratam ? makeBadge(tratam, 'badge-yellow') : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Orden Pedida a Cía</span>
                        <span class="modal-detail-value">${orden ? makeBadge(orden, 'badge-green') : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Verificación</span>
                        <span class="modal-detail-value">${verif ? makeBadge(verif, 'badge-orange') : '-'}</span>
                    </div>
                    
                    <h3 class="modal-section-title">Seguimiento</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Atendido por</span>
                        <span class="modal-detail-value" style="color:var(--primary-light);">${atendido || '-'}</span>
                    </div>
                `;
                openModal(title, body);
            });

            pane.appendChild(row);
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
        pane.classList.add('list-mode');
        if (!robos || !robos.length) { pane.appendChild(emptyState('No hay denuncias de Robo/Incendio.')); return; }

        const hdr = document.createElement('p');
        hdr.style.cssText = 'color:var(--white-70);font-size:.9rem;margin:0 0 10px;';
        hdr.textContent = `🔥 ${robos.length} denuncia${robos.length !== 1 ? 's' : ''} de robo/incendio`;
        pane.appendChild(hdr);

        robos.forEach(r => {
            const idReg    = strVal(r['ID_UNICO_GESTION']);
            const nSiniestro = strVal(r['NUMERO DE SINIESTRO']); // Usually doesn't exist here but just in case
            const tipo     = strVal(r['TIPO DE ROBO / INCENDIO ']) || strVal(r['CLASIFICACIÓN DEL SINIESTRO']) || strVal(r['TIPO DE ATENCIÓN']);
            const alcance  = strVal(r['ALCANCE DE COBERTURA']);
            const tratam   = strVal(r['Tratamiento']) || strVal(r['TIPO DE ATENCIÓN']) || strVal(r['TRATAMIENTO']);
            const resoluc  = strVal(r['TIPO DE RESOLUCION']) || strVal(r['Elegir Resolucion ']);
            const fecha    = strVal(r['FECHA DE CREACION']);
            const atendido = resolvedAtendido(r);
            const estado   = strVal(r['ES CLIENTE']);

            // Color tipo exacto
            let tipoCls = 'badge-gray';
            if (tipo) {
                const tu = tipo.toUpperCase();
                if (tu.includes('ROBO TOTAL')) tipoCls = 'badge-red';
                else if (tu.includes('INCENDIO TOTAL')) tipoCls = 'badge-purple';
                else if (tu.includes('INCENDIO PARCIAL')) tipoCls = 'badge-green';
            }

            const row = document.createElement('div');
            row.className = 'glass-list-item';
            
            row.innerHTML = `
                <div class="list-item-main">
                    <p class="list-item-title">
                        ${idReg ? `<span class="badge badge-orange" style="font-size:.65rem;">🔥 ${idReg}</span>` : ''} 
                        Robo Total / Incendio
                    </p>
                    <div class="list-item-meta">
                        <span><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> ${formatDate(fecha)}</span>
                        <span>👥 ${atendido || 'Agente IA'}</span>
                    </div>
                </div>
                <div class="list-item-badges">
                    ${tipo ? makeBadge(tipo, tipoCls) : ''}
                    ${resoluc ? makeBadge(resoluc, 'badge-orange') : ''}
                </div>
            `;

            row.addEventListener('click', () => {
                const title = `🔥 Robo/Incendio ${idReg || ''}`;
                const body = `
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Fecha del Siniestro</span>
                        <span class="modal-detail-value">${formatDateTime(fecha)}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Status Principal</span>
                        <span class="modal-detail-value">${estado ? makeBadge(estado, 'badge-gray') : '-'}</span>
                    </div>
                    
                    <h3 class="modal-section-title">Detalles del Hecho</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Tipo de Siniestro</span>
                        <span class="modal-detail-value">${tipo ? makeBadge(tipo, tipoCls) : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Análisis de Cobertura</span>
                        <span class="modal-detail-value">${alcance ? makeBadge(alcance, 'badge-blue') : '-'}</span>
                    </div>

                    <h3 class="modal-section-title">Progreso de Gestión</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Tratamiento</span>
                        <span class="modal-detail-value">${tratam ? makeBadge(tratam, 'badge-green') : '-'}</span>
                    </div>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Resolución</span>
                        <span class="modal-detail-value">${resoluc ? makeBadge(resoluc, 'badge-orange') : '-'}</span>
                    </div>
                    
                    <h3 class="modal-section-title">Seguimiento</h3>
                    <div class="modal-detail-row">
                        <span class="modal-detail-label">Atendido por</span>
                        <span class="modal-detail-value" style="color:var(--primary-light);">${atendido || '-'}</span>
                    </div>
                `;
                openModal(title, body);
            });

            pane.appendChild(row);
        });
    }
});
