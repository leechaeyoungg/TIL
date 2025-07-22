import os
import cv2
import numpy as np



# 1. 원본 고해상도 이미지가 있는 폴더 경로
INPUT_DIR = r"C:\Users\dromii\Downloads\20250710_ori_migum\20250710_lcy"

# 2. 분할된 타일 이미지를 저장할 폴더 경로 (폴더가 없으면 자동으로 생성됨)
OUTPUT_DIR = r"C:\Users\dromii\Downloads\20250710_ori_migum\lcy_tiles"

# 3. 타일 크기
TILE_WIDTH = 512
TILE_HEIGHT = 512

# 4. 타일 겹침 크기 (픽셀 단위)
#    - 경계에 걸친 객체가 잘리는 것을 방지하기 위함.
OVERLAP = 128


# 메인 로직 (이 아래는 수정할 필요 없음)


def tile_image(image_path, output_dir):
    """하나의 이미지를 받아서 겹치는 타일로 분할하여 저장하는 함수"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"경고: 이미지를 로드할 수 없습니다. 건너뜁니다: {image_path}")
            return 0
    except Exception as e:
        print(f"오류: 이미지 파일 '{os.path.basename(image_path)}'을(를) 읽는 중 오류 발생: {e}")
        return 0

    img_h, img_w, _ = image.shape
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # 보폭(Stride) 계산: 다음 타일로 얼마나 이동할지 결정
    stride_w = TILE_WIDTH - OVERLAP
    stride_h = TILE_HEIGHT - OVERLAP

    # 타일의 시작 좌표 리스트 생성
    # 이미지 경계를 포함하기 위해 마지막 좌표를 명시적으로 추가
    x_coords = list(range(0, img_w - TILE_WIDTH, stride_w)) + [img_w - TILE_WIDTH]
    y_coords = list(range(0, img_h - TILE_HEIGHT, stride_h)) + [img_h - TILE_HEIGHT]

    num_tiles = 0
    for y in y_coords:
        for x in x_coords:
            # 타일 추출
            tile = image[y : y + TILE_HEIGHT, x : x + TILE_WIDTH]
            
            # 타일 파일 이름 생성 (원본파일이름_tile_y좌표_x좌표.jpg)
            tile_filename = f"{base_name}_tile_y{y}_x{x}.jpg"
            output_path = os.path.join(output_dir, tile_filename)
            
            # 타일 저장 (JPEG 품질 95로 설정)
            cv2.imwrite(output_path, tile, [cv2.IMWRITE_JPEG_QUALITY, 95])
            num_tiles += 1
            
    return num_tiles

def main():
    """메인 실행 함수"""
    print("이미지 타일링을 시작합니다...")
    print(f"입력 폴더: {INPUT_DIR}")
    print(f"출력 폴더: {OUTPUT_DIR}")
    print(f"타일 크기: {TILE_WIDTH}x{TILE_HEIGHT}, 겹침: {OVERLAP}px")
    
    # 출력 폴더가 없으면 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 입력 폴더 내의 이미지 파일 목록 가져오기
    try:
        image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.jpg')]
        if not image_files:
            print("오류: 입력 폴더에 JPG 파일이 없습니다.")
            return
    except FileNotFoundError:
        print(f"오류: 입력 폴더를 찾을 수 없습니다: {INPUT_DIR}")
        return

    total_tiles_generated = 0
    total_images_processed = 0

    for filename in image_files:
        image_path = os.path.join(INPUT_DIR, filename)
        print(f"\n[{total_images_processed + 1}/{len(image_files)}] 처리 중: {filename}")
        
        num_generated = tile_image(image_path, OUTPUT_DIR)
        
        if num_generated > 0:
            print(f"-> {num_generated}개의 타일을 생성했습니다.")
            total_tiles_generated += num_generated
            total_images_processed += 1

    print("\n==================================================")
    print("모든 작업이 완료되었습니다.")
    print(f"총 {total_images_processed}개의 이미지에서 {total_tiles_generated}개의 타일을 생성했습니다.")
    print("==================================================")


if __name__ == "__main__":
    main()