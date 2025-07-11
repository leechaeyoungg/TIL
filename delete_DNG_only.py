import os
import glob

# 삭제할 디렉토리 경로 (백슬래시는 \\ 또는 r"" 형태로)
target_dir = r"I:\경기도_AI_실증지원사업\20250710_오리미금역촬영_서진형"

# .DNG 파일 전체 경로 목록 가져오기 (대소문자 구분 없이)
dng_files = glob.glob(os.path.join(target_dir, "*.DNG")) + glob.glob(os.path.join(target_dir, "*.dng"))

# 파일 삭제
for file_path in dng_files:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

print(f"총 삭제된 .DNG 파일 수: {len(dng_files)}")
