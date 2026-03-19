---
title: "Shark Jack Cable"
date: 2025-01-01
draft: false
description: "融入 Ethernet 線材外型的 Shark Jack，新增 USB UART 序列介面，更易隱蔽植入。"
featureimage: "/images/products/hak5/shark-jack-cable.png"
---

## 產品特色

- **線材形態**：所有 Shark Jack 功能，融入 Ethernet 線材外型，更易隱蔽
- **USB UART 序列介面**：新增 CP2102 序列介面，可直連 root shell
- **長期植入優化**：適合長期植入或需要串列除錯的場景
- **Android 支援**：支援 Android 序列設定（Android Serial Setup）
- **完全相容**：Payload 開發與 Shark Jack 完全相容

## 主要規格

| 規格項目 | 內容 |
|---------|------|
| SoC | MediaTek MT7628DAN |
| 介面 | Ethernet（802.3）、USB UART（CP2102） |
| 尺寸 | 62 × 21 × 12 mm |
| 電源 | 2.5W（USB 5V 0.5A） |
| 作業溫度 | 35°C ~ 45°C |
| 儲存溫度 | -20°C ~ 50°C |
| 相對濕度 | 0% ~ 90%（不凝露） |

## 應用環境

- 偽裝成普通 Ethernet 連接線的長期網路植入
- 需要序列 console 存取的進階 Payload 開發
- 紅隊現場部署，難以被目視識別
- Android 設備配合使用的行動滲透測試
