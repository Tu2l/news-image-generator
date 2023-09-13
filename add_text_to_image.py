from PIL import Image, ImageFont, ImageDraw, ImageFilter
from urllib.parse import urlparse
import requests
import os
import json


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = [""]
    for word in text.split():
        line = f"{lines[-1]} {word}".strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return "\n".join(lines)


def download_image(url):
    response = requests.get(url)
    if response.status_code:
        filename = os.path.basename(urlparse(url).path)
        fp = open(filename, "wb")
        fp.write(response.content)
        fp.close()
    return Image.open(filename), filename


def create_image(size, bgColor):
    image = Image.new("RGB", size, bgColor)
    return image


def write_in_image(image: Image, message, font, fontColor):
    W, H = image.size
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), message, font=font, fill=fontColor)
    return image


def generate_news_image(image_url, news_title, image_title):
    BG_IMAGE_SIZE_WIDTH = 1080
    BG_IMAGE_SIZE_HEIGHT = 1080
    FG_IMAGE_SIZE_WIDTH = int(BG_IMAGE_SIZE_WIDTH - (BG_IMAGE_SIZE_WIDTH * 0.1))
    FG_IMAGE_SIZE_HEIGHT = int(BG_IMAGE_SIZE_WIDTH * 0.65)

    font = ImageFont.truetype("Roboto-Light.ttf", 50)

    foreground, downloaded_filename = download_image(image_url)

    image = foreground.resize(
        (BG_IMAGE_SIZE_WIDTH, BG_IMAGE_SIZE_HEIGHT), resample=Image.BOX
    )
    image = image.filter(ImageFilter.GaussianBlur(radius=9))

    foreground = foreground.resize(
        (FG_IMAGE_SIZE_WIDTH, FG_IMAGE_SIZE_HEIGHT), resample=Image.BOX
    )

    # foreground.putalpha(100)
    offset_x = (int)((BG_IMAGE_SIZE_WIDTH - FG_IMAGE_SIZE_WIDTH) / 2)
    offset_y = offset_x

    image.paste(foreground, box=(offset_x, offset_y))

    text_box_bg = create_image(
        (BG_IMAGE_SIZE_WIDTH, int(BG_IMAGE_SIZE_HEIGHT * 0.25)), "white"
    )

    text_box_bg = write_in_image(
        image=text_box_bg,
        message=get_wrapped_text(news_title, font, FG_IMAGE_SIZE_WIDTH),
        font=font,
        fontColor="black",
    )

    offset_x = 0
    offset_y = int((BG_IMAGE_SIZE_HEIGHT - text_box_bg.size[1]))

    # print(offset_x, offset_y)

    image.paste(text_box_bg, box=(offset_x, offset_y))

    image.save(image_title + ".png")
    os.remove(downloaded_filename)


def main():
    f = open("news.json")
    data = json.load(f)
    f.close()

    for i, news in enumerate(data):
        print(i, news["title"])
        generate_news_image(
            image_url=news["imageUrl"],
            news_title=news["title"],
            image_title="generated_images/image_" + str(i),
        )


if __name__ == "__main__":
    main()
