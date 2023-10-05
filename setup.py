from pathlib import Path
from scripts import util


def __is_exists(path):
    return Path(path).exists()


def validate_directories():
    # check for config directories
    config_dir_path = util.join_path(Path.cwd(), "config")
    if __is_exists(config_dir_path):
        print("/config/ --- found")
        if __is_exists(util.join_path(config_dir_path, "config.ini")):
            print("/config/config.ini --- found")

    etc_dir_path = util.join_path(Path.cwd(), "etc")
    if __is_exists(etc_dir_path):
        print("/etc --- found")
        if __is_exists(util.join_path(etc_dir_path, "font")):
            print("/etc/font/ --- found")
        if __is_exists(util.join_path(etc_dir_path, "data")):
            print("/etc/data/ --- found")

    output_dir_path = util.join_path(Path.cwd(), "output")
    if __is_exists(output_dir_path):
        print("/output/ --- found")
        if __is_exists(util.join_path(output_dir_path, "generated_images")):
            print("/etc/generated_images/ --- found")
        else:
            util.create_dir(util.join_path(output_dir_path, "generated_images"))
    else:
        util.create_dir(output_dir_path)
        util.create_dir(util.join_path(output_dir_path, "generated_images"))

    temp_dir_path = util.join_path(Path.cwd(), "temp")
    if __is_exists(temp_dir_path):
        print("/temp --- found")
        if __is_exists(util.join_path(temp_dir_path, "images")):
            print("/temp/images/ --- found")
        else:
            util.create_dir(util.join_path(temp_dir_path, "images"))
    else:
        util.create_dir(temp_dir_path)
        util.create_dir(util.join_path(temp_dir_path, "images"))


def main():
    # check for directories
    validate_directories()
    pass


if __name__ == "__main__":
    main()
