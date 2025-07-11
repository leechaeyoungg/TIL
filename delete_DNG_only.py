import os
import glob
import time

target_dir = r"I:\경기도_AI_실증지원사업\20250710_오리미금역촬영_서진형"
dng_files = glob.glob(os.path.join(target_dir, "*.DNG")) + glob.glob(os.path.join(target_dir, "*.dng"))

deleted_count = 0

for file_path in dng_files:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
        deleted_count += 1
    except PermissionError:
        print(f"PermissionError (in use): {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

print(f"\n총 삭제 시도: {len(dng_files)}")
print(f"성공적으로 삭제된 파일 수: {deleted_count}")
