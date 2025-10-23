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

    // Rellenar y abrir modal de edicion de producto
    const editButtons = document.querySelectorAll('.btn-edit-product');
    const editModalEl = document.getElementById('editProductModal');
    const editForm = document.getElementById('edit-product-form');
    const editNombre = document.getElementById('edit-nombre');
    const editDisponible = document.getElementById('edit-disponible');

    if (editButtons && editModalEl && editForm && editNombre && editDisponible) {
        editButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-product-id');
                const nombre = btn.getAttribute('data-product-nombre') || '';
                const disponible = (btn.getAttribute('data-product-disponible') === 'true');
                editNombre.value = nombre;
                editDisponible.checked = !!disponible;
                // Fija la accion del formulario hacia el endpoint Flask
                editForm.setAttribute('action', `/products/${id}/update`);

                const modal = new bootstrap.Modal(editModalEl);
                modal.show();
            });
        });
    }
});
