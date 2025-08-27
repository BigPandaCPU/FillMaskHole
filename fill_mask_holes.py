import numpy as np
import cv2
import SimpleITK as sitk
from tqdm import tqdm
import argparse


def fill_holes_slices(img_array, direction="X"):
    """
    fill the 3d mask hole by slice from different direction
    """
    Z, Y, X = img_array.shape

    if direction == "Y":
        cur_img = np.zeros([Z, X, 4], dtype=np.uint8)
        for i in tqdm(range(Y)):
            cur_img[:] = 0
            cur_img[:, :, 3] = 255
            cur_binary = img_array[:, i, :]
            contours, hierarchy = cv2.findContours(cur_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(cur_img, contours, -1, (0, 0, 255), -1)

            cur_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(cur_gray, 1, 255, cv2.THRESH_BINARY)
            idx = np.where(binary > 0)

            cur_binary[:] = 0
            cur_binary[idx] = 255
            img_array[:, i, :] = cur_binary
    elif direction == "X":
        cur_img = np.zeros([Z, Y, 4], dtype=np.uint8)
        for i in tqdm(range(X)):
            cur_img[:] = 0
            cur_img[:, :, 3] = 255
            cur_binary = img_array[:, :, i]
            contours, hierarchy = cv2.findContours(cur_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(cur_img, contours, -1, (0, 0, 255), -1)

            cur_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(cur_gray, 1, 255, cv2.THRESH_BINARY)
            idx = np.where(binary > 0)

            cur_binary[:] = 0
            cur_binary[idx] = 255
            img_array[:, :, i] = cur_binary
    else:
        cur_img = np.zeros([Y, X, 4], dtype=np.uint8)
        for i in tqdm(range(Z)):
            cur_img[:] = 0
            cur_img[:, :, 3] = 255
            cur_binary = img_array[i, :, :]
            contours, hierarchy = cv2.findContours(cur_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(cur_img, contours, -1, (0, 0, 255), -1)

            cur_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(cur_gray, 1, 255, cv2.THRESH_BINARY)
            idx = np.where(binary > 0)

            cur_binary[:] = 0
            cur_binary[idx] = 255
            img_array[i, :, :] = cur_binary
    return img_array

def main(src_mask_file, save_mask_file, direction):
    """
    """
    img = sitk.ReadImage(src_mask_file)
    spacing = img.GetSpacing()
    origin = img.GetOrigin()
    img_array = sitk.GetArrayFromImage(img)
    img_array = fill_holes_slices(img_array, direction)
    img_new = sitk.GetImageFromArray(img_array)
    img_new.SetOrigin(origin)
    img_new.SetSpacing(spacing)
    sitk.WriteImage(img_new, save_mask_file, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_mask_file', help="mask file, only support nrrd or nii format, must have only one label, the value is > 1", required=True)
    parser.add_argument("-o", '--output_mask_file', help="filled hole mask file, saved as nrrd or nii file", required=True)
    parser.add_argument('-d', "--filling_direction", help="filling the hole from the direction, must be X, Y or Z", default="X", required=False)
    args = parser.parse_args()
    src_mask_file = args.input_mask_file
    save_mask_file = args.output_mask_file
    direction = args.filling_direction
    main(src_mask_file, save_mask_file, direction)

