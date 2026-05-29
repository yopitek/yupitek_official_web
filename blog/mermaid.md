<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>系統架構圖 · 三大風格</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&family=JetBrains+Mono:wght@400;700&family=Sora:wght@300;600;800&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --gap: 2.5rem;
  }

  body {
    font-family: 'Sora', 'Noto Sans TC', sans-serif;
    background: #0a0a0f;
    color: #e8e8f0;
    min-height: 100vh;
    padding: 3rem 1.5rem 5rem;
  }

  /* ── HEADER ── */
  .header {
    text-align: center;
    margin-bottom: 4rem;
    position: relative;
  }
  .header::after {
    content: '';
    display: block;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #7c5cbf, #3ecfcf);
    margin: 1.2rem auto 0;
    border-radius: 2px;
  }
  .header h1 {
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(120deg, #b8a0ff 0%, #3ecfcf 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .header p {
    margin-top: .6rem;
    font-size: .9rem;
    color: #888;
    font-weight: 300;
    letter-spacing: .06em;
  }

  /* ── TABS ── */
  .tab-bar {
    display: flex;
    justify-content: center;
    gap: .5rem;
    margin-bottom: 2.5rem;
    flex-wrap: wrap;
  }
  .tab-btn {
    padding: .45rem 1.4rem;
    border-radius: 99px;
    border: 1px solid #2a2a3a;
    background: transparent;
    color: #888;
    font-family: inherit;
    font-size: .82rem;
    font-weight: 600;
    letter-spacing: .04em;
    cursor: pointer;
    transition: all .25s;
  }
  .tab-btn:hover { border-color: #555; color: #ccc; }
  .tab-btn.active { color: #fff; border-color: transparent; }
  .tab-btn[data-style="cyber"].active  { background: linear-gradient(135deg,#7c3aed,#0ea5e9); }
  .tab-btn[data-style="forest"].active { background: linear-gradient(135deg,#065f46,#10b981); }
  .tab-btn[data-style="neutral"].active{ background: linear-gradient(135deg,#1e3a5f,#60a5fa); }

  /* ── CARDS ── */
  .card {
    display: none;
    max-width: 860px;
    margin: 0 auto var(--gap);
    border-radius: 16px;
    overflow: hidden;
    animation: fadeUp .35s ease both;
  }
  .card.visible { display: block; }

  @keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
  }

  .card-header {
    padding: 1rem 1.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .dot-row { display:flex; gap:6px; }
  .dot { width:12px; height:12px; border-radius:50%; }

  .card-title {
    font-size: .78rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: .1em;
    opacity: .7;
    margin-left: auto;
  }
  .badge {
    font-size: .68rem;
    padding: .22rem .7rem;
    border-radius: 99px;
    font-weight: 700;
    letter-spacing: .07em;
    text-transform: uppercase;
  }

  .card-body {
    padding: 2rem 1.5rem 2.5rem;
  }

  /* scroll container for diagram */
  .diagram-wrap {
    overflow-x: auto;
    border-radius: 10px;
    padding: 1rem;
  }

  /* style-specific overrides via theme init */
  .mermaid svg { display:block; margin:auto; max-width:100%; }

  /* ── STYLE 1 : CYBER PURPLE ── */
  .card-cyber .card-header { background:#120d1e; border-bottom:1px solid #2d1f4e; }
  .card-cyber .dot:nth-child(1){background:#ff5f56;}
  .card-cyber .dot:nth-child(2){background:#ffbd2e;}
  .card-cyber .dot:nth-child(3){background:#27c93f;}
  .card-cyber .badge { background:#2d1f4e; color:#b8a0ff; }
  .card-cyber { border:1px solid #2d1f4e; background:#0e0818; box-shadow:0 0 60px #7c3aed22; }
  .card-cyber .card-body { background:#0e0818; }
  .card-cyber .diagram-wrap { background:#140e24; }

  /* ── STYLE 2 : FOREST GREEN ── */
  .card-forest .card-header { background:#052e1a; border-bottom:1px solid #064e2e; }
  .card-forest .dot:nth-child(1){background:#ff5f56;}
  .card-forest .dot:nth-child(2){background:#ffbd2e;}
  .card-forest .dot:nth-child(3){background:#27c93f;}
  .card-forest .badge { background:#064e2e; color:#34d399; }
  .card-forest { border:1px solid #064e2e; background:#041a0e; box-shadow:0 0 60px #10b98122; }
  .card-forest .card-body { background:#041a0e; }
  .card-forest .diagram-wrap { background:#052914; }

  /* ── STYLE 3 : NEUTRAL BLUEPRINT ── */
  .card-neutral .card-header { background:#0c1929; border-bottom:1px solid #1e3a5f; }
  .card-neutral .dot:nth-child(1){background:#ff5f56;}
  .card-neutral .dot:nth-child(2){background:#ffbd2e;}
  .card-neutral .dot:nth-child(3){background:#27c93f;}
  .card-neutral .badge { background:#1e3a5f; color:#93c5fd; }
  .card-neutral { border:1px solid #1e3a5f; background:#080f1a; box-shadow:0 0 60px #1d4ed822; }
  .card-neutral .card-body { background:#080f1a; }
  .card-neutral .diagram-wrap { background:#0d1928; }

  /* ── DESCRIPTION ── */
  .desc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(160px,1fr));
    gap: .8rem;
    margin-top: 1.6rem;
  }
  .desc-item {
    border-radius: 10px;
    padding: .9rem 1rem;
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.06);
  }
  .desc-item h4 { font-size: .72rem; letter-spacing:.08em; text-transform:uppercase; margin-bottom:.3rem; opacity:.5; }
  .desc-item p  { font-size: .82rem; line-height: 1.5; }

  /* ── CODE BLOCK ── */
  details { margin-top:1.2rem; }
  summary {
    cursor:pointer;
    font-size:.76rem;
    font-family:'JetBrains Mono',monospace;
    color:#666;
    letter-spacing:.07em;
    user-select:none;
    transition:color .2s;
  }
  summary:hover { color:#aaa; }
  pre {
    margin-top:.8rem;
    padding:1.1rem;
    border-radius:10px;
    background:#0a0a12;
    border:1px solid #1a1a28;
    font-family:'JetBrains Mono',monospace;
    font-size:.73rem;
    color:#a0a0c0;
    overflow-x:auto;
    line-height:1.7;
  }
  .k{color:#b8a0ff;} .s{color:#3ecfcf;} .c{color:#556;}
</style>
</head>
<body>

<header class="header">
  <h1>Mermaid 架構圖 · 三大風格</h1>
  <p>DGX Spark GB10 系統架構 · 選擇最適合你的視覺語言</p>
</header>

<nav class="tab-bar">
  <button class="tab-btn active" data-style="cyber">① Cyber Purple</button>
  <button class="tab-btn" data-style="forest">② Forest Green</button>
  <button class="tab-btn" data-style="neutral">③ Blueprint Navy</button>
</nav>

<!-- ══════ CARD 1 : CYBER PURPLE ══════ -->
<div class="card card-cyber visible" id="card-cyber">
  <div class="card-header">
    <div class="dot-row"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    <span class="badge">Cyber Purple</span>
    <span class="card-title">theme: dark · purple accent</span>
  </div>
  <div class="card-body">
    <div class="diagram-wrap">
      <div class="mermaid" id="cyber-diagram">%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#2d1f4e","primaryTextColor":"#e2d9f3","primaryBorderColor":"#7c3aed","lineColor":"#9d6dff","secondaryColor":"#1a1030","tertiaryColor":"#0e0818","background":"#0e0818","mainBkg":"#1e1040","nodeBorder":"#7c3aed","clusterBkg":"#150d2a","titleColor":"#c4b5fd","edgeLabelBackground":"#1a1030","attributeBackgroundColorEven":"#1e1040","attributeBackgroundColorOdd":"#150d2a"}}}%%
flowchart TD
    subgraph 網路[" 🌐 網路層 "]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>模型訓練 · 大量資料傳輸"]
        B["📡 ALFA AWUS036ACM<br/>SSH 管理 · Jupyter · 系統更新"]
    end
    C["🖥️ DGX Spark / GB10<br/>ARM64 ｜ 128GB ｜ 20 核 CPU"]
    subgraph 場景[" 🎯 應用場景 "]
        D["🤖 AI 開發者<br/>推論 + SSH 雙線並行"]
        E["🔐 資安實驗室<br/>LLM 訓練 + 滲透測試"]
        F["🚀 邊緣部署<br/>生產網路 + 管理隔離"]
    end
    A -->|高速資料| C
    B -->|管理連線| C
    C --> D
    C --> E
    C --> F</div>
    </div>
    <div class="desc-grid">
      <div class="desc-item"><h4>風格</h4><p>暗黑賽博龐克，紫色高亮</p></div>
      <div class="desc-item"><h4>適合場景</h4><p>資安展示、技術 Demo、駭客文化</p></div>
      <div class="desc-item"><h4>GitHub 熱度</h4><p>⭐ 最受技術社群歡迎</p></div>
      <div class="desc-item"><h4>閱讀體驗</h4><p>高對比，視覺張力強</p></div>
    </div>
    <details>
      <summary>▶ 查看 init 主題設定</summary>
      <pre><span class="c">%%{init:{</span>
  <span class="k">"theme"</span>:<span class="s">"dark"</span>,
  <span class="k">"themeVariables"</span>:{
    <span class="k">"primaryColor"</span>:     <span class="s">"#2d1f4e"</span>,
    <span class="k">"primaryTextColor"</span>:  <span class="s">"#e2d9f3"</span>,
    <span class="k">"primaryBorderColor"</span>:<span class="s">"#7c3aed"</span>,
    <span class="k">"lineColor"</span>:         <span class="s">"#9d6dff"</span>,
    <span class="k">"secondaryColor"</span>:    <span class="s">"#1a1030"</span>,
    <span class="k">"clusterBkg"</span>:        <span class="s">"#150d2a"</span>,
    <span class="k">"titleColor"</span>:        <span class="s">"#c4b5fd"</span>
  }
<span class="c">}}%%</span></pre>
    </details>
  </div>
</div>

<!-- ══════ CARD 2 : FOREST GREEN ══════ -->
<div class="card card-forest" id="card-forest">
  <div class="card-header">
    <div class="dot-row"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    <span class="badge">Forest Green</span>
    <span class="card-title">theme: dark · emerald accent</span>
  </div>
  <div class="card-body">
    <div class="diagram-wrap">
      <div class="mermaid" id="forest-diagram">%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#064e2e","primaryTextColor":"#d1fae5","primaryBorderColor":"#10b981","lineColor":"#34d399","secondaryColor":"#052e1a","tertiaryColor":"#041a0e","background":"#041a0e","mainBkg":"#063b22","nodeBorder":"#059669","clusterBkg":"#042717","titleColor":"#6ee7b7","edgeLabelBackground":"#052e1a"}}}%%
flowchart TD
    subgraph 網路[" 🌐 網路層 "]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>模型訓練 · 大量資料傳輸"]
        B["📡 ALFA AWUS036ACM<br/>SSH 管理 · Jupyter · 系統更新"]
    end
    C["🖥️ DGX Spark / GB10<br/>ARM64 ｜ 128GB ｜ 20 核 CPU"]
    subgraph 場景[" 🎯 應用場景 "]
        D["🤖 AI 開發者<br/>推論 + SSH 雙線並行"]
        E["🔐 資安實驗室<br/>LLM 訓練 + 滲透測試"]
        F["🚀 邊緣部署<br/>生產網路 + 管理隔離"]
    end
    A -->|高速資料| C
    B -->|管理連線| C
    C --> D
    C --> E
    C --> F</div>
    </div>
    <div class="desc-grid">
      <div class="desc-item"><h4>風格</h4><p>森林翠綠，自然科技感</p></div>
      <div class="desc-item"><h4>適合場景</h4><p>開源文件、DevOps、基礎設施</p></div>
      <div class="desc-item"><h4>GitHub 熱度</h4><p>⭐ 開源社群首選</p></div>
      <div class="desc-item"><h4>閱讀體驗</h4><p>舒適護眼，長時間閱讀</p></div>
    </div>
    <details>
      <summary>▶ 查看 init 主題設定</summary>
      <pre><span class="c">%%{init:{</span>
  <span class="k">"theme"</span>:<span class="s">"dark"</span>,
  <span class="k">"themeVariables"</span>:{
    <span class="k">"primaryColor"</span>:     <span class="s">"#064e2e"</span>,
    <span class="k">"primaryTextColor"</span>:  <span class="s">"#d1fae5"</span>,
    <span class="k">"primaryBorderColor"</span>:<span class="s">"#10b981"</span>,
    <span class="k">"lineColor"</span>:         <span class="s">"#34d399"</span>,
    <span class="k">"clusterBkg"</span>:        <span class="s">"#042717"</span>,
    <span class="k">"titleColor"</span>:        <span class="s">"#6ee7b7"</span>
  }
<span class="c">}}%%</span></pre>
    </details>
  </div>
</div>

<!-- ══════ CARD 3 : BLUEPRINT NAVY ══════ -->
<div class="card card-neutral" id="card-neutral">
  <div class="card-header">
    <div class="dot-row"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
    <span class="badge">Blueprint Navy</span>
    <span class="card-title">theme: dark · steel blue accent</span>
  </div>
  <div class="card-body">
    <div class="diagram-wrap">
      <div class="mermaid" id="neutral-diagram">%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#1e3a5f","primaryTextColor":"#dbeafe","primaryBorderColor":"#3b82f6","lineColor":"#60a5fa","secondaryColor":"#0f2342","tertiaryColor":"#080f1a","background":"#080f1a","mainBkg":"#162d4e","nodeBorder":"#2563eb","clusterBkg":"#0d1f38","titleColor":"#93c5fd","edgeLabelBackground":"#0f2342"}}}%%
flowchart TD
    subgraph 網路[" 🌐 網路層 "]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>模型訓練 · 大量資料傳輸"]
        B["📡 ALFA AWUS036ACM<br/>SSH 管理 · Jupyter · 系統更新"]
    end
    C["🖥️ DGX Spark / GB10<br/>ARM64 ｜ 128GB ｜ 20 核 CPU"]
    subgraph 場景[" 🎯 應用場景 "]
        D["🤖 AI 開發者<br/>推論 + SSH 雙線並行"]
        E["🔐 資安實驗室<br/>LLM 訓練 + 滲透測試"]
        F["🚀 邊緣部署<br/>生產網路 + 管理隔離"]
    end
    A -->|高速資料| C
    B -->|管理連線| C
    C --> D
    C --> E
    C --> F</div>
    </div>
    <div class="desc-grid">
      <div class="desc-item"><h4>風格</h4><p>藍圖工程感，專業沉穩</p></div>
      <div class="desc-item"><h4>適合場景</h4><p>企業報告、架構文件、簡報</p></div>
      <div class="desc-item"><h4>GitHub 熱度</h4><p>⭐ 企業文件標準選擇</p></div>
      <div class="desc-item"><h4>閱讀體驗</h4><p>清晰專業，信任感強</p></div>
    </div>
    <details>
      <summary>▶ 查看 init 主題設定</summary>
      <pre><span class="c">%%{init:{</span>
  <span class="k">"theme"</span>:<span class="s">"dark"</span>,
  <span class="k">"themeVariables"</span>:{
    <span class="k">"primaryColor"</span>:     <span class="s">"#1e3a5f"</span>,
    <span class="k">"primaryTextColor"</span>:  <span class="s">"#dbeafe"</span>,
    <span class="k">"primaryBorderColor"</span>:<span class="s">"#3b82f6"</span>,
    <span class="k">"lineColor"</span>:         <span class="s">"#60a5fa"</span>,
    <span class="k">"clusterBkg"</span>:        <span class="s">"#0d1f38"</span>,
    <span class="k">"titleColor"</span>:        <span class="s">"#93c5fd"</span>
  }
<span class="c">}}%%</span></pre>
    </details>
  </div>
</div>

<script>
  // ── Mermaid init ──
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',
    fontFamily: "'Noto Sans TC', sans-serif",
  });

  const diagrams = ['cyber-diagram','forest-diagram','neutral-diagram'];
  async function renderAll() {
    for (const id of diagrams) {
      const el = document.getElementById(id);
      if (!el) continue;
      const code = el.textContent.trim();
      const { svg } = await mermaid.render('svg-' + id, code);
      el.innerHTML = svg;
    }
  }
  renderAll();

  // ── Tabs ──
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      const style = btn.dataset.style;
      tabs.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      document.querySelectorAll('.card').forEach(c => {
        c.classList.remove('visible');
        c.style.display = 'none';
      });
      const target = document.getElementById('card-' + style);
      if (target) {
        target.style.display = 'block';
        // re-trigger animation
        void target.offsetWidth;
        target.classList.add('visible');
      }
    });
  });
</script>
</body>
</html>
