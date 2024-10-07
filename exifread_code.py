import exifread

# 이미지 파일 열기
with open(r"H:\20241002-FOD\FOD_JPG_Files\DJI_0467.JPG", 'rb') as image_file:
    # EXIF 데이터 읽기
    tags = exifread.process_file(image_file)

    # 모든 태그 출력
    for tag in tags.keys():
        print(f"{tag}: {tags[tag]}")
