/* ==========================================================================
   Yupitek Project Showcase — Interactive Media Player & Gallery Engine
   Features: Dual Video/Gallery Switcher, Thumbnail Filmstrip, 
             Inline Video Player, Multi-Media Cinema Lightbox Modal
   ========================================================================== */

export function initMediaPlayer() {
  const cards = document.querySelectorAll('.project-card');
  const lightbox = document.getElementById('lightbox');
  const lightboxContent = document.getElementById('lightbox-content');
  const lightboxClose = document.getElementById('lightbox-close');

  // 全域 Lightbox 狀態
  let currentProjectMedia = [];
  let currentMediaIndex = 0;

  cards.forEach(card => {
    const cardId = card.id;
    const projectTitle = card.querySelector('.project-card__title')?.textContent?.trim() || '專案展示';

    // 收集該專案的所有媒體資源清單
    const videoContainer = card.querySelector('.video-container');
    const videoSrc = videoContainer?.getAttribute('data-video-src');
    const thumbBtns = card.querySelectorAll('.thumb-btn');

    const mediaList = [];
    if (videoSrc) {
      mediaList.push({
        type: 'video',
        src: videoSrc,
        title: `${projectTitle} — 展示影片`
      });
    }

    thumbBtns.forEach((thumb, idx) => {
      const imgSrc = thumb.getAttribute('data-img-src');
      if (imgSrc) {
        mediaList.push({
          type: 'image',
          src: imgSrc,
          title: `${projectTitle} — 實景相片 ${idx + 1}`
        });
      }
    });

    // 1. Tab 切換 (展示影片 vs 現場相簿)
    const tabs = card.querySelectorAll('.media-tab');
    const panels = card.querySelectorAll('.media-panel');

    tabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        e.preventDefault();
        const targetTab = tab.getAttribute('data-tab');

        tabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        panels.forEach(panel => {
          if (panel.classList.contains(`media-panel--${targetTab}`)) {
            panel.classList.add('active');
          } else {
            panel.classList.remove('active');
            // 若切換離開影片面板，暫停正在播放的行內影片
            const playingVideo = panel.querySelector('video');
            if (playingVideo && !playingVideo.paused) {
              playingVideo.pause();
            }
          }
        });
      });
    });

    // 2. 縮圖相簿點擊切換主圖
    const mainImg = card.querySelector('.gallery-active-img');
    thumbBtns.forEach((thumb, index) => {
      thumb.addEventListener('click', (e) => {
        e.preventDefault();
        thumbBtns.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');

        const newSrc = thumb.getAttribute('data-img-src');
        if (mainImg && newSrc) {
          mainImg.style.opacity = '0.3';
          mainImg.src = newSrc;
          mainImg.setAttribute('data-active-index', index);
          mainImg.onload = () => {
            mainImg.style.opacity = '1';
          };
        }
      });
    });

    // 3. 行內影片播放控制 (點擊播放按鈕或海報直接行內播放)
    if (videoContainer) {
      videoContainer.addEventListener('click', (e) => {
        const existingVideo = videoContainer.querySelector('.inline-video');
        if (!existingVideo) {
          const videoEl = document.createElement('video');
          videoEl.className = 'inline-video';
          videoEl.src = videoSrc;
          videoEl.controls = true;
          videoEl.autoplay = true;
          videoEl.playsInline = true;

          const poster = videoContainer.querySelector('.video-poster');
          const playBtn = videoContainer.querySelector('.video-play-btn');
          if (poster) poster.style.display = 'none';
          if (playBtn) playBtn.style.display = 'none';

          videoContainer.appendChild(videoEl);
          videoEl.play().catch(err => console.log('Autoplay prevented:', err));
        }
      });
    }

    // 4. 影院全螢幕按鈕 (開啟多媒體 Lightbox)
    const cinemaBtn = card.querySelector('.media-cinema-btn');
    if (cinemaBtn) {
      cinemaBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const activeTab = card.querySelector('.media-tab.active')?.getAttribute('data-tab');
        let startIndex = 0;
        if (activeTab === 'gallery') {
          const activeImgIdx = parseInt(mainImg?.getAttribute('data-active-index') || '0', 10);
          startIndex = videoSrc ? activeImgIdx + 1 : activeImgIdx;
        }
        openLightbox(mediaList, startIndex);
      });
    }

    // 5. 點擊相簿主圖直接開啟 Lightbox
    if (mainImg) {
      mainImg.addEventListener('click', () => {
        const activeImgIdx = parseInt(mainImg.getAttribute('data-active-index') || '0', 10);
        const startIndex = videoSrc ? activeImgIdx + 1 : activeImgIdx;
        openLightbox(mediaList, startIndex);
      });
    }
  });

  // ==========================================
  // Lightbox 核心控制器 (支援 Prev / Next / ESC)
  // ==========================================
  function openLightbox(mediaList, index = 0) {
    if (!lightbox || !lightboxContent || !mediaList.length) return;
    currentProjectMedia = mediaList;
    currentMediaIndex = Math.max(0, Math.min(index, mediaList.length - 1));

    renderLightboxContent();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function renderLightboxContent() {
    if (!currentProjectMedia.length) return;
    const item = currentProjectMedia[currentMediaIndex];
    lightboxContent.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'lightbox-media-wrapper';

    // 頂部 HUD 資訊列 (標題與計數器)
    const hudBar = document.createElement('div');
    hudBar.className = 'lightbox-hud';
    hudBar.innerHTML = `
      <div class="lightbox-hud__title">${item.title}</div>
      <div class="lightbox-hud__counter">${currentMediaIndex + 1} / ${currentProjectMedia.length}</div>
    `;
    wrapper.appendChild(hudBar);

    // 主體媒體容器
    const stage = document.createElement('div');
    stage.className = 'lightbox-stage';

    if (item.type === 'video') {
      const vid = document.createElement('video');
      vid.className = 'lightbox-video';
      vid.src = item.src;
      vid.controls = true;
      vid.autoplay = true;
      vid.playsInline = true;
      stage.appendChild(vid);
    } else {
      const img = document.createElement('img');
      img.className = 'lightbox-image';
      img.src = item.src;
      img.alt = item.title;
      stage.appendChild(img);
    }
    wrapper.appendChild(stage);

    // 切換按鈕 (Prev / Next)
    if (currentProjectMedia.length > 1) {
      const prevBtn = document.createElement('button');
      prevBtn.className = 'lightbox-arrow lightbox-arrow--prev';
      prevBtn.innerHTML = '‹';
      prevBtn.setAttribute('aria-label', 'Previous media');
      prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        navigateLightbox(-1);
      });

      const nextBtn = document.createElement('button');
      nextBtn.className = 'lightbox-arrow lightbox-arrow--next';
      nextBtn.innerHTML = '›';
      nextBtn.setAttribute('aria-label', 'Next media');
      nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        navigateLightbox(1);
      });

      wrapper.appendChild(prevBtn);
      wrapper.appendChild(nextBtn);
    }

    lightboxContent.appendChild(wrapper);
  }

  function navigateLightbox(direction) {
    if (!currentProjectMedia.length) return;
    const len = currentProjectMedia.length;
    currentMediaIndex = (currentMediaIndex + direction + len) % len;
    renderLightboxContent();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
    // 停止影片播放
    const vid = lightbox.querySelector('video');
    if (vid) vid.pause();
    setTimeout(() => {
      if (lightboxContent) lightboxContent.innerHTML = '';
      currentProjectMedia = [];
    }, 300);
  }

  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox || e.target.classList.contains('lightbox-media-wrapper')) {
        closeLightbox();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (!lightbox?.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
  });
}
