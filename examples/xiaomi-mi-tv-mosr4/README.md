# Xiaomi MiTV-MOSR4: initial device report

Tested on Xiaomi MiTV-MOSR4 (`irobot`), Android 11 / SDK 30, firmware
`RTM5.220609.003.1493`. This is an initial session report, not a debloat list
validated over several days. Do not apply it blindly to another firmware.

## Device configuration

`config.xml` contains the configuration verified on this TV:

| Purpose | Package |
| --- | --- |
| Netflix | `com.netflix.ninja` |
| YouTube | `com.google.android.youtube.tv` |
| Disney+ | `in.startv.hotstar.dplus.tv` |
| HBO Max | `com.wbd.stream` |
| Live TV | `com.mitv.livetv` |
| Original Google TV HOME | `com.google.android.apps.tv.launcherx/.home.HomeActivity` |

The repository launcher config currently matches this example. Build prerequisites
and Python environment setup are documented in the root README.

## HOME behavior observed

Setting the custom HOME returned `Success`, but the HOME key still opened Google TV.
The original HOME had priority 2, Setup/Recovery had priority 1, and the custom HOME
had priority 0. Disabling Google TV alone caused HOME to open
`com.google.android.tungsten.setupwraith/.RecoveryActivity`.

This firmware rejected shell changes to the individual HOME component state with
`SecurityException`. After explicit owner approval, disabling both packages below
for user 0 and setting the custom HOME made the actual HOME key open the new launcher:

- `com.google.android.apps.tv.launcherx`
- `com.google.android.tungsten.setupwraith`

The second package provides Google TV setup/recovery functionality. Restore both
packages before using those features. No packages were uninstalled; no other
packages were disabled. Voice, casting, firmware updates and input services were
not intentionally changed.

## Device-specific apply and restore

Use only after confirming this model, firmware, original HOME and original package
states. On the tested device both original package states were `default`, setup
was complete, and the original HOME above was enabled. The helper assumes that
baseline; it is not a generic package-state backup or restore tool.

Back up package lists, component states, getprop, settings and original HOME first,
following PROMPT.md. Keep those device dumps and ADB keys private.

From the repository root, with the TV's current IP supplied locally:

```powershell
$env:TV_HOST = '<TV_IP>'
& tools\venv\Scripts\python.exe -I examples\xiaomi-mi-tv-mosr4\configure-home.py
```

Restore the two original package states and Google TV HOME:

```powershell
& .\examples\xiaomi-mi-tv-mosr4\restore-home.ps1 -TvHost '<TV_IP>'
```

The helper checks command responses and the foreground activity after the HOME key.
On apply failure it attempts to restore the original setup. A lost ADB connection
can prevent rollback; restore manually with the current TV IP once reachable.
Logs go under ignored `backup/mitv-mosr4-home/`.

## Validation and limits

- Debug APK built with JDK 17, Gradle 8.9 and Android SDK 34; APK v2 signature verified.
- All four dock apps opened through D-pad selection; foreground activities matched.
- Screenshots checked dock, grid, top-bar boundaries and the Inputs menu.
- HOME from Settings opened the custom launcher with both packages disabled.
- Explicit restore re-enabled the original package states and verified Google TV HOME;
  applying the custom HOME again also passed.
- The exported helper uses the same tested commands, with portable paths and ignored
  logs. Its syntax was checked; this exported copy was not separately run on the TV.
- An ADB disconnect occurred during an earlier test. Connectivity later recovered at
  the same IP; its cause was not established. Automatic reconnect was not fault-tested.
- Reboot persistence, playback, HDMI switching and multi-day stability remain untested.

## Potential upstream contributions

1. Add a device report for MiTV-MOSR4 and its actual package names. Wait for multi-day
   testing before proposing a stable `debloat.txt`, as CONTRIBUTING.md requires.
2. Improve installation verification: `set-home-activity` returning `Success` does not
   prove the HOME key opens the requested launcher. Verify foreground activity and
   restore on failure; keep firmware-specific recovery choices explicit.
3. Improve recovery after ADB disconnects: reconnect before rollback, attempt all
   restore steps, and report any incomplete restoration.
4. Check the Gradle wrapper provenance/version: in the tested checkout the JAR SHA256
   differed from the official Gradle 8.9 wrapper JAR checksum. This alone does not prove
   malicious code. The build used a publisher-checksummed Gradle 8.9 distribution.

This report contains no TV IP, serial, account identifiers, device dumps or ADB keys.
