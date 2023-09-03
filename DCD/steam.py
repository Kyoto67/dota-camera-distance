import logging
import vdf
import time
import os
import system

logger = logging.getLogger(__name__)


def get_steam_library_path(steam_path):
    # Dota and Steam can have different install locations/drives.
    library_folders_path = os.path.join(steam_path, system.LIBRARY_FOLDERS_PATH)
    library_folders = vdf.load(open(library_folders_path))["libraryfolders"]
    logger.debug(f"Read {library_folders_path}")
    for key in library_folders:
        if system.DOTA_APP_ID in library_folders[key]["apps"]:
            dota_path = library_folders[key]["path"]
            logger.debug(f"Found Dota path: {dota_path} in libraryfolders")
            return dota_path
    raise Exception(
        "Dota 2 path was not found in libraryfolders.vdf file."
        " This usually happens when Dota 2 is not installed on the system."
        " If you have just installed Dota 2 you need to restart Steam"
        " for it to apply the changes to specific files."
    )


def dota_was_updating(steam_library_path):
    # If "StateFlags" is '4' that means that Dota is updated/installed
    app_manifest_path = os.path.join(steam_library_path, system.APP_MANIFEST_PATH)
    app_manifest = vdf.load(open(app_manifest_path))
    app_status = app_manifest["AppState"]["StateFlags"]
    logger.debug(f"Read app manifest: {app_manifest_path}, status: {app_status}")
    if app_status != "4":
        while app_status != "4":
            logger.info(f"Waiting for Dota 2 to get updates, status: {app_status}")
            time.sleep(3)
            app_manifest = vdf.load(open(app_manifest_path))
            app_status = app_manifest["AppState"]["StateFlags"]
        return True
    else:
        return False
