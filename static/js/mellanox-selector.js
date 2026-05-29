(function() {
  // NIC Database
  const nics = [
    // 10G
    {
      part: "MCX4121A-XCAT",
      generation: "ConnectX-4 Lx",
      ports: 2,
      speed: "10G",
      pcie: "PCIe 3.0 x8",
      pcieGen: 3,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "RoCEv2, VXLAN, NVGRE offloads",
      href: "/en/products/mellanox/nic/"
    },
    // 25G
    {
      part: "MCX4121A-ACAT",
      generation: "ConnectX-4 Lx",
      ports: 2,
      speed: "25G",
      pcie: "PCIe 3.0 x8",
      pcieGen: 3,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Standard 25G adapter, RoCE, SR-IOV",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX4121A-ACUT",
      generation: "ConnectX-4 Lx",
      ports: 2,
      speed: "25G",
      pcie: "PCIe 3.0 x8",
      pcieGen: 3,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "UEFI Enabled standard 25G card",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX512A-ACAT",
      generation: "ConnectX-5",
      ports: 2,
      speed: "25G",
      pcie: "PCIe 3.0 x8",
      pcieGen: 3,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Enhanced RoCEv2, NVMe-oF acceleration",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX512A-ACUT",
      generation: "ConnectX-5",
      ports: 2,
      speed: "25G",
      pcie: "PCIe 3.0 x8",
      pcieGen: 3,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "UEFI (x86/ARM) support, low latency",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX631102AN-ADAT",
      generation: "ConnectX-6 Lx",
      ports: 2,
      speed: "25G",
      pcie: "PCIe 4.0 x8",
      pcieGen: 4,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Secure Boot, hardware root of trust, No Crypto",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX623432AS-ADAB",
      generation: "ConnectX-6 Lx OCP",
      ports: 2,
      speed: "25G",
      pcie: "PCIe 4.0 x8",
      pcieGen: 4,
      connector: "SFP28",
      protocol: "EN",
      formFactor: "OCP 3.0",
      bracket: "Thumbscrew",
      features: "OCP 3.0 interface, Host management, Secure Boot",
      href: "/en/products/mellanox/nic/"
    },
    // 50G
    {
      part: "MCX515A-GCAT",
      generation: "ConnectX-5",
      ports: 1,
      speed: "50G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Single port 50GbE, storage offload, RoCE",
      href: "/en/products/mellanox/nic/"
    },
    // 100G
    {
      part: "MCX515A-CCAT",
      generation: "ConnectX-5",
      ports: 1,
      speed: "100G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Single port 100G Ethernet adapter, RoCE",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX555A-ECAT",
      generation: "ConnectX-5 VPI",
      ports: 1,
      speed: "100G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Single port EDR InfiniBand and 100GbE VPI",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX516A-CCAT",
      generation: "ConnectX-5",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Dual port 100G Ethernet, high throughput",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX516A-CDAT",
      generation: "ConnectX-5 Ex",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP28",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "PCIe 4.0 dual-port 100G Ethernet adapter",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX556A-ECAT",
      generation: "ConnectX-5 VPI",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Dual port EDR InfiniBand and 100GbE VPI",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX556A-EDAT",
      generation: "ConnectX-5 Ex VPI",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP28",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "PCIe 4.0 VPI card, EDR IB & 100GbE",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX653105A-ECAT",
      generation: "ConnectX-6 VPI",
      ports: 1,
      speed: "100G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Single port HDR100 IB (100Gb/s) & 100GbE VPI",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX653106A-ECAT",
      generation: "ConnectX-6 VPI",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 3.0 x16",
      pcieGen: 3,
      connector: "QSFP28",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Dual port HDR100 IB (100Gb/s) & 100GbE VPI",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX623106AN-CDAT",
      generation: "ConnectX-6 Dx",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP56",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Dual port QSFP56 100G, advanced virtualization, No Crypto",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX623436AN-CDAB",
      generation: "ConnectX-6 Dx OCP",
      ports: 2,
      speed: "100G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP56",
      protocol: "EN",
      formFactor: "OCP 3.0",
      bracket: "Thumbscrew",
      features: "OCP 3.0 interface, dual port 100GbE, No Crypto",
      href: "/en/products/mellanox/nic/"
    },
    // 200G
    {
      part: "MCX653105A-HDAT",
      generation: "ConnectX-6 VPI",
      ports: 1,
      speed: "200G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP56",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Single port HDR IB (200Gb/s) and 200GbE VPI",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX653106A-HDAT",
      generation: "ConnectX-6 VPI",
      ports: 2,
      speed: "200G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP56",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Dual port HDR IB (200Gb/s) and 200GbE VPI",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX623105A-VDAT",
      generation: "ConnectX-6 Dx",
      ports: 1,
      speed: "200G",
      pcie: "PCIe 4.0 x16",
      pcieGen: 4,
      connector: "QSFP56",
      protocol: "EN",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Single port 200GbE, high density virtualization",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX75310AAS-HEAT",
      generation: "ConnectX-7",
      ports: 1,
      speed: "200G",
      pcie: "PCIe 5.0 x16",
      pcieGen: 5,
      connector: "OSFP",
      protocol: "IB",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "NDR200 IB OSFP, Socket Direct ready, Secure Boot",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX755106AS-HEAT",
      generation: "ConnectX-7 VPI",
      ports: 2,
      speed: "200G",
      pcie: "PCIe 5.0 x16",
      pcieGen: 5,
      connector: "QSFP112",
      protocol: "VPI",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "Dual port 200G NDR200/HDR VPI (1 IB, 1 VPI port)",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX753436MS-HEAB",
      generation: "ConnectX-7 VPI OCP",
      ports: 2,
      speed: "200G",
      pcie: "PCIe 5.0 x16",
      pcieGen: 5,
      connector: "QSFP112",
      protocol: "VPI",
      formFactor: "OCP 3.0",
      bracket: "Thumbscrew",
      features: "OCP 3.0, 200GbE/HDR IB, Multi Host or Socket Direct",
      href: "/en/products/mellanox/nic/"
    },
    // 400G
    {
      part: "MCX75310AAS-NEAT",
      generation: "ConnectX-7",
      ports: 1,
      speed: "400G",
      pcie: "PCIe 5.0 x16",
      pcieGen: 5,
      connector: "OSFP",
      protocol: "IB",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "NDR 400Gb/s IB OSFP flagship, Secure Boot",
      href: "/en/products/mellanox/nic/"
    },
    {
      part: "MCX75510AAS-NEAT",
      generation: "ConnectX-7",
      ports: 1,
      speed: "400G",
      pcie: "PCIe 5.0 x16",
      pcieGen: 5,
      connector: "OSFP",
      protocol: "IB",
      formFactor: "PCIe Card",
      bracket: "Tall",
      features: "NDR 400Gb/s IB, Socket Direct ready (x16+x16 extension)",
      href: "/en/products/mellanox/nic/"
    }
  ];

  // Wizard state
  let currentStep = 1;
  const selections = {
    use_case: null,
    speed: null,
    pcie: null,
    protocol: null
  };

  // Styles Injection
  const styles = `
    .mlnx-widget {
      font-family: inherit;
      border: 1px solid #374151;
      border-radius: 12px;
      padding: 1.5rem;
      background-color: #1f2937;
      color: #f9fafb;
      margin: 1.5rem 0;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .mlnx-widget h3 {
      color: #38bdf8;
      margin-top: 0;
      margin-bottom: 0.5rem;
      font-size: 1.35rem;
      font-weight: 700;
    }
    .mlnx-widget p.intro {
      color: #9ca3af;
      font-size: 0.95rem;
      margin-bottom: 1.25rem;
    }
    .mlnx-progress {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      position: relative;
    }
    .mlnx-progress::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 2px;
      background-color: #4b5563;
      z-index: 1;
      transform: translateY(-50%);
    }
    .mlnx-progress-step {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background-color: #374151;
      border: 2px solid #4b5563;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 0.85rem;
      z-index: 2;
      transition: all 0.3s;
      color: #9ca3af;
    }
    .mlnx-progress-step.active {
      background-color: #0284c7;
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
    .mlnx-progress-step.completed {
      background-color: #059669;
      border-color: #34d399;
      color: #ffffff;
    }
    .mlnx-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }
    @media (min-width: 640px) {
      .mlnx-grid {
        grid-template-columns: 1fr 1fr;
      }
    }
    .mlnx-card {
      border: 1px solid #4b5563;
      background-color: #374151;
      border-radius: 8px;
      padding: 1rem;
      cursor: pointer;
      transition: all 0.2s;
      text-align: left;
    }
    .mlnx-card:hover {
      border-color: #38bdf8;
      background-color: #4b5563;
      transform: translateY(-2px);
    }
    .mlnx-card.selected {
      border-color: #38bdf8;
      background-color: rgba(2, 132, 199, 0.2);
    }
    .mlnx-card h4 {
      margin: 0 0 0.25rem 0;
      font-size: 1rem;
      font-weight: 600;
      color: #ffffff;
    }
    .mlnx-card p {
      margin: 0;
      font-size: 0.85rem;
      color: #d1d5db;
    }
    .mlnx-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .mlnx-btn {
      padding: 0.5rem 1.25rem;
      border-radius: 6px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      border: 1px solid transparent;
    }
    .mlnx-btn-back {
      background-color: transparent;
      color: #9ca3af;
      border-color: #4b5563;
    }
    .mlnx-btn-back:hover {
      color: #ffffff;
      border-color: #9ca3af;
    }
    .mlnx-btn-primary {
      background-color: #0284c7;
      color: #ffffff;
    }
    .mlnx-btn-primary:hover {
      background-color: #0369a1;
    }
    .mlnx-results-title {
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: #34d399;
      border-bottom: 1px solid #374151;
      padding-bottom: 0.5rem;
    }
    .mlnx-result-card {
      border: 1px solid #374151;
      background-color: #111827;
      border-radius: 8px;
      padding: 1.25rem;
      margin-bottom: 1rem;
      text-align: left;
    }
    .mlnx-result-card h5 {
      margin: 0 0 0.5rem 0;
      font-size: 1.1rem;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .mlnx-result-card h5 span.chip {
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      background-color: #374151;
      color: #e5e7eb;
    }
    .mlnx-result-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.5rem 1rem;
      font-size: 0.85rem;
      margin-bottom: 0.75rem;
      color: #d1d5db;
    }
    .mlnx-result-grid div span.label {
      color: #9ca3af;
      margin-right: 0.25rem;
    }
    .mlnx-result-features {
      font-size: 0.85rem;
      color: #9ca3af;
      border-top: 1px dashed #374151;
      padding-top: 0.5rem;
      margin-top: 0.5rem;
    }
    .mlnx-result-actions {
      display: flex;
      gap: 0.5rem;
      margin-top: 1rem;
    }
    .mlnx-btn-card {
      padding: 0.4rem 0.8rem;
      font-size: 0.8rem;
      border-radius: 4px;
      text-decoration: none;
      display: inline-block;
      text-align: center;
    }
    .mlnx-btn-card-primary {
      background-color: #059669;
      color: #ffffff !important;
    }
    .mlnx-btn-card-primary:hover {
      background-color: #047857;
    }
    .mlnx-btn-card-secondary {
      background-color: #374151;
      color: #e5e7eb !important;
      border: 1px solid #4b5563;
    }
    .mlnx-btn-card-secondary:hover {
      background-color: #4b5563;
    }
    .mlnx-no-results {
      text-align: center;
      padding: 2rem 1rem;
      color: #9ca3af;
    }
    .mlnx-no-results p {
      margin-bottom: 1.5rem;
    }
  `;

  // UI rendering helper
  function render(containerId) {
    const root = document.getElementById(containerId);
    if (!root) return;

    // Inject CSS once
    if (!document.getElementById('mlnx-selector-styles')) {
      const styleEl = document.createElement('style');
      styleEl.id = 'mlnx-selector-styles';
      styleEl.innerHTML = styles;
      document.head.appendChild(styleEl);
    }

    // Step content templates
    let contentHtml = '';

    if (currentStep === 1) {
      contentHtml = `
        <h3>Step 1: Select Your Use Case</h3>
        <p class="intro">Choose the main environment or workload for your server deployment.</p>
        <div class="mlnx-grid">
          <div class="mlnx-card" data-val="ai">
            <h4>🤖 AI / GPU Cluster</h4>
            <p>High-performance computing (HPC), GPU clusters (NVIDIA HGX/DGX), GPUDirect RDMA, NDR/HDR InfiniBand.</p>
          </div>
          <div class="mlnx-card" data-val="virt">
            <h4>🖥 Virtualization & Cloud</h4>
            <p>VMware ESXi, Proxmox VE, KVM, SR-IOV virtualization, high-density VMs, OVS offload.</p>
          </div>
          <div class="mlnx-card" data-val="storage">
            <h4>💾 NVMe-oF Storage</h4>
            <p>High-speed storage networking, NVMe over Fabrics (RoCEv2 or TCP), NVMe SNAP, database backends.</p>
          </div>
          <div class="mlnx-card" data-val="enterprise">
            <h4>🏢 General Enterprise DC</h4>
            <p>Standard data center networking, 10G/25G migration, server uplink, high availability core.</p>
          </div>
          <div class="mlnx-card" data-val="latency">
            <h4>⚡ Low-Latency Trading</h4>
            <p>Financial high-frequency trading (HFT), sub-microsecond latency, hardware timestamping.</p>
          </div>
        </div>
      `;
    } else if (currentStep === 2) {
      contentHtml = `
        <h3>Step 2: Select Bandwidth / Speed</h3>
        <p class="intro">Select the target networking bandwidth you require per card.</p>
        <div class="mlnx-grid">
          <div class="mlnx-card" data-val="10G">
            <h4>10 Gb/s</h4>
            <p>Entry-level enterprise connectivity, legacy server migration.</p>
          </div>
          <div class="mlnx-card" data-val="25G">
            <h4>25 Gb/s</h4>
            <p>Modern standard for enterprise servers and mainstream virtualization.</p>
          </div>
          <div class="mlnx-card" data-val="50G">
            <h4>50 Gb/s</h4>
            <p>Intermediate bandwidth, single-port storage connections.</p>
          </div>
          <div class="mlnx-card" data-val="100G">
            <h4>100 Gb/s</h4>
            <p>Enterprise core networks, virtualized backbones, high-speed storage.</p>
          </div>
          <div class="mlnx-card" data-val="200G">
            <h4>200 Gb/s</h4>
            <p>HDR InfiniBand or 200G Ethernet, GPU training nodes, high-density storage.</p>
          </div>
          <div class="mlnx-card" data-val="400G">
            <h4>400 Gb/s</h4>
            <p>NDR InfiniBand flagship, multi-node AI cluster backplanes.</p>
          </div>
        </div>
      `;
    } else if (currentStep === 3) {
      contentHtml = `
        <h3>Step 3: Select PCIe Slot Version</h3>
        <p class="intro">Ensure the host motherboard PCIe slot generation matches the network card.</p>
        <div class="mlnx-grid">
          <div class="mlnx-card" data-val="3">
            <h4>PCIe 3.0 Slot</h4>
            <p>Common in older servers (Intel Xeon Scalable 1st/2nd Gen, AMD EPYC 1st/2nd Gen).</p>
          </div>
          <div class="mlnx-card" data-val="4">
            <h4>PCIe 4.0 Slot</h4>
            <p>Standard in Intel Scalable 3rd Gen (Ice Lake), AMD EPYC 3rd Gen (Milan).</p>
          </div>
          <div class="mlnx-card" data-val="5">
            <h4>PCIe 5.0 Slot</h4>
            <p>Newest generation: Intel Scalable 4th/5th Gen, AMD EPYC 4th Gen (Genoa).</p>
          </div>
        </div>
      `;
    } else if (currentStep === 4) {
      contentHtml = `
        <h3>Step 4: Select Preferred Protocol</h3>
        <p class="intro">Choose the protocol stack required for your switch environment.</p>
        <div class="mlnx-grid">
          <div class="mlnx-card" data-val="EN">
            <h4>Ethernet only (EN)</h4>
            <p>For standard Ethernet switches, corporate networking, general TCP/IP.</p>
          </div>
          <div class="mlnx-card" data-val="VPI">
            <h4>VPI (InfiniBand + Ethernet)</h4>
            <p>Virtual Protocol Interconnect: auto-senses and supports either network. Most flexible.</p>
          </div>
          <div class="mlnx-card" data-val="IB">
            <h4>InfiniBand only (IB)</h4>
            <p>Dedicated low-latency InfiniBand subnetworks (HPC / AI clusters).</p>
          </div>
        </div>
      `;
    } else if (currentStep === 5) {
      const filtered = getRecommendations();
      contentHtml = `
        <h3>Recommendations</h3>
        <p class="intro">Based on your selections, we recommend the following Mellanox product(s):</p>
        <div class="mlnx-results-container">
      `;

      if (filtered.length > 0) {
        contentHtml += `<div class="mlnx-results-title">Recommended Network Interface Cards (${filtered.length})</div>`;
        filtered.forEach(nic => {
          contentHtml += `
            <div class="mlnx-result-card">
              <h5>
                ${nic.part} 
                <span class="chip">${nic.generation}</span>
              </h5>
              <div class="mlnx-result-grid">
                <div><span class="label">Speed:</span>${nic.speed}</div>
                <div><span class="label">Ports:</span>${nic.ports}x ${nic.connector}</div>
                <div><span class="label">PCIe Slot:</span>${nic.pcie}</div>
                <div><span class="label">Form Factor:</span>${nic.formFactor} (${nic.bracket} Bracket)</div>
                <div><span class="label">Protocol:</span>${nic.protocol === 'EN' ? 'Ethernet' : nic.protocol === 'VPI' ? 'VPI (IB/ETH)' : 'InfiniBand'}</div>
              </div>
              <div class="mlnx-result-features">
                <strong>Key Features:</strong> ${nic.features}
              </div>
              <div class="mlnx-result-actions">
                <a href="/en/contact/?ref=Mellanox-${nic.part}" class="mlnx-btn-card mlnx-btn-card-primary">Request Quote</a>
                <a href="${nic.href}" class="mlnx-btn-card mlnx-btn-card-secondary">View Specifications</a>
              </div>
            </div>
          `;
        });
      } else {
        contentHtml += `
          <div class="mlnx-no-results">
            <p><strong>No exact match in our standard catalog.</strong><br>
            However, we regularly design custom solutions for enterprise clients.</p>
            <a href="/en/contact/?ref=Mellanox-Custom-NIC" class="mlnx-btn mlnx-btn-primary">Consult Our Engineers</a>
          </div>
        `;
      }

      contentHtml += `</div>`;
    }

    // Wrap in standard layout
    const headerHtml = `
      <div class="mlnx-widget">
        <div class="mlnx-progress">
          <div class="mlnx-progress-step ${currentStep >= 1 ? 'active' : ''} ${currentStep > 1 ? 'completed' : ''}">1</div>
          <div class="mlnx-progress-step ${currentStep >= 2 ? 'active' : ''} ${currentStep > 2 ? 'completed' : ''}">2</div>
          <div class="mlnx-progress-step ${currentStep >= 3 ? 'active' : ''} ${currentStep > 3 ? 'completed' : ''}">3</div>
          <div class="mlnx-progress-step ${currentStep >= 4 ? 'active' : ''} ${currentStep > 4 ? 'completed' : ''}">4</div>
          <div class="mlnx-progress-step ${currentStep >= 5 ? 'active' : ''} ${currentStep > 5 ? 'completed' : ''}">✓</div>
        </div>
        <div class="mlnx-content">
          ${contentHtml}
        </div>
        <div class="mlnx-actions">
          ${currentStep > 1 ? `<button class="mlnx-btn mlnx-btn-back" id="mlnx-btn-prev">Back</button>` : '<div></div>'}
          ${currentStep < 5 ? `<button class="mlnx-btn mlnx-btn-back" id="mlnx-btn-reset">Reset</button>` : `<button class="mlnx-btn mlnx-btn-primary" id="mlnx-btn-restart">Restart Tool</button>`}
        </div>
      </div>
    `;

    root.innerHTML = headerHtml;

    // Attach Event Listeners
    if (currentStep < 5) {
      const cards = root.querySelectorAll('.mlnx-card');
      cards.forEach(card => {
        card.addEventListener('click', function() {
          const val = this.getAttribute('data-val');
          const stepKey = getStepKey(currentStep);
          selections[stepKey] = val;
          currentStep++;
          render(containerId);
        });
      });
    }

    const btnPrev = root.querySelector('#mlnx-btn-prev');
    if (btnPrev) {
      btnPrev.addEventListener('click', function() {
        currentStep--;
        render(containerId);
      });
    }

    const btnReset = root.querySelector('#mlnx-btn-reset');
    if (btnReset) {
      btnReset.addEventListener('click', function() {
        currentStep = 1;
        selections.use_case = null;
        selections.speed = null;
        selections.pcie = null;
        selections.protocol = null;
        render(containerId);
      });
    }

    const btnRestart = root.querySelector('#mlnx-btn-restart');
    if (btnRestart) {
      btnRestart.addEventListener('click', function() {
        currentStep = 1;
        selections.use_case = null;
        selections.speed = null;
        selections.pcie = null;
        selections.protocol = null;
        render(containerId);
      });
    }
  }

  function getStepKey(step) {
    switch (step) {
      case 1: return 'use_case';
      case 2: return 'speed';
      case 3: return 'pcie';
      case 4: return 'protocol';
    }
  }

  function getRecommendations() {
    return nics.filter(nic => {
      // 1. Bandwidth check
      if (selections.speed && nic.speed !== selections.speed) {
        return false;
      }

      // 2. PCIe generation compatibility (NIC slot version must be <= motherboard PCIe Gen)
      if (selections.pcie) {
        const boardGen = parseInt(selections.pcie);
        if (nic.pcieGen > boardGen) {
          return false;
        }
      }

      // 3. Protocol check
      if (selections.protocol) {
        // VPI cards can do both, EN can only do EN, IB can only do IB
        if (selections.protocol === 'EN') {
          if (nic.protocol !== 'EN' && nic.protocol !== 'VPI') return false;
        } else if (selections.protocol === 'IB') {
          if (nic.protocol !== 'IB' && nic.protocol !== 'VPI') return false;
        } else if (selections.protocol === 'VPI') {
          if (nic.protocol !== 'VPI') return false; // strict VPI preference
        }
      }

      // 4. Use Case smart filter adjustments
      if (selections.use_case === 'ai') {
        // AI workloads require low-latency. Prefer high speed (>=100G) or InfiniBand/VPI capabilities.
        const numericSpeed = parseInt(nic.speed);
        if (numericSpeed < 100 && nic.protocol !== 'VPI' && nic.protocol !== 'IB') {
          return false;
        }
      } else if (selections.use_case === 'latency') {
        // High Frequency Trading prefers ConnectX-6 Dx/Lx/7 with hardware timestamping (usually EN or VPI, speed >= 25G)
        const numericSpeed = parseInt(nic.speed);
        if (numericSpeed < 25) return false;
      }

      return true;
    });
  }

  // Auto-init on DOMContentLoaded or immediate execution
  function init() {
    const el = document.getElementById('mellanox-selector-root');
    if (el) {
      render('mellanox-selector-root');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose internationally for manual invocation
  window.MellanoxSelector = {
    init: init,
    render: render
  };
})();
