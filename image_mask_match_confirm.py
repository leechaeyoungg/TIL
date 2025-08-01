import os
import cv2

# 원본 이미지 경로와 마스크 경로 (필요시 수정)
image_dir = r"C:\Users\dromii\Downloads\20250710_ori_migum\crack_test_dataset"
mask_dir = r"C:\Users\dromii\Downloads\20250710_ori_migum\crack_test_mask_equalizeHist"

images = os.listdir(image_dir)
masks = os.listdir(mask_dir)

found = False

for fname in images:
    base = os.path.splitext(fname)[0]
    mask_path = os.path.join(mask_dir, base + ".png")
    image_path = os.path.join(image_dir, fname)

    if not os.path.exists(mask_path):
        print(f"No mask for {fname}")
        found = True
        continue

    img = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if img.shape[:2] != mask.shape[:2]:
        print(f"⚠️ Size mismatch: {fname} vs {base}.png → "
              f"{img.shape[:2]} != {mask.shape[:2]}")
        found = True

if not found:
    print("모든 마스크가 이름과 해상도까지 일치합니다.")
