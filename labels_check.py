import cv2
import os
from PIL import Image
import numpy as np
import re

# 한글 경로에서 이미지를 읽는 함수
def imread_with_unicode(image_path):
    try:
        print(f"[INFO] 이미지 불러오기 시도: {image_path}")
        with Image.open(image_path) as img:
            image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            print(f"[INFO] 이미지 크기: {image.shape}")
            return image
    except Exception as e:
        print(f"[ERROR] 이미지를 불러올 수 없습니다: {image_path}, 오류: {e}")
        return None

# 특수 문자 제거 함수
def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

# PIL을 이용한 이미지 저장 함수
def save_with_pil(image, output_file):
    try:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        pil_image.save(output_file, format='JPEG')
        print(f"[INFO] PIL로 이미지 저장 완료: {output_file}")
    except Exception as e:
        print(f"[ERROR] PIL로 이미지 저장 실패: {output_file}, 오류: {e}")

# 바운딩박스 그리기 및 저장
def draw_bounding_boxes(image_path, label_path, output_path):
    # 이미지 읽기
    image = imread_with_unicode(image_path)
    if image is None:
        print(f"[ERROR] 이미지 데이터를 불러올 수 없습니다: {image_path}")
        return
    
    h, w, _ = image.shape
    
    # 라벨 파일 읽기
    try:
        with open(label_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if not lines:
            print(f"[WARNING] 라벨 파일이 비어 있습니다: {label_path}")
            return
    except FileNotFoundError:
        print(f"[ERROR] 라벨 파일을 찾을 수 없습니다: {label_path}")
        return
    
    for line in lines:
        data = line.strip().split()
        if len(data) != 5:
            print(f"[WARNING] 라벨 형식이 잘못되었습니다: {label_path}")
            continue
        
        class_id, x_center, y_center, box_width, box_height = map(float, data)
        x_center, y_center = x_center * w, y_center * h
        box_width, box_height = box_width * w, box_height * h
        x1, y1 = int(x_center - box_width / 2), int(y_center - box_height / 2)
        x2, y2 = int(x_center + box_width / 2), int(y_center + box_height / 2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"Class {int(class_id)}", (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, sanitize_filename(os.path.basename(image_path)))
    
    # OpenCV로 저장
    success = cv2.imwrite(output_file, image)
    if not success:
        print(f"[ERROR] OpenCV로 이미지 저장 실패: {output_file}")
        print(f"[DEBUG] 저장하려는 이미지 크기: {image.shape}")
        # PIL을 사용하여 저장 시도
        output_file_pil = output_file.replace('.jpg', '_PIL.jpg')
        save_with_pil(image, output_file_pil)
    else:
        print(f"[INFO] OpenCV로 이미지 저장 완료: {output_file}")

# 경로 설정
image_dir = r"I:\라벨링_분배\하영님"
label_dir = r"C:\Users\dromii\Downloads\하영님_labels"
output_dir = r"I:\라벨링_분배\하영님_시각화"

# 이미지 파일 리스트
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg'))]

# 파일별 처리
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    label_path = os.path.join(label_dir, os.path.splitext(image_file)[0] + '.txt')
    
    if not os.path.exists(label_path):
        print(f"[WARNING] 라벨 파일이 존재하지 않습니다: {label_path}")
        continue
    
    draw_bounding_boxes(image_path, label_path, output_dir)

print(f"바운딩박스 시각화 완료. 결과는 '{output_dir}'에 저장되었습니다.")




