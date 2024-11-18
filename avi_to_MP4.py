import cv2

# 입력 및 출력 파일 경로 설정
input_video_path = r"C:\Users\dromii\20240401-송도\M3C\200m\obb_200m.avi"
output_video_path = r"C:\Users\dromii\20240401-송도\M3C\200m\obb_200m.MP4"

# 입력 비디오 열기
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# MP4 비디오 저장 설정 (mp4v 코덱 사용)
video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # 프레임을 MP4 비디오에 저장
    video_writer.write(frame)

cap.release()
video_writer.release()

print(f"비디오가 MP4 형식으로 변환되었습니다: {output_video_path}")
