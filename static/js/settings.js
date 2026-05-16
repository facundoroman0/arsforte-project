document.addEventListener('DOMContentLoaded', function() {
  const thresholdInput = document.getElementById('id_threshold');
  
  if (thresholdInput) {
    thresholdInput.addEventListener('input', function(e) {
      const value = e.target.value;
      document.getElementById('threshold-value').textContent = value + '%';
      document.getElementById('threshold-preview').textContent = value;
    });
  }
});