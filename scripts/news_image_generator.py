from PIL import Image, ImageFont, ImageDraw, ImageFilter
from string import Template
from scripts.news_model import News
from scripts.news_image_properties import NewsImageProperties
import scripts.image_gradient_generator as gradient
from scripts.image_gradient_generator import Rect

import scripts.util as util

class NewsImageGenerator:
    def __init__(self, props: NewsImageProperties):
        self.props = props

    def __get_wrapped_text(
        self, text: str, font: ImageFont.ImageFont, line_length: int
    ):
        lines = [""]
        for word in text.split():
            line = f"{lines[-1]} {word}".strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return "\n".join(lines)

    def __add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)),
                    (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def __create_tags(self, tag_text, size=(320, 50), bg_color="black", font_size=30, font_color="white"):
        font = ImageFont.truetype(self.props.font, font_size)
        tag_image = self.__create_image(size, bg_color)

        # draw = ImageDraw.Draw(tag_image)
        # draw.rounded_rectangle((-2.5, -2.5, size[0]+2.5, size[1]+2.5), fill=bg_color, outline="orange",
        #                        width=2, radius=8)
        tag_image = self.__write_in_image(
            tag_image, tag_text, font=font, fontColor=font_color)
        return tag_image

    def __create_image(self, size, bgColor):
        image = Image.new("RGB", size, bgColor)
        return image

    def __write_in_image(self, image: Image, message, font, fontColor):
        W, H = image.size
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), message, font=font)
        draw.text(((W - w) / 2, (H - h) / 2),
                  message, font=font, fill=fontColor)
        return image

    def generate_news_image(self, news: News):
        FG_IMAGE_SIZE_WIDTH = int(self.props.width * 0.8)
        FG_IMAGE_SIZE_HEIGHT = int(self.props.height * 0.6)

        font = ImageFont.truetype(self.props.font, self.props.font_size)

        try:
            downloaded_filename = util.download_file(
                news.image_url, self.props.download_dir
            )
        except:
            # use default image
            print("Unable to download image:", news.image_url)
            error_image = self.__create_image(
                (self.props.width, self.props.height), "red"
            )
            error_image = self.__write_in_image(
                error_image, "Image not available", font=font, fontColor="white"
            )
            error_image.save(self.props.download_dir + "/error.png")
            downloaded_filename = self.props.download_dir + "/error.png"

        foreground = Image.open(downloaded_filename)

        image = foreground.resize(
            (self.props.width, self.props.height), resample=Image.BOX
        )
        image = image.filter(ImageFilter.GaussianBlur(radius=9))

        foreground = foreground.resize(
            (FG_IMAGE_SIZE_WIDTH, FG_IMAGE_SIZE_HEIGHT), resample=Image.BOX
        )

        # foreground.putalpha(100)
        offset_x = (int)((self.props.width - FG_IMAGE_SIZE_WIDTH) / 2)
        offset_y = offset_x

        image.paste(foreground, box=(offset_x, offset_y))

        text_box_bg = self.__create_image(
            (self.props.width, int(self.props.height * 0.25)), self.props.bg_color
        )

        text_box_bg = self.__write_in_image(
            image=text_box_bg,
            message=self.__get_wrapped_text(
                news.title, font, FG_IMAGE_SIZE_WIDTH),
            font=font,
            fontColor=self.props.font_color,
        )

        offset_x = 0
        offset_y = int((self.props.height - text_box_bg.size[1]))

        # print(offset_x, offset_y)

        image.paste(text_box_bg, box=(offset_x, offset_y))

        # timestamp
        image.paste(self.__create_tags(str(news.timestamp)), box=(0, 0))

        # source
        image.paste(self.__create_tags(
            str("Source: "+news.source), size=(180, 50)), box=(self.props.width-180, 0))

        # handle tag
        image.paste(self.__create_tags(
            str("@autogennews_int"), size=(300, 50), bg_color="white", font_color="black"), box=(int((1080-300)/2), int(offset_y-30)))

        # desc instruction
        autogen_message = "This image is auto generated, it might contain errors. Please refer to the post description for information."
        image.paste(self.__create_tags(
            autogen_message, size=(self.props.width, 30), bg_color="white", font_color="black", font_size=20), box=(0, self.props.height-40))

        image_name = (
            util.join_path(
                self.props.generated_image_dir, str(
                    util.get_current_time_in_milisecs())
            )
            + ".png"
        )
       
        color_palette = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
        region = Rect(0, 0, FG_IMAGE_SIZE_WIDTH, FG_IMAGE_SIZE_HEIGHT)
        draw = ImageDraw.Draw(image)
        gradient.vert_gradient(draw, region, gradient.gradient_color, color_palette)

        image.save(image_name)

        util.remove_file(downloaded_filename)

        return image_name
