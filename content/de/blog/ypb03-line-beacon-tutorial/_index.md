---
title: "Vom U-Bahn-Pendeln bis zur Kaufhaus-Jubiläumsaktion: Wie Unternehmen mit dem YPB03 LINE Beacon Offline-Erlebnisse und präzises Retargeting aufwerten"
description: "Lerne, wie du das YPB03 LINE Beacon einrichtest: HWID registrieren, BeaconSET+ konfigurieren und mit Python Flask einen Webhook für OMO-Marketing bauen."
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
---

![YPB03 LINE Beacon Concept Banner](/images/blog/ypb03-line-beacon-tutorial.jpg)

Stell dir folgendes Szenario vor: Ein Kunde betritt dein Geschäft, und ohne eine zusätzliche App herunterzuladen, poppt auf seinem Handy in LINE automatisch eine freundliche Willkommensnachricht auf, liefert den heutigen Rabattgutschein oder leitet ihn zu den neuesten Highlight-Produkten weiter. Das ist keine Zauberei, sondern eine **LINE Beacon**-Anwendung, die Bluetooth-Standorttechnologie eng mit der LINE-Plattform verbindet.

Dieser Artikel führt Marketingteams und Projektentwickler Schritt für Schritt durch den Einsatz des industrietauglichen Langstrecken-Bluetooth-Geräts **YPB03** — von null an: Registrierung des LINE-Entwicklerkontos, Konfiguration der Bluetooth-Broadcast-Parameter und Implementierung eines Webhook-Empfangsdienstes für die Messaging API mit Python. So verwandelst du physischen Besucherstrom in wertvolle digitale Marketing-Assets!

---

## Warum das YPB03 als LINE Beacon wählen?

Auf dem Markt gibt es viele Bluetooth-Beacon-Varianten, doch für ein stabiles, kommerziell genutztes oder als Showcase dienendes LINE Beacon sind die Hardware-Spezifikationen entscheidend. Hier sind die zentralen Hardware-Highlights des YPB03:

* **Ultra-Langstrecken-Sendeleistung (240 Meter)**: Mit einer Hochgewinnantenne erreicht das Gerät in freier Umgebung bis zu 240 Meter Reichweite. Ob weiträumige Messehallen, große Supermärkte oder mehrstöckige Geschäfte — die Abdeckung gelingt mühelos.
* **10 Jahre ultra-lange Akkulaufzeit**: Vier Standard-AA-Batterien liefern insgesamt 5800 mAh. Bei der werkseitigen Sendefrequenz läuft das Gerät fast 10 Jahre — Schluss mit dem Albtraum häufiger Batteriewechsel.
* **IP65 Industrieschutz**: Das ABS- und Silikon-dichtete Gehäuse bietet Staub- und Spritzwasserschutz, sodass der Einsatz in feuchten Lagern oder halb-offenen Umgebungen sicher ist.
* **Flexible Montage**: Im Lieferumfang enthalten ist eine Schraub-Wandhalterung, die sich leicht an Wänden oder Trägern befestigen lässt.

---

## Gängige LINE-Beacon-Marketingmethoden und taiwanesische Praxisbeispiele

Dass LINE Beacon als OMO (Online-Merge-Offline)-Marketinginstrument überzeugt, liegt daran, dass es die Lücke schließt, die physische Geschäfte nicht schließen können — die Verhaltensverfolgung von Kunden — und gleichzeitig hochattraktive Echtzeit-Interaktion bietet.

### Gängige Marketingmethoden
* **Präzise Echtzeit-Begrüßung**: Sobald ein Kunde den Bereich betritt (löst ein `enter`-Ereignis aus), wird sofort eine persönliche Begrüßung oder ein sofort einlösbarer Rabattgutschein gepusht — präziser Fang von Passanten am Eingang.
* **Interaktives Sammelpunkte- und Check-in-Spiel**: Mehrere Beacon werden in verschiedenen Zonen oder an Ständen eines Einkaufszentrums verteilt. Erreicht der Kunde einen bestimmten Punkt, schaltet er eine Stufe frei oder sammelt Punkte, die er nach Erreichen des Ziels direkt in LINE gegen LINE Points oder physische Geschenke einlösen kann — das steigert den Entdecker-Spaß.
* **Offline-Daten-Retargeting**: Zeiterfassung und Frequenz der Beacon-Kontakte ermöglichen es Marken, über die LINE-Anzeigenplattform (LAP) diese Gruppe der „tatsächlich vor Ort Gewesenen" für Retargeting anzusprechen.

### Taiwanesische Praxisbeispiele

In Taiwan hat LINE Beacon bereits in vielen großen öffentlichen Einrichtungen und bei bekannten Marken beeindruckende Erfolge gezeigt:

