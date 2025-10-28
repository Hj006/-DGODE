import os
import subprocess
from tqdm import tqdm


BASE_PATH = r"G:\图神经网络数据集\IEMOCAP_full_release\IEMOCAP_full_release"

# 所有 Session 名称
sessions = [f"Session{i}" for i in range(1, 6)]


# 检查 ffmpeg 是否可用
try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    print("FFmpeg found:", result.stdout.split("\n")[0])
except Exception as e:
    print("FFmpeg not found or not executable:", e)
    raise SystemExit


# 删除隐藏文件
def remove_hidden_and_ico_files(root_path):
    deleted = 0
    for root, _, files in os.walk(root_path):
        for f in files:
            if f.startswith(".") or f.startswith("._") or f.lower().endswith(".ico"):
                try:
                    os.remove(os.path.join(root, f))
                    deleted += 1
                except Exception as e:
                    print(f"Failed to delete {f}: {e}")
    return deleted

# 批量转换函数
def convert_avi_to_mp4(avi_file):
    """将单个 AVI 文件转换为 MP4，并删除原文件"""
    if not os.path.exists(avi_file):
        return False

    mp4_path = avi_file.replace(".avi", ".mp4")

    # 如果已存在 MP4，跳过
    if os.path.exists(mp4_path):
        return False

    try:
        # 单线程执行，防止过载
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", avi_file,
                "-c:v", "libx264", "-crf", "28",
                "-pix_fmt", "yuv420p",
                "-threads", "1",
                "-loglevel", "error",
                mp4_path
            ],
            check=True
        )

        # 检查输出文件是否生成
        if os.path.exists(mp4_path) and os.path.getsize(mp4_path) > 0:
            # 删除原始 .avi
            try:
                os.remove(avi_file)
            except Exception as e:
                print(f"Failed to delete {avi_file}: {e}")
            return True
        else:
            print(f"Failed: no output for {avi_file}")
            return False
    except Exception as e:
        print(f"FFmpeg error for {avi_file}: {e}")
        return False



# 处理所有 Session

for session in sessions:
    print(f"\nProcessing {session} ...")

    avi_path = os.path.join(BASE_PATH, session, "dialog", "avi", "DivX")

    if not os.path.exists(avi_path):
        print(f"AVI folder not found: {avi_path}")
        continue

    # 清理隐藏文件
    total_removed = remove_hidden_and_ico_files(avi_path)
    if total_removed > 0:
        print(f"Removed {total_removed} hidden/.ico files in {session}")

    # 找出所有 .avi 文件
    avi_files = [f for f in os.listdir(avi_path) if f.lower().endswith(".avi")]
    print(f"Found {len(avi_files)} .avi files to convert.")

    converted = 0
    for f in tqdm(avi_files, desc=f"Converting {session}"):
        avi_file = os.path.join(avi_path, f)
        if convert_avi_to_mp4(avi_file):
            converted += 1

    print(f"Conversion complete for {session}: {converted}/{len(avi_files)} files converted.")

print("\nAll sessions processed successfully.")
