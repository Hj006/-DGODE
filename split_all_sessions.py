import os
import re
import ffmpeg

avi_dir = r"G:\dataset\IEMOCAP_full_release\IEMOCAP_full_release\Session1\dialog\avi\DivX"
transcript_dir = r"G:\dataset\IEMOCAP_full_release\IEMOCAP_full_release\Session1\dialog\transcriptions"
output_root = r"G:\dataset\IEMOCAP\S1"  # 输出根目录

os.makedirs(output_root, exist_ok=True)

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


def cut_segment(video_path, start, end, out_video, out_audio):
    """使用 ffmpeg 从视频中切出一段无音轨 mp4 + 单声道 wav"""
    duration = end - start
    if duration <= 0:
        print(f"[WARN] skip invalid segment {out_video}")
        return

    # 视频（无音轨）
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


def process_video(video_path, transcript_path):
    """处理单个视频及其对应的转录文件"""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(output_root, video_name)
    os.makedirs(output_dir, exist_ok=True)

    segments = parse_transcript(transcript_path)
    print(f"Parsed {len(segments)} utterances for {video_name}.")

    for seg in segments:
        utt_id = seg["utt_id"]
        start, end = seg["start"], seg["end"]
        out_video = os.path.join(output_dir, f"{utt_id}.mp4")
        out_audio = os.path.join(output_dir, f"{utt_id}.wav")

        if os.path.exists(out_video) and os.path.exists(out_audio):
            continue

        print(f"  Cutting {utt_id}  [{start:.2f}-{end:.2f}]s ...")
        try:
            cut_segment(video_path, start, end, out_video, out_audio)
        except Exception as e:
            print(f"[ERROR] {utt_id}: {e}")

    print(f" All segments for {video_name} done!\n")


def main():
    mp4_files = [f for f in os.listdir(avi_dir) if f.endswith(".mp4")]

    if not mp4_files:
        print(f"[ERROR] no mp4 files found in {avi_dir}")
        return

    for fname in mp4_files:
        base = os.path.splitext(fname)[0]
        video_path = os.path.join(avi_dir, fname)
        transcript_path = os.path.join(transcript_dir, f"{base}.txt")

        if not os.path.exists(transcript_path):
            print(f"[WARN] missing transcript for {base}")
            continue

        process_video(video_path, transcript_path)

    print(" All videos processed successfully!")


if __name__ == "__main__":
    main()
