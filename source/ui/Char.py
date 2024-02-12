import arcade

from source.constant import TEXT_FILE, SPRITE_SCALING, TEXT_ORIGIN, TEXT_SIZE


class Char(arcade.Sprite):

    def __init__(self, index: int, x: int, y: int):
        if index < 25:
            ix = TEXT_ORIGIN[0] + index * (TEXT_SIZE + 1)
            iy = TEXT_ORIGIN[1]
        else:
            ix = TEXT_ORIGIN[0] + (index - 25) * (TEXT_SIZE + 1)
            iy = TEXT_ORIGIN[1] + TEXT_SIZE + 1
        super().__init__(
            filename=TEXT_FILE,
            scale=SPRITE_SCALING,
            image_x=ix,
            image_y=iy,
            image_width=TEXT_SIZE,
            image_height=TEXT_SIZE,
            center_x=x,
            center_y=y
        )
