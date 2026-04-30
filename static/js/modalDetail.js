function openDetailModal(transactionId) {
  const modalElement = document.getElementById('detailModal');
  const modal = new bootstrap.Modal(modalElement);
  const modalBody = document.getElementById('modalBody');
  
  modalBody.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-secondary" role="status"><span class="visually-hidden">Cargando...</span></div><p class="mt-2 text-secondary">Cargando...</p></div>';
  
  fetch(`/transactions/${transactionId}/detail/`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }
      return response.text();
    })
    .then(html => {
      modalBody.innerHTML = html;
    })
    .catch(error => {
      modalBody.innerHTML = '<div class="alert glass alert-danger">Error al cargar los detalles</div>';
    });
  
  modal.show();
}

function closeModal() {
  const modal = bootstrap.Modal.getInstance(document.getElementById('detailModal'));
  if (modal) {
    modal.hide();
  }
}