/* =====================================================
   RAFAEL ALLENDE & ASOCIADOS - LINKTREE
   JavaScript - Modales, Formularios y Funcionalidad
   ===================================================== */

// Sucursales con datos reales de Airtable
const sucursales = [
    {
        nombre: "Casa Central - Fisherton",
        direccion: "Eva Perón esq. Donado (Est. YPF)",
        localidad: "Rosario",
        horario: "Lun-Vie 9:30-12:30 / 16-19 | Sáb 10-13",
        googleMap: "https://maps.app.goo.gl/6Equ8ozkoLjKcedq8"
    },
    {
        nombre: "Rosario Centro",
        direccion: "Alvear 1194 - Filial",
        localidad: "Rosario",
        horario: "Lun-Vie 9-14",
        googleMap: "https://maps.app.goo.gl/QY4T3is9R9BoFNqy5"
    },
    {
        nombre: "Rosario Sur",
        direccion: "Ovidio Lagos 4949",
        localidad: "Rosario",
        horario: "Lun-Vie 9:30-12:30 / 16:30-19:30",
        googleMap: "https://maps.app.goo.gl/Fjco6ZJGpA1ar4vi7"
    },
    {
        nombre: "Rosario Magna",
        direccion: "JJ Paso 6698 (Est. Magna)",
        localidad: "Rosario",
        horario: "Lun-Vie 10-13 / 17-19:30 | Sáb 10-13",
        googleMap: "https://maps.app.goo.gl/nYMFcopvFuu6v1Zx6"
    },
    {
        nombre: "Granadero Baigorria",
        direccion: "San Martín y Arenales",
        localidad: "Gro. Baigorria",
        horario: "Lun-Vie 9:30-12:30 / 16:30-19:30 | Sáb 10-13",
        googleMap: "https://maps.app.goo.gl/3aGLQ3VfZAmYa8HK8"
    },
    {
        nombre: "Villa G. Gálvez",
        direccion: "Mosconi 1416",
        localidad: "V.G. Gálvez",
        horario: "Lun-Vie 10-19",
        googleMap: "https://maps.app.goo.gl/gWc3KzadJX6YCN5DA"
    },
    {
        nombre: "San Lorenzo",
        direccion: "San Martín 910",
        localidad: "San Lorenzo",
        horario: "Lun-Vie 9:30-12:30 / 16:30-19:30",
        googleMap: "https://maps.app.goo.gl/dYN2yPUh2T9wXj377"
    },
    {
        nombre: "Puerto Gral. San Martín",
        direccion: "Córdoba 315",
        localidad: "Pto. San Martín",
        horario: "Lun-Vie 9:30-12:30 / 16:30-19:30",
        googleMap: "https://maps.app.goo.gl/biLTkcJQAuZiB2Xh6"
    },
    {
        nombre: "Santa Fe",
        direccion: "Blas Parera 5750 (Est. Puma)",
        localidad: "Santa Fe",
        horario: "Lun-Vie 9:30-12:30 / 16:30-19:30",
        googleMap: "https://maps.app.goo.gl/piSJiJfvZbm3k4ci9"
    },
    {
        nombre: "Rafaela",
        direccion: "Consc. Elias Zurbriggen 865",
        localidad: "Rafaela",
        horario: "Lun-Vie 10-13 / 16:30-19:30",
        googleMap: "https://maps.app.goo.gl/pz85ZwRaStjSLP8K8"
    },
    {
        nombre: "San Nicolás",
        direccion: "Av. Savio 670",
        localidad: "San Nicolás",
        horario: "Lun-Vie 9:30-13 / 16-19 | Sáb 10-13",
        googleMap: "https://maps.app.goo.gl/8xfzNuv3wanfa81HA"
    }
];

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

    // 3. Clear Inputs? (Optional - User might want to re-use DNI/Patente if just closed by mistake)
    // User complaint suggest they want to "cargar un NUEVO siniestro" (implying different data or type).
    // If I keep inputs, they can just click "Validar" again.
    // But if I clear inputs, they have to type again.
    // The main issue was "no me deja seleccionar otro tipo".
    // So resetting to Validation or Selection is key.
    // Let's reset to Validation but keep inputs for convenience?
    // No, "cargar un nuevo siniestro" implies different car/person potentially.
    // Let's clear inputs for clean slate.
    document.getElementById('val-patente-siniestro').value = '';
    document.getElementById('val-dni-siniestro').value = '';
    
    // Clear session storage to avoid stale data
    sessionStorage.removeItem('validacion_siniestro');
    
    // 4. Clear Error Message Container
    const errorContainer = document.getElementById('msg-val-error-siniestro');
    if (errorContainer) {
        errorContainer.style.display = 'none';
        errorContainer.innerHTML = '';
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
                <h3>${suc.nombre}</h3>
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
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach(stat => {
        const target = parseInt(stat.dataset.target);
        const duration = 1500;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                stat.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
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
    fetch(`${BACKEND_URL}/api/config-formularios`)
        .then(response => response.json())
        .then(config => {
            console.log('📝 Configuración de formularios cargada:', config);
            FORM_CONFIG = config;
        })
        .catch(error => {
            console.error('❌ Error cargando configuración de formularios:', error);
            // Fallback básico si falla la carga
            FORM_CONFIG = {}; 
            alert('Error cargando la configuración del sistema. Por favor recarga la página.');
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
    
    if (!patente || !dni) {
        if (errorContainer){
            errorContainer.textContent = 'Por favor completá DNI y Patente.';
            errorContainer.style.display = 'block';
        }
        return;
    }
    
    // Loading State
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validando...';
    btn.disabled = true;

    // Call EndPoint
    const url = `${WEBHOOK_VALIDACION_SINIESTRO}?dni=${dni}&patente=${patente}`;
    
    fetchWithTimeout(url)
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status !== 200 || !body.valid) {
                throw new Error(body.message || 'Datos incorrectos');
            }
            return body;
        })
        .then(data => {
            console.log('✅ Validación Exitosa:', data);
            
            // Guardar en Session para usar después
            const sessionData = {
                dni: dni,
                patente: patente,
                cliente: data.cliente,
                poliza: data.poliza
            };
            sessionStorage.setItem('validacion_siniestro', JSON.stringify(sessionData));
            
            // Ir al paso 2: Selección de Tipo
            mostrarSeleccionSiniestro(data);
        })
        .catch(err => {
            console.error('❌ Error validación:', err);
            if (errorContainer) {
                errorContainer.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${err.message}`;
                errorContainer.style.display = 'block';
            }
        })
        .finally(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
}

function mostrarSeleccionSiniestro(data) {
    const { cliente, poliza } = data;
    
    // Ocultar paso 1, mostrar paso 2
    document.getElementById('step-validation-siniestro').classList.remove('active');
    document.getElementById('step-selection-siniestro').classList.add('active');
    
    // Limpiar estado de la póliza para display (quitar emojis)
    let estadoLimpio = poliza.estado.replace(/✅|🔴|🟢|⏳|⚠️|❌/g, '').trim();
    
    // Detectar coberturas extra (Vida, Auxilio)
    let coverageBadges = '';
    
    if (poliza.vida) {
        coverageBadges += `<span class="status-badge vida"><i class="fas fa-heart"></i> VIDA</span>`;
    }
    if (poliza.auxilio) {
        coverageBadges += `<span class="status-badge aux"><i class="fas fa-tools"></i> AUXILIO</span>`;
    }

    // Renderizar Header de Bienvenida
    const container = document.getElementById('msg-bienvenida-siniestro');
    container.innerHTML = `
        <div class="welcome-card">
            <h4>👋 Hola, ${cliente.nombres}!</h4>
            <p class="vehicle-info">
                <i class="fas fa-car"></i> ${poliza.tipo_vehiculo} ${poliza.patente}
                <br>
                <small>${poliza.descripcion_completa}</small>
            </p>
            <div class="badges-container">
                <span class="status-badge ${estadoLimpio.includes('VIGENTE') || estadoLimpio.includes('VENCE') ? 'vigente' : ''}">
                    ${estadoLimpio || 'VIGENTE'}
                </span>
                ${coverageBadges}
            </div>
        </div>
        <p class="instruction-text">¿Qué te pasó? Seleccioná una opción:</p>
    `;

    // Renderizar Opciones Dinámicamente desde FORM_CONFIG
    // Si form_config falló, usar hardcoded o mostrar error
    renderTypeOptions();
}

function renderTypeOptions() {
    const grid = document.querySelector('.siniestro-options-grid');
    if (!grid) return;
    
    // Si no hay config cargada, mostrar error (o reintentar load)
    if (Object.keys(FORM_CONFIG).length === 0) {
        grid.innerHTML = '<p class="error-text">Cargando tipos de siniestro...</p>';
        setTimeout(() => {
             // Retry once
             loadFormConfig();
             // If still empty, show hard error
             if (Object.keys(FORM_CONFIG).length === 0) {
                 grid.innerHTML = '<p class="error-text">Error cargando opciones. Reintentá.</p>';
                 // Fallback Hardcoded could go here
             } else {
                 renderTypeOptions();
             }
        }, 2000);
        return;
    }

    const html = Object.keys(FORM_CONFIG).map(slug => {
        const form = FORM_CONFIG[slug];
        return `
            <div class="siniestro-option-card" onclick="seleccionarTipoSiniestro('${slug}')" style="border-left: 4px solid ${form.color}">
                <div class="icon-circle" style="background: ${form.color}20; color: ${form.color}">
                    <i class="fas ${form.icono}"></i>
                </div>
                <span>${form.titulo}</span>
            </div>
        `;
    }).join('');
    
    grid.innerHTML = html;
}

function seleccionarTipoSiniestro(tipo) {
    if (!FORM_CONFIG[tipo]) {
        alert('Error: Tipo de formulario no encontrado');
        return;
    }
    
    // Guardar selección
    const sessionData = JSON.parse(sessionStorage.getItem('validacion_siniestro') || '{}');
    sessionData.tipo = tipo;
    sessionStorage.setItem('validacion_siniestro', JSON.stringify(sessionData));
    
    // Renderizar Formulario
    renderDynamicForm(tipo);
    
    // Transición UI
    document.getElementById('step-selection-siniestro').classList.remove('active');
    document.getElementById('step-form-siniestro').classList.add('active');
}

function renderDynamicForm(tipo) {
    const config = FORM_CONFIG[tipo];
    const container = document.getElementById('dynamic-form-container');
    const title = document.getElementById('dynamic-form-title');
    
    // Set Header
    title.innerHTML = `<i class="fas ${config.icono}" style="color: ${config.color}"></i> ${config.titulo}`;
    
    // Build Fields
    // Usamos el array "campos" que viene del backend
    
    let fieldsHTML = '';
    
    if (!config.campos || config.campos.length === 0) {
        fieldsHTML = '<p>Error: Este formulario no tiene campos configurados.</p>';
    } else {
        fieldsHTML = config.campos.map(field => {
            const requiredAttr = field.required ? 'required' : '';
            const minAttr = field.min !== undefined ? `min="${field.min}"` : '';
            const maxAttr = field.max !== undefined ? `max="${field.max}"` : '';
            const placeholder = field.placeholder ? `placeholder="${field.placeholder}"` : '';
            
            let inputHTML = '';
            
            switch (field.type) {
                case 'textarea':
                case 'multilineText':
                    inputHTML = `<textarea id="field-${field.id}" name="${field.id}" rows="4" ${requiredAttr} ${placeholder}></textarea>`;
                    break;
                    
                case 'select':
                case 'singleSelect':
                    const options = (field.options || []).map(opt => `<option value="${opt}">${opt}</option>`).join('');
                    inputHTML = `
                        <select id="field-${field.id}" name="${field.id}" ${requiredAttr}>
                            <option value="" disabled selected>Seleccioná una opción...</option>
                            ${options}
                        </select>
                        <i class="fas fa-chevron-down select-arrow"></i>
                    `;
                    break;
                    
                case 'date':
                    inputHTML = `<input type="date" id="field-${field.id}" name="${field.id}" ${requiredAttr}>`;
                    break;
                    
                case 'time':
                    inputHTML = `<input type="time" id="field-${field.id}" name="${field.id}" ${requiredAttr}>`;
                    break;
                    
                case 'number':
                    inputHTML = `<input type="number" id="field-${field.id}" name="${field.id}" ${minAttr} ${maxAttr} ${requiredAttr} ${placeholder}>`;
                    break;
                case 'checkbox':
                    inputHTML = `
                        <label class="checkbox-container">
                            <input type="checkbox" id="field-${field.id}" name="${field.id}" ${requiredAttr}>
                            <span class="checkmark"></span>
                            ${field.label}
                        </label>
                    `;
                    // Label handleado distinto en checkbox
                    return `<div class="form-group checkbox-group">${inputHTML}</div>`;

                default: // text, singleLineText, email, url, phone, etc.
                    let inputType = 'text';
                    if (field.type === 'email') inputType = 'email';
                    if (field.type === 'phoneNumber') inputType = 'tel';
                    
                    inputHTML = `<input type="${inputType}" id="field-${field.id}" name="${field.id}" ${requiredAttr} ${placeholder}>`;
            }
            
            return `
                <div class="form-group">
                    <label for="field-${field.id}">${field.label} ${field.required ? '*' : ''}</label>
                    ${inputHTML}
                </div>
            `;
        }).join('');
    }
    
    container.innerHTML = fieldsHTML;
}

// Enviar Formulario Final
function submitDynamicForm(e) {
    e.preventDefault();
    
    const btn = document.getElementById('btn-submit-dynamic');
    const originalText = btn.innerHTML;
    
    // 1. Recopilar Datos
    const sessionData = JSON.parse(sessionStorage.getItem('validacion_siniestro') || '{}');
    const tipo = sessionData.tipo;
    const config = FORM_CONFIG[tipo];
    
    if (!config) {
        alert("Error de configuración de formulario.");
        return;
    }

    const formData = {
        tipo_siniestro: tipo,
        cliente: sessionData.cliente,
        poliza: sessionData.poliza,
        datos: {}
    };
    
    // Iterar campos para sacar valores
    let isValid = true;
    config.campos.forEach(field => {
        const el = document.getElementById(`field-${field.id}`);
        if (!el) return;
        
        if (field.type === 'checkbox') {
             formData.datos[field.label] = el.checked ? 'SI' : 'NO';
        } else {
             formData.datos[field.label] = el.value;
             if (field.required && !el.value) isValid = false;
        }
    });

    if (!isValid) {
        alert("Por favor completá todos los campos obligatorios.");
        return;
    }

    // 2. Enviar a Backend
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    btn.disabled = true;
    
    console.log("📤 Enviando Siniestro:", formData);
    
    fetchWithTimeout(BACKEND_CREATE_SINIESTRO, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => {
        console.log("✅ Siniestro Creado:", data);
        alert("¡Denuncia enviada con éxito! Te contactaremos a la brevedad.");
        closeModal('siniestro');
    })
    .catch(err => {
        console.error("❌ Error enviando:", err);
        alert("Hubo un error al enviar la denuncia. Por favor intentá nuevamente o contactanos por WhatsApp.");
    })
    .finally(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    });
}
