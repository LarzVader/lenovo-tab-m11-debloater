# Lenovo Tab M11 Debloater

**[Deutsche Anleitung](README.de.md)**

Your Lenovo Tab M11 comes with more than you asked for: an ad module, Lenovo's usage
statistics, a shop demo and a stack of Google apps. This tool removes what you don't want,
and you choose app by app what stays. For every app it tells you what it is and what changes
without it.

- **No root**: no unlocked bootloader, no flashing. The tool uses ADB, the developer tools
  that are built into Android.
- **Reversible**: apps are only removed for your user. You can restore system apps with the
  tool at any time, and a factory reset brings everything back.
- **Only what is on the list**: the tool can only remove the entries listed below, so it
  cannot remove something Android needs by accident.
- **Windows and Linux**, in English and German.

## What it looks like

```
1/5  Lenovo advertising, tracking and shop demos
================================================
Recommended to remove. None of these has a function you would miss.

  1  REMOVE           Tabtop Picks  (preselected, tested)
      com.lenovo.rt
      What:       Advertising module from the ad network Appnext. Suggests apps and
                  shows promotional notifications.
      If removed: No more app suggestions or ad notifications from it. Nothing else
                  changes.

  2  REMOVE           AppServices (Aura)  (preselected, tested)
      com.aura.oobe.lenovo
      What:       Aura app recommendation service. Offers partner apps during setup.
      If removed: No more offers of partner apps. Nothing else changes.
...
Numbers switch keep/remove (e.g. 1 3 5-7) | + remove all | - keep all | Enter = next |
b = back | q = cancel
>
```

## Is this for your tablet?

- **Lenovo Tab M11, model TB330FU** (Wi-Fi): tested with ZUI 17.0.502 (Android 15) in
  November 2026.
- The LTE model **TB330XU** should work the same way, but has not been tested.
- You find the model number in Settings > About tablet.
- Other firmware versions may come with other apps. The tool only shows apps that are on
  your tablet.

## What you need

- A computer with Windows 10/11 or Linux (macOS should work too, but is untested)
- Python 3.8 or newer
- A USB cable that carries data (a charge-only cable does not work)
- About 10 minutes

## Step by step

### 1. Turn on USB debugging on the tablet

1. Open **Settings > About tablet** and tap **Build number** seven times, until the tablet
   says that you are now a developer.
2. Open **Settings > System > Developer options** and turn on **USB debugging**.
3. Connect the tablet to your computer.

On some firmware versions the menus are named slightly differently.

### 2. Get the tool

On this page, click **Code > Download ZIP** and unpack the file. Or with git:

```bash
git clone https://github.com/LarzVader/lenovo-tab-m11-debloater.git
```

### 3. Start it

**Windows:** double-click `start-windows.bat`. If Python is missing, the window tells you.
Install it with this command, or from [python.org](https://www.python.org/downloads/) (tick
"Add python.exe to PATH" during setup), and start the file again:

```
winget install -e --id Python.Python.3.13
```

**Linux:** open a terminal in the folder and run:

```bash
./start-linux.sh
```

The tool needs ADB, which is part of Google's "platform tools". If it can't find ADB, it
offers to download Google's official package from dl.google.com into its own folder.
Nothing is installed system-wide.

### 4. Allow your computer on the tablet

The tablet asks "Allow USB debugging?". Tap **Allow**. With a tick at "Always allow from this
computer" it won't ask again.

**Linux only:** if the tool says that Linux does not allow access to the tablet, it shows two
commands that add a udev rule for Lenovo devices. Run them once, then unplug the cable and
plug it in again.

### 5. Choose

In the main menu, choose **1 Remove apps**. The tool shows the apps page by page, grouped by
topic. Each app is marked **REMOVE** or **keep**:

- Type the numbers of apps to switch them, for example `1 3 5-7`.
- `+` marks all apps on the page for removal, `-` keeps all of them.
- Enter goes to the next page, `b` goes back, `q` cancels.

Only ads, tracking and shop demos are preselected. Everything else stays unless you switch
it.

At the end you see a summary, and nothing changes until you confirm it. Then the tool removes
the apps and offers to restart the tablet, which is a good idea.

## Restoring apps

Start the tool, choose **2 Restore removed apps** and pick the apps by their numbers, or type
`+` for all of them. You can also type a package name.

Without the tool, this restores an app:

```bash
adb shell cmd package install-existing com.google.android.youtube
```

A few apps are not part of the system image. The tool marks them with "Not a system app".
After removal they only come back from the Play Store or with a factory reset.

## The list

"Tested" means: removed on a real TB330FU, then restarted and checked. Entries with "–" have
not been removed on a real tablet yet. The id is for the command line.

