import numpy as np
import skimage
from bioio import BioImage
from cellpose import models
from oic_toolkit import segment

from shared import core

img = skimage.io.imread(
    "../data/untiled_images/UHRF1BRAF_NK-01_stitched/UHRF1BRAF_NK-01_stitched_m001_ORG.tif"
)

img_adj = core.preprocess_image(img)

import matplotlib.pyplot as plt

# plt.imshow(img_adj)
# plt.show()

model = models.CellposeModel(gpu=True)
masks, _, _ = model.eval(img_adj, flow_threshold=0.4, cellprob_threshold=0.0)

target_color = (53, 109, 124)

plt.imshow(skimage.util.img_as_ubyte(img))
plt.show()

blue_cell_mask = segment.match_color(skimage.util.img_as_ubyte(img), target_color)

plt.imshow(blue_cell_mask)
plt.show()

ov = skimage.segmentation.mark_boundaries(img, masks)

ov = skimage.segmentation.mark_boundaries(ov, blue_cell_mask, color=(1, 0, 1))

plt.imshow(ov)
plt.show()
exit()

reader = BioImage("../data/UHRF1BRAF_NK-01_stitched_crop_01.czi")

img = (reader.data).squeeze()


print(img.shape)
print(img.dtype)

print(np.max(img))
print(np.min(img))

import matplotlib.pyplot as plt

# img_crop = img[::16, ::16, :]

# plt.imshow(skimage.util.img_as_ubyte(img_crop))
# plt.show()

plt.imshow(skimage.util.img_as_ubyte(img))
plt.show()
