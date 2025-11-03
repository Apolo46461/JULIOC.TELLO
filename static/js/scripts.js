// Funcionalidades JavaScript para CETPRO

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Confirmación para acciones destructivas
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || '¿Está seguro de realizar esta acción?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Formatear números en tiempo real
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.value = 0;
            }
            if (this.hasAttribute('max')) {
                const max = parseInt(this.getAttribute('max'));
                if (parseInt(this.value) > max) {
                    this.value = max;
                }
            }
        });
    });

    // Validación de DNI en tiempo real
    const dniInputs = document.querySelectorAll('input[name*="dni"]');
    dniInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 8) {
                this.value = this.value.slice(0, 8);
            }
        });
    });

    // Validación de teléfono en tiempo real
    const phoneInputs = document.querySelectorAll('input[name*="telefono"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9+\-\s]/g, '');
        });
    });

    // Máscara para fecha de nacimiento
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            const birthDate = new Date(this.value);
            const today = new Date();
            const age = today.getFullYear() - birthDate.getFullYear();

            if (age < 6 || age > 100) {
                alert('La fecha de nacimiento debe corresponder a una edad entre 6 y 100 años.');
                this.value = '';
            }
        });
    });

    // Funcionalidad para mostrar/ocultar contraseña
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                passwordInput.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
    });

    // Búsqueda en tiempo real para tablas
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = document.querySelector(this.getAttribute('data-table'));
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Filtros para cursos
    const levelFilters = document.querySelectorAll('.filter-level');
    levelFilters.forEach(filter => {
        filter.addEventListener('change', function() {
            const selectedLevel = this.value;
            const courseCards = document.querySelectorAll('.course-card');

            courseCards.forEach(card => {
                const cardLevel = card.getAttribute('data-level');
                if (selectedLevel === '' || cardLevel === selectedLevel) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Animación para contadores
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = parseInt(counter.getAttribute('data-duration')) || 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };

        updateCounter();
    });

    // Lazy loading para imágenes
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Funcionalidad para exportar tablas a CSV
    const exportButtons = document.querySelectorAll('.export-csv');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const table = document.querySelector(this.getAttribute('data-table'));
            exportTableToCSV(table, 'datos.csv');
        });
    });

    // Funcionalidad para imprimir contenido específico
    const printButtons = document.querySelectorAll('.print-content');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = document.querySelector(this.getAttribute('data-content'));
            printContent(content);
        });
    });

    // Validación de formularios en tiempo real
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });

    // Funcionalidad para subir archivos con preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const preview = document.querySelector(this.getAttribute('data-preview'));
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Notificaciones push (simuladas)
    if ('Notification' in window) {
        if (Notification.permission === 'granted') {
            showNotification('Bienvenido a CETPRO', 'Sistema de gestión educativa');
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    showNotification('Bienvenido a CETPRO', 'Sistema de gestión educativa');
                }
            });
        }
    }

    // Funcionalidad para el modo oscuro (opcional)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', function() {
            document.body.classList.toggle('dark-mode', this.checked);
            localStorage.setItem('darkMode', this.checked);
        });

        // Cargar preferencia guardada
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        darkModeToggle.checked = savedDarkMode;
        document.body.classList.toggle('dark-mode', savedDarkMode);
    }

    // Funcionalidad para el sidebar móvil
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });

        // Cerrar sidebar al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }

    // Funcionalidad para tabs dinámicos
    const tabButtons = document.querySelectorAll('[data-tab]');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Ocultar todas las pestañas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });

            // Mostrar la pestaña seleccionada
            document.getElementById(targetTab).classList.add('active');

            // Actualizar botones activos
            document.querySelectorAll('[data-tab]').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });

    // Funcionalidad para el chat en vivo (simulado)
    const chatToggle = document.getElementById('chatToggle');
    const chatWindow = document.getElementById('chatWindow');

    if (chatToggle && chatWindow) {
        chatToggle.addEventListener('click', function() {
            chatWindow.classList.toggle('show');
        });
    }

    // Funcionalidad para el calendario
    const calendar = document.getElementById('calendar');
    if (calendar) {
        renderCalendar(new Date());
    }

    // Funcionalidad para gráficos (usando Chart.js si está disponible)
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }

    console.log('CETPRO - Sistema de gestión educativa cargado correctamente');
});

