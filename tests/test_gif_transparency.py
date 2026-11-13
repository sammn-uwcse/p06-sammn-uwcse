from io import BytesIO

from PIL import Image, ImageDraw

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def test_resized_palette_gif_keeps_transparent_background():
    # Palette source: index 0 is transparent, index 1 is blue.
    source = Image.new("P", (40, 40), 0)
    source.putpalette([0, 0, 0, 0, 0, 255] + [0] * (768 - 6))
    ImageDraw.Draw(source).ellipse((5, 5, 34, 34), fill=1)
    buffer = BytesIO()
    source.save(buffer, "GIF", transparency=0)

    config = Config(PILLOW_PRESERVE_INDEXED_MODE=True)
    engine = Engine(Context(config=config))
    engine.image = engine.create_image(buffer.getvalue())
    engine.extension = ".gif"
    engine.resize(80, 80)

    output = engine.read(extension=".gif")

    # The top left corner was transparent in the source and must stay so.
    result = Image.open(BytesIO(output)).convert("RGBA")
    assert result.getpixel((0, 0))[3] == 0
