import os

# 데이터셋 폴더 경로 설정
base_folder = r"I:\라벨링_분배\yolo_dataset"

folders = {
    "train": {
        "images": os.path.join(base_folder, 'train', 'images'),
        "labels": os.path.join(base_folder, 'train', 'labels')
    },
    "valid": {
        "images": os.path.join(base_folder, 'valid', 'images'),
        "labels": os.path.join(base_folder, 'valid', 'labels')
    },
    "test": {
        "images": os.path.join(base_folder, 'test', 'images'),
        "labels": os.path.join(base_folder, 'test', 'labels')
    }
}

def check_file_matching(images_path, labels_path):
    images = [f for f in os.listdir(images_path) if f.lower().endswith('.jpg')]
    labels = [f for f in os.listdir(labels_path) if f.lower().endswith('.txt')]

    # 이미지와 라벨의 파일명(확장자 제외) 비교
    image_names = set(os.path.splitext(f)[0] for f in images)
    label_names = set(os.path.splitext(f)[0] for f in labels)

    # 일치하지 않는 파일 확인
    unmatched_images = image_names - label_names
    unmatched_labels = label_names - image_names

    return unmatched_images, unmatched_labels

# 각 폴더에서 확인
for dataset, paths in folders.items():
    print(f"\n[INFO] {dataset.upper()} 데이터셋 파일명 검증 중...")
    unmatched_images, unmatched_labels = check_file_matching(paths["images"], paths["labels"])

    if unmatched_images:
        print(f"[WARNING] 일치하지 않는 이미지 파일: {unmatched_images}")
    if unmatched_labels:
        print(f"[WARNING] 일치하지 않는 라벨 파일: {unmatched_labels}")
    
    if not unmatched_images and not unmatched_labels:
        print(f"[INFO] {dataset.upper()} 데이터셋: 모든 이미지와 라벨 파일이 일치합니다.")
    else:
        print(f"[ERROR] {dataset.upper()} 데이터셋에서 일치하지 않는 파일이 있습니다.")
