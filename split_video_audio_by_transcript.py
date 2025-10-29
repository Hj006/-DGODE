import os
import re
import ffmpeg

video_path = r"G:\dataset\IEMOCAP_full_release\IEMOCAP_full_release\Session1\dialog\avi\DivX\Ses01F_impro01.mp4"
transcript_path = r"G:\dataset\IEMOCAP_full_release\IEMOCAP_full_release\Session1\dialog\transcriptions\Ses01F_impro01.txt"
output_root = r"G:\dataset\IEMOCAP\S1"  # 根输出文件夹

# 自动创建输出根目录
os.makedirs(output_root, exist_ok=True)

# 解析转录文件 
def parse_transcript(path):
    """
    解析转录文件行，例如：
    Ses01F_impro01_F000 [006.2901-008.2357]: Excuse me.
    返回 [{'utt_id': ..., 'start': ..., 'end': ..., 'text': ...}, ...]
    """
    pattern = re.compile(r"(\S+)\s*\[(\d+\.\d+)-(\d+\.\d+)\]:\s*(.*)")
    segments = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = pattern.match(line)
            if not m:
                continue
            utt_id, start, end, text = m.groups()
            segments.append({
                "utt_id": utt_id,
                "start": float(start),
                "end": float(end),
                "text": text.strip()
            })
    return segments

# 切分函数
def cut_segment(video_path, start, end, out_video, out_audio):
    """
    使用 ffmpeg 从视频中切出一段 mp4 + wav
    """
    duration = end - start
    if duration <= 0:
        print(f"[WARN] skip invalid segment {out_video}")
        return

    # 视频 
    (
        ffmpeg
        .input(video_path, ss=start, t=duration)
        .output(out_video, vcodec='libx264', preset='ultrafast', an=None, loglevel="error")
        .overwrite_output()
        .run(quiet=False)
    )

    # 音频 
    (
        ffmpeg
        .input(video_path, ss=start, t=duration)
        .output(out_audio, format='wav', ac=1, ar=16000, loglevel="error")
        .overwrite_output()
        .run(quiet=False)
    )

#  主流程 
def main():
    # 提取视频基名（例如 Ses01F_impro01）
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # 为该视频单独创建子文件夹
    output_dir = os.path.join(output_root, video_name)
    os.makedirs(output_dir, exist_ok=True)

    # 解析转录文件
    segments = parse_transcript(transcript_path)
    print(f"Parsed {len(segments)} utterances for {video_name}.")

    # 切分每个片段
    for seg in segments:
        utt_id = seg["utt_id"]
        start, end = seg["start"], seg["end"]

        out_video = os.path.join(output_dir, f"{utt_id}.mp4")
        out_audio = os.path.join(output_dir, f"{utt_id}.wav")

        if os.path.exists(out_video) and os.path.exists(out_audio):
            continue

        print(f"Cutting {utt_id}  [{start:.2f}-{end:.2f}]s ...")
        try:
            cut_segment(video_path, start, end, out_video, out_audio)
        except Exception as e:
            print(f"[ERROR] {utt_id}: {e}")

    print(f"All segments for {video_name} done!")

if __name__ == "__main__":
    main()
