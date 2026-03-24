// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
        const headerHeight = document.querySelector('.site-header').offsetHeight;
        const targetPosition = targetElement.offsetTop - headerHeight - 20;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
});

// Add scroll effect to header
window.addEventListener('scroll', function() {
  const header = document.querySelector('.site-header');
  if (window.scrollY > 100) {
    header.style.background = 'rgba(102, 126, 234, 0.95)';
    header.style.backdropFilter = 'blur(10px)';
  } else {
    header.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    header.style.backdropFilter = 'none';
  }
});

// Animate elements on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Observe feature cards and other elements
document.addEventListener('DOMContentLoaded', function() {
  const animateElements = document.querySelectorAll('.feature-card, .stat, .credential-card, .deploy-card');
  
  animateElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
  });
});