import os
import subprocess

ffmpeg_path = r"D:\ffmpeg-2025-04-23-git-25b0a8e295-full_build\ffmpeg-2025-04-23-git-25b0a8e295-full_build\bin\ffmpeg.exe"  # ffmpeg.exe 경로 확인
input_dir = r"D:\split_videos_ffmpeg"
output_dir = r"D:\split_videos_ffmpeg"

# 출력 폴더가 없으면 생성
os.makedirs(output_dir, exist_ok=True)

# 모든 mp4 파일 반복 처리
for filename in os.listdir(input_dir):
    if filename.endswith(".mp4"):
        video_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        audio_path = os.path.join(output_dir, f"{base_name}.mp3")

        cmd = [
            ffmpeg_path,
            "-i", video_path,
            "-vn",  # 비디오 제거
            "-acodec", "libmp3lame",  # mp3 코덱
            "-q:a", "2",  # 오디오 품질 (0=최상, 9=최하)
            audio_path
        ]

        print(f"[🔄] 추출 중: {filename}")
        subprocess.run(cmd, check=True)

print("✅ 모든 오디오 추출 완료!")