<!-- PACKAGES:START -->

### Lenovo advertising, tracking and shop demos

Recommended to remove. None of these has a function you would miss.

| App | What it is | If removed | Preselected | Tested |
|---|---|---|:-:|:-:|
| **Tabtop Picks**<br>`com.lenovo.rt`<br>id: `tabtop-picks` | Advertising module from the ad network Appnext. Suggests apps and shows promotional notifications. | No more app suggestions or ad notifications from it. Nothing else changes. | yes | yes |
| **AppServices (Aura)**<br>`com.aura.oobe.lenovo`<br>id: `aura-appservices` | Aura app recommendation service. Offers partner apps during setup. | No more offers of partner apps. Nothing else changes. | yes | yes |
| **Play Auto Installs (PAI)**<br>`android.autoinstalls.config.Lenovo.tablet`<br>id: `play-auto-installs` | List of partner apps that Google Play installs automatically after setup. | Only used right after setup. Removing it has no visible effect. | yes | yes |
| **Opera Preinstall Data**<br>`com.opera.preinstall`<br>id: `opera-preinstall` | Small data package with partner data for the Opera browser. Opera itself is not installed. | None. | yes | yes |
| **User Experience**<br>`com.lenovo.ue.device`<br>id: `user-experience` | Lenovo's usage statistics. Collects data about the tablet and how it is used, and uploads it. | Lenovo no longer receives these statistics. Nothing else changes. | yes | yes |
| **Device Service Support (Lenovo push)**<br>`com.tblenovo.tabpushout`<br>id: `lenovo-push` | Receives push messages from Lenovo's servers. | No more push messages from Lenovo. | yes | yes |
| **Tips**<br>`com.tblenovo.lenovowhatsnew`<br>id: `tips` | Lenovo's tips and "what's new" notes. | No more tips. Nothing else changes. | yes | yes |
| **UDS real time engine**<br>`com.lenovo.tbengine`<br>id: `uds-engine` | Lenovo background service for tips and push messages that also downloads and installs Lenovo apps in the background. Always running. | No more tips or background installs, and a little more free memory. The tablet ran normally without it. It is not preselected only because no system update has been installed without it yet. | – | yes |
| **Lenovo Tab M11 (shop presentation)**<br>`com.lenovo.tab_m11`<br>id: `shop-presentation` | Product presentation with videos for display devices in shops. | None for you. | yes | yes |
| **Demo mode**<br>`com.motorola.demo`<br>id: `demo-mode` | Demo mode for display devices in shops. | None for you. | yes | yes |
| **OCZ deployment tools**<br>`com.lenovo.dsa`<br>`com.lenovo.ocpl`<br>id: `ocz-deployment` | Lenovo tools that download and apply customizations and apps, probably meant for setting up many devices at once (companies, schools, shops). | None on a private tablet. | yes | yes |

### Lenovo apps and features

Real features. Remove them only if you don't use them.

