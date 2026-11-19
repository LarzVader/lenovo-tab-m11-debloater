#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Lenovo Tab M11 Debloater - https://github.com/LarzVader/lenovo-tab-m11-debloater
"""Remove preinstalled apps from a Lenovo Tab M11 over ADB.

Apps are removed only for the main user (pm uninstall -k --user 0): no root,
nothing is deleted from the system partitions, and system apps can be restored
at any time. Only apps listed in packages.json can be removed.
"""

import argparse
import datetime
import json
import locale
import os
import re
import shutil
import subprocess
import sys
import textwrap
import time
import urllib.request
import zipfile

VERSION = "1.0.0"
SUPPORTED_MODELS = ("TB330FU", "TB330XU")
USER = "0"
PKG_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+$")

if getattr(sys, "frozen", False):  # packed with PyInstaller
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
    DATA_DIR = getattr(sys, "_MEIPASS", APP_DIR)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = APP_DIR

CATALOG_PATH = os.path.join(DATA_DIR, "packages.json")
LOG_NAME = "m11-debloater.log"
PT_URL = "https://dl.google.com/android/repository/platform-tools-latest-{}.zip"
PT_INFO_URL = "https://developer.android.com/tools/releases/platform-tools"
SDK_TERMS_URL = "https://developer.android.com/studio/terms"
UDEV_CMDS = [
    "echo 'SUBSYSTEM==\"usb\", ATTR{idVendor}==\"17ef\", MODE=\"0660\", TAG+=\"uaccess\"' "
    "| sudo tee /etc/udev/rules.d/51-android-lenovo.rules",
    "sudo udevadm control --reload-rules && sudo udevadm trigger",
]

# --------------------------------------------------------------------------
# Texts
# --------------------------------------------------------------------------

