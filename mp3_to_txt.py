import os
import whisper

# Whisper 모델 로드 (base 또는 small/medium 선택 가능)
model = whisper.load_model("medium")  # 더 정밀하게 하고 싶다면 "medium" 추천

# 오디오 파일들이 있는 폴더
input_dir = r"D:\split_videos_ffmpeg"
output_dir = r"D:\split_videos_ffmpeg"
os.makedirs(output_dir, exist_ok=True)

# mp3 파일들 반복
for filename in os.listdir(input_dir):
    if filename.endswith(".mp3"):
        audio_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.txt")

        print(f"🎧 변환 중: {filename} ...")
        result = model.transcribe(audio_path)
        
        # 텍스트 저장
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

print("✅ 전체 텍스트 변환 및 저장 완료!")
