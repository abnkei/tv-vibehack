# Project instructions

- Read README.md, PROMPT.md and CONTRIBUTING.md before device changes.
- Launcher: plain Java in launcher/app; Android Gradle Plugin 8.5.2, Gradle 8.9, Java 17, compileSdk 34, minSdk 26, targetSdk 29. Android SDK platform 34 and build-tools 34.0.0 are documented prerequisites.
- Configure device-specific dock packages, hidden apps and Live TV in launcher/app/src/main/res/values/config.xml. Verify package names on the target TV first.
- Build only: run a verified Gradle 8.9 distribution with assembleDebug from launcher/. The checked-in wrapper JAR does not match the official Gradle 8.9 wrapper checksum; verify its provenance before executing it. build-and-install.ps1 also changes the target TV and disables the specified stock launcher.
- Python ADB tools use tools/venv and tools/requirements.txt. Set TV_HOST explicitly; TV_PORT defaults to 5555.
- Before changes, save package lists, disabled packages, getprop, settings and the current HOME component under backup/. This directory and tools/adbkey/ are ignored; keep device dumps and private keys out of Git.
- Disable packages only with pm disable-user --user 0; never uninstall system packages. Verify each package and preserve input, remote, keyboard, Play Store and Play Services. Ask about streaming apps, voice, casting and updates before disabling them.
- Install and verify the new launcher before disabling stock HOME; keep a device-specific restore procedure.
- Validation requires real-TV D-pad navigation and screenshots. Do not claim device validation based on a build alone.
- Keep the launcher small: no new dependencies, blur, video backgrounds, network polling or telemetry.
