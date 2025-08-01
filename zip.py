import zipfile
import os

target_dir = r"C:\Users\dromii\Downloads\20250710_ori_migum\crack_test_mask_equalizeHist"
zip_path = r"C:\Users\dromii\Downloads\20250710_ori_migum\crack_test_mask_equalizeHist.zip"

with zipfile.ZipFile(zip_path, 'w') as zipf:
    for fname in os.listdir(target_dir):
        if fname.endswith('.png'):
            zipf.write(os.path.join(target_dir, fname), arcname=fname)

print("압축 완료")
