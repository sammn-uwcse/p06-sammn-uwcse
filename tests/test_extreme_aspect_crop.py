import unittest

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.engines.pil import Engine
from thumbor.point import FocalPoint
from thumbor.transformer import Transformer


def _make_transformer(source_size, target_width, target_height):
    config = Config()
    context = Context(config=config)
    context.request = RequestParameters(
        width=target_width,
        height=target_height,
    )
    engine = Engine(context)
    engine.image = Image.new("RGBA", source_size, (255, 0, 0, 255))
    context.request.engine = engine
    transformer = Transformer(context)
    transformer.target_width = float(target_width)
    transformer.target_height = float(target_height)
    transformer.focal_points = [
        FocalPoint.from_alignment(
            "center", "middle", source_size[0], source_size[1]
        )
    ]
    return transformer


def _make_fit_in_transformer(source_size, width, height):
    config = Config()
    context = Context(config=config)
    context.request = RequestParameters(
        width=width,
        height=height,
        fit_in=True,
    )
    engine = Engine(context)
    engine.image = Image.new("RGBA", source_size, (255, 0, 0, 255))
    context.request.engine = engine
    return Transformer(context)


class ExtremeAspectCropTestCase(unittest.TestCase):
    def test_one_pixel_source_to_wide_short_target_is_not_empty(self):
        transformer = _make_transformer((1, 1), 50, 25)
        transformer.auto_crop()
        width, height = transformer.engine.image.size
        self.assertGreaterEqual(width, 1)
        self.assertGreaterEqual(height, 1)

    def test_one_pixel_source_to_wide_short_target_keeps_pixel(self):
        transformer = _make_transformer((1, 1), 50, 25)
        transformer.auto_crop()
        pixel = transformer.engine.image.getpixel((0, 0))
        self.assertEqual(pixel, (255, 0, 0, 255))

    def test_fit_in_940x2_to_width_100_height_0_is_100x1(self):
        transformer = _make_fit_in_transformer((940, 2), 100, 0)
        transformer._calculate_target_dimensions()
        transformer.fit_in_resize()
        self.assertEqual(transformer.engine.image.size, (100, 1))


if __name__ == "__main__":
    unittest.main()
