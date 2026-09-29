/* ==========================================================================
   Yupitek Project Showcase — Core Application Entry Point
   ========================================================================== */

import { initHeroCanvas } from './hero-canvas.js';
import { initI18n } from './i18n.js';
import { initScrollAnimations } from './project-scroll.js';
import { initMediaPlayer } from './media-player.js';

async function bootstrap() {
  // 1. 初始化多語系引擎
  await initI18n();

  // 2. 初始化 Hero Canvas 科技粒子系統
  const heroCanvas = document.getElementById('hero-canvas');
  if (heroCanvas) {
    initHeroCanvas(heroCanvas);
  }

  // 3. 初始化 GSAP 滾動動畫與導航聯動
  initScrollAnimations();

  // 4. 初始化互動多媒體播放器與畫廊引擎 (含 Lightbox)
  initMediaPlayer();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrap);
} else {
  bootstrap();
}
