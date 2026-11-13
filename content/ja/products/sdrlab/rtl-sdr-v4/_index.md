---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — 入門SDRレシーバー"
description: "RTL-SDR Blog RTL SDR V4、500kHz〜1.766GHz広帯域SDRレシーバー、1PPM TCXO、内蔵HFアップコンバーター、RF研究入門に最適。"
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/rtl-sdr-v4.png"
hideFeatureImage: true
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "無線受信", "USB", "GNU Radio"]
faq:
  - question: "RTL-SDR Blog V4でHFを受信するためにダイレクトサンプリングモードは必要ですか？"
    answer: "いいえ。V4にはダイレクトサンプリング回路の代わりに内蔵アップコンバータが搭載されているため、HF信号は28.8 MHzアップコンバートされ、ドライバーが周波数シフトを処理します。V4でダイレクトサンプリングを有効にしても結果は得られません。"
  - question: "RTL-SDR Blog V4には特別なドライバーが必要ですか？"
    answer: "はい。V4にはRTL-SDR Blogドライバーが必要で、V3およびそれ以前のユニットと下位互換性があります。"
  - question: "RTL-SDR Blog V4のバイアスティーはどのように動作しますか？"
    answer: "バイアスティーはソフトウェアで制御され、定格は4.5 Vで、最大180 mAを連続供給します。Linuxではrtl_biastで切り替えます。"
---

## 製品特長

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- R828D チューナー（入力 3 系統）を採用。トリプレクサーが SMA 入力を HF・VHF・UHF の 3 帯域に分離し、帯域外の分離度を向上
- 内蔵 HF アップコンバーター：HF は 28.8 MHz アップコンバートされ、ダイレクトサンプリングモードは不要（最低受信周波数 500 kHz）
- 1 PPM 温度補償水晶発振器（TCXO）により、周波数安定性を大幅に向上
- ソフトウェア制御バイアスティー（Bias-Tee）搭載、外付け LNA またはアクティブアンテナへの給電が可能
- 放送 AM、放送 FM、DAB 帯域向けの切り替え式ノッチフィルターで、強力な放送波による干渉を低減
- シールドとヒートシンクを兼ねる導電性ブラック金属ケース。USB ノイズ対策と強化された ESD 保護も搭載
- 多機能ダイポールアンテナキット付属、開封後すぐに使用可能

## 仕様

| 仕様項目 | 値／説明 |
|---------|---------|
| チューナーチップ | Rafael Micro R828D |
| ADC チップ | RTL2832U |
| 周波数範囲 | 500 kHz – 1.766 GHz（HF モード含む） |
| 周波数精度 | 1 PPM TCXO |
| RF コネクタ | SMA |
| バイアス電源 | ソフトウェア有効化、最大 4.5 V |
| HF 受信 | 内蔵アップコンバーター（HF を 28.8 MHz アップコンバート、ダイレクトサンプリング不要） |
| ケース | 導電性ブラック金属ケース（シールド兼ヒートシンク） |
| インターフェース | USB（RTL-SDR Blog ドライバーが必要） |
| 対応 OS | Windows、Linux、macOS、Android |
| 付属品 | ダイポールアンテナキット（伸縮アンテナ 4 本：2× 23 cm–1 m、2× 5–13 cm、3 m 延長ケーブル、三脚、吸盤スタンド） |

## 用途

- ADS-B 航空機トラッキング
- 海事 AIS 船舶モニタリング
- NOAA/Meteor M2 気象衛星画像受信
- アマチュア無線（HF/VHF/UHF 受信）
- 電波天文学（水素線観測）
- P25、MotoTRBO デジタル音声デコード
- APRS、ACARS パケットトラッキング
- DAB デジタル放送受信
- RF スペクトラムモニタリングとセキュリティ研究

---

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}

{{< faq >}}

[セットアップガイドと技術詳細 — doc.yupitek.com](https://doc.yupitek.com/sdrlab/hardware/rtl-sdr-v4/)

[RTL-SDR Blog 公式 V4 ガイド](https://www.rtl-sdr.com/v4/)

**メーカー販売ページ（OpenSourceSDRLab）**：https://opensourcesdrlab.com/products/rtl-sdr-v4
