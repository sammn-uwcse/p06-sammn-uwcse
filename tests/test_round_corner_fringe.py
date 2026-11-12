from PIL import Image

from thumbor.ext.filters import _round_corner


def test_transparent_round_corner_edge_has_no_dark_ring():
    # 40x40 opaque white RGBA image, corners rounded with radius 10,
    # transparent flag on, fill color white.
    width, height, radius = 40, 40, 10
    source = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    data = _round_corner.apply(
        1,
        "RGBA",
        radius,
        radius,
        255,
        255,
        255,
        width,
        height,
        source.tobytes(),
        1,
    )
    result = Image.frombytes("RGBA", (width, height), data)

    # Any pixel that is still visible must keep the original white.
    # Today the anti-aliased edge pixels stay opaque but have their
    # RGB scaled toward black, which draws a dark ring.
    dark_visible = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = result.getpixel((x, y))
            if a > 0 and (r, g, b) != (255, 255, 255):
                dark_visible.append((x, y, (r, g, b, a)))

    assert dark_visible == [], (
        f"{len(dark_visible)} visible edge pixels are darkened, "
        f"first few: {dark_visible[:5]}"
    )
