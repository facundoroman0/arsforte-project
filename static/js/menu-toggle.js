document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.menu-toggle-btn');
  const navbarCollapse = document.getElementById('navbarNav');
  
  if (menuToggle) {
    const hamburger = menuToggle.querySelector('.icon-hamburger');
    const close = menuToggle.querySelector('.icon-close');

    menuToggle.addEventListener('click', function() {
      this.classList.toggle('collapsed');
      
      const isCollapsed = this.classList.contains('collapsed');
      hamburger.style.display = isCollapsed ? 'none' : 'block';
      close.style.display = isCollapsed ? 'block' : 'none';
    });

    const navLinks = navbarCollapse.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        menuToggle.classList.remove('collapsed');
        hamburger.style.display = 'block';
        close.style.display = 'none';
        
        const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
          toggle: false
        });
        bsCollapse.hide();
      });
    });
  }
});