S = {
    "en": {
        "intro": "Removes preinstalled apps from your Lenovo Tab M11, only for your user and "
                 "without root. System apps can be restored at any time, and a factory reset "
                 "brings everything back.",
        "dry_run": "Dry run: nothing is changed on the tablet.",
        "catalog_missing": "packages.json was not found next to the program. Download the "
                           "complete folder (on GitHub: Code > Download ZIP).",
        "catalog_broken": "packages.json is damaged: {err}",
        "adb_using": "ADB: {path}",
        "adb_missing": "ADB (Android platform tools) was not found.",
        "adb_offer": "I can download Google's official platform tools (a few MB) from "
                     "dl.google.com into this folder. By downloading them you accept Google's "
                     "terms: {terms}",
        "adb_offer_q": "Download now?",
        "adb_manual": "Install the platform tools yourself and start this tool again: {url}",
        "dl_progress": "Downloading ... {pct}",
        "dl_done": "Platform tools ready: {path}",
        "dl_failed": "Download failed: {err}",
        "adb_broken": "ADB does not work: {err}",
        "dev_wait": "Looking for the tablet ... (Ctrl+C to quit)",
        "dev_none": "No tablet found. Please check:\n"
                    "- The USB cable is plugged in (a data cable, not a charge-only cable).\n"
                    "- On the tablet: Settings > About tablet > tap \"Build number\" seven "
                    "times. Then Settings > System > Developer options > turn on \"USB "
                    "debugging\".",
        "dev_unauthorized": "The tablet is asking for permission. On the tablet, tap \"Allow\" "
                            "in the \"Allow USB debugging?\" window (best with a tick at "
                            "\"Always allow from this computer\").",
        "dev_no_permissions": "Linux does not allow access to the tablet. Run these two "
                              "commands once in a terminal (they add a udev rule for Lenovo "
                              "devices), then unplug the cable and plug it in again:",
        "dev_offline": "The tablet is connected, but \"offline\". Unplug the cable and plug it "
                       "in again.",
        "dev_other": "The tablet reports the state \"{state}\". Waiting ...",
        "dev_keep_waiting": "Still no tablet. Keep waiting?",
        "dev_choose": "Several devices are connected. Which one?",
        "dev_use_serial": "Choose one with --serial.",
        "dev_connected": "Connected: {model}, Android {android}, {build}",
        "model_unknown": "This tool is made for the Lenovo Tab M11 (TB330FU / TB330XU). Your "
                         "device reports \"{model}\". You will only see apps from the list that "
                         "exist on your device, but the descriptions may not fit.",
        "model_q": "Continue anyway?",
        "fw_note": "Tested with {tested}. Your firmware is different, so some apps may differ. "
                   "The tool only shows apps that are on your tablet.",
        "pm_failed": "Could not read the list of apps from the tablet: {err}",
        "menu_title": "What do you want to do?",
        "menu_remove": "Remove apps (you choose what stays)",
        "menu_restore": "Restore removed apps",
        "menu_list": "Show the list with the status on your tablet",
        "menu_lang": "Deutsch",
        "menu_quit": "Quit",
        "menu_prompt": "Choice: ",
        "how_it_works": "You will see the apps page by page. For each app you can read what it "
                        "is and what changes without it. Apps marked REMOVE will be removed. "
                        "Nothing happens until you confirm at the end.",
        "tag_keep": "keep",
        "tag_remove": "REMOVE",
        "tag_removed": "already removed",
        "tag_locked": "locked",
        "badge_recommended": "preselected",
        "badge_tested": "tested",
        "badge_untested": "not tested yet",
        "lbl_what": "What:",
        "lbl_effect": "If removed:",
        "not_system": "Not a system app: after removal it can only come back from the Play "
                      "Store or with a factory reset.",
        "page_help": "Numbers switch keep/remove (e.g. 1 3 5-7) | + remove all | - keep all | "
                     "Enter = next | b = back | q = cancel",
        "bad_input": "Did not understand \"{x}\".",
        "is_removed": "{n} is already removed. To get it back, use \"Restore removed apps\" in "
                      "the main menu.",
        "is_locked": "{n} is locked: {why}",
        "guard_webview": "Chrome provides the web view for other apps on this tablet. Without it, "
                         "web pages inside apps would stop working.",
        "sum_title": "Summary",
        "sum_remove": "These apps will be removed ({n}):",
        "sum_nothing": "Nothing selected. Nothing will be changed.",
        "sum_keep": "Everything else stays.",
        "sum_q": "Remove them now?",
        "cancelled": "Cancelled. Nothing was changed.",
        "run_line": "[{i}/{n}] {pkg} ... ",
        "ok": "OK",
        "failed": "FAILED",
        "dry_cmd": "would run: {cmd}",
        "rm_done": "Done: {ok} removed, {fail} failed.",
        "still_installed": "Still installed: {pkgs}",
        "reboot_q": "Restart the tablet now? (recommended)",
        "rebooting": "The tablet restarts.",
        "log_at": "Log file: {path}",
        "rest_none": "No removed apps from the list were found on your tablet.",
        "rest_title": "Removed apps from the list:",
        "rest_help": "Numbers to restore (e.g. 1 3) | + = all | or a package name | Enter = back",
        "rest_unknown_pkg": "{pkg} is not a removed app on this tablet.",
        "rest_q": "Restore now? ({n} package(s))",
        "rest_done": "Done: {ok} restored, {fail} failed.",
        "rest_missing": "Not restored: {pkgs}",
        "rest_hint": "Apps that could not be restored are not part of the system. Install them "
                     "from the Play Store.",
        "st_installed": "installed",
        "st_removed": "removed",
        "st_absent": "not present",
        "list_title": "The list ({n} entries)",
        "unknown_ids": "Unknown entries: {ids}. Valid entries: {valid}",
        "yn_y": "[Y/n]",
        "yn_n": "[y/N]",
        "aborted": "Aborted.",
        "press_enter": "Press Enter to continue.",
    },
    "de": {
        "intro": "Entfernt vorinstallierte Apps von deinem Lenovo Tab M11, nur für deinen "
                 "Nutzer und ohne Root. System-Apps lassen sich jederzeit zurückholen, und ein "
                 "Zurücksetzen auf Werkseinstellungen bringt alles zurück.",
        "dry_run": "Probelauf: Am Tablet wird nichts geändert.",
        "catalog_missing": "packages.json liegt nicht neben dem Programm. Lade den ganzen Ordner "
                           "herunter (auf GitHub: Code > Download ZIP).",
        "catalog_broken": "packages.json ist beschädigt: {err}",
        "adb_using": "ADB: {path}",
        "adb_missing": "ADB (Android Platform-Tools) wurde nicht gefunden.",
        "adb_offer": "Ich kann Googles offizielle Platform-Tools (ein paar MB) von dl.google.com "
                     "in diesen Ordner laden. Mit dem Herunterladen akzeptierst du Googles "
                     "Bedingungen: {terms}",
        "adb_offer_q": "Jetzt herunterladen?",
        "adb_manual": "Installiere die Platform-Tools selbst und starte dieses Werkzeug dann "
                      "erneut: {url}",
        "dl_progress": "Lade herunter ... {pct}",
        "dl_done": "Platform-Tools bereit: {path}",
        "dl_failed": "Herunterladen fehlgeschlagen: {err}",
        "adb_broken": "ADB funktioniert nicht: {err}",
        "dev_wait": "Suche das Tablet ... (Strg+C zum Beenden)",
        "dev_none": "Kein Tablet gefunden. Bitte prüfe:\n"
                    "- Das USB-Kabel steckt (ein Datenkabel, kein reines Ladekabel).\n"
                    "- Am Tablet: Einstellungen > Über das Tablet > siebenmal auf "
                    "„Build-Nummer“ tippen. Dann Einstellungen > System > Entwickleroptionen > "
                    "„USB-Debugging“ einschalten.",
        "dev_unauthorized": "Das Tablet fragt nach Erlaubnis. Tippe am Tablet im Fenster "
                            "„USB-Debugging zulassen?“ auf „Zulassen“ (am besten mit Haken bei "
                            "„Von diesem Computer immer zulassen“).",
        "dev_no_permissions": "Linux erlaubt keinen Zugriff auf das Tablet. Führe diese zwei "
                              "Befehle einmal im Terminal aus (sie legen eine udev-Regel für "
                              "Lenovo-Geräte an) und stecke dann das Kabel ab und wieder an:",
        "dev_offline": "Das Tablet ist verbunden, aber „offline“. Stecke das Kabel ab und wieder "
                       "an.",
        "dev_other": "Das Tablet meldet den Zustand „{state}“. Warte ...",
        "dev_keep_waiting": "Immer noch kein Tablet. Weiter warten?",
        "dev_choose": "Mehrere Geräte sind verbunden. Welches?",
        "dev_use_serial": "Wähle eines mit --serial aus.",
        "dev_connected": "Verbunden: {model}, Android {android}, {build}",
        "model_unknown": "Dieses Werkzeug ist für das Lenovo Tab M11 (TB330FU / TB330XU). Dein "
                         "Gerät meldet „{model}“. Du siehst nur Apps aus der Liste, die es auf "
                         "deinem Gerät gibt, aber die Beschreibungen passen womöglich nicht.",
        "model_q": "Trotzdem weitermachen?",
        "fw_note": "Getestet mit {tested}. Deine Firmware ist eine andere, einige Apps können "
                   "abweichen. Das Werkzeug zeigt nur Apps, die auf deinem Tablet sind.",
        "pm_failed": "Konnte die Liste der Apps nicht vom Tablet lesen: {err}",
        "menu_title": "Was möchtest du tun?",
        "menu_remove": "Apps entfernen (du wählst, was bleibt)",
        "menu_restore": "Entfernte Apps zurückholen",
        "menu_list": "Liste mit dem Stand auf deinem Tablet anzeigen",
        "menu_lang": "English",
        "menu_quit": "Beenden",
        "menu_prompt": "Auswahl: ",
        "how_it_works": "Du siehst die Apps Seite für Seite. Zu jeder App steht, was sie ist und "
                        "was sich ohne sie ändert. Apps mit ENTFERNEN werden entfernt. Es "
                        "passiert nichts, bevor du am Ende bestätigst.",
        "tag_keep": "bleibt",
        "tag_remove": "ENTFERNEN",
        "tag_removed": "schon entfernt",
        "tag_locked": "gesperrt",
        "badge_recommended": "vorausgewählt",
        "badge_tested": "getestet",
        "badge_untested": "noch nicht getestet",
        "lbl_what": "Was:",
        "lbl_effect": "Wenn entfernt:",
        "not_system": "Keine System-App: Nach dem Entfernen kommt sie nur über den Play Store "
                      "oder einen Werksreset zurück.",
        "page_help": "Nummern schalten bleibt/entfernen um (z. B. 1 3 5-7) | + alle entfernen | "
                     "- alle behalten | Enter = weiter | z = zurück | q = abbrechen",
        "bad_input": "„{x}“ nicht verstanden.",
        "is_removed": "{n} ist schon entfernt. Zurückholen kannst du sie im Hauptmenü unter "
                      "„Entfernte Apps zurückholen“.",
        "is_locked": "{n} ist gesperrt: {why}",
        "guard_webview": "Chrome stellt auf diesem Tablet die Webansicht für andere Apps bereit. "
                         "Ohne Chrome würden Webseiten in Apps nicht mehr gehen.",
        "sum_title": "Zusammenfassung",
        "sum_remove": "Diese Apps werden entfernt ({n}):",
        "sum_nothing": "Nichts ausgewählt. Es wird nichts geändert.",
        "sum_keep": "Alles andere bleibt.",
        "sum_q": "Jetzt entfernen?",
        "cancelled": "Abgebrochen. Es wurde nichts geändert.",
        "run_line": "[{i}/{n}] {pkg} ... ",
        "ok": "OK",
        "failed": "FEHLER",
        "dry_cmd": "würde ausführen: {cmd}",
        "rm_done": "Fertig: {ok} entfernt, {fail} fehlgeschlagen.",
        "still_installed": "Noch installiert: {pkgs}",
        "reboot_q": "Tablet jetzt neu starten? (empfohlen)",
        "rebooting": "Das Tablet startet neu.",
        "log_at": "Protokoll: {path}",
        "rest_none": "Auf deinem Tablet sind keine entfernten Apps aus der Liste.",
        "rest_title": "Entfernte Apps aus der Liste:",
        "rest_help": "Nummern zum Zurückholen (z. B. 1 3) | + = alle | oder ein Paketname | "
                     "Enter = zurück",
        "rest_unknown_pkg": "{pkg} ist auf diesem Tablet keine entfernte App.",
        "rest_q": "Jetzt zurückholen? ({n} Paket(e))",
        "rest_done": "Fertig: {ok} zurückgeholt, {fail} fehlgeschlagen.",
        "rest_missing": "Nicht zurückgeholt: {pkgs}",
        "rest_hint": "Apps, die sich nicht zurückholen ließen, gehören nicht zum System. "
                     "Installiere sie über den Play Store.",
        "st_installed": "installiert",
        "st_removed": "entfernt",
        "st_absent": "nicht vorhanden",
        "list_title": "Die Liste ({n} Einträge)",
        "unknown_ids": "Unbekannte Einträge: {ids}. Gültig sind: {valid}",
        "yn_y": "[J/n]",
        "yn_n": "[j/N]",
        "aborted": "Abgebrochen.",
        "press_enter": "Weiter mit Enter.",
    },
}

