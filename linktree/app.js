/* =====================================================
   RAFAEL ALLENDE & ASOCIADOS - LINKTREE
   JavaScript - Modales, Formularios y Funcionalidad
   ===================================================== */

// Sucursales - se cargan desde API
let sucursales = [];

// Cargar sucursales desde Airtable
async function loadSucursales() {
    try {
        const API_URL = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://web-production-2584d.up.railway.app';
        
        const response = await fetch(`${API_URL}/api/sucursales`);
        const data = await response.json();
        
        if (data.status === 'success' && data.sucursales) {
            sucursales = data.sucursales;
            renderSucursales();
        }
    } catch (error) {
        console.error('Error cargando sucursales:', error);
    }
}

// =====================================================
// UTILS
// =====================================================

async function fetchWithTimeout(resource, options = {}) {
    const { timeout = 10000 } = options;
    
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
  
    try {
        const response = await fetch(resource, {
        ...options,
        signal: controller.signal  
        });
        clearTimeout(id);
        return response;
    } catch (error) {
        clearTimeout(id);
        throw error;
    }
}

// =====================================================

function openModal(modalId) {
    const modal = document.getElementById(`modal-${modalId}`);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Hide Main Page Indicator
        const mainIndicator = document.getElementById('scroll-indicator');
        if (mainIndicator) mainIndicator.style.display = 'none';
        
        // Global Scroll Indicator Logic
        const scrollIndicator = document.getElementById('global-scroll-indicator');
        // Expanded list of long modals that might need scrolling
        const longModals = ['cotizador', 'siniestro', 'faq', 'sucursales', 'nosotros', 'calificar'];
        
        if (scrollIndicator) {
            // Reset state
            scrollIndicator.classList.remove('hidden');
            
            if (longModals.includes(modalId)) {
                scrollIndicator.style.display = 'flex';
                
                // Add scroll listener to the modal CONTENT (the part that scrolls)
                const modalContent = modal.querySelector('.modal-content');
                const innerScroll = modal.querySelector('.branches-list'); // Inner scrollable list?
                
                const scrollTarget = innerScroll || modalContent;

                if (scrollTarget) {
                    // Remove old listener if any (clean implementation would track listener, but for now specific naming helps)
                    scrollTarget.onscroll = function() {
                        if (scrollTarget.scrollTop > 50) {
                            scrollIndicator.classList.add('hidden');
                        } else {
                            scrollIndicator.classList.remove('hidden');
                        }
                    };
                }
            } else {
                scrollIndicator.style.display = 'none';
            }
        }
        
        // Animar estadísticas si es el modal "nosotros"
        if (modalId === 'nosotros') {
            setTimeout(animateStats, 300);
        }

        // Cargar sucursales si es el modal "sucursales"
        if (modalId === 'sucursales') {
            if (sucursales.length === 0) {
                loadSucursales();
            } else {
                renderSucursales();
            }
        }
        
        // Renderizar sucursales si es el modal
        if (modalId === 'sucursales') {
            renderSucursales();
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(`modal-${modalId}`);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
        
        // Show Main Page Indicator
        const mainIndicator = document.getElementById('scroll-indicator');
        if (mainIndicator) mainIndicator.style.display = 'flex';
        
        // Hide Global Indicator
        const scrollIndicator = document.getElementById('global-scroll-indicator');
        if (scrollIndicator) {
            scrollIndicator.style.display = 'none';
        }

        // RESET Siniestro Modal specifically
        if (modalId === 'siniestro') {
            resetSiniestro();
        }
    }
}

function resetSiniestro() {
    // 1. Reset Internal State (UI)
    // Hide Form & Selection steps
    document.getElementById('step-form-siniestro').classList.remove('active');
    document.getElementById('step-selection-siniestro').classList.remove('active');
    
    // Show Validation step (Start fresh)
    document.getElementById('step-validation-siniestro').classList.add('active');

    // 2. Clear Iframe content to stop video/form
    const iframeWrapper = document.getElementById('iframe-wrapper-siniestro');
    if (iframeWrapper) iframeWrapper.innerHTML = '';
}

// Función para actualizar el indicador de pasos
function updateSiniestroStep(step) {
    for (let i = 1; i <= 3; i++) {
        const dot = document.getElementById(`sin-dot-${i}`);
        if (dot) {
            dot.classList.remove('active', 'completed');
            if (i < step) {
                dot.classList.add('completed');
            } else if (i === step) {
                dot.classList.add('active');
            }
        }
    }
}

// Cerrar modal al hacer click afuera
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        const modalId = e.target.id.replace('modal-', '');
        closeModal(modalId);
    }
});

// Cerrar modal con ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            const modalId = modal.id.replace('modal-', '');
            closeModal(modalId);
        });
    }
});

// =====================================================
// ACCORDION (FAQ)
// =====================================================

document.querySelectorAll('.accordion-header').forEach(button => {
    button.addEventListener('click', () => {
        const item = button.parentElement;
        const isActive = item.classList.contains('active');
        
        // Cerrar todos
        document.querySelectorAll('.accordion-item').forEach(i => {
            i.classList.remove('active');
        });
        
        // Abrir el seleccionado si no estaba activo
        if (!isActive) {
            item.classList.add('active');
        }
    });
});

// =====================================================
// SUCURSALES
// =====================================================

function renderSucursales() {
    const container = document.querySelector('.branches-list');
    if (!container) return;
    
    container.innerHTML = sucursales.map(suc => `
        <div class="branch-item" 
             onclick="window.open('${suc.googleMap}', '_blank')"
             onmouseenter="updateMapPreview('${suc.direccion}, ${suc.localidad}')">
            <div class="branch-icon">
                <i class="fas fa-building"></i>
            </div>
            <div class="branch-info">
                <h3>${suc.nombre.replace(/\s*\([^)]*\)\s*$/, '').trim()}</h3>
                <p>${suc.direccion}</p>
                <span class="branch-locality">${suc.localidad}</span>
                <span class="branch-hours">${suc.horario}</span>
            </div>
            <i class="fas fa-external-link-alt"></i>
        </div>
    `).join('');
}

function updateMapPreview(address) {
    const mapFrame = document.querySelector('#map iframe');
    if (mapFrame) {
        // Simple Google Maps Embed without API Key (Search mode)
        const query = encodeURIComponent(address);
        mapFrame.src = `https://maps.google.com/maps?q=${query}&t=&z=15&ie=UTF8&iwloc=&output=embed`;
    }
}

