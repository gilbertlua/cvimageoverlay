import cv2
import numpy as np
from datetime import datetime
import os

class TwibbonGenerator:
    def __init__(self, base_image_path, overlay_image_path):
        self.base_image = cv2.imread(base_image_path)
        self.overlay_image = cv2.imread(overlay_image_path, cv2.IMREAD_UNCHANGED)
        
    def generate_twibbon(self, empty_area, output_dir="output", output_file_name=None):
        """Generates a twibbon and saves it in the output directory"""
        if self.base_image is None or self.overlay_image is None:
            raise ValueError("Base or overlay image not found")

        resized_base_image = cv2.resize(self.base_image, (empty_area['width'], empty_area['height']))
        combined_image = self.overlay_image.copy()

        x1, y1 = empty_area['x'], empty_area['y']
        x2, y2 = x1 + empty_area['width'], y1 + empty_area['height']

        if self.overlay_image.shape[2] == 4:  # Check for transparency
            alpha = self.overlay_image[y1:y2, x1:x2, 3] / 255.0  
            for c in range(0, 3):
                combined_image[y1:y2, x1:x2, c] = (
                    resized_base_image[:, :, c] * (1 - alpha) +
                    self.overlay_image[y1:y2, x1:x2, c] * alpha
                )
        else:
            combined_image[y1:y2, x1:x2, :3] = resized_base_image

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if output_file_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file_name = f"{output_dir}/twibbon_result_{timestamp}.png"

        cv2.imwrite(output_file_name, combined_image)
        print(f"Twibbon saved as: {output_file_name}")
        return output_file_name
