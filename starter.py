from scripts.news_model import News, NewsEncoder
from scripts.news_image_properties import NewsImageProperties
from scripts.news_image_generator import NewsImageGenerator
from collections import namedtuple
import configparser
import json


def custom_news_decoder(newstDict):
    return namedtuple("X", newstDict.keys())(*newstDict.values())


def main():
    CONFIG_FILE_PATH = "config/config.ini"
    # init configurations
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    image_props = config["NewsImage"]
    directories_props = config["Directories"]

    image_props = NewsImageProperties(
        height=image_props["image.height"],
        width=image_props["image.width"],
        bg_color=image_props["image.bgcolor"],
        font=image_props["image.font"],
        font_size=image_props["image.font.size"],
        download_dir=directories_props["directories.downloded.images"],
        generated_image_dir=directories_props["directories.generated.images"],
    )

    # print(news_image_props)

    generator_obj = NewsImageGenerator(image_props)

    f = open(directories_props["directories.news"] + "news.json")
    data = json.load(f)
    f.close()

    for i, data in enumerate(data):
        # news_json = json.dumps(data, indent=4, cls=NewsEncoder)
        # news = json.loads(news_json, object_hook=custom_news_decoder)
        news = News(
            title=data["title"],
            image_url=data["imageUrl"],
            link=data["url"],
            timestamp=data["timestamp"],
            source=data["source"],
            story=data["story"],
        )
        print(i, news.title)
        generator_obj.generate_news_image(news=news)


if __name__ == "__main__":
    main()
