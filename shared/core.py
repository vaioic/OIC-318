from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import skimage
from cellpose import models
from oic_toolkit import segment
from pylibCZIrw import czi as pyczi
from tqdm import tqdm


def process_directory(input_dir, output_dir, img_chunk_size=50):

    if not isinstance(input_dir, Path):
        input_dir = Path(input_dir)

    if not isinstance(output_dir, Path):
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True, parents=True)

    # Find image files
    file_list = list(input_dir.rglob("*.tif"))

    if not file_list:
        raise FileNotFoundError(f"No .tif files were found on path: {input_dir}")

    # Create the Cellpose model
    model = models.CellposeModel(gpu=True)

    source_base = input_dir.resolve()
    output_base = output_dir.resolve()

    # Process the images in chunks
    summary_data = []

    for i in tqdm(range(0, len(file_list), img_chunk_size), desc="Overall"):
        imgs = []
        imgs_original = []
        curr_path_list = file_list[i : i + img_chunk_size]

        curr_path_list_full = []

        for file in tqdm(curr_path_list, desc=f"Reading batch {i}", leave=False):
            img = skimage.io.imread(file)
            img_adj = preprocess_image(img)

            curr_path_list_full.append(file.resolve())
            imgs.append(img_adj)
            imgs_original.append(img)

        labels, _, _ = model.eval(imgs, flow_threshold=0.6, cellprob_threshold=-0.5)

        # Generate outputs and save masks
        for filepath, label, img, img_or in zip(
            curr_path_list, labels, imgs, imgs_original
        ):
            # Calculate the output file path
            file_source = filepath.resolve()
            relative_path = file_source.relative_to(source_base)
            target_output_dir = output_base / relative_path.parent

            target_output_dir.mkdir(parents=True, exist_ok=True)

            # Save cellpose mask
            save_path = target_output_dir / f"{filepath.stem}_mask.tif"
            skimage.io.imsave(save_path, label, check_contrast=False)

            # Identify blue cells
            blue_mask = segment_blue_regions(img_or)

            blue_mask[label == 0] = False

            # Measure data
            props = skimage.measure.regionprops_table(
                label,
                blue_mask,
                properties=(
                    "label",
                    "area",
                    "intensity_mean",
                    "centroid",
                ),
            )

            all_blue_counts = (props["area"] * props["intensity_mean"]).astype(int)

            raw_df = pd.DataFrame(props)
            raw_df["Image"] = filepath
            raw_df["blue_px_count"] = all_blue_counts
            raw_df["is_blue"] = all_blue_counts > 0

            save_path = target_output_dir / f"{filepath.stem}_rawdata.csv"
            raw_df.to_csv(save_path)

            # Calculate the summary data
            summary_data.append(
                {
                    "Image": str(filepath.stem),
                    "Dataset": str(filepath.parent),
                    "Num_cells": len(props["label"]),
                    "Num_blue_cells": np.count_nonzero(all_blue_counts > 0),
                }
            )

            # Save overlay
            ov = make_output_image(img_or, label, blue_mask, props)

            save_path = target_output_dir / f"{filepath.stem}_overlay.png"
            skimage.io.imsave(save_path, ov)

    # Save the summary data
    df = pd.DataFrame(summary_data)
    df.to_csv(output_dir / "summary.csv")


def make_output_image(img, labels, blue_mask, props):

    ov = skimage.segmentation.mark_boundaries(img, labels)
    ov = skimage.segmentation.mark_boundaries(ov, blue_mask, color=(1, 0, 1))

    ov_uint8 = (ov * 255).astype(np.uint8)

    for i in range(len(props["label"])):
        label = props["label"][i]

        y = int(props["centroid-0"][i])
        x = int(props["centroid-1"][i])

    cv2.putText(
        img=ov_uint8,
        text=str(label),
        org=(x, y),  # Coordinates as (X, Y)
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.4,  # Text size
        color=(255, 255, 255),  # White text in RGB
        thickness=1,
        lineType=cv2.LINE_AA,  # Smooth anti-aliased text
    )

    return ov_uint8


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


def segment_blue_regions(image, target_color=(53, 109, 124), min_region_size=15):

    blue_cell_mask = segment.match_color(skimage.util.img_as_ubyte(image), target_color)

    blue_cell_mask = skimage.morphology.remove_small_objects(
        blue_cell_mask, max_size=min_region_size
    )

    return blue_cell_mask
