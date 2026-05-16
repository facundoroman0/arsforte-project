document.addEventListener('DOMContentLoaded', function() {
  const thresholdInput = document.getElementById('id_threshold');
  const thresholdValue = document.getElementById('threshold-value');
  const thresholdPreview = document.getElementById('threshold-preview');
  
  if (thresholdInput && thresholdValue && thresholdPreview) {
    const initialValue = thresholdInput.value;
    thresholdValue.textContent = initialValue + '%';
    thresholdPreview.textContent = initialValue;
    
    thresholdInput.addEventListener('input', function(e) {
      const value = e.target.value;
      thresholdValue.textContent = value + '%';
      thresholdPreview.textContent = value;
    });
  }
});