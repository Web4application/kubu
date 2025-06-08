// main.js - Kubuverse interaction logic

document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for nav links
  const navLinks = document.querySelectorAll('nav a[href^="#"]');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('href').substring(1);
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Placeholder for future AI/blockchain dynamic scripts
  // Example: Connect wallet button handler, analytics fetch, etc.

  console.log('Kubuverse main.js loaded — ready for AI/blockchain magic 🚀');
});