| App | What it is | If removed | Preselected | Tested |
|---|---|---|:-:|:-:|
| **Lenovo Vantage**<br>`com.tblenovo.center`<br>`com.tblenovo.ue.config`<br>id: `lenovo-vantage` | Lenovo's help app: user guide, hardware tests, feedback and shop. Runs in the background. | The app and its notes disappear. System updates come from the separate "System update" app, which stays. | – | – |
| **Smart Connect**<br>`com.motorola.mobiledesktop`<br>`com.motorola.mobiledesktop.core`<br>`com.motorola.readyforsignature.app`<br>id: `smart-connect` | Lenovo's cross-device feature (based on Motorola "Ready For"): connects the tablet with a PC or phone, for example as a second screen or to share files. Runs in the background. | Smart Connect is gone. | – | – |
| **LTHD (diagnostics for Lenovo's PC tool)**<br>`com.lmsa.app.lmsapad`<br>id: `lthd` | Diagnostics helper for Lenovo's PC support tool (Rescue and Smart Assistant). | Only matters if you use that PC program. | – | – |
| **Notepad**<br>`com.zui.notes`<br>id: `lenovo-notepad` | Lenovo's notes app. | The app disappears. Remove it only if you have no notes in it. | – | – |
| **Weather**<br>`com.zui.weather`<br>id: `lenovo-weather` | Lenovo's weather app with the clock and weather widget. | The app and its home screen widget disappear. | – | – |

### Google: video, music and kids

Remove what you don't use. Purchases and subscriptions stay in your Google account.

| App | What it is | If removed | Preselected | Tested |
|---|---|---|:-:|:-:|
| **YouTube**<br>`com.google.android.youtube`<br>id: `youtube` | Google's video app. | The app disappears; YouTube still works in the browser. It can run in the background even if you never open it. | – | yes |
| **YouTube Music**<br>`com.google.android.apps.youtube.music`<br>`com.google.android.apps.youtube.music.setupwizard`<br>id: `youtube-music` | Google's music app. | The app disappears; music.youtube.com still works in the browser. | – | yes |
| **Google TV**<br>`com.google.android.videos`<br>id: `google-tv` | Google's app for renting and buying films and series. | The app disappears. It can run in the background even if you never open it. | – | yes |
| **Entertainment Space**<br>`com.google.android.apps.mediahome.launcher`<br>id: `entertainment-space` | Google's page with recommendations for videos, games and books. | The recommendations page disappears. It can run in the background even if you never open it. | – | yes |
| **Kids Space**<br>`com.google.android.apps.kids.home`<br>id: `kids-space` | Google's child-friendly mode with selected apps, books and videos. | The kids mode is no longer available. | – | yes |

### Google: mail, messages and calls

Remove what you don't use.

| App | What it is | If removed | Preselected | Tested |
|---|---|---|:-:|:-:|
| **Gmail**<br>`com.google.android.gm`<br>id: `gmail` | Google's mail app. | The app disappears; your mail stays in your account (mail.google.com). Email links open in another mail app, if you have one. | – | yes |
| **Google Messages**<br>`com.google.android.apps.messaging`<br>id: `google-messages` | Google's SMS and RCS app. | On the Wi-Fi model (TB330FU) it is only useful if you pair it with your phone to read your phone's messages. On the LTE model (TB330XU) it is the SMS app: keep it there if you use SMS. | – | yes |
| **Google Meet**<br>`com.google.android.apps.tachyon`<br>id: `google-meet` | Google's video calls. | No Meet app; meet.google.com still works in the browser. | – | yes |

### Google: other apps and services

Some of these are everyday apps. Read what changes before you remove them.

| App | What it is | If removed | Preselected | Tested |
|---|---|---|:-:|:-:|
| **Google app and Assistant**<br>`com.google.android.googlequicksearchbox`<br>`com.google.android.apps.googleassistant`<br>`com.android.hotwordenrollment.okgoogle`<br>`com.android.hotwordenrollment.xgoogle`<br>id: `google-app` | Google search with the search widget, Google Assistant ("Hey Google") and the Discover feed. | The search widget disappears from the home screen, and there is no digital assistant anymore. Voice typing in Gboard may stop working (not tested yet). | – | yes |
| **Chrome**<br>`com.android.chrome`<br>id: `chrome` | Google's web browser. | Install another browser first! Web pages inside other apps keep working, because they use "Android System WebView", which stays. The tool checks this before it removes Chrome. | – | – |
| **Google Maps**<br>`com.google.android.apps.maps`<br>id: `google-maps` | Maps and navigation. | No maps app; map links open in the browser. | – | yes |
| **Google Photos**<br>`com.google.android.apps.photos`<br>id: `google-photos` | Gallery and Google's photo cloud. | Backup to Google Photos stops; your pictures stay on the tablet. It may be the only gallery app: then you view pictures in a file manager or install another gallery. | – | yes |
| **Digital Wellbeing**<br>`com.google.android.apps.wellbeing`<br>id: `digital-wellbeing` | Screen time statistics, app timers, bedtime mode and focus mode. Runs in the background. | These features are gone. | – | yes |
| **Google Play Services for AR (ARCore)**<br>`com.google.ar.core`<br>id: `arcore` | Augmented reality for apps. | Apps can no longer use AR. You can install it again from the Play Store at any time. | – | yes |
| **Cross-Device Services**<br>`com.google.ambient.streaming`<br>id: `cross-device` | Google's features for using apps across devices, for example streaming apps to a Chromebook. | These cross-device features stop working. | – | yes |
| **Google Wi-Fi Provisioner**<br>`com.google.android.apps.carrier.carrierwifi`<br>id: `wifi-provisioner` | Carrier Wi-Fi, automatic sign-in to public OpenRoaming hotspots with your Google account, and a Wi-Fi quality rating. Runs in the background. | Normal Wi-Fi keeps working (tested). Automatic sign-in to OpenRoaming hotspots is gone. | – | yes |
| **Google Drive**<br>`com.google.android.apps.docs`<br>id: `google-drive` | Google's cloud storage. | No Drive app; your files stay in your account (drive.google.com). | – | – |
| **Google Calendar**<br>`com.google.android.calendar`<br>id: `google-calendar` | Calendar app. | No calendar app; your appointments stay in your account. | – | – |
| **Google Contacts**<br>`com.google.android.contacts`<br>id: `google-contacts` | Contacts app. | No contacts app; the contacts themselves stay stored. Apps in which you pick a contact may no longer be able to do that. | – | – |
| **Clock**<br>`com.google.android.deskclock`<br>id: `google-clock` | Alarm clock, timer, stopwatch and world clock. | No alarm clock and no timer anymore! | – | – |
| **Calculator**<br>`com.google.android.calculator`<br>id: `google-calculator` | Calculator app. | No calculator app. | – | – |
| **Files by Google**<br>`com.google.android.apps.nbu.files`<br>id: `files-by-google` | File manager and storage cleaner. | The file manager disappears. Apps can still open and save files through the system's file picker, which stays. | – | – |
| **Android System Key Verifier**<br>`com.google.android.contactkeys`<br>id: `key-verifier` | Lets you verify the encryption keys of your contacts in messaging apps. | Key verification is gone. Google Play may install it again. | – | – |

<!-- PACKAGES:END -->

## Deliberately not on the list

These stay, because the tablet needs them or because nobody knows yet what happens without
them:

- **Google Play Store and Google Play services**: apps, updates, sign-in
- **Gboard**: the only keyboard on the tablet
- **Android System WebView**: shows web pages inside apps
- **System update** (`com.lenovo.ota`), **Lenovo ID** and **Device Service**
  (`com.lenovo.lsf`, `com.lenovo.lsf.device`): system updates may depend on them
- **Face recognition** (`com.tbsmart.levision`): face unlock
- **Pen** (`com.lenovo.penservice`), **Dolby**, **SarReduce** (keeps the radio power within
  the limits for radiation exposure), launcher, camera and settings
- **Google Play Protect** (`com.google.android.odad`)
- **Android Developer Verifier** (`com.google.android.verifier`): Google's new check for apps
  from outside the Play Store. Nobody knows yet what happens to such installs without it.

## Good to know

- Removed apps don't run, don't get updates and don't show up anywhere. Their data stays on
  the tablet (`pm uninstall -k`), so a restored app finds its data again.
- Only the main user changes. A second user or a work profile keeps its apps.
- A system update may bring back single apps. Just run the tool again.
- A factory reset brings back all apps.
- Every change is written to `m11-debloater.log` in the tool's folder.

## Command line

The menus are optional. All options: `python3 m11_debloater.py --help`

| Option | What it does |
|---|---|
| `--lang en`, `--lang de` | Language. Without it, the tool uses the language of your system. |
| `--dry-run` | Changes nothing and shows the commands it would run. |
| `--list` | Prints the list with the status on your tablet and the ids. |
| `--remove recommended` | Removes the preselected apps without the menus. |
| `--remove youtube,google-tv` | Removes these entries (ids from the list). |
| `--restore all` | Restores all removed apps from the list. |
| `--restore youtube` | Restores these entries. |
| `--yes` | Doesn't ask for confirmation (with `--remove` or `--restore`). |
| `--reboot` | Restarts the tablet after `--remove`. |
| `--serial SERIAL` | Chooses the device if several are connected. |
| `--adb PATH` | Uses this adb. |
| `--force` | Skips the model check. |
| `--no-color` | Plain text without colors. |

Example: remove the preselected apps without questions, then restart:

```bash
python3 m11_debloater.py --remove recommended --yes --reboot
```

## If something goes wrong

- **"No tablet found"**: check the cable (charge-only cables don't work) and that USB
  debugging is on, and try another USB port.
- **The tablet never asks "Allow USB debugging?"**: unplug and replug the cable. In the
  Developer options, "Revoke USB debugging authorizations" and try again.
- **Linux says "no permissions"**: run the two udev commands that the tool shows.
- **An app you need is gone**: restore it (see above).
- **The tablet acts strangely**: restore everything with `--restore all` and restart. A
  factory reset brings everything back, but also erases your data.

## Risks

You use this tool at your own risk. It only removes apps for your user and only from its
list, and it was tested on one TB330FU with the firmware named above. Entries marked "not
tested yet" have not been removed on a real tablet so far. If you try one, please tell us
how it went.

This project is not affiliated with Lenovo or Google.

## Help with the list

Does your M11 have other apps, or did you test an entry? Please open an
[issue](https://github.com/LarzVader/lenovo-tab-m11-debloater/issues) with:

- model and firmware (Settings > About tablet)
- what you removed and what happened
- for apps that are missing from the list: the package name. `adb shell pm list packages -s`
  lists only system apps, so you don't share which apps you installed yourself.

After a change to `packages.json`, `python3 tools/make_tables.py` updates the tables in both
READMEs.

## License

MIT, see [LICENSE](LICENSE).