// =====================================================
// ESTADÍSTICAS ANIMADAS
// =====================================================

function animateStats() {
    // Seleccionar todos los elementos de estadísticas
    const stats = document.querySelectorAll('.stat-number, .qs-stat-number');
    
    stats.forEach(stat => {
        const targetAttr = stat.dataset.target;
        if (!targetAttr) return;
        
        const target = parseInt(targetAttr, 10);
        if (isNaN(target) || target <= 0) {
            stat.textContent = '0';
            return;
        }
        
        // Iniciar desde 0
        stat.textContent = '0';
        
        // Animación más fluida
        const duration = 5000; // 5 segundos
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Función de easing para efecto más natural
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(target * easeOut);
            
            stat.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                stat.textContent = target.toLocaleString();
            }
        }
        
        requestAnimationFrame(update);
    });
}

// =====================================================
// STAR RATING
// =====================================================

let selectedRating = 0;

document.querySelectorAll('.star-rating input').forEach(input => {
    input.addEventListener('change', (e) => {
        selectedRating = parseInt(e.target.value);
    });
});

// =====================================================
// FORMULARIOS
// =====================================================

// Número de WhatsApp de la empresa (cambiar por el real)
const WHATSAPP_NUMBER = '5493415551234';

// Formulario Cotizador
document.getElementById('form-cotizador')?.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const marca = document.getElementById('marca').value;
    const modelo = document.getElementById('modelo').value;
    const anio = document.getElementById('anio').value;
    const gnc = document.getElementById('gnc').value;
    const telefono = document.getElementById('telefono').value;
    
    const mensaje = `🚘 *COTIZACIÓN DE SEGURO*%0A%0A` +
        `*Vehículo:* ${marca} ${modelo} (${anio})%0A` +
        `*GNC:* ${gnc === 'si' ? 'Sí' : 'No'}%0A` +
        `*WhatsApp de contacto:* ${telefono}%0A%0A` +
        `Solicito cotización, gracias.`;
    
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${mensaje}`, '_blank');
    closeModal('cotizador');
});

// Formulario Siniestro
// Auto-fill form data from URL parameters
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const dni = urlParams.get('dni');
    const patente = urlParams.get('patente');
    const nombre = urlParams.get('nombre');

    if (dni) {
        if(document.getElementById('dni')) document.getElementById('dni').value = dni;
        if(document.getElementById('dni-califica')) document.getElementById('dni-califica').value = dni;
    }
    if (patente && document.getElementById('patente')) {
        document.getElementById('patente').value = patente;
    }
    if (nombre && document.getElementById('nombre-califica')) {
        document.getElementById('nombre-califica').value = nombre;
    }
});

// Formulario Siniestro
// Formulario Siniestro
// [MOVIDO A FLUJO IFRAME AIRTABLE - VER SECCIÓN FINAL DEL ARCHIVO]

// Dynamic Siniestro File Logic
document.getElementById('tipo-siniestro')?.addEventListener('change', (e) => {
    updateFileRequirements(e.target.value);
});

function updateFileRequirements(tipo) {
    const groups = document.querySelectorAll('.file-group');
    const extraRuedas = document.getElementById('extra-ruedas');
    const extraParcial = document.getElementById('extra-robo-parcial');
    const usoVehiculo = document.getElementById('uso-vehiculo-container');
    
    // 1. Hide EVERYTHING first
    groups.forEach(g => g.classList.add('hidden'));
    if(extraRuedas) extraRuedas.classList.add('hidden');
    if(extraParcial) extraParcial.classList.add('hidden');
    if(usoVehiculo) usoVehiculo.classList.add('hidden');

    // 2. Helper to show specific groups
    const show = (names) => {
        names.forEach(n => {
            document.querySelectorAll(`.file-group[data-group="${n}"]`).forEach(el => el.classList.remove('hidden'));
        });
    };

    // 3. Logic by Type
    switch(tipo) {
        case 'choque':
            show(['identidad', 'carnet', 'daños', 'denuncia']);
            if(usoVehiculo) {
                usoVehiculo.classList.remove('hidden');
                usoVehiculo.style.display = ''; // Clear inline cleanup
            }
            break;
            
        case 'granizo':
            show(['identidad', 'daños']);
            break;

        case 'cristales':
            show(['identidad', 'daños']);
            if(extraParcial) {
                extraParcial.classList.remove('hidden');
                extraParcial.style.display = '';
            } 
            break;
            
        case 'robo': // ROBO TOTAL
            // Solo identidad y denuncia. El auto no está, no hay fotos de daño ni carnet necesario.
            show(['identidad', 'denuncia']);
            break;

        case 'robo-ruedas':
            show(['identidad', 'denuncia']);
            // Usuario especificó: NO fotos de daño.
            if(extraRuedas) {
                extraRuedas.classList.remove('hidden');
                extraRuedas.style.display = '';
            }
            break;

        case 'robo-bateria':
            show(['identidad', 'denuncia', 'bateria']);
            break;

        case 'robo-parcial':
            // Robo de espejo, auxiliar, etc.
            show(['identidad', 'denuncia', 'daños']);
            if(extraParcial) {
                extraParcial.classList.remove('hidden');
                extraParcial.style.display = '';
            }
            break;
            
        case 'incendio-total':
        case 'incendio-parcial':
            show(['identidad', 'denuncia', 'daños', 'bomberos']);
            break;

        case 'otro':
            show(['identidad', 'daños', 'denuncia']);
            break;
    }
}

function showGroup(groupName) {
    // Deprecated by new logic above, but kept if called elsewhere or alias
    const group = document.querySelector(`.file-group[data-group="${groupName}"]`);
    if(group) group.classList.remove('hidden');
}

// Formulario Calificación
// Toggle DNI field visibility based on ES_CLIENTE selection
document.querySelectorAll('input[name="es-cliente"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const dniGroup = document.getElementById('dni-group');
        const fotoGroup = document.getElementById('foto-group');
        const esCliente = e.target.value === 'Sí';
        
        if (dniGroup) {
            dniGroup.style.display = esCliente ? 'flex' : 'none';
        }
        if (fotoGroup) {
            fotoGroup.style.display = esCliente ? 'block' : 'none';
            // Reset checkbox si no es cliente
            if (!esCliente) {
                document.getElementById('usar-foto').checked = false;
            }
        }
    });
});

document.getElementById('form-calificar')?.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const nombre = document.getElementById('nombre-califica').value;
    const esCliente = document.querySelector('input[name="es-cliente"]:checked')?.value || 'No';
    const dni = document.getElementById('dni-califica')?.value || '';
    const servicio = document.getElementById('servicio-califica').value;
    const comentario = document.getElementById('comentario').value;
    
    if (selectedRating === 0) {
        alert('Por favor selecciona una calificación');
        return;
    }
    
    if (!servicio) {
        alert('Por favor selecciona qué servicio estás calificando');
        return;
    }
    
    // Datos para enviar al webhook de n8n
    const autorizaPublicar = document.getElementById('autoriza-publicar')?.checked || false;
    const usarFoto = document.getElementById('usar-foto')?.checked || false;
    
    const calificacionData = {
        estrellas: selectedRating,
        nombre: nombre,
        es_cliente: esCliente,
        dni: esCliente === 'Sí' && dni ? parseInt(dni) : null,
        servicio: servicio,
        comentario: comentario,
        modo: 'Online',
        autoriza_publicar: autorizaPublicar,
        usar_foto: usarFoto
    };
    
    console.log('📊 Datos de calificación:', calificacionData);
    
    // Enviar a webhook n8n
    const submitBtn = e.target.querySelector('.btn-submit');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    submitBtn.disabled = true;
    
    fetchWithTimeout('https://web-production-2584d.up.railway.app/api/rating', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(calificacionData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('✅ Calificación guardada:', data);
        alert(`¡Gracias ${nombre || 'por tu tiempo'}! Tu calificación de ${selectedRating} estrellas ha sido registrada.`);
        closeModal('calificar');
        
        // Reset form
        e.target.reset();
        selectedRating = 0;
        document.getElementById('dni-group').style.display = 'none';
    })
    .catch(error => {
        console.error('❌ Error:', error);
        alert('Hubo un error al enviar tu calificación. Por favor intenta nuevamente.');
    })
    .finally(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
});

// =====================================================
// RATING DINÁMICO
// =====================================================

function loadDynamicRating() {
    const ratingDisplay = document.getElementById('rating-display');
    if (!ratingDisplay) return;
    
    // URL del webhook n8n para obtener rating promedio
    const RATING_ENDPOINT = 'https://web-production-2584d.up.railway.app/api/rating';
    
    fetchWithTimeout(RATING_ENDPOINT)
        .then(response => response.json())
        .then(data => {
            console.log('⭐ Rating cargado:', data);
            
            const rating = data.rating || 0;
            const total = data.total || 0;
            
            // Generar estrellas visuales con Font Awesome
            let starsHTML = '';
            const fullStars = Math.floor(rating);
            const hasHalf = rating - fullStars >= 0.3 && rating - fullStars < 0.8;
            const emptyStars = 5 - fullStars - (hasHalf ? 1 : 0);
            
            // Estrellas llenas
            for (let i = 0; i < fullStars; i++) {
                starsHTML += '<i class="fas fa-star"></i>';
            }
            
            // Media estrella si aplica
            if (hasHalf) {
                starsHTML += '<i class="fas fa-star-half-alt"></i>';
            }
            
            // Estrellas vacías
            for (let i = 0; i < emptyStars; i++) {
                starsHTML += '<i class="far fa-star"></i>';
            }
            
            // Actualizar display
            // Usamos una abreviatura o palabra completa según el espacio (aquí "Calificaciones")
            ratingDisplay.innerHTML = `
                ${starsHTML}
                <span>${rating}/5</span>
                <small class="rating-count">(${total} Calificaciones)</small>
            `;
        })
        .catch(error => {
            console.error('❌ Error cargando rating:', error);
            // Mostrar fallback
            ratingDisplay.innerHTML = `
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="far fa-star"></i>
                <span>4/5</span>
            `;
        });
}

// =====================================================
// TESTIMONIOS CARRUSEL
// =====================================================

let currentTestimonial = 0;
let testimonialInterval = null;

function loadTestimonials() {
    const carousel = document.getElementById('testimonials-carousel');
    const dotsContainer = document.getElementById('carousel-dots');
    if (!carousel) return;
    
    const TESTIMONIOS_ENDPOINT = 'https://web-production-2584d.up.railway.app/api/testimonios';
    
    fetchWithTimeout(TESTIMONIOS_ENDPOINT)
        .then(response => response.json())
        .then(data => {
            console.log('💬 Testimonios cargados:', data);
            
            const testimonios = data.testimonios || [];
            
            if (testimonios.length === 0) {
                carousel.innerHTML = '<div class="no-testimonials">Aún no hay opiniones publicadas</div>';
                return;
            }
            
            // Generar HTML del carrusel
            let trackHTML = '<div class="testimonials-track">';
            let dotsHTML = '';
            
            testimonios.forEach((t, index) => {
                // Generar estrellas
                let starsHTML = '';
                for (let i = 0; i < 5; i++) {
                    starsHTML += i < t.estrellas 
                        ? '<i class="fas fa-star"></i>' 
                        : '<i class="far fa-star"></i>';
                }
                
                // Avatar con foto o iniciales
                const avatarContent = t.fotoUrl 
                    ? `<img src="${t.fotoUrl}" alt="${t.nombre}" onerror="this.outerHTML='${t.iniciales}'">`
                    : t.iniciales;
                
                trackHTML += `
                    <div class="testimonial-bubble">
                        <div class="testimonial-card">
                            <div class="testimonial-header">
                                <div class="testimonial-avatar">${avatarContent}</div>
                                <div class="testimonial-info">
                                    <div class="testimonial-name">${t.nombre}</div>
                                    <div class="testimonial-stars">${starsHTML}</div>
                                </div>
                            </div>
                            <p class="testimonial-comment">"${t.comentario}"</p>
                            <div class="testimonial-date">${t.fecha}</div>
                        </div>
                    </div>
                `;
                
                dotsHTML += `<div class="carousel-dot ${index === 0 ? 'active' : ''}" data-index="${index}"></div>`;
            });
            
            trackHTML += '</div>';
            carousel.innerHTML = trackHTML;
            dotsContainer.innerHTML = dotsHTML;
            
            // Eventos de dots
            dotsContainer.querySelectorAll('.carousel-dot').forEach(dot => {
                dot.addEventListener('click', () => {
                    goToTestimonial(parseInt(dot.dataset.index));
                });
            });
            
            // Auto-rotación cada 5 segundos
            if (testimonios.length > 1) {
                testimonialInterval = setInterval(() => {
                    currentTestimonial = (currentTestimonial + 1) % testimonios.length;
                    goToTestimonial(currentTestimonial);
                }, 5000);
            }
        })
        .catch(error => {
            console.error('❌ Error cargando testimonios:', error);
            carousel.innerHTML = '<div class="no-testimonials">Error al cargar opiniones</div>';
        });
}

function goToTestimonial(index) {
    currentTestimonial = index;
    const track = document.querySelector('.testimonials-track');
    const dots = document.querySelectorAll('.carousel-dot');
    
    if (track) {
        track.style.transform = `translateX(-${index * 100}%)`;
    }
    
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

// =====================================================
// INICIALIZACIÓN
// =====================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🛡️ Rafael Allende & Asociados - Linktree Premium cargado');
    
    // Cargar configuración de formularios
    loadFormConfig();
    
    // Cargar rating dinámico
    loadDynamicRating();
    
    // Cargar testimonios
    loadTestimonials();

    // Indicador de Scroll logic
    const scrollIndicator = document.getElementById('scroll-indicator');
    if (scrollIndicator) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                scrollIndicator.classList.add('hidden');
            } else {
                scrollIndicator.classList.remove('hidden');
            }
        });
    }
});
// =====================================================
//  SINIESTROS - NUEVO FLUJO DE 3 PASOS
// =====================================================

// =====================================================
//  SINIESTROS - NUEVO FLUJO CUSTOM FORMS (NO IFRAME)
// =====================================================

const BACKEND_URL = "https://web-production-2584d.up.railway.app";
const WEBHOOK_VALIDACION_SINIESTRO = `${BACKEND_URL}/api/validate-siniestro`;
// const BACKEND_CREATE_SINIESTRO = "http://localhost:8000/api/create-siniestro"; // DEV
const BACKEND_CREATE_SINIESTRO = `${BACKEND_URL}/api/create-siniestro`; // PROD

// Configuración de Formularios (Cargada dinámicamente)
let FORM_CONFIG = {};

function loadFormConfig() {
    const primaryUrl = `${BACKEND_URL}/api/config-formularios`;
    const fallbackUrl = 'FORM_CONFIG.json';

    fetch(primaryUrl)
        .then(response => {
            if (!response.ok) throw new Error(`Backend Status: ${response.status}`);
            return response.json();
        })
        .then(config => {
            console.log('📝 Configuración de formularios cargada (Backend):', config);
            FORM_CONFIG = config;
            renderDynamicMenu(); // NEW: Render menu dynamically
        })
        .catch(errorBackend => {
            console.warn('⚠️ Fallo carga de Backend, intentando local...', errorBackend);
            
            // INTENTO DE FALLBACK
            fetch(fallbackUrl)
                .then(response => response.json())
                .then(config => {
                    console.log('📝 Configuración de formularios cargada (Local Fallback):', config);
                    FORM_CONFIG = config;
                    renderDynamicMenu(); // NEW: Render menu dynamically
                })
                .catch(errorLocal => {
                    console.error('❌ Error total cargando configuración:', errorLocal);
                    FORM_CONFIG = {}; 
                    alert('Error cargando la configuración del sistema. Por favor recarga la página.');
                });
        });
}

// NUEVO: Renderizado dinámico del menú de siniestros
function renderDynamicMenu() {
    const container = document.getElementById('siniestros-menu-dynamic');
    if (!container) return;

    if (Object.keys(FORM_CONFIG).length === 0) {
        container.innerHTML = '<p style="text-align:center;">No hay tipos de denuncia disponibles.</p>';
        return;
    }

    container.innerHTML = ''; // Limpiar loader

    Object.keys(FORM_CONFIG).forEach(key => {
        const config = FORM_CONFIG[key];
        
        // Detectar si es FontAwesome o Emoji/Texto
        const iconHtml = config.icono.match(/fa-/)
            ? `<i class="fas ${config.icono}" style="font-size: 2rem; color: ${config.color || 'var(--primary)'};"></i>`
            : `<span style="font-size: 2rem;">${config.icono}</span>`;

        const btn = document.createElement('button');
        btn.className = 'option-card-btn animate-fade-in';
        btn.onclick = () => seleccionarTipoSiniestro(key);
        btn.innerHTML = `
            ${iconHtml}
            <span>${config.titulo}</span>
        `;
        
        container.appendChild(btn);
    });
}

function validarClienteSiniestro() {
    console.log('🚀 Iniciando validación...');
    const patente = document.getElementById('val-patente-siniestro').value.trim().toUpperCase();
    const dni = document.getElementById('val-dni-siniestro').value.trim();
    const btn = document.getElementById('btn-validar-siniestro'); 
    
    // Contenedor de Error
    const errorContainer = document.getElementById('msg-val-error-siniestro');
    if (errorContainer) {
        errorContainer.style.display = 'none';
    }

    if (patente.length < 6 || dni.length < 7) {
        mostrarErrorValidacion('Por favor revisá los datos ingresados (DNI o Patente incompletos).');
        return;
    }

    if(btn) {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verificando...';
        btn.disabled = true;
    }

    const url = `${WEBHOOK_VALIDACION_SINIESTRO}?patente=${patente}&dni=${dni}`;
    
    fetchWithTimeout(url)
        .then(res => res.json().then(data => {
            if (!res.ok) throw new Error(data.message || 'Error en validación');
            return data;
        }))
        .then(data => {
            if (data.valid) {
                // Guardar datos
                sessionStorage.setItem('validacion_siniestro', JSON.stringify({
                    nombres: data.cliente.nombres,
                    apellido: data.cliente.apellido,
                    dni: dni,
                    patente: patente,
                    polizaRecordId: data.poliza.record_id,
                    polizaNumero: data.poliza.numero,
                    polizaInfo: data.poliza
                }));
                mostrarSeleccionSiniestro(data);
            } else {
                mostrarErrorValidacion(data.message || 'No logramos validar tu cobertura.');
            }
        })
        .catch(err => {
            console.error(err);
            mostrarErrorValidacion('No pudimos verificar tu cobertura. Por favor intentá nuevamente.');
        })
        .finally(() => {
            if (btn) {
                btn.innerHTML = '<i class="fas fa-check-circle"></i> Verificar Cobertura';
                btn.disabled = false;
            }
        });
}

function mostrarErrorValidacion(msg) {
    const errorContainer = document.getElementById('msg-val-error-siniestro');
    if (errorContainer) {
        errorContainer.style.display = 'block';
        errorContainer.innerHTML = `<strong><i class="fas fa-exclamation-circle"></i></strong> ${msg}`;
    } else {
        Swal.fire('Atención', msg, 'warning');
    }
}

function mostrarSeleccionSiniestro(data) {
    document.getElementById('step-validation-siniestro').classList.remove('active');
    document.getElementById('step-selection-siniestro').classList.add('active');
    
    // Renderizar tarjeta de bienvenida
    const poliza = data.poliza;

    // Limpiar estado para evitar duplicados visuales
    let estadoLimpio = poliza.estado.replace(/🆘|AUX|INFINITY|❤️|VIDA|✅|⏰/g, '').trim();
    if (!estadoLimpio) estadoLimpio = "CONSULTAR";

    // Badges de Cobertura (Vida / Auxilio)
    let coverageBadges = '';
    
    if (poliza.vida || poliza.estado.includes('VIDA')) {
        coverageBadges += `<span class="info-pill vida"><i class="fas fa-heart"></i> VIDA</span>`;
    }
    
    // Detectar Auxilio por flag o texto
    if (poliza.auxilio || poliza.estado.includes('AUX')) {
        coverageBadges += `<span class="info-pill aux"><i class="fas fa-tools"></i> AUXILIO</span>`;
    }

    document.getElementById('msg-bienvenida-siniestro').innerHTML = `
        <div class="welcome-card">
            <h3>👋 Hola, ${data.cliente.nombres}</h3>
            
            <div class="policy-details-grid">
                <!-- Columna 1: Vehículo -->
                <div class="policy-column">
                    <span class="info-pill"><i class="fas fa-car"></i> ${poliza.tipo_vehiculo}</span>
                    <span class="info-pill"><i class="fas fa-id-card"></i> ${poliza.patente}</span>
                </div>
                
                <!-- Columna 2: Póliza -->
                <div class="policy-column">
                    <span class="info-pill"><i class="fas fa-shield-alt"></i> Póliza: ${poliza.numero}</span>
                    <span class="info-pill ${estadoLimpio.includes('VIGENTE') || estadoLimpio.includes('VENCE') ? 'vigente' : ''}">
                        <i class="fas fa-clock"></i> ${estadoLimpio}
                    </span>
                </div>
                
                <!-- Columna 3: Coberturas Extra (Si existen) -->
                ${coverageBadges ? `
                <div class="policy-column">
                    ${coverageBadges}
                </div>
                ` : ''}
            </div>
        </div>
    `;
}

function seleccionarTipoSiniestro(tipo) {
    const config = FORM_CONFIG[tipo];
    if (!config) return;

    // 1. Ocultar pasos anteriores
    document.getElementById('step-selection-siniestro').classList.remove('active');
    const stepForm = document.getElementById('step-form-siniestro');
    stepForm.classList.add('active');

    // 2. Renderizar Formulario dinámico
    const validationData = JSON.parse(sessionStorage.getItem('validacion_siniestro') || '{}');
    const container = document.getElementById('iframe-wrapper-siniestro'); // Reusamos este ID por conveniencia
    
    container.innerHTML = `
        <div class="custom-form-container">
            <div class="form-header" style="border-left: 4px solid ${config.color}">
                <h2>
                    ${config.icono.match(/fa-/) 
                        ? `<i class="fas ${config.icono}"></i>` 
                        : `<span style="font-style: normal;">${config.icono}</span>`
                    } 
                    ${config.titulo}
                </h2>
                <p>Completá los detalles de lo sucedido</p>
            </div>
            
            <form id="dynamic-siniestro-form" class="animate-fade-in">
                <!-- Campos ocultos de contexto -->
                <input type="hidden" name="tipo_formulario" value="${tipo}">
                <input type="hidden" name="poliza_record_id" value="${validationData.polizaRecordId || ''}">
                <input type="hidden" name="patente" value="${validationData.patente || ''}">
                <input type="hidden" name="dni" value="${validationData.dni || ''}">

                ${config.campos.map(campo => renderCampo(campo)).join('')}

                <div class="form-actions">
                    <button type="submit" class="btn-submit" style="background: ${config.color}">
                        Enviar Denuncia <i class="fas fa-paper-plane"></i>
                    </button>
                    <button type="button" class="btn-secondary" onclick="volverSeleccionSiniestro()">
                        Cancelar
                    </button>
                </div>
            </form>
        </div>
    `;

    // 3. Bindear evento submit
    document.getElementById('dynamic-siniestro-form').addEventListener('submit', handleSiniestroSubmit);
}

function renderCampo(campo) {
    let inputHtml = '';
    
    switch(campo.type) {
        case 'file':
            inputHtml = `
                <input type="file" id="${campo.id}" name="${campo.id}" 
                    ${campo.required ? 'required' : ''} 
                    class="form-input" accept="image/*" multiple 
                    data-max-files="5">
                <small style="color: #ccc; display: block; margin-top: 5px;">
                    📷 Podés seleccionar hasta 5 fotos por campo
                </small>
            `;
            break;
        case 'select':
            const options = campo.options || [];
            inputHtml = `
                <select id="${campo.id}" name="${campo.id}" 
                    ${campo.required ? 'required' : ''} 
                    class="form-input">
                    <option value="">-- Seleccioná --</option>
                    ${options.map(opt => `<option value="${opt.trim()}">${opt.trim()}</option>`).join('')}
                </select>
            `;
            break;
        case 'textarea':
            inputHtml = `
                <textarea id="${campo.id}" name="${campo.id}" 
                    ${campo.required ? 'required' : ''} 
                    class="form-input" rows="4" 
                    placeholder="${campo.placeholder || 'Describí lo sucedido con el mayor detalle posible...'}"></textarea>
            `;
            break;
        default: // text, date, number, time...
            inputHtml = `
                <input type="${campo.type}" id="${campo.id}" name="${campo.id}" 
                    ${campo.required ? 'required' : ''} 
                    class="form-input" placeholder="${campo.placeholder || ''}">
            `;
    }

    return `
        <div class="form-group-dynamic">
            <label for="${campo.id}">${campo.label} ${campo.required ? '<span class="req">*</span>' : ''}</label>
            ${inputHtml}
        </div>
    `;
}

/**
 * Comprime una imagen usando Canvas antes de subirla.
 * Reduce drasticamente el tamaño de fotos de cámara de celular.
 * @param {File} file - Archivo original
 * @param {number} maxPx - Máximo ancho/alto en píxeles (default 1200)
 * @param {number} quality - Calidad JPEG 0-1 (default 0.75)
 * @returns {Promise<File>} Archivo comprimido
 */
async function compressImage(file, maxPx = 1200, quality = 0.75) {
    // Solo comprimir formatos raster comunes. SVG o PDF se pasan directo.
    const RASTER = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/heic', 'image/heif'];
    if (!RASTER.includes(file.type.toLowerCase())) {
        console.log(`📎 Saltando compresión para tipo: ${file.type}`);
        return file;
    }

    return new Promise((resolve) => {
        // Timeout de 5s para evitar que el canvas se cuelgue infinitamente
        const timer = setTimeout(() => {
            console.warn(`🕒 Timeout compresión (5s) para "${file.name}". Usando original.`);
            resolve(file);
        }, 5000);

        const img = new Image();
        const url = URL.createObjectURL(file);
        
        img.onload = () => {
            clearTimeout(timer);
            let { width, height } = img;
            if (width > maxPx || height > maxPx) {
                if (width > height) {
                    height = Math.round((height * maxPx) / width);
                    width = maxPx;
                } else {
                    width = Math.round((width * maxPx) / height);
                    height = maxPx;
                }
            }
            
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            
            URL.revokeObjectURL(url);
            
            canvas.toBlob(
                (blob) => {
                    const compressed = new File([blob], file.name.replace(/\.[^/.]+$/, "") + ".jpg", {
                        type: 'image/jpeg',
                        lastModified: Date.now()
                    });
                    if (compressed.size > file.size) {
                        // Si la compresión resultó más pesada, usar original
                        resolve(file);
                    } else {
                        const reduction = Math.round((1 - compressed.size / file.size) * 100);
                        console.log(`🗜️ Comprimida "${file.name}": ${(file.size/1024/1024).toFixed(1)}MB → ${(compressed.size/1024).toFixed(0)}KB (-${reduction}%)`);
                        resolve(compressed);
                    }
                },
                'image/jpeg',
                quality
            );
        };

        img.onerror = () => {
            clearTimeout(timer);
            URL.revokeObjectURL(url);
            console.error(`❌ Error cargando imagen para compresión: ${file.name}`);
            resolve(file);
        };

        img.src = url;
    });
}

async function handleSiniestroSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    
    // UI Loading
    const originalBtnContent = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';

    // Recolectar datos
    const formData = new FormData(form);
    
    // Preparar Payload Multipart
    const payload = new FormData();
    const datos = {};
    const standardFields = ['tipo_formulario', 'poliza_record_id', 'dni', 'patente'];
    const fileFields = []; // Detectaremos cuales son archivos

    // Iteramos entradas una sola vez
    // Iterar entradas: campos standard al payload, archivos se comprimen, resto a datos
    // Primero mostrar estado de compresión si hay archivos
    let tieneArchivos = false;
    for (const [key, value] of formData.entries()) {
        // Verificación robusta de archivo
        const isFile = value instanceof File || (value && typeof value === 'object' && value.name && value.type);
        if (isFile && value.size > 0) { 
            tieneArchivos = true; 
            console.log(`📎 Detectado archivo: ${key} - ${value.name} (${value.size} bytes)`);
            break; 
        }
    }
    if (tieneArchivos) {
        btn.innerHTML = '<i class="fas fa-compress-arrows-alt fa-spin"></i> Comprimiendo fotos...';
    }

    for (const [key, value] of formData.entries()) {
        // Verificación robusta de archivo
        const isFile = value instanceof File || (value && typeof value === 'object' && value.name && value.type);
        
        if (standardFields.includes(key)) {
            payload.append(key, value);
        } else if (isFile) {
            if (value.size > 0) {
                // Comprimir imagen antes de subir
                const compressed = await compressImage(value);
                console.log(`🗜️ ${key}: ${(value.size/1024/1024).toFixed(1)}MB → ${(compressed.size/1024).toFixed(0)}KB`);
                payload.append(key, compressed, compressed.name);
            }
            // Si el archivo tiene size 0 (no seleccionado), lo ignoramos
        } else {
            datos[key] = value;
        }
    }
    
    // Adjuntar JSON de datos
    payload.append('datos', JSON.stringify(datos));

    btn.innerHTML = '<i class="fas fa-cloud-upload-alt fa-spin"></i> Subiendo...';
    console.log("📨 Enviando payload Multipart via fetch...");

    // Usamos fetch con AbortController para el timeout (más compatible con CORS que XHR)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // 300 segundos (5 minutos)

    try {
        const response = await fetch(BACKEND_CREATE_SINIESTRO, {
            method: 'POST',
            body: payload,
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        console.log("📬 Respuesta del servidor:", response.status, response.ok);
        const data = await response.json();
        console.log("📬 Data recibida:", data);

        if (!response.ok) {
            throw new Error(data.detail || `Error del servidor (${response.status})`);
        }

        console.log("✅ Siniestro creado:", data);

        // Cerrar el modal del formulario primero
        const modalSiniestro = document.getElementById('modal-siniestro');
        if (modalSiniestro) {
            modalSiniestro.classList.remove('active');
        }

        // Construir mensaje detallado según el resultado
        const hayFallidos = data.archivos_fallidos && data.archivos_fallidos.length > 0;
        const archivosSubidos = data.archivos_subidos || 0;

        let htmlMsg = `<p>✅ <b>Envío exitoso</b> — La información fue registrada correctamente.</p>`;
        htmlMsg += `<br><b>Número de gestión: <span style="font-size:1.2em;color:#4ade80">${data.id || 'Asignado'}</span></b>`;

        if (archivosSubidos > 0 && !hayFallidos) {
            htmlMsg += `<br><br>📎 <span style="color:#4ade80">Carga exitosa — ${archivosSubidos} archivo(s) subido(s) correctamente.</span>`;
        } else if (hayFallidos) {
            htmlMsg += `<br><br>⚠️ <span style="color:#fbbf24">Algunos archivos no se pudieron cargar: ${data.archivos_fallidos.join(', ')}.<br>El resto de la información fue enviada correctamente.</span>`;
        }
        htmlMsg += `<br><br><small style="color:#aaa">Un asesor te contactará a la brevedad.</small>`;

        // Mostrar mensaje de éxito
        console.log("🎄 Intentando mostrar Swal...");
        
        if (typeof Swal !== 'undefined') {
            const numeroGestion = data.id || 'Asignado';
            
            Swal.fire({
                icon: hayFallidos ? 'warning' : 'success',
                title: hayFallidos ? '¡Denuncia Recibida con Advertencias!' : '¡Denuncia Recibida!',
                html: htmlMsg,
                showDenyButton: true,
                confirmButtonColor: '#4ade80',
                denyButtonColor: '#3b82f6',
                confirmButtonText: 'Aceptar',
                denyButtonText: '<i class="fas fa-download"></i> Guardar Comprobante',
                allowOutsideClick: false
            }).then((result) => {
                if (result.isDenied) {
                    // Generar y descargar el comprobante en texto simple
                    const fecha = new Date().toLocaleString();
                    const textoComprobante = `
