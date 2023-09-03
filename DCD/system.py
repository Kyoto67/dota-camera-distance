import subprocess
import os
import sys
import logging

logger = logging.getLogger(__name__)

# constants
DOTA_APP_ID = "570"
DOTA_URL = f"steam://rungameid/{DOTA_APP_ID}"

LIBRARY_FOLDERS_PATH = os.path.join("steamapps", "libraryfolders.vdf")
APP_MANIFEST_PATH = os.path.join("steamapps", f"appmanifest_{DOTA_APP_ID}.acf")
BIN_PATH = os.path.join("steamapps", "common", "dota 2 beta", "game", "dota", "bin")

DEFAULT_DISTANCE = "1200"
SERVER_LINK = "https://raw.githubusercontent.com/searayeah/dota-camera-distance/main/"

if sys.platform.startswith("win32"):
    import winreg

    SERVER_PATTERN_LINK = SERVER_LINK + "patterns/pattern_windows"
    SERVER_PATTERN_OLD_LINK = SERVER_LINK + "hex_strings/current_hex_string_windows"
    SHARED_LIBRARY_PATH = os.path.join(BIN_PATH, "win64", "client.dll")

    def get_steam_path():
        steam_registry_key = os.path.join("SOFTWARE", "WOW6432Node", "Valve", "Steam")
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_registry_key)
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")[0]
        winreg.CloseKey(hkey)
        logger.debug(
            f"Retrieved Steam path: {steam_path} from winreg: {steam_registry_key}"
        )
        return steam_path

    def start_game():
        os.startfile(DOTA_URL)

elif sys.platform.startswith("linux"):
    SERVER_PATTERN_LINK = SERVER_LINK + "patterns/pattern_linux"
    SERVER_PATTERN_OLD_LINK = SERVER_LINK + "hex_strings/current_hex_string_linux"
    SHARED_LIBRARY_PATH = os.path.join(BIN_PATH, "linuxsteamrt64", "libclient.so")

    def get_steam_path():
        steam_path = os.path.expanduser(os.path.join("~", ".steam", "steam"))
        logger.debug(f"Retrieved Steam path: {steam_path}")
        return steam_path

    def start_game():
        subprocess.Popen(
            ["xdg-open", DOTA_URL],
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

elif sys.platform.startswith("darwin"):
    SERVER_PATTERN_LINK = SERVER_LINK + "patterns/pattern_macos_intel"
    SERVER_PATTERN_OLD_LINK = SERVER_LINK + "hex_strings/current_hex_string_macos_intel"
    SHARED_LIBRARY_PATH = os.path.join(BIN_PATH, "osx64", "libclient.dylib")

    def get_steam_path():
        steam_path = os.path.expanduser(
            os.path.join("~", "Library", "Application Support", "Steam")
        )
        logger.debug(f"Retrieved Steam path: {steam_path}")
        return steam_path

    def start_game():
        subprocess.Popen(
            ["open", DOTA_URL],
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

else:
    raise Exception("OS not supported")
