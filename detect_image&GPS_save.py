import cv2
import os
from ultralytics import YOLO
import re
from datetime import datetime, timedelta

# GPS 정보와 타임코드 추출 함수
def parse_srt_with_timecodes(srt_file):
    gps_data = []

    with open(srt_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # 정규 표현식 사용하여 타임코드와 GPS 정보 추출
    pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n<font size="28">.*?\n.*?\[latitude:\s*([\d\.\-]+)\]\s*\[longitude:\s*([\d\.\-]+)\]\s*\[rel_alt:\s*([\d\.\-]+)\s*abs_alt:\s*([\d\.\-]+)\]',
        re.IGNORECASE | re.DOTALL
    )

    matches = pattern.findall(srt_content)

    for match in matches:
        start_time, end_time, latitude, longitude, rel_altitude, abs_altitude = match
        gps_data.append({
            'start_time': start_time,
            'end_time': end_time,
            'latitude': float(latitude),
            'longitude': float(longitude),
            'relative_altitude': float(rel_altitude),
            'absolute_altitude': float(abs_altitude)
        })

    return gps_data

# 타임코드를 datetime 객체로 변환하는 함수
def timecode_to_datetime(timecode):
    return datetime.strptime(timecode, "%H:%M:%S,%f")

# 프레임에 가장 가까운 GPS 정보를 찾는 함수
def find_nearest_gps_info(timecode, gps_data, tolerance=timedelta(seconds=1)):
    target_time = timecode_to_datetime(timecode)
    closest_match = None
    smallest_diff = None

    for data in gps_data:
        start_time = timecode_to_datetime(data['start_time'])
        end_time = timecode_to_datetime(data['end_time'])

        if start_time <= target_time <= end_time:
            return data

        diff = min(abs((start_time - target_time).total_seconds()), abs((end_time - target_time).total_seconds()))
        if (smallest_diff is None or diff < smallest_diff) and diff <= tolerance.total_seconds():
            smallest_diff = diff
            closest_match = data

    return closest_match

# 프레임 번호에서 타임코드를 계산하는 함수
def frame_to_timecode(frame_num, fps, offset=timedelta(seconds=0)):
    total_seconds = frame_num / fps
    frame_time = timedelta(seconds=total_seconds) + offset
    hours, remainder = divmod(frame_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

# 객체 정보 표시 함수
def draw_boxes(frame, results, class_names):
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf[0]
        cls = int(box.cls[0])
        label = f"{class_names[cls]}: {conf:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

# 클래스 인덱스를 클래스 이름으로 매핑
class_names = ["Compost", "livestock_waste"]

# 동영상 경로 및 SRT 파일 경로 설정
video_path = r"D:\DJI_0880.MP4"
srt_file = r"D:\DJI_0880.SRT"
output_dir = r"D:\output_frames"

# 출력 디렉토리 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# YOLO 모델 로드
model = YOLO(r"D:\compost,livestock_waste_best.pt")

# SRT 파일에서 GPS 데이터 추출
gps_data = parse_srt_with_timecodes(srt_file)

# 동영상 파일 열기
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 모델에 프레임 전달하여 객체 감지
    results = model(frame)[0]

    # 감지된 객체가 있을 때 처리
    if len(results.boxes) > 0:
        # 프레임에 바운딩 박스, 클래스, 신뢰도 표시
        frame = draw_boxes(frame, results, class_names)

        # 프레임의 타임코드 계산
        timecode = frame_to_timecode(frame_count, fps)
        
        # 타임코드에 해당하는 GPS 정보 검색
        gps_info = find_nearest_gps_info(timecode, gps_data)

        # GPS 정보가 있는 경우 처리
        if gps_info:
            frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            
            with open(os.path.join(output_dir, f"frame_{frame_count:04d}_gps.txt"), 'w') as f:
                f.write(f"Latitude: {gps_info['latitude']}\n")
                f.write(f"Longitude: {gps_info['longitude']}\n")
                f.write(f"Relative Altitude: {gps_info['relative_altitude']} meters\n")
                f.write(f"Absolute Altitude: {gps_info['absolute_altitude']} meters\n")

            print(f"Saved {frame_filename} at location: "
                  f"Latitude: {gps_info['latitude']}, "
                  f"Longitude: {gps_info['longitude']}, "
                  f"Relative Altitude: {gps_info['relative_altitude']} meters, "
                  f"Absolute Altitude: {gps_info['absolute_altitude']} meters")
        else:
            print(f"No GPS info for frame {frame_count}, timecode {timecode}.")

    frame_count += 1

cap.release()













