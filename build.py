
import PyInstaller.__main__

# Build updater
PyInstaller.__main__.run([
    'updater.py',
    '--onefile',
    '--console',
    '--icon=ogrimmar.ico',
    '--name=Updater',
    '--clean'
])

# Build main app
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--console',
    '--icon=ogrimmar.ico',
    '--name=WebhookManager',
    '--clean',
    '--add-data=ogrimmar.ico;.',  # Using semicolon for Windows
    '--hidden-import=colorama',
    '--hidden-import=discord_webhook',
    '--hidden-import=requests',
    '--runtime-hook=windows_fix.py'
])
