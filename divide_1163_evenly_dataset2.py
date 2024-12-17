import os
import shutil

# 원본 이미지 및 라벨 폴더
image_folders = [
    r"I:\라벨링_분배\이미지_데이터\성희님",
    r"I:\라벨링_분배\이미지_데이터\주한님",
    r"I:\라벨링_분배\이미지_데이터\지선님",
    r"I:\라벨링_분배\이미지_데이터\진수님",
    r"I:\라벨링_분배\이미지_데이터\하영님",
    r"I:\라벨링_분배\이미지_데이터\현구님",
    r"I:\라벨링_분배\이미지_데이터\채영님"
]

label_folders = [
    r"I:\라벨링_분배\라벨링_데이터\성희님_labels",
    r"I:\라벨링_분배\라벨링_데이터\주한님_labels",
    r"I:\라벨링_분배\라벨링_데이터\지선님_labels",
    r"I:\라벨링_분배\라벨링_데이터\진수님_labels",
    r"I:\라벨링_분배\라벨링_데이터\하영님_labels",
    r"I:\라벨링_분배\라벨링_데이터\강현구_labels",
    r"I:\라벨링_분배\라벨링_데이터\채영님_labels"
]

# 결과 데이터셋 폴더 설정
output_folder = r"I:\라벨링_분배\yolo_dataset"
train_image_folder = os.path.join(output_folder, 'train', 'images')
valid_image_folder = os.path.join(output_folder, 'valid', 'images')
test_image_folder = os.path.join(output_folder, 'test', 'images')
train_label_folder = os.path.join(output_folder, 'train', 'labels')
valid_label_folder = os.path.join(output_folder, 'valid', 'labels')
test_label_folder = os.path.join(output_folder, 'test', 'labels')

# 폴더 생성
os.makedirs(train_image_folder, exist_ok=True)
os.makedirs(valid_image_folder, exist_ok=True)
os.makedirs(test_image_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(valid_label_folder, exist_ok=True)
os.makedirs(test_label_folder, exist_ok=True)

# 파일 복사 함수 (폴더명을 추가하여 고유 파일명 생성)
def copy_files(file_list, dest_image_folder, dest_label_folder):
    copied_count = 0
    for image_path, label_path, folder_name in file_list:
        if os.path.exists(image_path) and os.path.exists(label_path):
            try:
                image_new_name = f"{folder_name}_{os.path.basename(image_path)}"
                label_new_name = f"{folder_name}_{os.path.basename(label_path)}"
                shutil.copy(image_path, os.path.join(dest_image_folder, image_new_name))
                shutil.copy(label_path, os.path.join(dest_label_folder, label_new_name))
                copied_count += 1
            except Exception as e:
                print(f"[ERROR] 복사 실패: {image_path}, 오류: {e}")
        else:
            print(f"[WARNING] 파일 누락: {image_path} 또는 {label_path}")
    print(f"[INFO] 복사된 파일 수: {copied_count}")

# 데이터셋 수집
all_files = []

for img_folder, lbl_folder in zip(image_folders, label_folders):
    images = [f for f in os.listdir(img_folder) if f.lower().endswith('.jpg')]
    labels = [f for f in os.listdir(lbl_folder) if f.lower().endswith('.txt')]
    
    # 이미지와 라벨 매칭
    image_base = set(os.path.splitext(f)[0] for f in images)
    label_base = set(os.path.splitext(f)[0] for f in labels)
    common_files = sorted(list(image_base & label_base))
    
    for file_base in common_files:
        image_path = os.path.join(img_folder, file_base + '.jpg')
        label_path = os.path.join(lbl_folder, file_base + '.txt')
        folder_name = os.path.basename(img_folder)  # 폴더명 추가
        all_files.append((image_path, label_path, folder_name))

# 데이터셋 나누기
train_count, valid_count, test_count = 930, 117, 116
train_files = all_files[:train_count]
valid_files = all_files[train_count:train_count + valid_count]
test_files = all_files[train_count + valid_count:train_count + valid_count + test_count]

# 파일 복사
print("[INFO] Train 데이터셋 복사 중...")
copy_files(train_files, train_image_folder, train_label_folder)
print("[INFO] Validation 데이터셋 복사 중...")
copy_files(valid_files, valid_image_folder, valid_label_folder)
print("[INFO] Test 데이터셋 복사 중...")
copy_files(test_files, test_image_folder, test_label_folder)

# 복사된 파일 수 확인
train_actual = len(os.listdir(train_image_folder))
valid_actual = len(os.listdir(valid_image_folder))
test_actual = len(os.listdir(test_image_folder))

print(f"Train 데이터셋: {train_actual}장")
print(f"Validation 데이터셋: {valid_actual}장")
print(f"Test 데이터셋: {test_actual}장")
print("데이터셋이 성공적으로 나누어졌습니다.")
