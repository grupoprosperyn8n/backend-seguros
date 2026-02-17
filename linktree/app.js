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
        coverageBadges += `<span class="status-badge vida"><i class="fas fa-heart"></i> VIDA</span>`;
    }
    
    // Detectar Auxilio por flag o texto
    if (poliza.auxilio || poliza.estado.includes('AUX')) {
        coverageBadges += `<span class="status-badge aux"><i class="fas fa-tools"></i> AUXILIO</span>`;
    }

    document.getElementById('msg-bienvenida-siniestro').innerHTML = `
        <div class="welcome-card">
            <h3>👋 Hola, ${data.cliente.nombres}</h3>
            <div class="policy-details">
                <p><strong>${poliza.tipo_vehiculo}</strong> | ${poliza.patente}</p>
                <p class="sub-info"><i class="fas fa-shield-alt"></i> Póliza: ${poliza.numero}</p>
                
                <div class="badges-container">
                    <span class="status-badge ${estadoLimpio.includes('VIGENTE') || estadoLimpio.includes('VENCE') ? 'vigente' : ''}">
                        ${estadoLimpio}
                    </span>
                </div>
                
                ${coverageBadges ? `<div class="badges-container coverage-group">${coverageBadges}</div>` : ''}
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
                    class="form-input" accept="image/*" multiple>
                <small style="color: #ccc; display: block; margin-top: 5px;">Podés subir varias fotos</small>
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
    // Nota: formData.entries() puede devolver duplicados para multiples archivos con mismo nombre
    // Pero File objects son instancias de File.
    
    // Estrategia:
    // 1. Campos standard -> directo a payload
    // 2. Archivos -> directo a payload
    // 3. Resto -> al objeto 'datos'
    
    // Para manejar multiples archivos correctamente, no podemos usar Object.fromEntries ciegamente
    
    for (const [key, value] of formData.entries()) {
        if (standardFields.includes(key)) {
            payload.append(key, value);
        } else if (value instanceof File && value.name) {
            // Es un archivo real (si no tiene nombre suele ser input vacio, pero checkear size > 0)
            if (value.size > 0) {
                payload.append(key, value);
            }
        } else {
            // Es un dato del formulario (texto, fecha, etc)
            datos[key] = value;
        }
    }
    
    // Adjuntar JSON de datos
    payload.append('datos', JSON.stringify(datos));

    try {
        console.log("📨 Enviando payload Multipart...");

        // Fetch NO lleva Content-Type header manualmente cuando es FormData, 
        // el navegador lo pone con el boundary correcto.
        const response = await fetchWithTimeout(BACKEND_CREATE_SINIESTRO, {
            method: 'POST',
            body: payload
        });
        
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Error al enviar formulario');
        }
       
        // ÉXITO
        console.log("✅ Siniestro creado:", data);

        Swal.fire({
            icon: 'success',
            title: '¡Denuncia Recibida!',
            text: 'Hemos recibido los datos y tu número de gestión es #' + (data.id || 'N/A') + '. Un asesor procesará tu denuncia y te contactará a la brevedad.',
            confirmButtonColor: '#4ade80'
        }).then(() => {
            location.reload(); // Reiniciar flujo
        });

    } catch (error) {
        console.error("❌ Error envio siniestro:", error);
        Swal.fire('Error', `No pudimos enviar la denuncia: ${error.message || 'Error de conexión'}`, 'error');
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
