import os
import shutil

# 원본 이미지 및 라벨 경로
base_image_folder = r"C:\Users\dromii\Desktop\분뇨,퇴비\compost_livestock_waste"
label_folder = r"C:\Users\dromii\Desktop\분뇨,퇴비\compost_livestock_waste_labels"

# 기존 YOLO 데이터셋 경로
existing_dataset_folder = r"C:\Users\dromii\Desktop\분뇨,퇴비\yolo_dataset"
existing_train_folder = os.path.join(existing_dataset_folder, 'train', 'images')
existing_valid_folder = os.path.join(existing_dataset_folder, 'valid', 'images')
existing_test_folder = os.path.join(existing_dataset_folder, 'test', 'images')

# 새로운 YOLO 데이터셋 경로
output_folder = r"C:\Users\dromii\Desktop\분뇨,퇴비\yolo_dataset1"
train_image_folder = os.path.join(output_folder, 'train', 'images')
valid_image_folder = os.path.join(output_folder, 'valid', 'images')
test_image_folder = os.path.join(output_folder, 'test', 'images')
train_label_folder = os.path.join(output_folder, 'train', 'labels')
valid_label_folder = os.path.join(output_folder, 'valid', 'labels')
test_label_folder = os.path.join(output_folder, 'test', 'labels')

# 폴더가 존재하지 않으면 생성
os.makedirs(train_image_folder, exist_ok=True)
os.makedirs(valid_image_folder, exist_ok=True)
os.makedirs(test_image_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(valid_label_folder, exist_ok=True)
os.makedirs(test_label_folder, exist_ok=True)

# 기존 데이터셋의 이미지 파일 목록을 가져오기
existing_files = set(os.listdir(existing_train_folder)) | set(os.listdir(existing_valid_folder)) | set(os.listdir(existing_test_folder))

# 전체 파일 목록 가져오기
all_files = [f for f in os.listdir(base_image_folder) if f.lower().endswith('.jpg')]

# 기존 데이터셋에 없는 파일만 선별
new_files = [f for f in all_files if f not in existing_files]

# 기존 파일을 train, valid, test 폴더로 분배
train_files = list(existing_files.intersection(set(os.listdir(existing_train_folder))))
valid_files = list(existing_files.intersection(set(os.listdir(existing_valid_folder))))
test_files = list(existing_files.intersection(set(os.listdir(existing_test_folder))))

# 남은 파일을 주로 train에 추가하고, valid와 test로 분배
train_files.extend(new_files[:int(len(new_files) * 0.7)])
valid_files.extend(new_files[int(len(new_files) * 0.7):int(len(new_files) * 0.9)])
test_files.extend(new_files[int(len(new_files) * 0.9):])

# 겹치는 파일 제거
train_files = list(set(train_files))
valid_files = list(set(valid_files))
test_files = list(set(test_files))

# 총 파일 수 조정
total_files = len(train_files) + len(valid_files) + len(test_files)

# 필요한 경우 train에서 일부를 valid와 test로 이동
if total_files > 693:
    excess_files = total_files - 693
    if excess_files <= len(train_files):
        valid_files.extend(train_files[-excess_files:])
        train_files = train_files[:-excess_files]
    else:
        excess_files -= len(train_files)
        test_files.extend(valid_files[-excess_files:])
        valid_files = valid_files[:-excess_files]

# 파일 복사 함수
def copy_files(files, src_folder, dest_image_folder, dest_label_folder):
    for file in files:
        # 원본 파일 경로
        image_src_path = os.path.join(src_folder, file)
        
        # 대응하는 라벨 파일 이름 생성 (.jpg -> .txt)
        label_name = os.path.splitext(file)[0] + '.txt'
        label_src_path = os.path.join(label_folder, label_name)
        
        # 대상 경로 생성
        image_dest_path = os.path.join(dest_image_folder, file)
        label_dest_path = os.path.join(dest_label_folder, label_name)
        
        # 이미지 파일 복사
        shutil.copy2(image_src_path, image_dest_path)
        
        # 라벨 파일 존재 여부 확인 후 복사
        if os.path.exists(label_src_path):
            shutil.copy2(label_src_path, label_dest_path)
        else:
            print(f"경고: 라벨 파일이 없습니다. 이미지: {file}")

# 파일 복사 실행
copy_files(train_files, base_image_folder, train_image_folder, train_label_folder)
copy_files(valid_files, base_image_folder, valid_image_folder, valid_label_folder)
copy_files(test_files, base_image_folder, test_image_folder, test_label_folder)

# 각 데이터셋의 이미지 수 출력
print(f"Train 데이터셋: {len(train_files)}장")
print(f"Validation 데이터셋: {len(valid_files)}장")
print(f"Test 데이터셋: {len(test_files)}장")
print(f"총 이미지 수: {len(train_files) + len(valid_files) + len(test_files)}장")
print("YOLO 데이터셋이 성공적으로 구성되었습니다.")
