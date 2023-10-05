from PIL import Image, ImageFont, ImageDraw, ImageFilter
from string import Template
from scripts.news_model import News
from scripts.news_image_properties import NewsImageProperties
import scripts.util as util


class NewsImageGenerator:
    def __init__(self, props: NewsImageProperties):
        self.props = props

    def _get_wrapped_text(self, text: str, font: ImageFont.ImageFont, line_length: int):
        lines = [""]
        for word in text.split():
            line = f"{lines[-1]} {word}".strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return "\n".join(lines)

    def _create_image(self, size, bgColor):
        image = Image.new("RGB", size, bgColor)
        return image

    def _write_in_image(self, image: Image, message, font, fontColor):
        W, H = image.size
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), message, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), message, font=font, fill=fontColor)
        return image

    def generate_news_image(self, news: News):
        FG_IMAGE_SIZE_WIDTH = int(self.props.width - (self.props.width * 0.1))
        FG_IMAGE_SIZE_HEIGHT = int(self.props.width * 0.65)

        font = ImageFont.truetype(self.props.font, self.props.font_size)
        downloaded_filename = util.download_file(
            news.image_url, self.props.download_dir
        )
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

        text_box_bg = self._create_image(
            (self.props.width, int(self.props.height * 0.25)), self.props.bg_color
        )

        text_box_bg = self._write_in_image(
            image=text_box_bg,
            message=self._get_wrapped_text(news.title, font, FG_IMAGE_SIZE_WIDTH),
            font=font,
            fontColor=self.props.font_color,
        )

        offset_x = 0
        offset_y = int((self.props.height - text_box_bg.size[1]))

        # print(offset_x, offset_y)

        image.paste(text_box_bg, box=(offset_x, offset_y))

        image_name = (
            util.join_path(
                self.props.generated_image_dir, str(util.get_current_time_in_milisecs())
            )
            + ".png"
        )
        image.save(image_name)

        util.remove_file(downloaded_filename)

        return image_name
