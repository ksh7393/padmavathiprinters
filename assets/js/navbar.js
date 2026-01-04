document.addEventListener('DOMContentLoaded', () => {
  const label = document.getElementById('nav-current-label');
  const links = document.querySelectorAll('.offcanvas-body .nav-link, .navbar-nav .nav-link');

  function setLabel(text){
    if (label) label.textContent = text || '';
  }

  // Initialize from current path (resolve hrefs to absolute paths and match)
  const path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  let active = null;
  Array.from(links).forEach(a => {
    try {
      const resolved = new URL(a.getAttribute('href'), location.href).pathname.split('/').pop().toLowerCase();
      if (resolved === path) active = a;
    } catch (e) {
      // ignore malformed href
    }
  });
  if (!active) active = Array.from(links).find(a => a.classList.contains('active')) || null;
  if (active) setLabel(active.textContent.trim());
  else {
    const parts = document.title.split(' - ');
    setLabel(parts[0] || document.title);
  }

  links.forEach(a => {
    a.addEventListener('click', (e) => {
      // set label immediately (navigation may follow)
      setLabel(a.textContent.trim());
    });
  });

  // Update label on history navigation (back/forward)
  window.addEventListener('popstate', () => {
    const p = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    const found = Array.from(links).find(a => {
      try { return new URL(a.getAttribute('href'), location.href).pathname.split('/').pop().toLowerCase() === p; }
      catch (e) { return false; }
    });
    if (found) setLabel(found.textContent.trim());
  });
});
