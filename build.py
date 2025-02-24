
import PyInstaller.__main__

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
