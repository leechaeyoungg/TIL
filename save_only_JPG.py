import os
import shutil

# 원본 폴더 경로
source_folder = r"C:\Users\dromii\Desktop\분뇨,퇴비\논_위의_분뇨,퇴비"

# JPG 파일을 저장할 새로운 폴더 경로
destination_folder = r"C:\Users\dromii\Desktop\분뇨,퇴비\논_위의_분뇨,퇴비_JPG"

# 폴더가 존재하지 않으면 생성
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 원본 폴더에서 파일들을 검사
for filename in os.listdir(source_folder):
    # 파일이 JPG 형식인지 확인
    if filename.lower().endswith(".jpg"):
        # 원본 파일의 전체 경로
        source_file = os.path.join(source_folder, filename)
        # 복사할 목적지의 전체 경로
        destination_file = os.path.join(destination_folder, filename)
        
        # 파일 복사
        shutil.copy(source_file, destination_file)

print("JPG 파일이 성공적으로 복사되었습니다.")
