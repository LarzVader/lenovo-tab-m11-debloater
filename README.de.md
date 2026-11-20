# Lenovo Tab M11 Debloater

**[English version](README.md)**

Dein Lenovo Tab M11 bringt mehr mit, als du wolltest: ein Werbemodul, Lenovos
Nutzungsstatistik, eine Laden-Vorführung und einen Stapel Google-Apps. Dieses Werkzeug
entfernt, was du nicht willst, und du entscheidest App für App, was bleibt. Zu jeder App
steht da, was sie ist und was sich ohne sie ändert.

- **Ohne Root**: kein entsperrter Bootloader, kein Flashen. Das Werkzeug nutzt ADB, die
  Entwicklerwerkzeuge, die in Android eingebaut sind.
- **Umkehrbar**: Apps werden nur für deinen Nutzer entfernt. System-Apps holst du mit dem
  Werkzeug jederzeit zurück, und ein Zurücksetzen auf Werkseinstellungen bringt alles
  zurück.
- **Nur, was auf der Liste steht**: Das Werkzeug kann nur die Einträge unten entfernen. So
  kann es nicht aus Versehen etwas entfernen, das Android braucht.
- **Windows und Linux**, auf Deutsch und Englisch.

## So sieht es aus

```
1/5  Lenovo-Werbung, Datensammler und Laden-Vorführung
======================================================
Empfohlen zum Entfernen. Keine davon hat eine Funktion, die du vermissen würdest.

  1  ENTFERNEN       Tabtop Picks  (vorausgewählt, getestet)
      com.lenovo.rt
      Was:           Werbemodul des Werbenetzwerks Appnext. Schlägt Apps vor und zeigt
                     Werbe-Benachrichtigungen.
      Wenn entfernt: Keine App-Vorschläge und Werbe-Benachrichtigungen mehr. Sonst
                     ändert sich nichts.

  2  ENTFERNEN       AppServices (Aura)  (vorausgewählt, getestet)
      com.aura.oobe.lenovo
      Was:           App-Empfehlungsdienst Aura. Bietet bei der Einrichtung
                     Partner-Apps an.
      Wenn entfernt: Keine Angebote für Partner-Apps mehr. Sonst ändert sich nichts.
...
Nummern schalten bleibt/entfernen um (z. B. 1 3 5-7) | + alle entfernen | - alle
behalten | Enter = weiter | z = zurück | q = abbrechen
>
```

## Passt das zu deinem Tablet?

- **Lenovo Tab M11, Modell TB330FU** (WLAN): getestet mit ZUI 17.0.502 (Android 15) im
  November 2026.
- Das LTE-Modell **TB330XU** sollte genauso funktionieren, ist aber nicht getestet.
- Die Modellnummer steht unter Einstellungen > Über das Tablet.
- Andere Firmware-Versionen bringen womöglich andere Apps mit. Das Werkzeug zeigt nur Apps,
  die auf deinem Tablet sind.

## Was du brauchst

- Einen Computer mit Windows 10/11 oder Linux (macOS sollte auch gehen, ist aber nicht
  getestet)
- Python 3.8 oder neuer
- Ein USB-Kabel, das Daten überträgt (ein reines Ladekabel geht nicht)
- Etwa 10 Minuten

## Schritt für Schritt

### 1. USB-Debugging am Tablet einschalten

1. Öffne **Einstellungen > Über das Tablet** und tippe siebenmal auf **Build-Nummer**, bis
   das Tablet meldet, dass du jetzt Entwickler bist.
2. Öffne **Einstellungen > System > Entwickleroptionen** und schalte **USB-Debugging** ein.
3. Verbinde das Tablet mit deinem Computer.

Bei manchen Firmware-Versionen heißen die Menüs etwas anders.

### 2. Werkzeug holen

Klicke auf dieser Seite auf **Code > Download ZIP** und entpacke die Datei. Oder mit git:

```bash
git clone https://github.com/LarzVader/lenovo-tab-m11-debloater.git
```

### 3. Starten

