/* ==========================================================================
   Yupitek Project Showcase — Core Application Entry Point
   ========================================================================== */

import { initHeroCanvas } from './hero-canvas.js';
import { initI18n } from './i18n.js';
import { initScrollAnimations } from './project-scroll.js';

document.addEventListener('DOMContentLoaded', async () => {
  // 1. 初始化多語系引擎
  await initI18n();

  // 2. 初始化 Hero Canvas 科技粒子系統
  const heroCanvas = document.getElementById('hero-canvas');
  if (heroCanvas) {
    initHeroCanvas(heroCanvas);
  }

  // 3. 初始化 GSAP 滾動動畫與導航聯動
  initScrollAnimations();

  // 4. 初始化 Lightbox 多媒體展示彈窗
  initLightbox();
});

function initLightbox() {
  const lightbox = document.getElementById('lightbox');
  const lightboxContent = document.getElementById('lightbox-content');
  const closeBtn = document.getElementById('lightbox-close');

  if (!lightbox || !lightboxContent) return;

  function openMedia(type, src) {
    lightboxContent.innerHTML = '';
    if (type === 'video') {
      const vid = document.createElement('video');
      vid.src = src;
      vid.controls = true;
      vid.autoplay = true;
      vid.playsInline = true;
      lightboxContent.appendChild(vid);
    } else {
      const img = document.createElement('img');
      img.src = src;
      img.alt = 'Enlarged project media';
      lightboxContent.appendChild(img);
    }
    lightbox.classList.add('open');
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    setTimeout(() => {
      lightboxContent.innerHTML = '';
    }, 300);
  }

  document.querySelectorAll('[data-lightbox]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const type = el.getAttribute('data-media-type') || 'image';
      const src = el.getAttribute('data-lightbox-src');
      if (src) {
        openMedia(type, src);
      }
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeLightbox);
  }

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox.classList.contains('open')) {
      closeLightbox();
    }
  });
}