1. **Taipei U-Bahn-Pendler-Überraschung**:
   Die Taipei U-Bahn hat an mehreren Verkehrsknotenpunkten (z. B. Taipei Hauptbahnhof, Ximen, Zhongxiao Fuxing) LINE Beacon ausgerollt. Pendler erhalten während der Fahrt — sofern Bluetooth und LINE aktiv sind — Veranstaltungshinweise. Über Check-in-Missionen wie die „U-Bahn-Überraschungszüge" lassen sich bestimmte Puzzleteile sammeln und gegen kostenlose LINE Points einlösen. So wurden die täglichen Millionen-Pendlerströme nahtlos in interaktive digitale Marketing-Assets verwandelt.
2. **Taiwan Laternenfest in Taipei (intelligente Ausstellungsführung)**:
   Beim „2023 Taiwan Laternenfest in Taipei" setzten die Veranstalter **350 LINE Beacon** ein, die vier große Ausstellungsbereiche flächendeckend abdeckten. Näherten sich Besucher bestimmten Laternenkunstwerken, pushpte LINE automatisch Sprachführungen, gastronomische Empfehlungen (gekoppelt mit LINE-Spots) oder Taxigutscheine (gekoppelt mit LINE TAXI). Statt vor Ort Papierprospekte abzuholen, wurde das Handy zum persönlichen Cloud-Führer.
3. **SOGO Kaufhaus Jubiläumsaktion — Passanten-Abfang**:
   SOGO nutzte die Nähe zur U-Bahn-Station und platzierte LINE Beacon an den U-Bahn-Ausgängen und rund um das Kaufhaus. Während der Jubiläumsaktion poppte bei Annäherung potenzieller Kunden proaktiv ein Aktionshinweis auf. In nur 4 Tagen entstanden 5 Millionen Impressionen und über 1 Million effektive Kontakte — die „Passanten" außerhalb wurden erfolgreich abgefangen und ins Geschäft gelenkt.
4. **FamilyMart Let's Café-Kampagne**:
   FamilyMart setzte über das dichte taiwanische Filialnetz Beacon ein. Begleitend zu einer Themenkampagne startete ein Online-Spiel, das Kunden in der Filiale über LINE Beacon auslöste, um einen Rabattgutschein für Let's Café-Eiskaffee zu erhalten. Mitgliedsaktivität und Filialbesuchsbereitschaft stiegen spürbar.
5. **Shiseido Beauty-Counter-Zuströmung**:
   Shiseido platzierte LINE Beacon an mehreren Kaufhaus-Countern in ganz Taiwan. Näherte sich ein Kunde dem Beauty-Counter, pushpte das System proaktiv einen Tausch-Gutschein für eine Neuprodukt-Probe und lenkte Passanten zur Interaktion mit dem Counter-Personal — die Thekenfrequenz und die nachfolgende Proben-Conversion stiegen merklich.

---

## Schritt 1: LINE Official Account registrieren und die Hardware ID (HWID) erhalten

Damit LINE unser YPB03 erkennt, musst du zuerst in der LINE-Entwicklerkonsole eine exklusive „Geräte-Ausweisnummer" beantragen — die Hardware ID (HWID).

