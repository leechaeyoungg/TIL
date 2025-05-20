import subprocess
import os

ffmpeg_path = r"D:\ffmpeg-2025-04-23-git-25b0a8e295-full_build\ffmpeg-2025-04-23-git-25b0a8e295-full_build\bin\ffmpeg.exe"  # 실제 경로에 맞게 수정
video_path = r"D:\HW 14일차_1_Q&A.mp4"
output_dir = r"D:\split_videos_ffmpeg"
os.makedirs(output_dir, exist_ok=True)

# 15분 단위 (900초)로 분할
segment_seconds = 2000

output_template = os.path.join(output_dir, "part_%03d.mp4")

cmd = [
    ffmpeg_path,
    "-i", video_path,
    "-c", "copy",
    "-map", "0",
    "-f", "segment",
    "-segment_time", str(segment_seconds),
    "-reset_timestamps", "1",
    output_template
]

print("분할 시작...")
subprocess.run(cmd, check=True)
print("완료! 🎉")
