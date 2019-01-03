"""Sprite rendered UI elements (widget ancestors)."""

from stargateRL.objects.widgets import FilledBoxWidget
from stargateRL.objects.ftext import Text


class StringInput(FilledBoxWidget):
    """Simple string input."""

    def __init__(self, position, dimensions, colors, background_tile_id,
                 text_limit):
        """Construct the String Input."""
        text_static_color, text_input_color, background_tile_color = colors
        super(StringInput, self).__init__(position, dimensions, False,
                                          background_tile_color,
                                          background_tile_id)
        self._text = Text('INPUT:', text_static_color, position, dimensions,
                          batch=self._batch)
