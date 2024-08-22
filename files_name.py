import os

# 폴더 경로 설정
folder1 = r"C:\Users\dromii\Desktop\분뇨,퇴비\compost_livestock_waste"
folder2 = r"C:\Users\dromii\Desktop\분뇨,퇴비\compost_livestock_waste_labels"

# 파일 이름에서 확장자를 제거하는 함수
def remove_extension(filename):
    return os.path.splitext(filename)[0]

# 폴더 1의 파일 목록 가져오기
files1 = sorted([remove_extension(f) for f in os.listdir(folder1)])

# 폴더 2의 파일 목록 가져오기
files2 = sorted([remove_extension(f) for f in os.listdir(folder2)])

# 일치하지 않는 파일 이름을 담을 리스트
mismatch_files = []

# 두 파일 목록을 비교하여 일치하지 않는 파일 이름을 찾기
for file1, file2 in zip(files1, files2):
    if file1 != file2:
        mismatch_files.append((file1, file2))

# 결과 출력
if mismatch_files:
    print("일치하지 않는 파일 목록:")
    for f1, f2 in mismatch_files:
        print(f"폴더1: {f1} - 폴더2: {f2}")
else:
    print("전부 다 일치합니다.")