// Funciones auxiliares

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    // Validación específica para emails
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });

    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function exportTableToCSV(table, filename) {
    const csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => cell.textContent.trim());
        csv.push(rowData.join(','));
    });

    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();

    window.URL.revokeObjectURL(url);
}

function printContent(content) {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>Imprimir</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .no-print { display: none; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f5f5f5; }
            </style>
        </head>
        <body>
            ${content.innerHTML}
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

function showNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, {
            body: message,
            icon: '/static/images/logo.png'
        });
    }
}

function renderCalendar(date) {
    const calendar = document.getElementById('calendar');
    if (!calendar) return;

    const year = date.getFullYear();
    const month = date.getMonth();

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    let calendarHTML = `
        <div class="calendar-header">
            <h5>${date.toLocaleString('es', { month: 'long', year: 'numeric' })}</h5>
        </div>
        <div class="calendar-grid">
            <div class="calendar-day">Dom</div>
            <div class="calendar-day">Lun</div>
            <div class="calendar-day">Mar</div>
            <div class="calendar-day">Mié</div>
            <div class="calendar-day">Jue</div>
            <div class="calendar-day">Vie</div>
            <div class="calendar-day">Sáb</div>
    `;

    // Días vacíos antes del primer día del mes
    for (let i = 0; i < startingDayOfWeek; i++) {
        calendarHTML += '<div class="calendar-date empty"></div>';
    }

    // Días del mes
    for (let day = 1; day <= daysInMonth; day++) {
        const currentDate = new Date(year, month, day);
        const isToday = currentDate.toDateString() === new Date().toDateString();
        const dayClass = isToday ? 'calendar-date today' : 'calendar-date';

        calendarHTML += `<div class="${dayClass}">${day}</div>`;
    }

    calendarHTML += '</div>';
    calendar.innerHTML = calendarHTML;
}

function initializeCharts() {
    // Gráfico de estadísticas generales
    const statsChart = document.getElementById('statsChart');
    if (statsChart) {
        new Chart(statsChart, {
            type: 'doughnut',
            data: {
                labels: ['Estudiantes', 'Profesores', 'Cursos', 'Matrículas'],
                datasets: [{
                    data: [
                        parseInt(document.getElementById('totalEstudiantes')?.textContent || '0'),
                        parseInt(document.getElementById('totalProfesores')?.textContent || '0'),
                        parseInt(document.getElementById('totalCursos')?.textContent || '0'),
                        parseInt(document.getElementById('totalMatriculas')?.textContent || '0')
                    ],
                    backgroundColor: [
                        '#007bff',
                        '#28a745',
                        '#ffc107',
                        '#17a2b8'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Gráfico de cursos por nivel
    const coursesChart = document.getElementById('coursesChart');
    if (coursesChart) {
        new Chart(coursesChart, {
            type: 'bar',
            data: {
                labels: ['Primaria', 'Secundaria'],
                datasets: [{
                    label: 'Cursos',
                    data: [
                        parseInt(document.getElementById('cursosPrimaria')?.textContent || '0'),
                        parseInt(document.getElementById('cursosSecundaria')?.textContent || '0')
                    ],
                    backgroundColor: ['#007bff', '#28a745']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
}

// Funcionalidad para el tema oscuro
const darkModeStyles = `
    .dark-mode {
        background-color: #1a1a1a;
        color: #ffffff;
    }

    .dark-mode .card {
        background-color: #2d2d2d;
        color: #ffffff;
        border-color: #404040;
    }

    .dark-mode .table {
        background-color: #2d2d2d;
        color: #ffffff;
    }

    .dark-mode .table thead th {
        background-color: #404040;
        color: #ffffff;
        border-color: #555;
    }

    .dark-mode .table tbody tr:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }

    .dark-mode .form-control {
        background-color: #2d2d2d;
        color: #ffffff;
        border-color: #555;
    }

    .dark-mode .form-control:focus {
        background-color: #2d2d2d;
        color: #ffffff;
        border-color: #007bff;
    }

    .dark-mode .navbar {
        background-color: #2d2d2d !important;
        border-bottom: 1px solid #404040;
    }

    .dark-mode footer {
        background-color: #2d2d2d;
        border-top: 1px solid #404040;
    }
`;

// Agregar estilos del tema oscuro al documento
const styleSheet = document.createElement('style');
styleSheet.textContent = darkModeStyles;
document.head.appendChild(styleSheet);
