# Progress Reader – NVDA-Addon
(C) 2025, Imam Kahraman

Lizenz: GNU General Public License v3 (GPL-3.0) (siehe LICENSE-Datei: https://www.gnu.org/licenses/gpl-3.0.txt)

Dieses NVDA-Addon ermöglicht es, Fortschrittsbalken (Progressbars) in verschiedenen Anwendungen auszulesen und den aktuellen Fortschritt per Sprachausgabe wiederzugeben. Die Erkennung erfolgt über mehrere Schnittstellen, um eine breite Kompatibilität mit unterschiedlichen Software-Technologien sicherzustellen.

---

## Inhalt

1. Installation des Add-ons
2. Verwendung der Fortschrittsanzeige
3. Hinweise zur Funktionalität
4. Versionsverlauf
5. Lizenz & Haftungsausschluss

---

## 1) Installation des Add-ons

### Installation über den NVDA Add-on Store
1. Öffne NVDA und navigiere zu Werkzeuge > Store für Addon-Erweiterungen.
2. Suche nach "Progress Reader" und wähle es aus.
3. Klicke auf "Installieren" und folge den Anweisungen.
4. Starte NVDA neu, um das Add-on zu aktivieren.

### Manuelle Installation (.nvda-addon-Datei)
#### Falls das Add-on nicht im Store verfügbar ist:
1. Lade die `.nvda-addon`-Datei herunter.
2. Öffne NVDA und navigiere zu Werkzeuge > Store für Addon-Erweiterungen.
3. Klicke auf „Aus externer Quelle installieren…“ und wähle die `.nvda-addon`-Datei aus.
4. Bestätige die Installation und starte NVDA neu, um das Add-on zu aktivieren.

---

## 2) Verwendung der Fortschrittsanzeige

1. **Wechsle in eine Anwendung mit einer aktiven Fortschrittsanzeige (z. B. Dateiübertragung, Ladebalken, Softwareinstallation).**
2. **Drücke NVDA + Shift + U, um den aktuellen Fortschritt auszulesen.**
3. **NVDA gibt den Fortschritt in Prozent aus, z. B. "42% Fortschritt (aktiv)".**

---

## 3) Hinweise zur Funktionalität

- Falls mehrere Fortschrittsbalken im aktiven Fenster vorhanden sind, wird der erste gefundene verwendet.
- Wenn kein Progressbar erkannt wird, dann gibt NVDA die Meldung "Keine Progressbar gefunden" aus.
- Falls der Fortschrittswert oder das Maximum nicht ermittelt werden kann, wird ein Standardwert von 0-100% angenommen.
- Manche Anwendungen verwenden proprietäre UI-Elemente, die nicht standardmäßig erkannt werden können.

---

## 4) Versionsverlauf

### v0.1.3
- Tastenkombination umgestellt auf NVDA + SHIFT + U
- Update der Tastenkombination in ReadMe-Datei
- Code bereinigt
- Verwenden von GPL v3.0

### v0.1.2
- ReadMe-Datei verbessert und Nutzungshinweise ergänzt.
- Erweiterte Unterstützung für verschiedene UI-Technologien:
  - Native Windows-Controls (klassische Fortschrittsbalken)
  - WPF / WinForms (Microsoft-.NET-Technologien)
  - wxPython/wxWidgets (z. B. `wx.Gauge`)
  - Java-Anwendungen (mit korrekter Accessibility-API)
  - Webbasierte Progressbars (abhängig vom Browser und ARIA-Support)

### v0.1.0
- Erste Version mit Basisfunktionalität für das Erkennen und Auslesen von Fortschrittsbalken.

---

## 5) Lizenz & Haftungsausschluss  

Dieses Add-on wird unter der GNU General Public License v3 (GPL-3.0) veröffentlicht. Siehe die LICENSE-Datei für weitere Informationen. Diese Datei gibt es hier: https://www.gnu.org/licenses/gpl-3.0.txt

### Lizenzbestimmungen:
- Dieses Add-on ist freie Software und darf verbreitet, verändert und weitergegeben werden, solange es Open Source bleibt.  
- Jegliche Modifikationen müssen mit dem ursprünglichen Autor (Imam Kahraman) abgesprochen und unter derselben Lizenz veröffentlicht werden.
- Die Verwendung in proprietärer oder kommerzieller Software ist untersagt.

### Haftungsausschluss:
Dieses Add-on wird ohne jegliche Garantie oder Gewährleistung bereitgestellt. Der Autor übernimmt keine Verantwortung für Schäden oder Datenverluste, die durch die Nutzung dieses Add-ons entstehen könnten.

(C) 2025, Imam Kahraman

Lizenz: GNU General Public License v3 (GPL-3.0) (siehe LICENSE-Datei: https://www.gnu.org/licenses/gpl-3.0.txt)
