import time
import logging
import sys

# logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Version: 6.1")
logger.info(f"OS: {sys.platform}")

import system
import utils
import steam
import distance


def dcd(pattern, camera_config, path_config):
    distance.set_distance(
        pattern,
        camera_config["distance"],
        path_config["shared_library_path"],
    )
    if camera_config.getboolean("autostart_game"):
        system.start_game()
        logger.info("Launching game ...")

        # When launching Dota for the first time it might get updates,
        # so shared library file needs to be rewritten again.
        if steam.dota_was_updating(path_config["steam_library_path"]):
            distance.set_distance(
                camera_config["hex_string"],
                camera_config["distance"],
                path_config["shared_library_path"],
            )
            logger.info('Press "Play game"')


def main():
    camera_config, path_config = utils.set_config()

    try:
        dcd(camera_config["pattern"], camera_config, path_config)
    except Exception as e:
        logger.info("Exception", exc_info=True)
        logger.info("New pattern not working, using the old one")
        dcd(camera_config["pattern_old"], camera_config, path_config)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Program crashed", exc_info=True)
        logger.error(
            "If nothing helps or there's a bug, send me a screenshot via"
            " https://github.com/searayeah/dota-camera-distance/issues",
        )
    finally:
        for i in range(5, 0, -1):
            logger.info(f"Exit in: {i}")
            time.sleep(1)
