import os
import subprocess

# 输入目录：存放视频的文件夹
input_dir = r"G:\dataset\MELD.Raw\test\test_splits"

# 输出目录：目标 WAV 保存位置
output_dir = r"G:\dataset\MELD.Raw\test\wav"
os.makedirs(output_dir, exist_ok=True)

# 扫描所有 mp4 文件
for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(".mp4"):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name.replace(".mp4", ".wav"))

        # 构建 ffmpeg 命令
        command = [
            "ffmpeg",
            "-i", input_path,        # 输入视频
            "-vn",                   # 不要视频
            "-ac", "1",              # 单声道
            "-ar", "16000",          # 采样率 16kHz
            "-acodec", "pcm_s16le",  # PCM 编码
            output_path,
            "-y"                     # 覆盖已存在文件
        ]

        print(f"提取音频中: {file_name}")
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("所有音频已提取完成！保存目录：G:\\dataset\\MELD.Raw\\dev\\wav")
