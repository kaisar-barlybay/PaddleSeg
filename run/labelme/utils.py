import base64
import json
import os
from pathlib import Path

import cv2
import numpy as np
import PIL.Image
from labelme import utils


def generate_masks(base_path: str):
    jsons_path = os.path.join(base_path, 'jsons')
    images_path = os.path.join(base_path, 'images')
    masks_path = os.path.join(base_path, 'masks')
    for dpath in [jsons_path, images_path, masks_path]:
      Path(dpath).mkdir(parents=True, exist_ok=True)

    for json_name in os.listdir(jsons_path):
      json_path = os.path.join(jsons_path, json_name)
      fname = json_name.split('.')[0]
      mask_path = os.path.join(masks_path, f'{fname}.png')
      image_path = os.path.join(images_path, f'{fname}.png')

      data = json.load(open(json_path))
      imageData = data.get("imageData")

      if not imageData:
          imagePath = os.path.join(os.path.dirname(json_path), data["imagePath"])
          with open(imagePath, "rb") as f:
              imageData = f.read()
              imageData = base64.b64encode(imageData).decode("utf-8")
      img = utils.img_b64_to_arr(imageData)

      label_name_to_value = {"_background_": 0}
      for shape in sorted(data["shapes"], key=lambda x: x["label"]):
          label_name = shape["label"]
          if label_name in label_name_to_value:
              label_value = label_name_to_value[label_name]
          else:
              label_value = len(label_name_to_value)
              label_name_to_value[label_name] = label_value
      lbl, _ = utils.shapes_to_label(
          img.shape, data["shapes"], label_name_to_value
      )
      utils.lblsave(mask_path, lbl)
      PIL.Image.fromarray(img).save(image_path)

def refine_masks(base_path: str):
    masks_path = os.path.join(base_path, 'images')
    for fname in os.listdir(masks_path):
      mask_path = os.path.join(masks_path, fname)
      # Read the image
      image = cv2.imread(mask_path, 0)

      # Resize the image
      resized_image = cv2.resize(image, (400, 400), interpolation=cv2.INTER_LINEAR)

      # Apply Gaussian blurring
      blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0)

      # Determine distortion type
      contours, _ = cv2.findContours(blurred_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      # print(_, contours)
      contour_area = sum(cv2.contourArea(contour) for contour in contours)

      # Define kernel for morphological operations
      kernel = np.ones((3, 3), np.uint8)

      print(contour_area)
      some_threshold = 1000

      # Apply erosion or dilation based on distortion
      if contour_area < some_threshold:  # Threshold to be determined
          processed_image = cv2.erode(blurred_image, kernel, iterations=1)
      else:
          processed_image = cv2.dilate(blurred_image, kernel, iterations=1)

      cv2.imwrite(os.path.join(base_path, 'refined', fname), processed_image)

