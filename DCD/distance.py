import re
import struct
import logging
import system

logger = logging.getLogger(__name__)


def get_pattern_regex(pattern, distance):
    pattern = pattern.lower().strip().replace(" ", "").replace("\n", "")
    logger.debug(f"Initial pattern: {pattern}")

    default_distance = struct.pack("f", float(system.DEFAULT_DISTANCE)).hex()
    distance = struct.pack("f", float(distance)).hex()
    distance_length = len(distance)
    distance_index = pattern.find(default_distance)

    pattern_regex = (
        pattern[:distance_index]
        + f"\w{{{distance_length}}}"  # regex \w{8} means any 8 characters [a-zA-Z0-9_]
        + pattern[distance_index + distance_length :]
    )
    logger.debug(f"Regex pattern: {pattern_regex}")
    pattern_regex = re.compile(
        pattern_regex
    )  # there is 200 char display truncation, it's normal

    return pattern_regex, distance, distance_index, distance_length


def get_pattern_replace(
    pattern_regex, distance, distance_index, distance_length, shared_library_path
):
    with open(shared_library_path, "rb") as f:
        shared_library = f.read().hex()
    logger.debug(f"Read: {shared_library_path}")

    matches = re.findall(pattern_regex, shared_library)
    matches_count = len(matches)
    logger.debug(f"Matches count: {matches_count}. Matches: {matches}")
    if matches_count == 0:
        raise Exception(
            "Couldn't find the pattern in shared library file."
            " It might have been changed due to the updates."
        )

    pattern_replace = (
        matches[0][:distance_index]
        + distance
        + matches[0][distance_index + distance_length :]
    )
    logger.debug(f"Replacement pattern: {pattern_replace}")

    return pattern_replace, shared_library


def replace_pattern(
    pattern_regex, pattern_replace, shared_library, shared_library_path
):
    shared_library_new = re.subn(pattern_regex, pattern_replace, shared_library, 1)[0]

    try:
        with open(shared_library_path, "wb") as f:
            f.write(bytes.fromhex(shared_library_new))
        logger.debug(f"Wrote: {shared_library_path}")
    except PermissionError as e:
        raise Exception(
            "Couldn't open shared library file, close the game before launching the app",
        )


def set_distance(pattern, distance, shared_library_path):
    if ".." in pattern:
        pattern_regex, distance, distance_index, distance_length = get_pattern_regex(
            pattern, distance
        )
        pattern_replace, shared_library = get_pattern_replace(
            pattern_regex,
            distance,
            distance_index,
            distance_length,
            shared_library_path,
        )

        replace_pattern(
            pattern_regex, pattern_replace, shared_library, shared_library_path
        )
    elif pattern in ["none", "None", "unknown"]:
        raise Exception("Pattern unknown")
    else:
        set_distance_old(pattern, distance, shared_library_path)


def set_distance_old(hex_string, distance, shared_library_path):
    hex_string = hex_string.lower().replace(" ", "")
    hex_string_length = len(hex_string)

    if hex_string_length <= 8:
        raise Exception(
            f"Hex string {hex_string} is only {hex_string_length} symbols long,"
            " which makes search inaccurate, as there is certainly"
            " more than one occurences of that string in shared library file."
            " Please update hex code to have at least 24 symbols."
        )
    elif hex_string_length <= 16:
        logger.critical(
            f"Hex string {hex_string} is only {hex_string_length} symbols long"
            " which makes search inaccurate, as there might be"
            " more than one occurences of that string in shared library file."
            " Please update hex code to have at least 24 symbols."
        )

    default_distance_hex = struct.pack("f", float(system.DEFAULT_DISTANCE)).hex()
    distance_hex = struct.pack("f", float(distance)).hex()
    distance_hex_length = len(distance_hex)
    distance_index = hex_string.find(default_distance_hex)

    if distance_index == -1:
        raise Exception(
            f"Default hex distance {default_distance_hex}"
            f" is not found in the hex string {hex_string}"
        )
    elif distance_index == 0:
        logger.warning(
            f"Hex string {hex_string} starting with default distance"
            f" code {default_distance_hex} makes search a lot slower."
            " Please shift the code, so it starts with other symbols"
        )

    hex_string_regex = re.compile(
        hex_string[:distance_index]
        + f"\w{{{distance_hex_length}}}"  # regex \w{8} means any 8 characters [a-zA-Z0-9_]
        + hex_string[distance_index + distance_hex_length :]
    )
    logger.debug(f"Regex code: {hex_string_regex}")

    distance_hex_string = (
        hex_string[:distance_index]
        + distance_hex
        + hex_string[distance_index + distance_hex_length :]
    )
    logger.debug(f"Replacement string: {distance_hex_string}")

    with open(shared_library_path, "rb") as f:
        shared_library_hex = f.read().hex()
    logger.debug(f"Read: {shared_library_path}")

    matches = re.findall(hex_string_regex, shared_library_hex)
    matches_count = len(matches)
    logger.debug(f"Matches count: {matches_count}. Matches: {matches}")

    if matches_count == 0:
        raise Exception(
            "Couldn't find the hex value in shared library file."
            " It might have been changed due to the updates."
        )
    elif matches_count > 1:
        raise Exception(
            f"Hex string {hex_string} is not precise enough to clearly find"
            f" it's location in shared library file. Currently found {matches_count}"
            " matches. Please, update the string's length to be more precise."
        )

    shared_library_hex_new, changes_count = re.subn(
        hex_string_regex, distance_hex_string, shared_library_hex, 1
    )
    logger.debug(f"Replaced string, changes count: {changes_count}")

    new_matches = re.findall(hex_string_regex, shared_library_hex_new)
    logger.debug(f"Old: {matches}")
    logger.debug(f"New: {new_matches}")

    try:
        with open(shared_library_path, "wb") as f:
            f.write(bytes.fromhex(shared_library_hex_new))
        logger.debug(f"Written: {shared_library_path}")
    except PermissionError as e:
        raise Exception(
            "Couldn't open shared library file, close the game before launching the app",
        )
