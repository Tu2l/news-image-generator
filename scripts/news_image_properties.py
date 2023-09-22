class NewsImageProperties:
    def __init__(
        self,
        height,
        width,
        bg_color,
        font,
        font_size,
        download_dir,
        generated_image_dir,
    ):
        self.height = int(height)
        self.width = int(width)
        self.bg_color = bg_color
        self.font = font
        self.font_size = int(font_size)
        self.download_dir = download_dir
        self.generated_image_dir = generated_image_dir