**Windows:** Doppelklick auf `start-windows.bat`. Fehlt Python, steht das im Fenster.
Installiere es mit diesem Befehl oder von [python.org](https://www.python.org/downloads/)
(bei der Installation „Add python.exe to PATH“ anhaken) und starte die Datei erneut:

```
winget install -e --id Python.Python.3.13
```

**Linux:** Öffne ein Terminal im Ordner und starte:

```bash
./start-linux.sh
```

Das Werkzeug braucht ADB, das zu Googles „Platform-Tools“ gehört. Findet es kein ADB, bietet
es an, Googles offizielles Paket von dl.google.com in seinen eigenen Ordner zu laden.
Systemweit wird nichts installiert.

### 4. Computer am Tablet erlauben

Das Tablet fragt „USB-Debugging zulassen?“. Tippe auf **Zulassen**. Mit Haken bei „Von
diesem Computer immer zulassen“ fragt es nicht noch einmal.

**Nur Linux:** Meldet das Werkzeug, dass Linux keinen Zugriff auf das Tablet erlaubt, zeigt
es zwei Befehle, die eine udev-Regel für Lenovo-Geräte anlegen. Führe sie einmal aus und
stecke dann das Kabel ab und wieder an.

### 5. Auswählen

Wähle im Hauptmenü **1 Apps entfernen**. Das Werkzeug zeigt die Apps Seite für Seite, nach
Themen geordnet. Jede App ist mit **ENTFERNEN** oder **bleibt** markiert:

- Tippe die Nummern von Apps, um sie umzuschalten, zum Beispiel `1 3 5-7`.
- `+` markiert alle Apps der Seite zum Entfernen, `-` behält alle.
- Enter geht zur nächsten Seite, `z` zurück, `q` bricht ab.

Vorausgewählt sind nur Werbung, Datensammler und Laden-Vorführung. Alles andere bleibt, wenn
du es nicht umschaltest.

Am Ende siehst du eine Zusammenfassung, und es ändert sich nichts, bevor du sie bestätigst.
Dann entfernt das Werkzeug die Apps und bietet an, das Tablet neu zu starten. Das ist eine
gute Idee.

## Apps zurückholen

Starte das Werkzeug, wähle **2 Entfernte Apps zurückholen** und wähle die Apps über ihre
Nummern aus, oder tippe `+` für alle. Du kannst auch einen Paketnamen eintippen.

Ohne das Werkzeug holt dieser Befehl eine App zurück:

```bash
adb shell cmd package install-existing com.google.android.youtube
```

Einige wenige Apps gehören nicht zum System-Abbild. Das Werkzeug kennzeichnet sie mit
„Keine System-App“. Nach dem Entfernen kommen sie nur über den Play Store oder einen
Werksreset zurück.

## Die Liste

„Getestet“ heißt: an einem echten TB330FU entfernt, danach neu gestartet und geprüft.
Einträge mit „–“ wurden noch an keinem echten Tablet entfernt. Die id ist für die
Kommandozeile.

<!-- PACKAGES:START -->

### Lenovo-Werbung, Datensammler und Laden-Vorführung

Empfohlen zum Entfernen. Keine davon hat eine Funktion, die du vermissen würdest.

| App | Was es ist | Wenn entfernt | Vorausgewählt | Getestet |
|---|---|---|:-:|:-:|
| **Tabtop Picks**<br>`com.lenovo.rt`<br>id: `tabtop-picks` | Werbemodul des Werbenetzwerks Appnext. Schlägt Apps vor und zeigt Werbe-Benachrichtigungen. | Keine App-Vorschläge und Werbe-Benachrichtigungen mehr. Sonst ändert sich nichts. | ja | ja |
| **AppServices (Aura)**<br>`com.aura.oobe.lenovo`<br>id: `aura-appservices` | App-Empfehlungsdienst Aura. Bietet bei der Einrichtung Partner-Apps an. | Keine Angebote für Partner-Apps mehr. Sonst ändert sich nichts. | ja | ja |
| **Play Auto Installs (PAI)**<br>`android.autoinstalls.config.Lenovo.tablet`<br>id: `play-auto-installs` | Liste von Partner-Apps, die Google Play nach der Einrichtung automatisch installiert. | Wird nur direkt nach der Einrichtung gebraucht. Entfernen hat keine sichtbare Wirkung. | ja | ja |
| **Opera Preinstall Data**<br>`com.opera.preinstall`<br>id: `opera-preinstall` | Kleines Datenpaket mit Partnerdaten für den Opera-Browser. Opera selbst ist nicht installiert. | Keine. | ja | ja |
| **User Experience**<br>`com.lenovo.ue.device`<br>id: `user-experience` | Lenovos Nutzungsstatistik. Sammelt Daten über das Tablet und seine Nutzung und lädt sie hoch. | Lenovo bekommt diese Statistik nicht mehr. Sonst ändert sich nichts. | ja | ja |
| **Kundendienst für Einheit (Lenovo-Push)**<br>`com.tblenovo.tabpushout`<br>id: `lenovo-push` | Empfängt Push-Nachrichten von Lenovos Servern. | Keine Push-Nachrichten mehr von Lenovo. | ja | ja |
| **Tipps**<br>`com.tblenovo.lenovowhatsnew`<br>id: `tips` | Lenovos Tipps und „Was ist neu“-Hinweise. | Keine Tipps mehr. Sonst ändert sich nichts. | ja | ja |
| **UDS-Echtzeit-Engine**<br>`com.lenovo.tbengine`<br>id: `uds-engine` | Lenovo-Hintergrunddienst für Tipps und Push-Nachrichten, der auch Lenovo-Apps im Hintergrund herunterlädt und installiert. Läuft ständig. | Keine Tipps und Hintergrund-Installationen mehr und etwas mehr freier Arbeitsspeicher. Das Tablet lief ohne ihn normal. Nur deshalb nicht vorausgewählt, weil ohne ihn noch kein Systemupdate eingespielt wurde. | – | ja |
| **Lenovo Tab M11 (Laden-Präsentation)**<br>`com.lenovo.tab_m11`<br>id: `shop-presentation` | Produktvorstellung mit Videos für Vorführgeräte im Laden. | Für dich keine. | ja | ja |
| **Demomodus**<br>`com.motorola.demo`<br>id: `demo-mode` | Vorführmodus für Geräte im Laden. | Für dich keine. | ja | ja |
| **OCZ-Bereitstellungswerkzeuge**<br>`com.lenovo.dsa`<br>`com.lenovo.ocpl`<br>id: `ocz-deployment` | Lenovo-Werkzeuge, die Anpassungen und Apps herunterladen und einspielen, vermutlich für die Einrichtung vieler Geräte auf einmal (Firmen, Schulen, Läden). | Auf einem privaten Tablet keine. | ja | ja |

### Lenovo-Apps und -Funktionen

Echte Funktionen. Nur entfernen, wenn du sie nicht nutzt.

| App | Was es ist | Wenn entfernt | Vorausgewählt | Getestet |
|---|---|---|:-:|:-:|
| **Lenovo Vantage**<br>`com.tblenovo.center`<br>`com.tblenovo.ue.config`<br>id: `lenovo-vantage` | Lenovos Hilfe-App: Anleitung, Hardwaretests, Feedback und Shop. Läuft im Hintergrund. | Die App und ihre Hinweise verschwinden. In den Einstellungen unter „Über das Tablet“ fällt der Feedback-Eintrag weg, er gehört zu Vantage. Systemupdates kommen von der eigenen App „Systemupdate“, die bleibt. | – | ja |
| **Smart Connect**<br>`com.motorola.mobiledesktop`<br>`com.motorola.mobiledesktop.core`<br>`com.motorola.readyforsignature.app`<br>id: `smart-connect` | Lenovos Geräteverbund (basiert auf Motorolas „Ready For“): verbindet das Tablet mit PC oder Handy, zum Beispiel als zweiter Bildschirm oder zum Teilen von Dateien. Läuft im Hintergrund. | Smart Connect fällt weg. | – | ja |
| **LTHD (Diagnose für Lenovos PC-Programm)**<br>`com.lmsa.app.lmsapad`<br>id: `lthd` | Diagnose-Helfer für Lenovos PC-Supportprogramm (Rescue and Smart Assistant). | Nur wichtig, wenn du dieses PC-Programm benutzt. | – | – |
| **Notepad (Notizen)**<br>`com.zui.notes`<br>id: `lenovo-notepad` | Lenovos Notiz-App. | Die App verschwindet. Nur entfernen, wenn du darin keine Notizen hast. | – | – |
| **Wetter**<br>`com.zui.weather`<br>id: `lenovo-weather` | Lenovos Wetter-App mit dem Uhr- und Wetter-Widget. | Die App und ihr Widget auf dem Startbildschirm verschwinden. | – | – |

### Google: Video, Musik und Kinder

Entferne, was du nicht nutzt. Käufe und Abos bleiben in deinem Google-Konto.

| App | Was es ist | Wenn entfernt | Vorausgewählt | Getestet |
|---|---|---|:-:|:-:|
| **YouTube**<br>`com.google.android.youtube`<br>id: `youtube` | Googles Video-App. | Die App verschwindet; YouTube geht weiter im Browser. Sie kann im Hintergrund laufen, auch wenn du sie nie öffnest. | – | ja |
| **YouTube Music**<br>`com.google.android.apps.youtube.music`<br>`com.google.android.apps.youtube.music.setupwizard`<br>id: `youtube-music` | Googles Musik-App. | Die App verschwindet; music.youtube.com geht weiter im Browser. | – | ja |
| **Google TV**<br>`com.google.android.videos`<br>id: `google-tv` | Googles App zum Leihen und Kaufen von Filmen und Serien. | Die App verschwindet. Sie kann im Hintergrund laufen, auch wenn du sie nie öffnest. | – | ja |
| **Entertainment Space**<br>`com.google.android.apps.mediahome.launcher`<br>id: `entertainment-space` | Googles Seite mit Empfehlungen für Videos, Spiele und Bücher. | Die Empfehlungsseite verschwindet. Sie kann im Hintergrund laufen, auch wenn du sie nie öffnest. | – | ja |
| **Kids Space**<br>`com.google.android.apps.kids.home`<br>id: `kids-space` | Googles kindgerechter Modus mit ausgewählten Apps, Büchern und Videos. | Den Kindermodus gibt es dann nicht mehr. | – | ja |

### Google: Mail, Nachrichten und Anrufe

Entferne, was du nicht nutzt.

| App | Was es ist | Wenn entfernt | Vorausgewählt | Getestet |
|---|---|---|:-:|:-:|
| **Gmail**<br>`com.google.android.gm`<br>id: `gmail` | Googles Mail-App. | Die App verschwindet; deine Mails bleiben im Konto (mail.google.com). Mail-Links öffnen sich in einer anderen Mail-App, falls du eine hast. | – | ja |
| **Google Messages**<br>`com.google.android.apps.messaging`<br>id: `google-messages` | Googles SMS- und RCS-App. | Auf dem WLAN-Modell (TB330FU) nützt sie nur, wenn du sie mit deinem Handy koppelst, um dessen Nachrichten zu lesen. Auf dem LTE-Modell (TB330XU) ist sie die SMS-App: dort behalten, wenn du SMS nutzt. | – | ja |
| **Google Meet**<br>`com.google.android.apps.tachyon`<br>id: `google-meet` | Googles Videoanrufe. | Keine Meet-App; meet.google.com geht weiter im Browser. | – | ja |

### Google: weitere Apps und Dienste

Einige davon sind Alltags-Apps. Lies vor dem Entfernen, was sich ändert.

| App | Was es ist | Wenn entfernt | Vorausgewählt | Getestet |
|---|---|---|:-:|:-:|
| **Google-App und Assistant**<br>`com.google.android.googlequicksearchbox`<br>`com.google.android.apps.googleassistant`<br>`com.android.hotwordenrollment.okgoogle`<br>`com.android.hotwordenrollment.xgoogle`<br>id: `google-app` | Google-Suche mit Such-Widget, Google Assistant („Hey Google“) und Discover-Feed. | Das Such-Widget verschwindet vom Startbildschirm, und es gibt keinen digitalen Assistenten mehr. Die Spracheingabe in Gboard kann danach fehlen (noch nicht getestet). | – | ja |
| **Chrome**<br>`com.android.chrome`<br>id: `chrome` | Googles Webbrowser. | Vorher einen anderen Browser installieren! Webseiten in anderen Apps gehen weiter, weil sie „Android System WebView“ nutzen, das bleibt. Das Werkzeug prüft das, bevor es Chrome entfernt. | – | – |
| **Google Maps**<br>`com.google.android.apps.maps`<br>id: `google-maps` | Karten und Navigation. | Keine Karten-App; Karten-Links öffnen sich im Browser. | – | ja |
| **Google Fotos**<br>`com.google.android.apps.photos`<br>id: `google-photos` | Galerie und Googles Foto-Cloud. | Die Sicherung zu Google Fotos endet; deine Bilder bleiben auf dem Tablet. Womöglich ist sie die einzige Galerie-App: Dann siehst du Bilder über einen Dateimanager an oder installierst eine andere Galerie. | – | ja |
| **Digital Wellbeing**<br>`com.google.android.apps.wellbeing`<br>id: `digital-wellbeing` | Bildschirmzeit-Statistik, App-Timer, Schlafenszeit- und Konzentrationsmodus. Läuft im Hintergrund. | Diese Funktionen fallen weg. | – | ja |
| **Google Play-Dienste für AR (ARCore)**<br>`com.google.ar.core`<br>id: `arcore` | Erweiterte Realität (AR) für Apps. | Apps können kein AR mehr nutzen. Du kannst es jederzeit wieder aus dem Play Store installieren. | – | ja |
| **Cross-Device Services (geräteübergreifende Dienste)**<br>`com.google.ambient.streaming`<br>id: `cross-device` | Googles Funktionen für Apps über Gerätegrenzen hinweg, zum Beispiel Apps auf ein Chromebook streamen. | Diese geräteübergreifenden Funktionen gehen nicht mehr. | – | ja |
| **Google Wi-Fi Provisioner**<br>`com.google.android.apps.carrier.carrierwifi`<br>id: `wifi-provisioner` | Netzbetreiber-WLAN, automatische Anmeldung an öffentlichen OpenRoaming-Hotspots mit dem Google-Konto und eine WLAN-Bewertung. Läuft im Hintergrund. | Normales WLAN geht weiter (getestet). Die automatische Anmeldung an OpenRoaming-Hotspots fällt weg. | – | ja |
| **Google Drive**<br>`com.google.android.apps.docs`<br>id: `google-drive` | Googles Cloud-Speicher. | Keine Drive-App; deine Dateien bleiben im Konto (drive.google.com). | – | – |
| **Google Kalender**<br>`com.google.android.calendar`<br>id: `google-calendar` | Kalender-App. | Keine Kalender-App; deine Termine bleiben im Konto. | – | – |
| **Google Kontakte**<br>`com.google.android.contacts`<br>id: `google-contacts` | Kontakte-App. | Keine Kontakte-App; die Kontakte selbst bleiben gespeichert. Apps, in denen du einen Kontakt auswählst, können das womöglich nicht mehr. | – | – |
| **Uhr**<br>`com.google.android.deskclock`<br>id: `google-clock` | Wecker, Timer, Stoppuhr und Weltuhr. | Kein Wecker und kein Timer mehr! | – | – |
| **Rechner**<br>`com.google.android.calculator`<br>id: `google-calculator` | Taschenrechner. | Kein Taschenrechner mehr. | – | – |
| **Files by Google**<br>`com.google.android.apps.nbu.files`<br>id: `files-by-google` | Dateimanager und Speicher-Aufräumer. | Der Dateimanager verschwindet. Apps können weiter über die Dateiauswahl des Systems Dateien öffnen und speichern, die bleibt. | – | – |
| **Android System Key Verifier**<br>`com.google.android.contactkeys`<br>id: `key-verifier` | Prüft die Verschlüsselungsschlüssel deiner Kontakte in Messenger-Apps. | Die Schlüsselprüfung fällt weg. Google Play installiert sie womöglich wieder. | – | – |

<!-- PACKAGES:END -->

## Bewusst nicht auf der Liste

Diese bleiben, weil das Tablet sie braucht oder weil noch niemand weiß, was ohne sie
passiert:

- **Google Play Store und Google-Play-Dienste**: Apps, Updates, Anmeldung
- **Gboard**: die einzige Tastatur auf dem Tablet
- **Android System WebView**: zeigt Webseiten in Apps an
- **Systemupdate** (`com.lenovo.ota`), **Lenovo-ID** und **Gerätedienst**
  (`com.lenovo.lsf`, `com.lenovo.lsf.device`): Systemupdates hängen womöglich daran
- **Gesichtserkennung** (`com.tbsmart.levision`): Entsperren per Gesicht
- **Stift** (`com.lenovo.penservice`), **Dolby**, **SarReduce** (hält die Sendeleistung in
  den Grenzwerten für Strahlung), Launcher, Kamera und Einstellungen
- **Google Play Protect** (`com.google.android.odad`)
- **Android Developer Verifier** (`com.google.android.verifier`): Googles neue Prüfung für
  Apps, die nicht aus dem Play Store kommen. Was ohne ihn mit solchen Installationen
  passiert, weiß noch niemand.

## Gut zu wissen

- Entfernte Apps laufen nicht, bekommen keine Updates und tauchen nirgends auf. Ihre Daten
  bleiben auf dem Tablet (`pm uninstall -k`), eine zurückgeholte App findet ihre Daten also
  wieder.
- Es ändert sich nur der Hauptnutzer. Ein zweiter Nutzer oder ein Arbeitsprofil behält seine
  Apps.
- Ein Systemupdate bringt womöglich einzelne Apps zurück. Starte das Werkzeug dann einfach
  noch einmal.
- Ein Zurücksetzen auf Werkseinstellungen bringt alle Apps zurück.
- Jede Änderung steht in `m11-debloater.log` im Ordner des Werkzeugs.

## Kommandozeile

Die Menüs sind kein Muss. Alle Optionen: `python3 m11_debloater.py --help`

| Option | Was sie tut |
|---|---|
| `--lang de`, `--lang en` | Sprache. Ohne die Option nimmt das Werkzeug die Sprache deines Systems. |
| `--dry-run` | Ändert nichts und zeigt die Befehle, die es ausführen würde. |
| `--list` | Zeigt die Liste mit dem Stand auf deinem Tablet und den ids. |
| `--remove recommended` | Entfernt die vorausgewählten Apps ohne Menüs. |
| `--remove youtube,google-tv` | Entfernt diese Einträge (ids aus der Liste). |
| `--restore all` | Holt alle entfernten Apps aus der Liste zurück. |
| `--restore youtube` | Holt diese Einträge zurück. |
| `--yes` | Fragt nicht nach (mit `--remove` oder `--restore`). |
| `--reboot` | Startet das Tablet nach `--remove` neu. |
| `--serial SERIAL` | Wählt das Gerät, wenn mehrere verbunden sind. |
| `--adb PFAD` | Nimmt dieses adb. |
| `--force` | Überspringt die Modellprüfung. |
| `--no-color` | Text ohne Farben. |

Beispiel: die vorausgewählten Apps ohne Nachfrage entfernen und danach neu starten:

```bash
python3 m11_debloater.py --remove recommended --yes --reboot
```

## Wenn etwas nicht klappt

- **„Kein Tablet gefunden“**: Prüfe das Kabel (reine Ladekabel gehen nicht) und ob
  USB-Debugging an ist, und versuche einen anderen USB-Anschluss.
- **Das Tablet fragt nie „USB-Debugging zulassen?“**: Kabel ab- und wieder anstecken. In den
  Entwickleroptionen „USB-Debugging-Autorisierungen widerrufen“ und erneut versuchen.
- **Linux meldet „no permissions“**: Führe die zwei udev-Befehle aus, die das Werkzeug
  zeigt.
- **Eine App fehlt dir**: Hol sie zurück (siehe oben).
- **Das Tablet benimmt sich seltsam**: Hol alles mit `--restore all` zurück und starte neu.
  Ein Zurücksetzen auf Werkseinstellungen bringt alles zurück, löscht aber auch deine Daten.

## Risiken

Du nutzt dieses Werkzeug auf eigene Gefahr. Es entfernt Apps nur für deinen Nutzer und nur
von seiner Liste, und es wurde an einem TB330FU mit der oben genannten Firmware getestet.
Einträge mit „noch nicht getestet“ wurden bisher an keinem echten Tablet entfernt. Wenn du
einen ausprobierst, erzähl uns bitte, wie es lief.

Dieses Projekt hat nichts mit Lenovo oder Google zu tun.

## Mithelfen an der Liste

Hat dein M11 andere Apps, oder hast du einen Eintrag getestet? Dann öffne bitte ein
[Issue](https://github.com/LarzVader/lenovo-tab-m11-debloater/issues) mit:

- Modell und Firmware (Einstellungen > Über das Tablet)
- was du entfernt hast und was passiert ist
- bei Apps, die auf der Liste fehlen: dem Paketnamen. `adb shell pm list packages -s` listet
  nur System-Apps, so gibst du nicht preis, welche Apps du selbst installiert hast.

Nach einer Änderung an `packages.json` aktualisiert `python3 tools/make_tables.py` die
Tabellen in beiden READMEs.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
