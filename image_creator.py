from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps


def create_image(size, bgColor):
    image = Image.new("RGB", size, bgColor)
    return image


def add_corners(im, rad):
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new("L", im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def main():
    MAIN_BG_BORDER_SIZE = 1
    MAIN_BG_SIZE = 1080
    SEC_BG_SIZE = int(MAIN_BG_SIZE - (MAIN_BG_SIZE * 0.1))

    # size recalculation due to border
    new_image_size = int(1080 - (MAIN_BG_BORDER_SIZE * 2))
    main_background = create_image((new_image_size, new_image_size), "#cacaca")
    main_background = ImageOps.expand(
        main_background,
        border=MAIN_BG_BORDER_SIZE,
        fill="#f0de1a",
    )

    # secondary_background = create_image((SEC_BG_SIZE, SEC_BG_SIZE), "gray")
    secondary_background = Image.open("generated_images/image_0.png").resize(
        (SEC_BG_SIZE, int(MAIN_BG_SIZE * 0.65)), resample=Image.BOX
    )

    secondary_background = secondary_background.filter(
        ImageFilter.GaussianBlur(radius=9)
    )

    offset_x = int((MAIN_BG_SIZE - SEC_BG_SIZE) / 2)
    offset_y = int((MAIN_BG_SIZE - SEC_BG_SIZE) / 2)
    print(offset_x, offset_y)

    main_background.paste(secondary_background, box=(offset_x, offset_y))

    offset_y = int((MAIN_BG_SIZE - 310))
    text_box_bg = create_image((SEC_BG_SIZE, int(MAIN_BG_SIZE * 0.25)), "white")
    # text_box_bg.putalpha(127)

    # text_box_bg = add_corners(im=text_box_bg, rad=10)

    # text_box_bg = ImageOps.expand(text_box_bg, border=1, fill="black")

    main_background.paste(text_box_bg, box=(offset_x, offset_y))

    main_background.save("main.png")


if __name__ == "__main__":
    main()