1. **LINE Developers Plattform öffnen**:
   Melde dich in der [LINE Developers Console](https://developers.line.biz/) mit deinem LINE-Konto an.
2. **Provider und Channel anlegen**:
   - Erstelle einen neuen **Provider** (z. B. den Namen deines Studios oder deines Schulprojekts).
   - Lege unter diesem Provider einen Channel vom Typ **Messaging API** an (das erzeugt einen LINE Official Account, kurz LINE Bot).
3. **LINE Official Account Manager öffnen**:
   - Melde dich im [LINE Official Account Manager](https://manager.line.me/) an.
   - Wähle deinen neuen Official Account, klicke oben rechts auf „Einstellungen".
   - Finde im linken Menü „Messaging API" und bestätige, dass die API aktiviert ist.
4. **LINE Beacon-Gerät beantragen**:
   - Klicke auf derselben Messaging-API-Einstellungsseite auf **„LINE Beacon associated device registration"**.
   - Folge den Anweisungen; LINE erzeugt zufällig eine **5-Byte (10 Hexadezimalzeichen)** lange **Hardware ID (HWID)** (Beispiel: `0123456789`). Notiere dir diese HWID — wir brauchen sie gleich zum Konfigurieren der Bluetooth-Parameter.

---

## Schritt 2: YPB03 mit der BeaconSET+ App konfigurieren

Mit deiner Ausweisnummer (HWID) in der Hand musst du diese Nummer ins YPB03-Beacon „schreiben" und es so einrichten, dass es im von LINE vorgegebenen Format rundfunkt.

### 1. Einrichtungswerkzeug installieren
Lade auf dem Handy die offizielle Einrichtungssoftware von Minew herunter:
* iOS-Nutzer: Suche im App Store nach **BeaconSET+**
* Android-Nutzer: Suche im Google Play nach **BeaconSET+**

### 2. Mit dem YPB03 verbinden
1. Aktiviere Bluetooth am Handy und öffne die **BeaconSET+** App.
2. Suche in der Geräteliste nach einem Gerät namens `YPB03` oder der zugehörigen MAC-Adresse.
3. Tippe auf „Verbinden"; die App fordert ein Passwort. Das Werkspasswort lautet `minew123` (ändere es nach dem Verbinden aus Sicherheitsgründen).

### 3. LINE Simple Beacon Broadcast-Slot konfigurieren
YPB03 unterstützt simultanes Multi-Channel-Broadcasting. Wir widmen einen SLOT dem LINE-Format:
1. Wähle nach dem Verbinden einen ungenutzten Broadcast-SLOT.
2. Setze den **Frame Type** auf **Service Data**.
3. Lege diese beiden Schlüsselparameter fest:
   * **Service UUID**: Gib `FE6F` ein (die LINE-Beacon-exklusive Standard-Service-UUID).
   * **Data Value**: Gib die zusammengesetzten 9-Byte-Hexadezimaldaten ein. Die Formel lautet:
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{deine 5-Byte HWID} + \text{Endemarker (7F00)}$$
     *Beispiel: Ist deine HWID `0123456789`, trägst du im Feld Data Value ein: `FE6F01234567897F00`*.
4. Tippe nach Abschluss oben rechts auf **Save**.
5. Trenne die Verbindung. Das YPB03 sendet nun offiziell das LINE-Beacon-Signal!

---

## Schritt 3: Python-Webhook-Code zum Empfangen des Signals

Wenn das Handy eines Nutzers in die Nähe des YPB03 kommt, erkennt die LINE-App den Bluetooth-Broadcast und sendet über die LINE-Plattform einen HTTP-POST-Request (also einen Webhook) an deinen Backend-Server.

Im Folgenden nutzen wir das leichtgewichtige Python-Webframework **Flask**, um diesen Webhook-Server aufzusetzen und die Annäherungsereignisse zu parsen.

### 1. Benötigte Pakete installieren
Führe im Terminal folgenden Befehl aus, um Flask zu installieren:
```bash
pip install Flask
```

### 2. Code schreiben (`app.py`)
Lege eine Datei `app.py` an und füge folgenden Code ein:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# LINE Developers 註冊的 HWID（這裡改為您申請到的 HWID）
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 平台傳過來的 JSON 資料
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # 巡檢所有的事件
    for event in body["events"]:
        # 篩選事件類型為 beacon 的事件
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (進入), stay (逗留), banner (點擊橫幅)
            
            print(f"收到 Beacon 事件！使用者 ID: {user_id}")
            print(f"設備 HWID: {hwid} | 觸發類型: {beacon_type}")
            
            # 判斷是否為我們的 YPB03 設備
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> 使用者進入了 YPB03 範圍！觸發迎賓機制。")
                    # 在這裡，您可以呼叫 LINE Messaging API 送出歡迎折價券給 user_id
                elif beacon_type == "stay":
                    print("--> 使用者持續在範圍內...")
                elif beacon_type == "banner":
                    print("--> 使用者點擊了聊天室上方的 LINE Beacon 橫幅！")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # 本地測試執行在 5000 端口
    app.run(port=5000)
```

### 3. Lokaler Test und Tunnel ins öffentliche Internet
Die LINE-Plattform verlangt, dass der Webhook an eine öffentliche HTTPS-URL geliefert wird. In der Entwicklungsphase nutzen wir **ngrok** für den Tunnel aus dem lokalen Netz ins öffentliche Internet:
1. Starte den Python-Dienst:
   ```bash
   python app.py
   ```
2. Lade ngrok herunter und starte es, um den lokalen Port 5000 an das öffentliche Internet weiterzuleiten:
   ```bash
   ngrok http 5000
   ```
3. ngrok liefert eine zufällige URL beginnend mit `https://` (z. B. `https://xxxx.ngrok-free.app`). Kopiere diese URL, hänge `/callback` an und trage sie in der LINE Developers Console im Feld **Webhook URL** des Channels ein (z. B. `https://xxxx.ngrok-free.app/callback`), dann klicke auf **Verify**, um die Verbindung zu prüfen.

---

## Vor-Ort-Verifikation und Test

1. Stelle sicher, dass **Bluetooth** am Handy aktiviert ist.
2. Stelle sicher, dass LINE installiert ist und in den Einstellungen die **LINE Beacon**-Empfangsfunktion freigegeben wurde (Pfad: LINE App -> Einstellungen -> Datenschutzeinstellungen -> LINE Beacon -> Zustimmung anhaken).
3. Füge deinen LINE Official Account als Freund hinzu.
4. Nimm das Handy zur Hand und gehe langsam in den Broadcast-Bereich des YPB03 (für den Innentest kannst du die Sendeleistung manuell reduzieren).
5. Beobachte die Python-Konsole — du siehst die Echtzeit-Log-Ausgabe:
   ```text
   收到 Beacon 事件！使用者 ID: U1234567890abcdef...
   設備 HWID: 0123456789 | 觸發類型: enter
   --> 使用者進入了 YPB03 範圍！觸發迎賓機制。
   ```

---

## YPB03 Kernparameter-Übersicht

| Technischer Parameter | Wert / Einstellung | Beschreibung |
| :--- | :--- | :--- |
| **Bluetooth-Spezifikation** | BLE 5.0 (nRF52 series) | Niedriger Stromverbrauch, hocheffiziente Übertragung |
| **Standard-Service UUID** | `0xFE6F` | LINE-Beacon-exklusive Dienstkennung |
| **Einrichtungssoftware** | **BeaconSET+** | Wireless-Konfiguration unter iOS und Android |
| **Schutzklasse** | IP65 | Staub- und spritzwassergeschützt, geeignet für Industrie- und halb-offene Umgebungen |
| **Stromversorgung** | 4 × AA Batterien (5800mAh) | Bis zu 10 Jahre Laufzeit (abhängig vom Broadcast-Intervall) |
| **Service Data-Formel** | `FE6F` + `[5-Byte HWID]` + `7F00` | Hexadezimalwert zum Eintragen in BeaconSET+ |

---

## Häufige Fragen (FAQ)

#### F: Kann das YPB03 ausschließlich als LINE Beacon genutzt werden?
**A**: Nein. Das YPB03 ist ein multifunktionaler Bluetooth-Beacon; neben dem LINE Simple Beacon-Protokoll lassen sich gleichzeitig der Standard-**iBeacon** und der **Eddystone**-Broadcast aktivieren. Entwickler können in einem SLOT iBeacon für die Positionierung mit einer Eigenbau-App ausstrahlen und in einem anderen SLOT LINE Beacon für installationsfreies Marketing.

#### F: Warum findet BeaconSET+ das YPB03 beim Scannen nicht?
**A**: Prüfe Folgendes:
1. Stelle sicher, dass das YPB03 mit Batterien bestückt und eingeschaltet ist (meist gibt es einen Schalter an der Seite oder die LED blinkt beim ersten Stromkontakt).
2. Bluetooth und der Standortdienst (GPS) am Handy müssen aktiviert sein und BeaconSET+ die Standortberechtigung erhalten.
3. Ist das Gerät bereits von einem anderen Handy verbunden, kann es vorübergehend nicht gescannt werden — stelle sicher, dass andere Konfigurationsgeräte getrennt sind.

#### F: Was ist der Unterschied zwischen dem `stay`- und dem `enter`-Ereignis bei LINE Beacon?
**A**:
- **`enter`**-Ereignis: Wird genau einmal ausgelöst, wenn der Nutzer „erstmals" in den Bluetooth-Signalbereich des Beacon eintritt — ideal für Willkommensnachrichten oder Tagesrabattgutscheine.
- **`stay`**-Ereignis: Während der Nutzer im Signalbereich verweilt, sendet die LINE-Plattform etwa alle 10 Sekunden ein `stay`-Ereignis. Damit lässt sich die Aufenthaltsdauer in der Zone berechnen — bei hoher Nebenläufigkeit ist jedoch die Serverbelastung zu beachten.

---

## Fazit

Mit dem industrietauglichen Bluetooth-Beacon YPB03 können physische Geschäfte bei minimalen Wartungskosten und komplett ohne Entwicklung einer eigenen App eine nahtlose OMO-Interaktion (Online-Merge-Offline) mit der großen LINE-Nutzerschaft schaffen — egal ob für ein Schulprojekt oder einen großflächigen kommerziellen Rollout. YPB03 ist die erste Wahl, wenn es um Stabilität und Reichweite geht.

Für ein Angebot zum YPB03-Gerät oder weitere IoT-Kundenaufträge [komm über die Yupitek-Website mit uns in Kontakt](https://www.yupitek.com/de/contact/)!
