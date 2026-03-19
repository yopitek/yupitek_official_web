---
title: "Packet Squirrel Mark II"
date: 2025-01-01
draft: false
description: "口袋大小的 Ethernet 中間人多功能工具，支援 WireGuard / OpenVPN VPN 與五種網路模式。"
featureimage: "/images/products/hak5/packet-squirrel.png"
---

## 產品特色

- **多功能 Ethernet MitM 工具**：口袋大小，支援五種網路模式：NAT、BRIDGE、TRANSPARENT、JAIL、ISOLATE
- **雙 VPN 支援**：同時支援 WireGuard 與 OpenVPN VPN 連線
- **Web UI + SSH 存取**：預設管理 IP：172.16.32.1:1471
- **4 段模式切換**：單顆按鈕可重新啟動 / 恢復出廠
- **USB 儲存擴充**：支援 USB-A 2.0，可選 LUKS 全磁碟加密
- **多語言 Payload**：以 Bash / Python 撰寫，支援 DuckyScript
- **Cloud C² 支援**：遠端管理
- **安全自毀**：支援 SELFDESTRUCT payload 命令

## 主要規格

| 規格項目 | 內容 |
|---------|------|
| 介面 | Dual Ethernet（Target 及 Network 埠）、USB-C（電源）、USB-A 2.0（儲存） |
| 網路標準 | 802.3 |
| 電源 | USB-C（5V） |
| 預設管理 IP | 172.16.32.1 |
| 作業系統 | Linux-based |
| LED | 多色狀態 LED |

## 應用環境

- 企業網路中間人（MitM）封包擷取與分析
- 隱蔽 VPN 通道建立（WireGuard / OpenVPN）
- 紅隊網路植入與遠端持久存取
- 流量操控、DNS 欺騙（SPOOFDNS）、封包注入
- 藍隊演練：隔離可疑設備（JAIL / ISOLATE 模式）
- 企業網路弱點評估自動化
