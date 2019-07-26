import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string


def get_character_img(character, font, colour_mode="L", background="white", foreground="black"):
    assert len(character) == 1
    char_size = font.getsize("|")
    image = Image.new(colour_mode, char_size, background)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), character, foreground, font=font)
    return image


def render_text(text, font, colour_mode="L", img_size=None, background="white", foreground="black"):
    if img_size == None:
        char_size = font.getsize("|")
        lines = text.split("\n")
        img_width = max(map(len, lines)) * char_size[0]
        img_height = len(lines) * char_size[1]
        img_size = (img_width, img_height)

    image = Image.new(colour_mode, img_size, background)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, foreground, font=font)
    return image


def open_grayscale_img(filename):
    image = Image.open(filename)
    image = image.convert("L")
    return image


def get_image_blocks(image, block_size):
    # Block size must be in the form (width, height)
    image = np.array(image, dtype=np.int32)
    height, width = image.shape
    width_blocks = width // block_size[0]
    height_blocks = height // block_size[1]
    image_blocks = np.empty((height_blocks, width_blocks, block_size[1], block_size[0]), dtype=np.int32)
    for i in range(height_blocks):
        for j in range(width_blocks):
            block = image[i*block_size[1]:(i+1)*block_size[1], j*block_size[0]:(j+1)*block_size[0]]
            image_blocks[i, j] = block.reshape((1,1,block_size[1],block_size[0]))
    return image_blocks


def save_diagram_image(lines, circles, fname, x_limits=None, y_limits=None, linewidth=3, margin_pct=0.1, dpi=160):
    if x_limits is None:
        if len(lines) > 0:
            x_limits = [lines[0][0], lines[0][0]]
        elif len(circles) > 0:
            x_limits = [circles[0][0], circles[0][0]]
        else:
            x_limits = [0,0]
    if y_limits is None:
        if len(lines) > 0:
            y_limits = [lines[0][1], lines[0][1]]
        elif len(circles) > 0:
            y_limits = [circles[0][1], circles[0][1]]
        else:
            y_limits = [0,0]


    for x1, y1, x2, y2 in lines:
        x_limits[0] = min(x_limits[0], x1, x2)
        y_limits[0] = min(y_limits[0], y1, y2)
        x_limits[1] = max(x_limits[1], x1, x2)
        y_limits[1] = max(y_limits[1], y1, y2)
    for x, y, r in circles:
        x_limits[0] = min(x_limits[0], x - r)
        y_limits[0] = min(y_limits[0], y - r)
        x_limits[1] = max(x_limits[1], x + r)
        y_limits[1] = max(y_limits[1], y + r)

    margin = int(margin_pct * max(x_limits[1] - x_limits[0], y_limits[1] - y_limits[0]))

    x_limits[0], x_limits[1] = x_limits[0] - margin, x_limits[1] + margin
    y_limits[0], y_limits[1] = y_limits[0] - margin, y_limits[1] + margin

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)
    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_visible(False)
    cur_axes.axes.get_yaxis().set_visible(False)

    for x1, y1, x2, y2 in lines:
        line = plt.plot([x1, x2], [y1, y2], linewidth=linewidth, color="black")

    for x, y, r in circles:
        circle = plt.Circle((x, y), r, linewidth=linewidth, color="black", fill=False)
        ax.add_patch(circle)

    plt.savefig(fname, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    return x_limits, y_limits


def img2text(fname, fontsize, ttf_font_path, alphabet=string.punctuation+" "):
    font = ImageFont.truetype(ttf_font_path, fontsize)
    img = open_grayscale_img(fname)
    character_size = get_character_img("#", font).size
    character_width, character_height = character_size
    image_blocks = get_image_blocks(img, character_size)
    alphabet_size = len(alphabet)
    ascii_string = ""
    character_imgs = []

    for char in alphabet:
        char_img = np.array(get_character_img(char, font))
        character_imgs.append(char_img)
    character_imgs = np.vstack([character_imgs])

    for row in image_blocks:
        for block in row:
            block_stacked = np.broadcast_to(block, (alphabet_size,character_height,character_width))
            error = block_stacked - character_imgs
            error = error.reshape(alphabet_size, -1)
            mse = np.mean(np.square(error), axis=1)
            best_character_index = np.argmin(mse)
            ascii_string += alphabet[best_character_index]
        ascii_string += "\n"


    ascii_string = ascii_string[:-1]  # Remove trailing newline
    return ascii_string
