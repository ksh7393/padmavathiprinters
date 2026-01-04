document.addEventListener('DOMContentLoaded', async () => {
  // Load manifest
  const resp = await fetch('data/cards.json');
  const cards = await resp.json();
  const container = document.getElementById('cards-list');

  // Create a lightbox modal container (one shared modal)
  const modal = createLightboxModal();
  document.body.appendChild(modal);

  cards.forEach((card, idx) => {
    const col = document.createElement('div');
    col.className = 'col-12 col-md-6 col-lg-4';

    const cardEl = document.createElement('div');
    cardEl.className = 'card h-100';

    const carouselId = `carousel-${idx}`;

    // Build carousel inner with lazy-loading, alt text and click handlers to open lightbox
    const carouselInner = card.images.map((img, i) => `
      <div class="carousel-item ${i===0? 'active':''}">
        <img loading="lazy" src="assets/images/cards/${card.folder}/${img}" class="d-block w-100 card-sample-image" alt="${escapeHtml(card.title)} image ${i+1}" data-card="${idx}" data-index="${i}">
      </div>
    `).join('');

    cardEl.innerHTML = `
      <div id="${carouselId}" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          ${carouselInner}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#${carouselId}" data-bs-slide="prev" aria-label="Previous image">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#${carouselId}" data-bs-slide="next" aria-label="Next image">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
      <div class="card-body">
        <h5 class="card-title">${escapeHtml(card.title)}</h5>
        <p class="card-text">${escapeHtml(card.description || '')}</p>
      </div>
    `;

    col.appendChild(cardEl);
    container.appendChild(col);
  });

  // Attach click handler for all images (delegation)
  container.addEventListener('click', (e) => {
    const img = e.target.closest('.card-sample-image');
    if (!img) return;
    const cardIndex = parseInt(img.dataset.card, 10);
    const imgIndex = parseInt(img.dataset.index, 10);
    openLightbox(cards, cardIndex, imgIndex);
  });

  // Helpers
  function escapeHtml(s){
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function createLightboxModal(){
    const div = document.createElement('div');
    div.className = 'modal fade';
    div.id = 'imageLightbox';
    div.tabIndex = -1;
    div.setAttribute('aria-hidden','true');
    div.innerHTML = `
      <div class="modal-dialog modal-fullscreen modal-dialog-centered">
        <div class="modal-content bg-transparent border-0">
          <div class="modal-body d-flex align-items-center justify-content-center position-relative">
            <button type="button" class="btn-close position-absolute top-0 end-0 m-3 text-white" data-bs-dismiss="modal" aria-label="Close"></button>
            <button class="lightbox-prev btn btn-link text-white position-absolute start-0 top-50 translate-middle-y ms-2" aria-label="Previous image">&larr;</button>
            <img src="" alt="" class="lightbox-image img-fluid rounded shadow" style="max-height:90vh; max-width:90vw;">
            <button class="lightbox-next btn btn-link text-white position-absolute end-0 top-50 translate-middle-y me-2" aria-label="Next image">&rarr;</button>
          </div>
        </div>
      </div>
    `;

    // Keyboard navigation
    div.addEventListener('keydown', (ev) => {
      if (ev.key === 'ArrowRight') div.querySelector('.lightbox-next').click();
      if (ev.key === 'ArrowLeft') div.querySelector('.lightbox-prev').click();
      if (ev.key === 'Escape') {
        const bs = bootstrap.Modal.getInstance(div);
        if (bs) bs.hide();
      }
    });

    // Prev/Next handlers will be wired when opened
    return div;
  }

  function openLightbox(cards, cardIndex, imgIndex){
    const modalEl = document.getElementById('imageLightbox');
    const imgEl = modalEl.querySelector('.lightbox-image');
    const prevBtn = modalEl.querySelector('.lightbox-prev');
    const nextBtn = modalEl.querySelector('.lightbox-next');

    function show(){
      const card = cards[cardIndex];
      const fname = card.images[imgIndex];
      imgEl.src = `assets/images/cards/${card.folder}/${fname}`;
      imgEl.alt = `${card.title} image ${imgIndex+1}`;
    }

    prevBtn.onclick = () => {
      imgIndex = (imgIndex - 1 + cards[cardIndex].images.length) % cards[cardIndex].images.length;
      show();
    };
    nextBtn.onclick = () => {
      imgIndex = (imgIndex + 1) % cards[cardIndex].images.length;
      show();
    };

    show();

    const bs = new bootstrap.Modal(modalEl, {keyboard:true});
    bs.show();
    // focus for keyboard handling
    modalEl.focus();
  }
});

