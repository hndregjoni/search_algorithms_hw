from typing import Any, TypeVar, Callable
from .state import GridState
from PIL import Image, ImageDraw, ImageFont

def draw_rectangle(im: Image, i: int, j: int, rec_dim: float):
    draw = ImageDraw.Draw(im)

    tl = (i*rec_dim, j*rec_dim)
    br = ((i+1)*rec_dim, (j+1)*rec_dim)

    draw.rectangle((*tl, *br), '#fff', '#000', 2)

def draw_text(im: Image, content: str, i: int, j: int, rec_dim: float) -> None:
    left = i * rec_dim + rec_dim/2
    top = j * rec_dim + rec_dim/2

    draw_centered_text(im, content, left, top)

def draw_centered_text(im: Image, content: str, x, y, fill=None) -> None:
    draw = ImageDraw.Draw(im)

    w,h = draw.textsize(content)
    draw.text((x - w/2,y - y/2), content, fill="#000", anchor='mm')


TDrawContent = TypeVar('TDrawContent')
def draw_grid_state(state: GridState[TDrawContent], rec_dim: float = 50, str_map: Callable[[TDrawContent], str] = str) -> Image:
    grid = state._state

    w: int = len(grid)
    h: int = len(grid[0]) 

    im = Image.new("RGB", (w*rec_dim, h*rec_dim))

    for j in range(h):
        for i in range(w):
            draw_rectangle(im, i, j, rec_dim)
            draw_text(im, str_map(grid[i][j]), i, j, rec_dim)
    
    return im


def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """

    # (C): https://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html

    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#%02x%02x%02x" % tuple(new_rgb_int)
