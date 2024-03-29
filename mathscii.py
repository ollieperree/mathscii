from functools import reduce, partial
import numpy as np
import diagrams



def str_to_char_array(string):
    lines = string.split("\n")
    width = max(len(l) for l in lines)
    height = len(lines)
    return np.array([[c for c in l.ljust(width, " ")] for l in lines])


def text(string):
    return str_to_char_array(string)


def display(arr):
    print("\n".join(["".join(line) for line in arr]))


def big_sigma(width=9, height=8):
    # Includes a blank line at the bottom
    assert height >= 4
    assert width >= 2
    assert height % 2 == 0

    string = "_" * width
    string += "\n\\"
    if height > 4:
        string += " " * (width - 2) + "|"
    for i in range(1, (height // 2) - 1):
        string += "\n" + (" " * i) + "\\"
    for i in range((height // 2) - 1)[::-1]:
        string += "\n" + (" " * i) + "/"
    string += "_" * (width - 2)
    string += "|" if height > 4 else "_"
    string += "\n"

    return str_to_char_array(string)


def pi():
    string = "__\n||"
    return str_to_char_array(string)


def big_pi(width=10, height=6):
    # Includes a blank line at the bottom
    assert height >= 3
    assert width >= 2
    string = "_" * width
    d = (width - height - 2) // 2
    string += ("\n" + " " * d + "|" + " " * height + "|") * (height - 2)
    string += "\n"

    return str_to_char_array(string)


def integral(width=5, height=8):
    # Includes a blank line at the bottom
    assert width >= 5
    assert height >= 6
    assert width % 2 == 1

    string = " " * ((width // 2) + 1) + "_" * ((width // 2) - 1)
    string += "\n" + " " * (width // 2) + "/" + " " * ((width // 2) - 1) + "\\"
    string += ("\n" + " " * (width // 2) + "|") * (height - 4)
    string += "\n\\" + "_" * ((width // 2) - 1) + "/"
    string += "\n"

    return str_to_char_array(string)


def neq():
    """Not equal sign"""
    string = "___/_\n__/__\n /"
    return str_to_char_array(string)


def dots(width=5, height=3):
    assert width >= 3
    assert height >= 1

    string = ""
    for i in range(height):
        if i == height // 2:
            string += (" " * ((width - 1) // 3)).join("...") + "\n"
        else:
            string += " " * width + "\n"

    string = string[:-1]  # remove trailing newline
    return str_to_char_array(string)


def vdots(width=5, height=3):
    dot_vertical_spacing = (height + 1) // 3
    string = ""
    for i in range(height):
        if i % dot_vertical_spacing == 0:
            string += ".".center(width) + "\n"
        else:
            string += " " * width + "\n"

    string = string[:-1]  # remove trailing newline
    return str_to_char_array(string)


def ddots(width=5, height=3):
    dot_vertical_spacing = (height + 1) // 3
    dot_horizontal_spacing_per_line = (width + 1) // height
    string = "." + " " * (width - 1)  # Trailing spaces ensure that char_array shape is correct
    for i in range(1, height):
        string += "\n"
        if i % dot_vertical_spacing == 0:
            string += " " * i * dot_horizontal_spacing_per_line + "."

    return str_to_char_array(string)


def _center(char_array, height=None, width=None):
    char_array_height, char_array_width = char_array.shape

    if height is None:
        height = char_array_height
    else:
        assert height >= char_array_height
    if width is None:
        width = char_array_width
    else:
        assert width >= char_array_width

    vert_pad = height - char_array_height
    horiz_pad = width - char_array_width
    top_pad = vert_pad // 2
    bottom_pad = vert_pad - top_pad
    left_pad = horiz_pad // 2
    right_pad = horiz_pad - left_pad
    return np.pad(char_array, ((top_pad, bottom_pad), (left_pad, right_pad)), "constant", constant_values=" ")


def matrix(char_arrays:list, horizontal_gap=1, vertical_gap=0):
    """Creates a character array for a matrix. char_arrays should be a 2D list of character arrays. There is also a padding of 1 row/column around the outside."""
    # Find the maximum character array shape of each of the items
    char_array_width = 0
    char_array_height = 0
    n_rows = len(char_arrays)  # Number of rows
    n_columns = len(char_arrays[0]) # Number of columns (should probably check that the char_arrays is a complete matrix)
    for i in range(len(char_arrays)):
        for j in range(len(char_arrays[i])):
            item = char_arrays[i][j]
            if type(item) != np.ndarray:
                item = char_arrays[i][j] = str_to_char_array(str(item))
            item_height, item_width = item.shape
            char_array_width = max(char_array_width, item_width)
            char_array_height = max(char_array_height, item_height)
  
    width = char_array_width * n_columns + horizontal_gap * (n_columns + 1) + 4
    height = char_array_height * n_rows + vertical_gap * (n_rows + 1) + 3

    # First construct character array for blank matrix:
    string = " _" + " " * (width - 4) + "_ "
    for i in range(height - 2):
        string += "\n|" + " " * (width - 2) + "|"
    string += "\n|_" + " " * (width - 4) + "_|"
    matrix = str_to_char_array(string)

    # Now go through items in char_arrays and add them to the matrix
    for i in range(len(char_arrays)):
        for j in range(len(char_arrays[i])):
            item = char_arrays[i][j]
            item_height, item_width = item.shape
            item = _center(item, char_array_height, char_array_width)
            # Add item to matrix:
            x_pos = 2 + char_array_width * j + horizontal_gap * (j + 1)
            y_pos = 2 + char_array_height * i + vertical_gap * (i + 1)
            matrix[y_pos:y_pos+char_array_height, x_pos:x_pos+char_array_width] = item


    return matrix


def _concat_align_vertical(a, b, gap=0):
    """Places two char arrays horizontally next to each other (a to the left of b), vertically centered"""
    if type(a) != np.ndarray:
        a = str_to_char_array(str(a))
    if type(b) != np.ndarray:
        b = str_to_char_array(str(b))

    a_height, a_width = a.shape
    b_height, b_width = b.shape
    a_top_pad = a_bottom_pad = b_top_pad = b_bottom_pad = 0

    if a_height > b_height:
        delta_height = a_height - b_height
        b_top_pad = delta_height // 2
    elif a_height < b_height:
        delta_height = b_height - a_height
        a_top_pad = delta_height // 2

    # Construct array of spaces, then insert a and b in correct positions
    concatenated = np.full([max(a_height, b_height), a_width + gap + b_width], " ")
    concatenated[a_top_pad:a_top_pad+a_height, 0:a_width] = a
    concatenated[b_top_pad:b_top_pad+b_height, a_width+gap:a_width+gap+b_width] = b
    return concatenated


def concat(*items, spacing=0):
    return reduce(partial(_concat_align_vertical, gap=spacing), items)


def product(*items:list):
    return concat(*items, spacing=0)


def add(a, b):
    return concat(a, "+", b, spacing=1)


def frac(a, b, line_char="-", line_extra=2):
    """Fraction (a over b). line_extra is how much the line extends past the numerator and denominator (on each side)"""
    if type(a) != np.ndarray:
        a = str_to_char_array(str(a))
    if type(b) != np.ndarray:
        b = str_to_char_array(str(b))

    a_height, a_width = a.shape
    b_height, b_width = b.shape

    max_width = max(a_width, b_width)
    a = _center(a, width=max_width+2*line_extra)
    b = _center(b, width=max_width+2*line_extra)

    char_array = np.full([a_height+1+b_height, max_width+2*line_extra], " ")
    char_array[:a_height] = a
    char_array[a_height] = line_char  # Draw line
    char_array[a_height+1:] = b
    return char_array


def exp(a, b):
    """Places b above and to the right of a, which might look a bit like exponentiation"""
    if type(a) != np.ndarray:
        a = str_to_char_array(str(a))
    if type(b) != np.ndarray:
        b = str_to_char_array(str(b))

    a_height, a_width = a.shape
    b_height, b_width = b.shape
    char_array = np.full([a_height+b_height, a_width+b_width], " ")
    char_array[b_height:,:a_width] = a
    char_array[:b_height,a_width:] = b
    return char_array


def _left_parenthesis(height):
    assert height > 0
    if height == 1:
        return str_to_char_array("(")
    else:
        string = " /"
        for i in range(height - 2):
            string += "\n|"
        string += "\n \\"
        return str_to_char_array(string)


def _right_parenthesis(height):
    assert height > 0
    if height == 1:
        return str_to_char_array(")")
    else:
        string = "\\"
        for i in range(height - 2):
            string += "\n |"
        string += "\n/"
        return str_to_char_array(string)


def parentheses(a):
    """Puts parentheses around a"""
    if type(a) != np.ndarray:
        a = str_to_char_array(str(a))

    height, width = a.shape
    left = _left_parenthesis(height)
    right = _right_parenthesis(height)
    return concat(left, a, right)


def diagram(lines, circles, labels, fontsize=12, ttf_font_path="/usr/share/fonts/droid/DroidSansMono.ttf"):
    x_limits, y_limits = diagrams.save_diagram_image(lines, circles, "diagram.jpg")
    string = diagrams.img2text("diagram.jpg", fontsize, ttf_font_path)
    char_array = str_to_char_array(string)

    # Now add the labels
    height, width = char_array.shape
    x_range = x_limits[1] - x_limits[0]
    y_range = y_limits[1] - y_limits[0]
    for x, y, label_char_array in labels:
        if type(label_char_array) != np.ndarray:
            label_char_array = str_to_char_array(str(label_char_array))
        x_index = round(((x - x_limits[0]) / x_range) * width)
        y_index = round(((y_limits[1] - y) / y_range) * height)
        char_array[y_index:y_index+label_char_array.shape[0], x_index:x_index+label_char_array.shape[1]] = label_char_array

    return char_array


class Diagram:
    def __init__(self, fontsize=12, ttf_font_path="/usr/share/fonts/droid/DroidSansMono.ttf"):
        self.fontsize = fontsize
        self.ttf_font_path = ttf_font_path
        self.lines = []
        self.circles = []
        self.labels = []

    def circle(self, x, y, r):
        self.circles.append([x, y, r])

    def line(self, x1, y1, x2, y2):
        self.lines.append([x1, y1, x2, y2])

    def polygon(self, *coords):
        assert len(coords) % 2 == 0, "x and y coordinates for each vertex should be given as separate arguments"
        for i in range(0, len(coords) - 2, 2):
            self.lines.append([coords[i], coords[i+1], coords[i+2], coords[i+3]])
        self.lines.append([coords[-2], coords[-1], coords[0], coords[1]])

    def label(self, x, y, text):
        self.labels.append([x, y, text])

    def draw(self):
        return diagram(self.lines, self.circles, self.labels, self.fontsize, self.ttf_font_path)
