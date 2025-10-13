// JavaScript para funcionalidades adicionales
document.addEventListener('DOMContentLoaded', function() {
    // Ejemplo: Cargar productos via AJAX
    const loadProducts = async () => {
        try {
            const response = await fetch('/api/products');
            const products = await response.json();
            console.log('Productos cargados:', products);
        } catch (error) {
            console.error('Error cargando productos:', error);
        }
    };

    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});