LANG = "en"


def t(key, **kw):
    text = S[LANG].get(key) or S["en"][key]
    return text.format(**kw) if kw else text


def loc(d):
    """Pick the current language from a {"en": ..., "de": ...} dict."""
    return d.get(LANG) or d.get("en") or ""


def detect_lang():
    if os.name == "nt":
        try:
            import ctypes
            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return "de" if (langid & 0x3FF) == 0x07 else "en"
        except Exception:
            pass
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        value = os.environ.get(var, "")
        if value:
            return "de" if value.lower().startswith("de") else "en"
    try:
        name = locale.getlocale()[0] or ""
    except Exception:
        name = ""
    return "de" if name.lower().startswith(("de", "german")) else "en"


# --------------------------------------------------------------------------
# Terminal output and input
# --------------------------------------------------------------------------

COLOR = False


def setup_terminal(no_color):
    global COLOR
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    if no_color or os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        COLOR = False
        return
    if os.name == "nt":
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            handle = kernel.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if kernel.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel.SetConsoleMode(handle, mode.value | 0x0004)
                COLOR = True
        except Exception:
            COLOR = False
    else:
        COLOR = os.environ.get("TERM") != "dumb"


def _c(code, text):
    return "\033[%sm%s\033[0m" % (code, text) if COLOR else text


