import numpy as np
import skimage as sk
from bioio import BioImage
from matplotlib import pyplot as plt

test_file = "../data/Cropped for testing/UHRF1BRAF_NK-01_stitched_crop_01.czi"

reader = BioImage(test_file)

img = (reader.data).squeeze()

print(img.shape)
print(img.dtype)
print((np.max(img), np.min(img)))

img_filt = sk.filters.gaussian(img, sigma=0.5, channel_axis=-1)
img_ds = sk.exposure.rescale_intensity(img_filt, out_range=(0.0, 1.0))


background_gradient = sk.filters.gaussian(img_ds, sigma=100, channel_axis=-1)

# Divide original by background to normalize lighting, clip to prevent overflow
img_flattened = np.clip(img_ds / (background_gradient + 1e-5), 0.0, 1.0)


# plt.imshow(img_flattened)
# plt.show()

# Convert image to CIELAB
img_LAB = sk.color.rgb2lab(img_flattened)

target_color = (0.778, 0.901, 0.98)
target_LAB = sk.color.rgb2lab(np.array([[target_color]], dtype=np.float32))
target_LAB = target_LAB[0, 0, :]

print(target_LAB.shape)

color_similarity_radius = 12

mask = ((img_LAB[..., 1] - target_LAB[1]) ** 2 +
       (img_LAB[..., 2] - target_LAB[2]) ** 2) <= (color_similarity_radius ** 2)

mask = sk.morphology.closing(mask, sk.morphology.disk(4))
mask = sk.morphology.opening(mask, sk.morphology.disk(2))

# plt.subplot(1, 2, 1)
# plt.imshow(img_flattened)

# plt.subplot(1, 2, 2)
# plt.imshow(mask)
# plt.show()

# ov = sk.segmentation.mark_boundaries(img_ds, mask, mode="thick")
# plt.imshow(ov)
# plt.show()

# MAYBE watershed
labels = sk.measure.label(mask)
props = sk.measure.regionprops_table(labels, properties=("centroid",))

plt.imshow(sk.exposure.rescale_intensity(img, out_range=(0.0, 1.0)))
plt.scatter(props["centroid-1"], props["centroid-0"], 1)
plt.show()
