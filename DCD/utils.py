import configparser
import os
import logging
import requests
import system
import steam


logger = logging.getLogger(__name__)


def get_current_hex_string(link, default):
    # This is done to avoid hardcoding
    # this value and enable updating it through Github.
    try:
        response = requests.get(link)
        response.raise_for_status()
        response_text_repr = repr(response.text)
        logger.debug(f"String {response_text_repr} received from GitHub")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(
            "Couldn't receive pattern from GitHub, using the one written in config.ini"
        )
        return str(default)


def set_config():
    config_path = os.path.join(os.getcwd(), "config.ini")
    config_file = configparser.ConfigParser()

    try:
        config_file.read(config_path)
    except Exception as e:
        logger.error(
            "Something wrong with the config, creating new one...", exc_info=True
        )

    if not config_file.has_section("CAMERA-DISTANCE"):
        config_file["CAMERA-DISTANCE"] = {}
    if not config_file.has_section("PATHS"):
        config_file["PATHS"] = {}
    camera_config = config_file["CAMERA-DISTANCE"]
    path_config = config_file["PATHS"]

    if not camera_config.get("logging_level"):
        camera_config["logging_level"] = "INFO"
    logger.setLevel(camera_config["logging_level"].upper())
    logger.info(f"Logging level: {logging.getLevelName(logger.getEffectiveLevel())}")

    if not camera_config.get("distance"):
        distance_message = "Enter distance[default 1200, recommended 1400]: "
        camera_config["distance"] = input(distance_message) or system.DEFAULT_DISTANCE
    logger.info(f"Distance: {camera_config['distance']}")

    if not camera_config.get("receive_pattern_from_git"):
        camera_config["receive_pattern_from_git"] = "yes"
    logger.info(
        f"Receive pattern from git: {camera_config['receive_pattern_from_git']}"
    )

    if not camera_config.get("autostart_game"):
        camera_config["autostart_game"] = "yes"
    logger.info(f"Autostart game: {camera_config['autostart_game']}")

    # set this config variable to False, set your manual string, and the program won't update it
    # automatically every time you launch it.
    if camera_config.getboolean("receive_pattern_from_git") or not camera_config.get(
        "pattern"
    ):
        camera_config["pattern"] = get_current_hex_string(
            system.SERVER_PATTERN_LINK, camera_config.get("pattern")
        )
    logger.info(f"Pattern: {camera_config['pattern']}")

    if camera_config.getboolean("receive_pattern_from_git") or not camera_config.get(
        "pattern_old"
    ):
        camera_config["pattern_old"] = get_current_hex_string(
            system.SERVER_PATTERN_OLD_LINK, camera_config.get("pattern_old")
        )
    logger.info(f"Pattern old: {camera_config['pattern_old']}")

    if not path_config.get("steam_path"):
        path_config["steam_path"] = system.get_steam_path()
    logger.info(f"Steam path: {path_config['steam_path']}")

    if not path_config.get("steam_library_path"):
        path_config["steam_library_path"] = steam.get_steam_library_path(
            path_config["steam_path"]
        )
    logger.info(f"Steam library path: {path_config['steam_library_path']}")

    if not path_config.get("shared_library_path"):
        path_config["shared_library_path"] = os.path.join(
            path_config["steam_library_path"], system.SHARED_LIBRARY_PATH
        )
    logger.info(f"Shared library path: {path_config['shared_library_path']}")

    with open(config_path, "w") as configfile:
        config_file.write(configfile)
    logger.info(f"Updated config: {config_path}")

    return camera_config, path_config
