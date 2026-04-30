document.addEventListener('DOMContentLoaded', function() {
  const currencyBtns = document.querySelectorAll('.currency-btn');
  const arsValues = document.querySelectorAll('.ars-value');
  const usdValues = document.querySelectorAll('.usd-value');
  
  function setCurrency(currency) {
    if (currency === 'usd') {
      arsValues.forEach(el => el.classList.add('d-none'));
      usdValues.forEach(el => el.classList.remove('d-none'));
      currencyBtns.forEach(btn => {
        if (btn.dataset.currency === 'usd') {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    } else {
      arsValues.forEach(el => el.classList.remove('d-none'));
      usdValues.forEach(el => el.classList.add('d-none'));
      currencyBtns.forEach(btn => {
        if (btn.dataset.currency === 'ars') {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    }
  }
  
  currencyBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      setCurrency(this.dataset.currency);
    });
  });
  
  setCurrency('ars');
});