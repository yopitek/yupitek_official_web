/* ==========================================================================
   Yupitek Project Showcase — Scroll & Interaction Animations
   Tech: GSAP 3.12 + ScrollTrigger
   ========================================================================== */

export function initScrollAnimations() {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    console.warn('[Scroll] GSAP or ScrollTrigger not loaded, falling back to static presentation.');
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // 1. 各專案卡片進場動畫
  const cards = document.querySelectorAll('.project-card');
  cards.forEach((card, index) => {
    gsap.fromTo(card, 
      {
        opacity: 0,
        y: 40
      },
      {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: card,
          start: 'top 85%',
          toggleActions: 'play none none none'
        }
      }
    );

    // 2. 監聽滾動同步更新 Sticky 導航目前焦點
    ScrollTrigger.create({
      trigger: card,
      start: 'top center',
      end: 'bottom center',
      onEnter: () => setActiveNav(card.id),
      onEnterBack: () => setActiveNav(card.id)
    });
  });

  // 3. 點擊導航按鈕平滑滾動定位
  document.querySelectorAll('.project-nav__item').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('href');
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        const navHeight = document.querySelector('.project-nav-wrapper')?.offsetHeight || 60;
        const targetPos = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
        window.scrollTo({
          top: targetPos,
          behavior: 'smooth'
        });
      }
    });
  });
}

function setActiveNav(projectId) {
  if (!projectId) return;
  document.querySelectorAll('.project-nav__item').forEach(item => {
    const isTarget = item.getAttribute('href') === `#${projectId}`;
    item.classList.toggle('active', isTarget);
    if (isTarget) {
      item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  });
}
