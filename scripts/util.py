from urllib.parse import urlparse
import requests
import os
import time


def download_file(url, download_dir=""):
    response = requests.get(url)
    if response.status_code:
        filename = get_name_from_url(url=url)
        path = join_path(dir=download_dir, file=filename)
        fp = open(path, "wb")
        fp.write(response.content)
        fp.close()

    return path


def create_dir(dirname):
    print(dirname, " --- created")
    os.makedirs(dirname)


def remove_file(filename):
    os.remove(filename)


def get_current_time_in_milisecs():
    return round(time.time() * 1000)


def join_path(dir, file):
    return os.path.join(dir, file)


def get_name_from_url(url):
    return os.path.basename(urlparse(url).path)


# def main():
#     print(
#         download_image(
#             "https://d3lzcn6mbbadaf.cloudfront.net/media/details/__sized__/ANI-20230913130734-thumbnail-320x180-70.jpg"
#         )
#     )


# if __name__ == "__main__":
#     main()