def bold(text):
    return _c("1", text)


def dim(text):
    return _c("2", text)


def red(text):
    return _c("1;31", text)


def green(text):
    return _c("32", text)


def yellow(text):
    return _c("33", text)


def cyan(text):
    return _c("1;36", text)


def width():
    return max(40, min(100, shutil.get_terminal_size((80, 24)).columns - 1))


def say(text="", indent=0, hang=None):
    """Print plain text wrapped to the terminal width, keeping line breaks."""
    if not text:
        print()
        return
    first = " " * indent
    rest = " " * (indent if hang is None else hang)
    for para in str(text).split("\n"):
        if not para.strip():
            print()
            continue
        print(textwrap.fill(para, width(), initial_indent=first, subsequent_indent=rest,
                            break_long_words=False, break_on_hyphens=False))


def heading(text):
    print()
    print(cyan(text))
    print(cyan("=" * min(len(text), width())))


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        print()
        raise KeyboardInterrupt


def confirm(question, default=False):
    hint = t("yn_y") if default else t("yn_n")
    while True:
        answer = ask("%s %s " % (question, hint)).lower()
        if not answer:
            return default
        if answer in ("y", "yes", "j", "ja"):
            return True
        if answer in ("n", "no", "nein"):
            return False


def parse_numbers(text, count):
    """'1 3 5-7' -> [1, 3, 5, 6, 7]. Returns (numbers, bad_token)."""
    numbers = set()
    for token in re.split(r"[\s,;]+", text.strip()):
        if not token:
            continue
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", token)
        if not match:
            return None, token
        low, high = int(match.group(1)), int(match.group(2) or match.group(1))
        if low > high:
            low, high = high, low
        if low < 1 or high > count:
            return None, token
        numbers.update(range(low, high + 1))
    return sorted(numbers), None


# --------------------------------------------------------------------------
# Log file
# --------------------------------------------------------------------------

class Log:
    def __init__(self, enabled=True):
        self.path = None
        folders = (APP_DIR, os.path.expanduser("~")) if enabled else ()
        for folder in folders:
            path = os.path.join(folder, LOG_NAME)
            try:
                with open(path, "a", encoding="utf-8"):
                    pass
                self.path = path
                break
            except OSError:
                continue

    def write(self, message):
        if not self.path:
            return
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.path, "a", encoding="utf-8") as handle:
                handle.write("%s  %s\n" % (stamp, message))
        except OSError:
            pass


# --------------------------------------------------------------------------
# ADB
# --------------------------------------------------------------------------

class Adb:
    def __init__(self, path):
        self.path = path
        self.serial = None

    def run(self, args, timeout=60, device=True):
        cmd = [self.path]
        if device and self.serial:
            cmd += ["-s", self.serial]
        cmd += args
        try:
            # stdin=DEVNULL: "adb shell" would otherwise read (and swallow) the user's input
            proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired:
            return 124, "timeout"
        except OSError as err:
            return 127, str(err)
        text = proc.stdout.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
        return proc.returncode, text.strip()

    def shell(self, command, timeout=60):
        return self.run(["shell", command], timeout=timeout)

    def devices(self):
        """List of (serial, state) as reported by 'adb devices'."""
        code, text = self.run(["devices"], timeout=30, device=False)
        if code != 0:
            raise RuntimeError(text or "adb devices failed")
        lines = text.splitlines()
        start = 0
        for index, line in enumerate(lines):
            if line.startswith("List of devices"):
                start = index + 1
                break
        found = []
        for line in lines[start:]:
            line = line.strip()
            if not line or line.startswith("*"):
                continue
            parts = line.split(None, 1)
            serial = parts[0]
            rest = parts[1].strip() if len(parts) > 1 else ""
            state = "no permissions" if rest.startswith("no permissions") else (rest.split() or ["?"])[0]
            found.append((serial, state))
        return found


