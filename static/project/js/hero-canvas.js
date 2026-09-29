/* ==========================================================================
   Yupitek Project Showcase — Hero Canvas Particle System
   Tech: Pure Canvas 2D API · Brand Blue #02A0E9 & Orange #FF7A45
   ========================================================================== */

export function initHeroCanvas(canvas) {
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let animationFrameId;
  let width, height;

  const particles = [];
  const PARTICLE_COUNT = 55;
  const CONNECT_DISTANCE = 140;

  const COLOR_BLUE = 'rgba(2, 160, 233, ';
  const COLOR_ORANGE = 'rgba(255, 122, 69, ';

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  window.addEventListener('resize', resize);
  resize();

  // 粒子建構子
  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.7;
      this.vy = (Math.random() - 0.5) * 0.7;
      this.radius = Math.random() * 2 + 1;
      this.isOrange = Math.random() < 0.25; // 25% 品牌橘，75% 品牌藍
      this.alpha = Math.random() * 0.6 + 0.3;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = (this.isOrange ? COLOR_ORANGE : COLOR_BLUE) + this.alpha + ')';
      ctx.fill();
    }
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < CONNECT_DISTANCE) {
          const alpha = (1 - dist / CONNECT_DISTANCE) * 0.22;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(51, 181, 238, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
  }

  function loop() {
    ctx.clearRect(0, 0, width, height);

    for (let p of particles) {
      p.update();
      p.draw();
    }

    drawConnections();
    animationFrameId = requestAnimationFrame(loop);
  }

  loop();

  return () => {
    cancelAnimationFrame(animationFrameId);
    window.removeEventListener('resize', resize);
  };
}
