from typing import Optional

from .process import ImgProcessor
from .renderer import Renderer
from .utils import DEFAULT_CHARSET


def asciify(
    image_path: str,
    color_mode: str = "color",
    edges_detection: bool = False,
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True,
    f_type: str = "in_terminal",
    blur: list[tuple[int, int], float, float] = [(9, 9), 1.5, 1.5],
    canny_thresh: tuple[int, int] = (200, 300),
    angles_thresh: int = 3,
    aspect_ratio_correction: float = 1.10
) -> str:
    """
    Draw the input image in ASCII art. This function wraps the objects defined in ``process.py`` and ``renderer.py`` and orchestrate their workflow.

    Refer to the doces for :class:`ImgProcessor` and :class:`Renderer` for further details.
    """

    processor = ImgProcessor(image_path)
    img_h, img_w, _ = processor.image.shape

    if not height and not width:
        term_height, term_width = processor.calculate_print_size()
    elif width and not height:
        term_width = width
        from .utils import get_font_aspect_ratio
        font_aspect_ratio = get_font_aspect_ratio() / aspect_ratio_correction
        term_height = int((img_h / img_w) * term_width / font_aspect_ratio)
    elif height and not width:
        term_height = height
        from .utils import get_font_aspect_ratio
        font_aspect_ratio = get_font_aspect_ratio() / aspect_ratio_correction
        term_width = int((img_w / img_h) * term_height * font_aspect_ratio)
    else:
        term_height, term_width = height, width

    ds_f = processor.calculate_downsample_factor(
        term_height=term_height,
        term_width=term_width,
        keep_aspect_ratio=keep_aspect_ratio,
        f_type=f_type,
        aspect_ratio_correction=aspect_ratio_correction,
    )
    ds_img = processor.downsample_image(f=ds_f, aspect_ratio_correction=aspect_ratio_correction, keep_aspect_ratio=keep_aspect_ratio)
    img_hsv = processor.convert_to_hsv(image=ds_img)
    angles = processor.calculate_angles(image=ds_img, k_size=angles_thresh)
    edges = processor.detect_edges(image=ds_img, blur=blur, canny_thresh=canny_thresh)

    renderer = Renderer(color_mode=color_mode, charset=DEFAULT_CHARSET)

    if edges_detection:
        return renderer.draw_in_ascii_with_edges(
            img_hsv=img_hsv, angles=angles, edges=edges
        )
    else:
        return renderer.draw_in_ascii(img_hsv=img_hsv)
