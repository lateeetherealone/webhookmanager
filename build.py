
import PyInstaller.__main__
import os

# Set Windows-specific options
is_windows = os.name == 'nt'
separator = ';' if is_windows else ':'

# Build updater
PyInstaller.__main__.run([
    'updater.py',
    '--onefile',
    '--console',
    '--icon=ogrimmar.ico',
    '--name=Updater',
    '--clean',
    f'--add-data=ogrimmar.ico{separator}.'
])

# Build main app
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--console',
    '--icon=ogrimmar.ico',
    '--name=WebhookManager',
    '--clean',
    f'--add-data=ogrimmar.ico{separator}.',
    '--hidden-import=colorama',
    '--hidden-import=discord_webhook',
    '--hidden-import=requests',
    '--hidden-import=pytz',
    '--runtime-hook=windows_fix.py'
])
