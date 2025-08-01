import os

# 입력 이미지 경로와 저장 경로 설정
input_dir = r"C:\Users\dromii\Downloads\20250710_ori_migum\crack_test_dataset"
output_txt_path = r"C:\Users\dromii\Downloads\20250710_ori_migum\crack_test_mask_equalizeHist_VOC\ImageSets\Segmentation\train.txt"

# 이미지 확장자 목록
valid_exts = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")

# 이미지 파일명(확장자 제거) 리스트 추출
image_names = [
    os.path.splitext(f)[0]
    for f in os.listdir(input_dir)
    if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith(valid_exts)
]

# 정렬 (선택사항)
image_names.sort()

# 출력 디렉터리가 없다면 생성
os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)

# 텍스트 파일로 저장
with open(output_txt_path, "w") as f:
    for name in image_names:
        f.write(name + "\n")

print(f"{len(image_names)}개 파일명이 저장되었습니다 → {output_txt_path}")
