from pathlib import Path
from scripts import util


def is_exists(path):
    return Path(path).exists()


def main():
    # check for directories
    # check for config directories
    config_dir_path = util.join_path(Path.cwd(), "config")
    if is_exists(config_dir_path):
        print("/config/ --- found")
        if is_exists(util.join_path(config_dir_path, "config.ini")):
            print("/config/config.ini --- found")

    etc_dir_path = util.join_path(Path.cwd(), "etc")
    if is_exists(etc_dir_path):
        print("/etc --- found")
        if is_exists(util.join_path(etc_dir_path, "font")):
            print("/etc/font/ --- found")
        if is_exists(util.join_path(etc_dir_path, "data")):
            print("/etc/data/ --- found")

    output_dir_path = util.join_path(Path.cwd(), "output")
    if is_exists(output_dir_path):
        print("/output --- found")
        if is_exists(util.join_path(output_dir_path, "generated_images")):
            print("/etc/generated_images/ --- found")

    temp_dir_path = util.join_path(Path.cwd(), "temp")
    if is_exists(temp_dir_path):
        print("/temp --- found")
        if is_exists(util.join_path(temp_dir_path, "images")):
            print("/etc/images/ --- found")

    # check for necessary parameters

    pass


if __name__ == "__main__":
    main()
