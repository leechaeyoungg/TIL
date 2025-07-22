import sys
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from contextlib import nullcontext
import os

# ====================== 경로 및 설정 (사용자 수정 필요) ======================
# SAM2 프로젝트 경로
sys.path.append(r"C:\Users\dromii\segment-anything-2")
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

# 모델 가중치 및 설정 파일 경로
sam2_checkpoint = r"C:\Users\dromii\segment-anything-2\checkpoints\sam2_hiera_large.pt"
sam2_model_cfg = r"C:\Users\dromii\segment-anything-2\sam2_configs\sam2_hiera_l.yaml"

# 추출할 이미지 경로
image_path = r"C:\Users\dromii\Downloads\20250710_ori_migum\20250710_lcy\DJI_0177.JPG"

# ====================== 장치 설정 ======================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ====================== 모델 로드 ======================
# Hydra 설정은 predict.py 등을 실행하지 않으면 필요 없을 수 있습니다.
# 만약 오류가 발생하면 원래 코드처럼 hydra 초기화를 추가하세요.
try:
    sam2_model = build_sam2(sam2_model_cfg, sam2_checkpoint, device=device)
    sam2_predictor = SAM2ImagePredictor(sam2_model)
    print("SAM2 model loaded successfully.")
except Exception as e:
    print(f"Error loading SAM2 model. Ensure Hydra is configured if needed: {e}")
    # Hydra 초기화 코드 추가 (원본 코드 참고)
    import hydra
    config_dir = os.path.join(os.path.dirname(sam2_checkpoint), "..", "sam2_configs")
    hydra.core.global_hydra.GlobalHydra.instance().clear()
    hydra.initialize_config_dir(config_dir=config_dir, version_base="1.1")
    sam2_model = build_sam2(sam2_model_cfg, sam2_checkpoint, device=device)
    sam2_predictor = SAM2ImagePredictor(sam2_model)
    print("SAM2 model loaded successfully after Hydra initialization.")


# ====================== 이미지 로드 및 OpenCV 변환 ======================
image = Image.open(image_path)
image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB) # Matplotlib 시각화용

# ====================== 인터랙티브 포인트 선택 ======================
input_points = []
window_name = 'Select Road Points - Press "s" to segment, "r" to reset, "q" to quit'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.imshow(window_name, image_cv)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        input_points.append([x, y])
        cv2.circle(image_cv, (x, y), 10, (0, 255, 0), -1) # 클릭 지점에 녹색 점 표시
        cv2.imshow(window_name, image_cv)

cv2.setMouseCallback(window_name, mouse_callback)

print('도로 영역에 포함되는 지점들을 마우스로 클릭하세요.')
print('선택이 완료되면 "s" 키를, 다시 선택하려면 "r" 키를, 종료하려면 "q" 키를 누르세요.')

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()
        sys.exit("작업을 종료합니다.")
    elif key == ord('r'):
        input_points = []
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # 이미지 초기화
        cv2.imshow(window_name, image_cv)
        print("포인트를 초기화했습니다. 다시 선택하세요.")
    elif key == ord('s'):
        if not input_points:
            print("선택된 포인트가 없습니다. 하나 이상 선택해주세요.")
            continue
        cv2.destroyAllWindows()
        break

# ====================== SAM2를 이용한 도로 영역 분할 ======================
print(f"선택된 포인트 수: {len(input_points)}")
print("SAM2로 도로 영역 분할을 시작합니다...")

# SAM2에 이미지 설정
sam2_predictor.set_image(image_rgb)

# 입력 포인트와 레이블 준비
# 모든 포인트는 객체에 포함되므로 레이블은 1
points_np = np.array(input_points)
labels_np = np.ones(len(points_np))

# 혼합 정밀도 컨텍스트
autocast_ctx = torch.autocast("cuda", dtype=torch.bfloat16) if torch.cuda.is_available() else nullcontext()

with torch.inference_mode(), autocast_ctx:
    masks, scores, _ = sam2_predictor.predict(
        point_coords=points_np,
        point_labels=labels_np,
        multimask_output=False,  # 가장 좋은 마스크 하나만 반환
    )

if masks is None:
    print("분할된 영역을 찾지 못했습니다.")
    sys.exit()

if masks is None:
    print("분할된 영역을 찾지 못했습니다.")
    sys.exit()

# [수정] SAM2 출력 마스크를 boolean 타입으로 변환
# masks[0]은 이미 NumPy 배열이므로 바로 사용합니다.
road_mask_scores = masks[0]
road_mask = road_mask_scores > 0.0 # 임계값 0.0을 적용하여 boolean 마스크 생성

print(f"Mask shape: {road_mask.shape}, Mask dtype: {road_mask.dtype}")
print(f"Number of True pixels in mask: {np.sum(road_mask)}")

# ====================== 결과 시각화 및 저장 ======================
# 원본 이미지에 마스크 오버레이
overlay_image = image_rgb.copy()
# ... (이하 코드는 동일)


# ====================== 결과 시각화 및 저장 ======================
# 원본 이미지에 마스크 오버레이
overlay_image = image_rgb.copy()
color_mask = np.array([255, 0, 0], dtype=np.uint8) # 도로 영역을 빨간색으로 표시



color_mask = np.array([255, 0, 0], dtype=np.uint8) # 도로 영역을 빨간색으로 표시

alpha = 0.5 # 오버레이 투명도
overlay_image[road_mask] = (overlay_image[road_mask] * (1 - alpha) + color_mask * alpha).astype(np.uint8)

# 선택된 포인트 표시
for point in input_points:
    cv2.circle(overlay_image, tuple(point), 15, (0, 255, 0), -1) # 녹색 점

# 시각화
plt.figure(figsize=(15, 15))
plt.imshow(overlay_image)
plt.title("Extracted Road Area")
plt.axis('off')
plt.show()

# 마스크 저장 (후속 작업에 사용)
# 마스크는 0과 255 값을 가지는 흑백 이미지로 저장하는 것이 일반적
road_mask_binary = (road_mask * 255).astype(np.uint8)
output_mask_path = "road_mask.png"
cv2.imwrite(output_mask_path, road_mask_binary)
print(f"도로 영역 마스크가 '{output_mask_path}' 파일로 저장되었습니다.")

# 원본 이미지에서 도로 영역만 추출하여 저장
road_only_image = image_rgb.copy()
road_only_image[~road_mask] = 0 # 도로가 아닌 영역은 검은색으로 처리
plt.figure(figsize=(15, 15))
plt.imshow(road_only_image)
plt.title("Road Area Only")
plt.axis('off')
plt.show()

output_road_path =r"C:\Users\dromii\Downloads\road_out_result.png"
cv2.imwrite(output_road_path, cv2.cvtColor(road_only_image, cv2.COLOR_RGB2BGR))
print(f"추출된 도로 이미지가 '{output_road_path}' 파일로 저장되었습니다.")