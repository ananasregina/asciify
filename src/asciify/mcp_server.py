import os
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .core import asciify

# Create an MCP server
mcp = FastMCP("asciify-them")

@mcp.tool()
def asciify_image(
    image_path: str,
    output_path: Optional[str] = None,
    color_mode: str = "color",
    edges_detection: bool = False,
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True,
    f_type: str = "in_terminal",
    aspect_ratio_correction: float = 1.10
) -> str:
    """
    Generate ASCII art from an image and save it to disk.

    Args:
        image_path: Path to the image file.
        output_path: Optional path to save the generated ASCII art. Defaults to <input_filename>.txt.
        color_mode: Color mode for the output ("color" or "grayscale").
        edges_detection: Whether to enable edge detection.
        width: Optional width for the output.
        height: Optional height for the output.
        keep_aspect_ratio: Whether to maintain the aspect ratio.
        f_type: Output type ("in_terminal" or other).
        aspect_ratio_correction: Correction factor for character aspect ratio.
    
    Returns:
        The path to the saved ASCII art file.
    """
    ascii_art = asciify(
        image_path=image_path,
        color_mode=color_mode,
        edges_detection=edges_detection,
        width=width,
        height=height,
        keep_aspect_ratio=keep_aspect_ratio,
        f_type=f_type,
        aspect_ratio_correction=aspect_ratio_correction
    )

    if not output_path:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"{base_name}_ascii.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ascii_art)

    return f"ASCII art saved to: {os.path.abspath(output_path)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
