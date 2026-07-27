import numpy as np
import skimage
from pylibCZIrw import czi as pyczi


def read_image(filepath):

    with pyczi.open_czi(filepath) as czidoc:
        scene_roi = czidoc.scenes_bounding_rectangle[0]

        image_data = czidoc.read(roi=scene_roi)

        return image_data


def preprocess_image(image):

    # Convert the image to a float
    img_float = skimage.util.img_as_float32(image)

    img_lab = skimage.color.rgb2lab(img_float)

    # Pull out the lightness channel
    lightness = img_lab[:, :, 0]

    # Try to even out the illumination
    background = skimage.filters.gaussian(lightness, sigma=60)
    corrected_lightness = lightness - background + np.mean(background)
    corrected_lightness = np.clip(corrected_lightness, 0.0, 100.0)

    enhanced_lightness = skimage.exposure.equalize_adapthist(
        corrected_lightness / 100.0, kernel_size=(8, 8), clip_limit=0.02
    )

    img_lab[:, :, 0] = enhanced_lightness * 100.0

    # Convert image back to rgb
    img_rgb = skimage.color.lab2rgb(img_lab)

    return img_rgb
