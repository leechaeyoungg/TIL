from pathlib import Path
import shutil

# ---- 경로 설정 ----
SRC_IMAGES_DIR = Path(r"C:\Users\dromii\Downloads\20250710_ori_migum\20250710_tiled_512\images")
DST_MASKS_DIR  = Path(r"C:\Users\dromii\Downloads\crack_masks")

# ---- 옵션 ----
OVERWRITE = True   # True로 하면 동일 파일명이 있어도 덮어씀

def main():
    if not SRC_IMAGES_DIR.is_dir():
        raise FileNotFoundError(f"소스 폴더 없음: {SRC_IMAGES_DIR}")
    if not DST_MASKS_DIR.is_dir():
        raise FileNotFoundError(f"대상 폴더 없음: {DST_MASKS_DIR}")

    # 1) 대상 PNG 마스크의 '파일명(확장자 제외)' 수집
    mask_basenames = {p.stem.lower(): p for p in DST_MASKS_DIR.glob("*.png")}

    # 2) 소스 이미지 폴더에서 jpg/jpeg를 전부 인덱싱 (대소문자 무관)
    image_index = {}
    for p in SRC_IMAGES_DIR.iterdir():
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg"}:
            image_index[p.stem.lower()] = p  # 같은 이름이 있으면 마지막 항목으로 덮임

    # 3) 매칭되는 이미지만 복사
    copied, skipped, missing = 0, 0, 0
    for base in sorted(mask_basenames.keys()):
        src_img = image_index.get(base)
        if not src_img:
            missing += 1
            continue

        dst_path = DST_MASKS_DIR / src_img.name  # 원본 확장자/대소문자 유지
        if dst_path.exists() and not OVERWRITE:
            skipped += 1
            continue

        shutil.copy2(src_img, dst_path)
        copied += 1

    # 4) 요약 출력
    total_masks = len(mask_basenames)
    print(f"[완료] 마스크 개수: {total_masks}")
    print(f" - 복사됨: {copied}")
    print(f" - 이미 존재해서 건너뜀: {skipped}")
    print(f" - 매칭 이미지 없음: {missing}")

if __name__ == "__main__":
    main()
