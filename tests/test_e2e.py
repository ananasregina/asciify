import os
import pytest
import numpy as np
import cv2
from asciify.core import asciify
from asciify.mcp_server import mcp
import asyncio

# Helper to create test images
def create_test_image(path, size=(100, 100), color=(255, 255, 255), channels=3):
    if channels == 4:
        img = np.zeros((size[1], size[0], 4), dtype=np.uint8)
        img[:, :] = list(color) + [255]
    else:
        img = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        img[:, :] = color
    cv2.imwrite(path, img)
    return path

@pytest.fixture
def sample_image(tmp_path):
    path = str(tmp_path / "test.png")
    return create_test_image(path)

@pytest.fixture
def small_image(tmp_path):
    path = str(tmp_path / "small.png")
    return create_test_image(path, size=(50, 50))

@pytest.fixture
def large_image(tmp_path):
    path = str(tmp_path / "large.png")
    return create_test_image(path, size=(4000, 4000))

@pytest.fixture
def portrait_image(tmp_path):
    path = str(tmp_path / "portrait.png")
    return create_test_image(path, size=(100, 200))

@pytest.fixture
def landscape_image(tmp_path):
    path = str(tmp_path / "landscape.png")
    return create_test_image(path, size=(200, 100))

@pytest.fixture
def rgba_image(tmp_path):
    path = str(tmp_path / "rgba.png")
    return create_test_image(path, size=(100, 100), channels=4)

### Basic Functionality Tests

def test_asciify_basic(sample_image):
    result = asciify(sample_image, width=50)
    assert isinstance(result, str)
    assert len(result) > 0

def test_asciify_color_mode(sample_image):
    result_color = asciify(sample_image, width=50, color_mode="color")
    result_gray = asciify(sample_image, width=50, color_mode="grayscale")
    assert "\x1b[" in result_color
    assert "\x1b[" in result_gray
    # Grayscale should have white color codes
    assert "255;255;255m" in result_gray

def test_asciify_various_formats(tmp_path):
    for ext in ["jpg", "png"]:
        path = str(tmp_path / f"test.{ext}")
        create_test_image(path)
        result = asciify(path, width=50)
        assert len(result) > 0

### Parameter Combination Tests

def test_keep_aspect_ratio_partial_width(sample_image):
    # This was the bug reported by Tina
    result = asciify(sample_image, width=80, keep_aspect_ratio=True)
    assert len(result) > 0

def test_keep_aspect_ratio_partial_height(sample_image):
    result = asciify(sample_image, height=40, keep_aspect_ratio=True)
    assert len(result) > 0

def test_explicit_dimensions(sample_image):
    result = asciify(sample_image, width=80, height=40, keep_aspect_ratio=False)
    assert len(result) > 0

def test_aspect_ratio_correction(sample_image):
    for val in [0.5, 1.0, 1.1, 2.0]:
        result = asciify(sample_image, width=50, aspect_ratio_correction=val)
        assert len(result) > 0

def test_edges_detection(sample_image):
    result = asciify(sample_image, width=50, edges_detection=True)
    assert len(result) > 0

### Edge Case Tests

def test_very_small_image(small_image):
    result = asciify(small_image, width=10)
    assert len(result) > 0

def test_very_large_image(large_image):
    result = asciify(large_image, width=100)
    assert len(result) > 0

def test_unusual_aspect_ratios(portrait_image, landscape_image):
    assert len(asciify(portrait_image, width=50)) > 0
    assert len(asciify(landscape_image, width=50)) > 0

def test_rgba_image(rgba_image):
    result = asciify(rgba_image, width=50)
    assert len(result) > 0

def test_corrupted_image(tmp_path):
    path = str(tmp_path / "corrupted.png")
    with open(path, "w") as f:
        f.write("not an image")
    with pytest.raises(Exception): # Should fail gracefully
        asciify(path, width=50)

### MCP Server Persistence Tests

@pytest.mark.asyncio
async def test_mcp_persistence(sample_image, tmp_path):
    output_path = str(tmp_path / "output.txt")
    result_msg = await mcp.call_tool("asciify_image", {
        "image_path": sample_image,
        "output_path": output_path
    })
    
    assert os.path.exists(output_path)
    with open(output_path, "r") as f:
        content = f.read()
    assert len(content) > 0
    assert output_path in str(result_msg)

@pytest.mark.asyncio
async def test_mcp_default_output(sample_image):
    expected_output = os.path.splitext(os.path.basename(sample_image))[0] + "_ascii.txt"
    if os.path.exists(expected_output):
        os.remove(expected_output)
        
    await mcp.call_tool("asciify_image", {
        "image_path": sample_image
    })
    
    assert os.path.exists(expected_output)
    os.remove(expected_output)