COMPROBANTE DE DENUNCIA DE SINIESTRO
Rafael Allende & Asociados

Fecha: ${fecha}
Número de Gestión: ${numeroGestion}
Estado: Recibido correctamente.
Archivos adjuntos: ${archivosSubidos}
                    
Un asesor te contactará a la brevedad.
Gracias por confiar en nosotros.
`.trim();

                    // Intentar usar Web Share API si está en celular
                    if (navigator.share) {
                        navigator.share({
                            title: 'Comprobante de Siniestro',
                            text: textoComprobante
                        }).then(() => {
                            location.reload();
                        }).catch((err) => {
                            console.log('Error compartiendo:', err);
                            descargarTxt(textoComprobante, numeroGestion);
                            location.reload();
                        });
                    } else {
                        // Fallback: Descargar TXT
                        descargarTxt(textoComprobante, numeroGestion);
                        location.reload();
                    }
                } else {
                    location.reload();
                }
            }).catch((err) => {
                console.error("🎄 Error en Swal:", err);
                alert('¡Denuncia enviada correctamente!\n\nUn asesor te contactará a la brevedad.\n\nNúmero de gestión: ' + numeroGestion);
                location.reload();
            });
        } else {
            console.log("🎄 Swal no disponible, usando alert");
            alert('¡Denuncia enviada correctamente!\n\nUn asesor te contactará a la brevedad.\n\nNúmero de gestión: ' + (data.id || 'Asignado'));
            location.reload();
        }

        // Función auxiliar para descargar archivo de texto
        function descargarTxt(texto, numeroGestion) {
            const blob = new Blob([texto], { type: 'text/plain;charset=utf-8' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `comprobante_siniestro_${numeroGestion.replace(/[/\\?%*:|"<>]/g, '-')}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }


    } catch (error) {
        clearTimeout(timeoutId);
        console.error("❌ Error envio siniestro:", error);
        const msg = error.name === 'AbortError'
            ? 'Tiempo agotado (5 min). Las fotos son muy grandes o la conexión es lenta. Intentá nuevamente.'
            : (error.message || 'Error de conexión. Intentá nuevamente.');
        Swal.fire({ icon: 'error', title: 'Error al enviar', text: msg });
        btn.disabled = false;
        btn.innerHTML = originalBtnContent;
    }
}


function volverValidacionSiniestro() {
    document.getElementById('step-selection-siniestro').classList.remove('active');
    document.getElementById('step-validation-siniestro').classList.add('active');
}

function volverSeleccionSiniestro() {
    document.getElementById('step-form-siniestro').classList.remove('active');
    document.getElementById('iframe-wrapper-siniestro').innerHTML = ''; // Limpiar form
    document.getElementById('step-selection-siniestro').classList.add('active');
}

// =============================================================================
// CARGA DINÁMICA DE FAQ Y QUIÉNES SOMOS DESDE AIRTABLE
// =============================================================================

const FAQ_ENDPOINT = `${BACKEND_URL}/api/faqs`;
const QUIENES_SOMOS_ENDPOINT = `${BACKEND_URL}/api/quienes-somos`;

// Variable para cachear los datos
let faqsCache = null;
let quienesSomosCache = null;

// Cargar FAQs dinámicamente
async function loadFAQs() {
    const container = document.getElementById('faq-dynamic-content');
    if (!container) return;
    
    // Si ya están cargados, no volver a cargar
    if (faqsCache && container.querySelector('.accordion-item')) {
        return;
    }
    
    try {
        const response = await fetchWithTimeout(FAQ_ENDPOINT, { timeout: 10000 });
        const data = await response.json();
        
        if (!data.faqs || data.faqs.length === 0) {
            container.innerHTML = '<p style="text-align:center;">No hay preguntas frecuentes disponibles.</p>';
            return;
        }
        
        faqsCache = data.faqs;
        
        // Renderizar FAQs con soporte para FontAwesome y emojis
        container.innerHTML = data.faqs.map(faq => {
            // Detectar si es FontAwesome o emoji
            const icono = faq.icono || 'fa-question-circle';
            const iconoHtml = icono.match(/^fa-/) 
                ? `<i class="fas ${icono}"></i>` 
                : `<span>${icono}</span>`;
            
            return `<div class="accordion-item">
                <button class="accordion-header">
                    ${iconoHtml} ${faq.pregunta}
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>`;
        }).join('');
        
        // Re-inicializar los event listeners del accordion
        initAccordion();
        
    } catch (error) {
        console.error('❌ Error cargando FAQs:', error);
        container.innerHTML = '<p style="text-align:center;">Error al cargar preguntas frecuentes.</p>';
    }
}

// Cargar Quiénes Somos dinámicamente
async function loadQuienesSomos() {
    const container = document.getElementById('nosotros-dynamic-content');
    if (!container) return;
    
    // Si ya está cargado, no volver a cargar
    if (quienesSomosCache && container.querySelector('.about-hero')) {
        return;
    }
    
    try {
        const response = await fetchWithTimeout(QUIENES_SOMOS_ENDPOINT, { timeout: 10000 });
        const data = await response.json();
        
        if (!data.visible) {
            container.innerHTML = '<p style="text-align:center;">Sección no disponible.</p>';
            return;
        }
        
        quienesSomosCache = data;
        
        // Construir HTML dinámico - DISEÑO PREMIUM
        const statsHTML = data.estadisticas.mostrar ? `
            <div class="qs-stats-grid">
                ${data.estadisticas.anos_experiencia > 0 ? `
                <div class="qs-stat-card">
                    <div class="qs-stat-icon"><i class="fas fa-calendar-alt"></i></div>
                    <div class="qs-stat-info">
                        <span class="qs-stat-number" data-target="${data.estadisticas.anos_experiencia}">0</span>
                        <span class="qs-stat-label">Años de Experiencia</span>
                    </div>
                </div>` : ''}
                ${data.estadisticas.cantidad_clientes > 0 ? `
                <div class="qs-stat-card">
                    <div class="qs-stat-icon"><i class="fas fa-users"></i></div>
                    <div class="qs-stat-info">
                        <span class="qs-stat-number" data-target="${data.estadisticas.cantidad_clientes}">0</span>
                        <span class="qs-stat-label">Clientes Felices</span>
                    </div>
                </div>` : ''}
                ${data.estadisticas.cantidad_sucursales > 0 ? `
                <div class="qs-stat-card">
                    <div class="qs-stat-icon"><i class="fas fa-building"></i></div>
                    <div class="qs-stat-info">
                        <span class="qs-stat-number" data-target="${data.estadisticas.cantidad_sucursales}">0</span>
                        <span class="qs-stat-label">Sucursales</span>
                    </div>
                </div>` : ''}
                ${data.estadisticas.cantidad_polizas > 0 ? `
                <div class="qs-stat-card">
                    <div class="qs-stat-icon"><i class="fas fa-file-contract"></i></div>
                    <div class="qs-stat-info">
                        <span class="qs-stat-number" data-target="${data.estadisticas.cantidad_polizas}">0</span>
                        <span class="qs-stat-label">Pólizas Activas</span>
                    </div>
                </div>` : ''}
            </div>
        ` : '';
        
        const valoresHTML = data.valores && data.valores.length > 0 ? `
            <div class="qs-values-section">
                <h4 class="qs-section-title"><i class="fas fa-heart"></i> Nuestros Valores</h4>
                <div class="qs-values-grid">
                    ${data.valores.map(v => `<span class="qs-value-tag"><i class="fas fa-check-circle"></i> ${v}</span>`).join('')}
                </div>
            </div>
        ` : '';
        
        const fotoSrc = data.responsable.foto || 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&h=300&fit=crop';
        
        // Video presentation
        const videoHTML = data.video_presentacion ? `
            <div class="qs-video-section">
                <div class="qs-video-container">
                    <iframe 
                        src="${data.video_presentacion.replace('watch?v=', 'embed/')}" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
            </div>
        ` : '';
        
        // Imagen de fondo - aplicar al modal-content si existe imagen
        const modalContent = document.querySelector('#modal-nosotros .modal-content');
        if (modalContent && data.imagen_fondo) {
            modalContent.style.backgroundImage = `linear-gradient(rgba(10, 22, 61, 0.92), rgba(10, 22, 61, 0.98)), url('${data.imagen_fondo}')`;
            modalContent.style.backgroundSize = 'cover';
            modalContent.style.backgroundPosition = 'center';
        }
        
        // Usar colores dinámicos o defaults
        const colorPrincipal = data.colores?.principal || '#1e40af';
        const colorSecundario = data.colores?.secundario || '#f59e0b';
        
        container.innerHTML = `
            <div class="qs-modal-wrapper" style="--color-primary: ${colorPrincipal}; --color-secondary: ${colorSecundario};">
                <!-- Header Premium -->
                <div class="qs-header" style="background: linear-gradient(135deg, ${colorPrincipal} 0%, ${colorPrincipal} 100%);">
                    <div class="qs-header-shine"></div>
                    <div class="qs-header-content">
                        <div class="qs-avatar-wrapper">
                            <img src="${fotoSrc}" alt="${data.responsable.nombre || 'Empresa'}" class="qs-avatar" />
                            <div class="qs-avatar-badge"><i class="fas fa-shield-alt"></i></div>
                        </div>
                        <div class="qs-header-text">
                            <h2 class="qs-title">${data.titulo}</h2>
                            ${data.subtitulo ? `<p class="qs-subtitle">${data.subtitulo}</p>` : ''}
                            ${data.responsable.nombre ? `<p class="qs-responsable"><i class="fas fa-user-tie"></i> ${data.responsable.nombre} <span class="qs-cargo">${data.responsable.cargo || ''}</span></p>` : ''}
                        </div>
                    </div>
                </div>
                
                <!-- Contenido Principal -->
                <div class="qs-body">
                    ${data.texto_principal ? `
                    <div class="qs-description">
                        <p>${data.texto_principal}</p>
                    </div>
                    ` : ''}
                    
                    <!-- Video -->
                    ${videoHTML}
                    
                    <!-- Misión y Visión -->
                    <div class="qs-mv-grid">
                        ${data.mision ? `
                        <div class="qs-mv-card qs-mision">
                            <div class="qs-mv-icon"><i class="fas fa-bullseye"></i></div>
                            <h4>Misión</h4>
                            <p>${data.mision}</p>
                        </div>` : ''}
                        ${data.vision ? `
                        <div class="qs-mv-card qs-vision">
                            <div class="qs-mv-icon"><i class="fas fa-eye"></i></div>
                            <h4>Visión</h4>
                            <p>${data.vision}</p>
                        </div>` : ''}
                    </div>
                    
                    <!-- Valores -->
                    ${valoresHTML}
                    
                    <!-- Estadísticas -->
                    ${statsHTML}
                </div>
                
                <!-- Footer -->
                <div class="qs-footer">
                    <p><i class="fas fa-map-marker-alt"></i> Rosario, Argentina</p>
                </div>
            </div>
        `;
        
        // Inicializar animación de estadísticas después de cargar
        setTimeout(() => {
            animateStats();
        }, 100);
        
    } catch (error) {
        console.error('❌ Error cargando Quiénes Somos:', error);
        container.innerHTML = '<p style="text-align:center;">Error al cargar la información.</p>';
    }
}

// Modificar openModal para cargar datos dinámicamente
const originalOpenModal = openModal;
openModal = function(modalId) {
    originalOpenModal(modalId);
    
    // Cargar FAQ cuando se abre el modal
    if (modalId === 'faq') {
        loadFAQs();
    }
    
    // Cargar Quiénes Somos cuando se abre el modal
    if (modalId === 'nosotros') {
        loadQuienesSomos();
    }
};

// Función para inicializar accordion después de cargar FAQs dinámicamente
function initAccordion() {
    document.querySelectorAll('.accordion-header').forEach(button => {
        button.addEventListener('click', () => {
            const item = button.parentElement;
            const isActive = item.classList.contains('active');
            
            // Cerrar todos
            document.querySelectorAll('.accordion-item').forEach(i => {
                i.classList.remove('active');
            });
            
            // Abrir el seleccionado si no estaba activo
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}
