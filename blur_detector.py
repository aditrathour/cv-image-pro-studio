import cv2
import numpy as np
import os
from datetime import datetime

def pro_studio_master(image_path, my_name="Adit Rathour"):
    # 1. Load the photo
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not find photo at {image_path}")
        return

    # --- TECHNICAL ANALYSIS REPORT ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Calculate Saturation Score
    hsv_orig = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_saturation = np.mean(hsv_orig[:,:,1])

    print(f"\n--- Technical Report: {os.path.basename(image_path)} ---")
    print(f"Sharpness Score: {sharpness:.2f}")
    print(f"Brightness Level: {brightness:.2f}")
    print(f"Saturation Score: {avg_saturation:.2f}")
    print("-" * 40)

    # --- PREPARE WATERMARK DATA ---
    current_date = datetime.now().strftime("%d/%m/%Y")
    stamp = f"{my_name} | {current_date}"
    h_i, w_i = img.shape[:2]

    # --- 1. GENERATE VIVID COLOR VERSION ---
    vivid = cv2.convertScaleAbs(img, alpha=1.3, beta=35)
    hsv = cv2.cvtColor(vivid, cv2.COLOR_BGR2HSV).astype("float32")
    (h, s, v) = cv2.split(hsv)
    s = np.clip(s * 1.4, 0, 255)
    color_final = cv2.cvtColor(cv2.merge([h, s, v]).astype("uint8"), cv2.COLOR_HSV2BGR)
    cv2.putText(color_final, stamp, (w_i - 450, h_i - 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    
    color_file = "final_vivid_edition.jpg"
    cv2.imwrite(color_file, color_final)
    os.startfile(color_file) # Opens the Color version
    print(f"Successfully opened: {color_file}")

    # --- 2. GENERATE AESTHETIC B&W VERSION ---
    contrast_img = cv2.convertScaleAbs(img, alpha=1.4, beta=-10)
    bw_gray = cv2.cvtColor(contrast_img, cv2.COLOR_BGR2GRAY)
    # Re-convert to BGR so we can add a white watermark
    bw_final = cv2.cvtColor(bw_gray, cv2.COLOR_GRAY2BGR)
    cv2.putText(bw_final, stamp + " (B&W)", (w_i - 550, h_i - 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    
    bw_file = "final_bw_edition.jpg"
    cv2.imwrite(bw_file, bw_final)
    os.startfile(bw_file) # Opens the B&W version
    print(f"Successfully opened: {bw_file}")

# EXECUTION
photo_address = r'C:\Users\aditr\OneDrive\Pictures\download.jpg'
pro_studio_master(photo_address)