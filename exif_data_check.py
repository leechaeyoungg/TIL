from PIL import Image
from PIL.ExifTags import TAGS

# 이미지 파일 경로 설정
image_path = r"H:\20241002-FOD\M3C-01\DJI_0231.JPG"

# 이미지 열기
image = Image.open(image_path)

# EXIF 데이터 추출
exif_data = image._getexif()

# EXIF 데이터가 존재하는지 확인
if exif_data:
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f"{tag:25}: {value}")
else:
    print("No EXIF data found.")
