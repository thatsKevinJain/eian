# Edited Images Analyser (EIAN)

Official documents like driving license, aadhar card, and PAN cards are used everywhere as a proof of identity. They are also clicked on smartphones to make them accessible digitally. Many times these images are edited using photoshop softwares which such precision that they become indistinguishable to the human eye.

This project attempts to analyse such images and detect traces which makes them different from their original counterparts.

We make use of `Error Level Analysis (ELA)` for proof of possible tampering of digital images.

ELA can be performed on images with lossy compression (like JPEG). By definition, ELA permits identifying areas within an image that are at different compression levels. With original images, the entire picture is roughly at the same level. Any section of the image at a different level might indicate a digital modification.

This module simply attempts to detect edited images and is not a full-proof source of truth, however, it should be used as a pipeline to further investigate images that are flagged using this algorithm.

### Assumptions
There are a set of assumptions that should be in place for the algorithm to work. They are - 
- The images provided should be in JPEG format.<br>
    - The algorithm does not work with PNG images
- The images provided should not be heavily compressed.<br>
    - Heavy compression strips the image of a lot of important data thus the algorithm fails to find significant differences in different parts of an image
- Typed characters on top of original images will produce sharp edges.<br>
    - This will be explained in detail in the description.

### Description
The algorithm works in the following steps - 
- Load the image provided by user (via URL or filepath)
- Sharpen the image by a small factor (to remove noisy regions) and convert the whole image to black and white.
- Apply Error Level Analysis -
    + Compress the image by 85% (constant value)
    + Generate a new image which is a pixel by pixel difference between the two images.<br>
    `difference_img = abs(original_img - compressed_img)`
- The difference image will not be visible because of close difference between original and compressed image. To solve this, we will find the tonal value of extrema (which is maximum pixel value) and use that to increase the brightness of the image.

If an image is edited, it will contain signatures that do not match that of an original image. By following the above process, we get a result that will contain white pixels scattered throughout the image. The scattering is random in an unedited image, but for an edited image, these pixels will appear very close to each other and specifically in the region of the edited portion.

- The above indentification is a visual process, so the module will use Connected Components Labelling (CCL) and Union-Find Algorithm (UFA) to create and analyse clusters.
    + A cluster is defined as a group of very close pixels spanning in a portion of the image.

- The final output will be a boolean value which will indicate if the image is edited or not.

### How to install
Check this [install guide](https://github.com/thatsKevinJain/eian/blob/master/INSTALL.md) to setup and test this library. It won't take more than 2 minutes :)