def adb_works(path):
    try:
        proc = subprocess.run([path, "version"], stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
        return proc.returncode == 0, proc.stdout.decode("utf-8", "replace").strip()
    except (OSError, subprocess.TimeoutExpired) as err:
        return False, str(err)


def find_adb(explicit):
    exe = "adb.exe" if os.name == "nt" else "adb"
    candidates = [explicit, os.environ.get("ADB"), shutil.which("adb"),
                  os.path.join(APP_DIR, "platform-tools", exe)]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def download_platform_tools():
    system = {"win32": "windows", "darwin": "darwin"}.get(sys.platform, "linux")
    url = PT_URL.format(system)
    archive = os.path.join(APP_DIR, "platform-tools.zip")
    try:
        with urllib.request.urlopen(url, timeout=60) as response, open(archive, "wb") as out:
            total = int(response.headers.get("Content-Length") or 0)
            done = 0
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                out.write(chunk)
                done += len(chunk)
                pct = "%d %%" % (done * 100 // total) if total else "%d KB" % (done // 1024)
                sys.stdout.write("\r" + t("dl_progress", pct=pct) + "   ")
                sys.stdout.flush()
        print()
        with zipfile.ZipFile(archive) as zipped:
            for member in zipped.infolist():
                parts = member.filename.replace("\\", "/").split("/")
                if parts[0] != "platform-tools" or ".." in parts:
                    continue
                zipped.extract(member, APP_DIR)
        os.remove(archive)
        folder = os.path.join(APP_DIR, "platform-tools")
        if os.name != "nt":
            for name in ("adb", "fastboot"):
                path = os.path.join(folder, name)
                if os.path.exists(path):
                    os.chmod(path, 0o755)
        path = os.path.join(folder, "adb.exe" if os.name == "nt" else "adb")
        return path if os.path.isfile(path) else None
    except Exception as err:  # network, disk or archive problems
        print()
        say(red(t("dl_failed", err=err)))
        try:
            os.remove(archive)
        except OSError:
            pass
        return None


def get_adb(explicit, interactive):
    if explicit and not os.path.isfile(explicit):
        say(red(t("adb_broken", err=explicit)))
        return None
    path = find_adb(explicit)
    if not path:
        say(yellow(t("adb_missing")))
        if not interactive:
            say(t("adb_manual", url=PT_INFO_URL))
            return None
        say(t("adb_offer", terms=SDK_TERMS_URL))
        if not confirm(t("adb_offer_q"), default=True):
            say(t("adb_manual", url=PT_INFO_URL))
            return None
        path = download_platform_tools()
        if not path:
            say(t("adb_manual", url=PT_INFO_URL))
            return None
        say(green(t("dl_done", path=path)))
    works, info = adb_works(path)
    if not works:
        say(red(t("adb_broken", err=info)))
        return None
    print(dim(t("adb_using", path=path)))
    return Adb(path)


def wait_for_device(adb, wanted, interactive):
    """Wait until exactly one ready device is chosen. Returns the serial or None."""
    say(t("dev_wait"))
    shown = None
    started = time.time()
    while True:
        try:
            devices = adb.devices()
        except RuntimeError as err:
            say(red(t("adb_broken", err=err)))
            return None
        if wanted:
            devices = [d for d in devices if d[0] == wanted]
        ready = [serial for serial, state in devices if state == "device"]
        if len(ready) == 1:
            return ready[0]
        if len(ready) > 1:
            say(t("dev_choose"))
            for number, serial in enumerate(ready, 1):
                print("  %d  %s" % (number, serial))
            if not interactive:
                say(t("dev_use_serial"))
                return None
            while True:
                picked, _ = parse_numbers(ask(t("menu_prompt")), len(ready))
                if picked and len(picked) == 1:
                    return ready[picked[0] - 1]
        states = [state for _, state in devices]
        if not states:
            key = "none"
        elif "unauthorized" in states:
            key = "unauthorized"
        elif "no permissions" in states:
            key = "no permissions"
        elif "offline" in states:
            key = "offline"
        else:
            key = states[0]
        if key != shown:
            shown = key
            print()
            if key == "none":
                say(t("dev_none"), hang=2)
            elif key == "unauthorized":
                say(yellow(t("dev_unauthorized")))
            elif key == "no permissions":
                say(yellow(t("dev_no_permissions")))
                for line in UDEV_CMDS:
                    print("    " + line)
            elif key == "offline":
                say(yellow(t("dev_offline")))
            else:
                say(t("dev_other", state=key))
        if not interactive:
            return None
        if time.time() - started > 180:
            if not confirm(t("dev_keep_waiting"), default=True):
                return None
            started = time.time()
        time.sleep(2)


# --------------------------------------------------------------------------
# Tablet state
# --------------------------------------------------------------------------

class Tablet:
    def __init__(self, adb):
        self.adb = adb
        self.installed = set()
        self.known = set()
        self.system = set()
        self._webview = None

    def prop(self, name):
        return self.adb.shell("getprop " + name)[1].strip()

    def _packages(self, flags):
        code, text = self.adb.shell("pm list packages %s --user %s" % (flags, USER), timeout=90)
        names = {line[8:].strip() for line in text.splitlines() if line.startswith("package:")}
        if code != 0 or not names:
            raise RuntimeError(t("pm_failed", err=text[:300]))
        return names

    def refresh(self):
        self.installed = self._packages("")
        self.known = self._packages("-u")
        self.system = self._packages("-s -u")

    def webview_provider(self):
        if self._webview is None:
            _, text = self.adb.shell("dumpsys webviewupdate")
            match = re.search(r"Current WebView package \(name, version\): \(([^,()]+),", text)
            self._webview = match.group(1).strip() if match else ""
        return self._webview

    def state(self, item):
        present = [p for p in item["packages"] if p in self.known]
        if not present:
            return "absent"
        if any(p in self.installed for p in present):
            return "installed"
        return "removed"

    def lock_reason(self, item):
        if item.get("guard") == "webview-not-chrome":
            provider = self.webview_provider()
            if not provider or provider in item["packages"]:
                return t("guard_webview")
        return None

    def not_system(self, item):
        return any(p in self.installed and p not in self.system for p in item["packages"])


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------

def load_catalog():
    try:
        with open(CATALOG_PATH, encoding="utf-8") as handle:
            catalog = json.load(handle)
    except FileNotFoundError:
        raise SystemExit(t("catalog_missing"))
    except ValueError as err:
        raise SystemExit(t("catalog_broken", err=err))
    seen = set()
    for category in catalog["categories"]:
        for item in category["items"]:
            if item["id"] in seen:
                raise SystemExit(t("catalog_broken", err="duplicate id " + item["id"]))
            seen.add(item["id"])
            for package in item["packages"]:
                if not PKG_RE.match(package):
                    raise SystemExit(t("catalog_broken", err="bad package " + package))
    return catalog


def all_items(catalog):
    for category in catalog["categories"]:
        for item in category["items"]:
            yield item


def item_line(number, item, tag, tag_width):
    badges = []
    if item.get("recommended"):
        badges.append(t("badge_recommended"))
    badges.append(t("badge_tested") if item.get("tested") else t("badge_untested"))
    label = tag.ljust(tag_width)
    if tag == t("tag_remove"):
        label = red(label)
    elif tag == t("tag_keep"):
        label = green(label)
    else:
        label = dim(label)
    number_text = "%3d " % number if number else "    "
    print("%s %s  %s  %s" % (number_text, label, bold(loc(item["name"])),
                             dim("(" + ", ".join(badges) + ")")))


def item_details(item, tablet=None, show_id=False):
    pad = 6
    packages = ", ".join(item["packages"])
    print(" " * pad + dim(("id: %s  |  %s" % (item["id"], packages)) if show_id else packages))
    label_width = max(len(t("lbl_what")), len(t("lbl_effect"))) + 1
    say(t("lbl_what").ljust(label_width) + loc(item["what"]), indent=pad, hang=pad + label_width)
    say(t("lbl_effect").ljust(label_width) + loc(item["effect"]), indent=pad,
        hang=pad + label_width)
    if tablet is not None and tablet.not_system(item):
        say(yellow(t("not_system")), indent=pad, hang=pad)


# --------------------------------------------------------------------------
# Remove
# --------------------------------------------------------------------------

def choose_removals(catalog, tablet):
    """Interactive pages. Returns the list of items to remove, or None if cancelled."""
    selected = {}
    locked = {}
    pages = []
    for category in catalog["categories"]:
        visible = [item for item in category["items"] if tablet.state(item) != "absent"]
        if visible:
            pages.append((category, visible))
        for item in visible:
            if tablet.state(item) != "installed":
                continue
            reason = tablet.lock_reason(item)
            if reason:
                locked[item["id"]] = reason
            else:
                selected[item["id"]] = bool(item.get("recommended"))
    tag_width = max(len(t(k)) for k in ("tag_keep", "tag_remove", "tag_removed", "tag_locked"))
    print()
    say(t("how_it_works"))
    page = 0
    while page < len(pages):
        category, items = pages[page]
        heading("%d/%d  %s" % (page + 1, len(pages), loc(category["name"])))
        say(loc(category["note"]))
        print()
        for number, item in enumerate(items, 1):
            state = tablet.state(item)
            if state == "removed":
                tag = t("tag_removed")
            elif item["id"] in locked:
                tag = t("tag_locked")
            else:
                tag = t("tag_remove") if selected[item["id"]] else t("tag_keep")
            item_line(number, item, tag, tag_width)
            item_details(item, tablet)
            print()
        say(dim(t("page_help")))
        answer = ask("> ").strip()
        lowered = answer.lower()
        if not answer:
            page += 1
        elif lowered in ("b", "z", "<"):
            page = max(0, page - 1)
        elif lowered in ("q", "quit", "abbrechen"):
            return None
        elif answer in ("+", "-"):
            for item in items:
                if item["id"] in selected:
                    selected[item["id"]] = answer == "+"
        else:
            numbers, bad = parse_numbers(answer, len(items))
            if numbers is None:
                say(yellow(t("bad_input", x=bad)))
                continue
            for number in numbers:
                item = items[number - 1]
                name = loc(item["name"])
                if item["id"] in selected:
                    selected[item["id"]] = not selected[item["id"]]
                elif item["id"] in locked:
                    say(yellow(t("is_locked", n=name, why=locked[item["id"]])))
                else:
                    say(yellow(t("is_removed", n=name)))
    return [item for item in all_items(catalog) if selected.get(item["id"])]


def show_summary(items, tablet):
    heading(t("sum_title"))
    if not items:
        say(t("sum_nothing"))
        return False
    say(t("sum_remove", n=len(items)))
    for item in items:
        packages = [p for p in item["packages"] if p in tablet.installed]
        print("  - %s  %s" % (bold(loc(item["name"])), dim(", ".join(packages))))
    say(t("sum_keep"))
    return True


def remove_items(adb, tablet, items, log, dry_run):
    packages = [p for item in items for p in item["packages"] if p in tablet.installed]
    failed = []
    for number, package in enumerate(packages, 1):
        sys.stdout.write(t("run_line", i=number, n=len(packages), pkg=package))
        sys.stdout.flush()
        command = "pm uninstall -k --user %s %s" % (USER, package)
        if dry_run:
            print(dim(t("dry_cmd", cmd=command)))
            continue
        code, text = adb.shell(command, timeout=120)
        if "Success" in text:
            print(green(t("ok")))
        else:
            print(red(t("failed")) + "  " + (text.splitlines() or [""])[-1])
            failed.append(package)
        log.write("remove  %-50s %s" % (package, " ".join(text.split())))
    if dry_run:
        return
    tablet.refresh()
    still = [p for p in packages if p in tablet.installed]
    print()
    say(bold(t("rm_done", ok=len(packages) - len(still), fail=len(still))))
    if still:
        say(red(t("still_installed", pkgs=", ".join(still))))


def remove_flow(adb, tablet, catalog, log, dry_run):
    items = choose_removals(catalog, tablet)
    if items is None:
        say(t("cancelled"))
        return
    if not show_summary(items, tablet):
        return
    if not confirm(t("sum_q"), default=False):
        say(t("cancelled"))
        return
    print()
    remove_items(adb, tablet, items, log, dry_run)
    if not dry_run:
        if log.path:
            print(dim(t("log_at", path=log.path)))
        if confirm(t("reboot_q"), default=True):
            adb.run(["reboot"], timeout=30)
            log.write("reboot")
            say(t("rebooting"))
            raise SystemExit(0)


# --------------------------------------------------------------------------
# Restore
# --------------------------------------------------------------------------

def restore_packages(adb, tablet, packages, log, dry_run):
    for number, package in enumerate(packages, 1):
        sys.stdout.write(t("run_line", i=number, n=len(packages), pkg=package))
        sys.stdout.flush()
        command = "cmd package install-existing --user %s %s" % (USER, package)
        if dry_run:
            print(dim(t("dry_cmd", cmd=command)))
            continue
        code, text = adb.shell(command, timeout=120)
        log.write("restore %-50s %s" % (package, " ".join(text.split())))
        print(dim((text.splitlines() or [""])[-1]))
    if dry_run:
        return
    tablet.refresh()
    missing = [p for p in packages if p not in tablet.installed]
    print()
    say(bold(t("rest_done", ok=len(packages) - len(missing), fail=len(missing))))
    if missing:
        say(yellow(t("rest_missing", pkgs=", ".join(missing))))
        say(t("rest_hint"))


def restore_flow(adb, tablet, catalog, log, dry_run):
    removed = [item for item in all_items(catalog) if tablet.state(item) == "removed"]
    heading(t("menu_restore"))
    if removed:
        say(t("rest_title"))
        for number, item in enumerate(removed, 1):
            print("%3d  %s  %s" % (number, bold(loc(item["name"])),
                                   dim(", ".join(item["packages"]))))
    else:
        say(t("rest_none"))
    print()
    say(dim(t("rest_help")))
    while True:
        answer = ask("> ").strip()
        if not answer:
            return
        packages = []
        if answer == "+":
            chosen = removed
        else:
            chosen = []
            bad = None
            for token in re.split(r"[\s,;]+", answer):
                if not token:
                    continue
                if PKG_RE.match(token):
                    if token in tablet.known and token not in tablet.installed:
                        packages.append(token)
                    else:
                        say(yellow(t("rest_unknown_pkg", pkg=token)))
                    continue
                numbers, bad = parse_numbers(token, len(removed))
                if numbers is None:
                    break
                chosen += [removed[n - 1] for n in numbers]
            if bad:
                say(yellow(t("bad_input", x=bad)))
                continue
        for item in chosen:
            packages += [p for p in item["packages"]
                         if p in tablet.known and p not in tablet.installed]
        packages = list(dict.fromkeys(packages))
        if not packages:
            continue
        if confirm(t("rest_q", n=len(packages)), default=True):
            print()
            restore_packages(adb, tablet, packages, log, dry_run)
        return


# --------------------------------------------------------------------------
# List
# --------------------------------------------------------------------------

def show_list(catalog, tablet=None):
    count = sum(1 for _ in all_items(catalog))
    heading(t("list_title", n=count))
    tag_width = max(len(t(k)) for k in ("st_installed", "st_removed", "st_absent"))
    for category in catalog["categories"]:
        print()
        print(bold(loc(category["name"])))
        say(dim(loc(category["note"])))
        print()
        for item in category["items"]:
            if tablet is not None:
                state = tablet.state(item)
                tag = {"installed": t("st_installed"), "removed": t("st_removed"),
                       "absent": t("st_absent")}[state]
                text = tag.ljust(tag_width)
                text = green(text) if state == "installed" else dim(text)
                print("    %s  %s" % (text, bold(loc(item["name"]))))
            else:
                print("    %s" % bold(loc(item["name"])))
            item_details(item, show_id=True)
            print()


# --------------------------------------------------------------------------
# Non-interactive use
# --------------------------------------------------------------------------

def pick_items(catalog, spec, keyword):
    """Turn 'recommended' / 'all' / 'id1,id2' into a list of items."""
    items = list(all_items(catalog))
    names = [s.strip() for s in spec.split(",") if s.strip()]
    if names == [keyword]:
        if keyword == "recommended":
            return [item for item in items if item.get("recommended")]
        return items
    by_id = {item["id"]: item for item in items}
    unknown = [n for n in names if n not in by_id]
    if unknown:
        raise SystemExit(t("unknown_ids", ids=", ".join(unknown),
                           valid=", ".join(sorted(by_id))))
    return [by_id[n] for n in names]


def run_batch_remove(adb, tablet, catalog, log, args):
    items = [item for item in pick_items(catalog, args.remove, "recommended")
             if tablet.state(item) == "installed"]
    locked = [item for item in items if tablet.lock_reason(item)]
    for item in locked:
        say(yellow(t("is_locked", n=loc(item["name"]), why=tablet.lock_reason(item))))
    items = [item for item in items if item not in locked]
    if not show_summary(items, tablet):
        return
    if not args.yes and not confirm(t("sum_q"), default=False):
        say(t("cancelled"))
        return
    print()
    remove_items(adb, tablet, items, log, args.dry_run)
    if args.reboot and not args.dry_run:
        adb.run(["reboot"], timeout=30)
        log.write("reboot")
        say(t("rebooting"))


def run_batch_restore(adb, tablet, catalog, log, args):
    items = [item for item in pick_items(catalog, args.restore, "all")
             if tablet.state(item) == "removed"]
    packages = [p for item in items for p in item["packages"]
                if p in tablet.known and p not in tablet.installed]
    if not packages:
        say(t("rest_none"))
        return
    for package in packages:
        print("  - " + package)
    if not args.yes and not confirm(t("rest_q", n=len(packages)), default=True):
        say(t("cancelled"))
        return
    restore_packages(adb, tablet, packages, log, args.dry_run)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Lenovo Tab M11 Debloater: remove preinstalled apps over ADB, reversibly.")
    parser.add_argument("--lang", choices=("en", "de"), help="language / Sprache")
    parser.add_argument("--serial", help="ADB serial number, if several devices are connected")
    parser.add_argument("--adb", help="path to adb")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen, change nothing")
    parser.add_argument("--list", action="store_true", help="print the list and exit")
    parser.add_argument("--remove", metavar="IDS",
                        help="remove without the menus: 'recommended' or entry ids, comma separated")
    parser.add_argument("--restore", metavar="IDS",
                        help="restore without the menus: 'all' or entry ids, comma separated")
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    parser.add_argument("--reboot", action="store_true", help="restart the tablet after --remove")
    parser.add_argument("--force", action="store_true", help="skip the model check")
    parser.add_argument("--no-color", action="store_true", help="plain text output")
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    return parser.parse_args(argv)


def check_model(tablet, args, interactive, catalog):
    """Show the device. Returns (ok, model, build)."""
    model = tablet.prop("ro.product.model")
    build = tablet.prop("ro.build.display.id")
    android = tablet.prop("ro.build.version.release")
    say(green(t("dev_connected", model=model or "?", android=android or "?", build=build or "?")))
    ok = True
    if model not in SUPPORTED_MODELS and not args.force:
        say(yellow(t("model_unknown", model=model or "?")))
        if not args.list:
            ok = interactive and confirm(t("model_q"), default=False)
    tested = catalog.get("tested_on", {}).get("firmware", "")
    if ok and tested and build and build != tested:
        say(dim(t("fw_note", tested=tested)))
    return ok, model, build


def main(argv=None):
    global LANG
    args = parse_args(sys.argv[1:] if argv is None else argv)
    LANG = args.lang or detect_lang()
    setup_terminal(args.no_color)
    batch = bool(args.remove or args.restore or args.list)
    interactive = not batch or not args.yes

    print()
    print(cyan("Lenovo Tab M11 Debloater " + VERSION))
    say(t("intro"))
    if args.dry_run:
        say(yellow(t("dry_run")))
    print()

    catalog = load_catalog()

    adb = get_adb(args.adb, interactive=not args.list)
    if adb is None:
        if args.list:
            show_list(catalog)
            return 0
        return 1

    serial = wait_for_device(adb, args.serial, interactive=not args.list and interactive)
    if serial is None:
        if args.list:
            show_list(catalog)
            return 0
        return 1
    adb.serial = serial
    tablet = Tablet(adb)
    ok, model, build = check_model(tablet, args, interactive, catalog)
    if not ok:
        return 1
    try:
        tablet.refresh()
    except RuntimeError as err:
        say(red(str(err)))
        return 1

    log = Log(enabled=not args.dry_run and not args.list)
    log.write("connected %s, model %s, firmware %s, tool %s" % (serial, model, build, VERSION))

    if args.list:
        show_list(catalog, tablet)
        return 0
    if args.remove:
        run_batch_remove(adb, tablet, catalog, log, args)
        return 0
    if args.restore:
        run_batch_restore(adb, tablet, catalog, log, args)
        return 0

    while True:
        heading(t("menu_title"))
        print("  1  " + t("menu_remove"))
        print("  2  " + t("menu_restore"))
        print("  3  " + t("menu_list"))
        print("  l  " + t("menu_lang"))
        print("  q  " + t("menu_quit"))
        choice = ask(t("menu_prompt")).lower()
        if choice == "1":
            remove_flow(adb, tablet, catalog, log, args.dry_run)
        elif choice == "2":
            restore_flow(adb, tablet, catalog, log, args.dry_run)
        elif choice == "3":
            show_list(catalog, tablet)
            ask(t("press_enter"))
        elif choice in ("l", "s"):
            LANG = "de" if LANG == "en" else "en"
        elif choice in ("q", "x", "0"):
            return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        say(t("aborted"))
        sys.exit(130)
