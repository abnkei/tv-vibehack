import json
from pathlib import Path
import sys
import time

base = Path(__file__).resolve().parent
repo = base.parent.parent
log_dir = repo / 'backup' / 'mitv-mosr4-home'
log_dir.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / 'tools'))
import tv

old_home = 'com.google.android.apps.tv.launcherx/.home.HomeActivity'
recovery_package = 'com.google.android.tungsten.setupwraith'
new_home = 'com.gathin.tvhome/.MainActivity'
restoring = sys.argv[1:] == ['--restore']
if sys.argv[1:] not in ([], ['--restore']):
    raise SystemExit('Usage: configure-home.py [--restore]')
dev = tv.connect(timeout=20)
log = []

def run(command, expected=None):
    global dev
    try:
        out = dev.shell(command, read_timeout_s=30)
    except (ConnectionError, TimeoutError) as error:
        print('ADB connection lost; reconnecting once: ' + str(error), flush=True)
        try:
            dev.close()
        except OSError as close_error:
            print('Closing broken ADB connection failed: ' + str(close_error), flush=True)
        dev = tv.connect(timeout=10)
        out = dev.shell(command, read_timeout_s=30)
    log.append({'command': command, 'output': out})
    print(command + '\n' + out, flush=True)
    if expected and expected not in out:
        raise RuntimeError('Unexpected response to ' + command)
    return out

def restore():
    errors = []
    commands = [
        ('pm default-state --user 0 com.google.android.apps.tv.launcherx', 'new state: default'),
        ('pm default-state --user 0 ' + recovery_package, 'new state: default'),
        ('cmd package set-home-activity --user 0 ' + old_home, 'Success'),
        ('input keyevent KEYCODE_HOME', None),
    ]
    for command, expected in commands:
        try:
            run(command, expected)
        except Exception as error:
            errors.append(command + ': ' + str(error))
            print('RESTORE ERROR: ' + errors[-1], flush=True)
    if errors:
        raise RuntimeError('Restoration incomplete: ' + '; '.join(errors))

try:
    if restoring:
        restore()
        expected_home = old_home
    else:
        run('am start -W -n ' + new_home, 'Status: ok')
        run('pm disable-user --user 0 com.google.android.apps.tv.launcherx', 'new state: disabled-user')
        run('pm disable-user --user 0 ' + recovery_package, 'new state: disabled-user')
        run('cmd package set-home-activity --user 0 ' + new_home, 'Success')
        expected_home = new_home
    run('cmd package resolve-activity --brief --user 0 -a android.intent.action.MAIN -c android.intent.category.HOME')
    run('am start -W -a android.settings.SETTINGS', 'Status: ok')
    run('input keyevent KEYCODE_HOME')
    time.sleep(2)
    state = dev.shell('dumpsys activity activities', read_timeout_s=30)
    resumed = '\n'.join(line.strip() for line in state.splitlines() if 'mResumedActivity:' in line)
    log.append({'foreground': resumed})
    print(resumed, flush=True)
    if expected_home not in resumed:
        raise RuntimeError('HOME key did not launch ' + expected_home)
    print('HOME VERIFIED: ' + expected_home, flush=True)
except Exception:
    if not restoring:
        print('Applying HOME failed; restoring original HOME', flush=True)
        restore()
    raise
finally:
    (log_dir / ('home-restore.json' if restoring else 'home-apply.json')).write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')
    dev.close()
