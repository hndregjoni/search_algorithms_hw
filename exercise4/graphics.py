from .solution import UnblockState, Axis
from common.graphics import color_variant

from PIL import Image, ImageDraw

BORDER = "#A37C33"
TILE_AREA = "#6A491E"
TILE = "#DE7500"
MAIN_TILE = "#DB0000"

def create_image(rows: int, columns: int, edge_size: float, border: int) -> Image:
    width = 2*border + columns * edge_size
    height = 2*border + rows * edge_size

    # Draw the main background
    im = Image.new("RGB", (width, height), color=BORDER)

    # Draw the tile area 
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((border, border, width-border, height-border), fill=TILE_AREA, radius=5)
    # Draw the exit at roughly the 3rd tile:
    draw.rectangle((width-border-1, border+2*edge_size, width, border+3*edge_size), fill=TILE_AREA)

    return im

def draw_tile(im: Image, i: int, j: int, edge_size: float, axis: Axis, length: int, offset: float, main: bool = False, ):
    x1 = offset + i*edge_size
    y1 = offset + j*edge_size

    x2 = x1 + (1 if axis == Axis.V else length) * edge_size
    y2 = y1 + (1 if axis == Axis.H else length) * edge_size

    color = TILE if not main else MAIN_TILE
    stroke = color_variant(color, -10)

    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((x1, y1, x2, y2), fill=color, radius=5, outline=stroke, width=2)

def draw_unblock_state(state: UnblockState, edge_size: float = 50) -> Image:
    rows = state.h
    cols = state.w

    border = 10

    im = create_image(rows, cols, edge_size, border)

    # Draw the tiles:

    for tile in state._state:
        draw_tile(im, tile.coord[1], tile.coord[0], edge_size, tile.axis, tile.length, border, tile.index==0) 

    return im

