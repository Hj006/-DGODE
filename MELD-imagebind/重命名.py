import os
from pathlib import Path

# === 配置 ===
DIR = r"G:\dataset\MELD.Raw\test1"   # 改成你的目标文件夹路径
PREFIX = "final_videos_test"    # 需要去掉的前缀
DRY_RUN = True                  # 先试跑看看；确认OK后改为 False 执行

# 当去掉前缀后如果目标文件名已存在，是否自动改名避免覆盖
AUTO_DEDUPE = True              # True: 自动加后缀 _dup1, _dup2...
                               # False: 跳过并提示

def non_conflicting_name(folder: Path, name: str) -> str:
    """如果 name 已存在，返回 name_dupX.扩展名 的新名字。"""
    stem = Path(name).stem
    suffix = Path(name).suffix
    i = 1
    new_name = name
    while (folder / new_name).exists():
        new_name = f"{stem}_dup{i}{suffix}"
        i += 1
    return new_name

def main():
    folder = Path(DIR)
    if not folder.exists() or not folder.is_dir():
        print(f"[错误] 目录不存在或不是文件夹：{folder}")
        return

    to_rename = []
    for entry in folder.iterdir():
        if not entry.is_file():
            continue
        old_name = entry.name
        if old_name.startswith(PREFIX):
            new_name = old_name[len(PREFIX):]  # 去掉前缀
            # 去掉前缀后如果还残留分隔符（可选清理）
            # 例如前缀后面意外多了下划线或空格，这里顺便清掉一次
            while new_name.startswith(("_", "-", " ", ".")):
                new_name = new_name[1:]
            to_rename.append((entry, new_name))

    if not to_rename:
        print(f"没有发现以 '{PREFIX}' 开头的文件。")
        return

    print(f"将处理 {len(to_rename)} 个文件：")
    for src, new_name in to_rename:
        target_name = new_name
        target_path = src.parent / target_name

        if target_path.exists():
            if AUTO_DEDUPE:
                target_name = non_conflicting_name(src.parent, target_name)
                target_path = src.parent / target_name
                print(f"  冲突：{src.name} -> {new_name} 已存在，改为 {target_name}")
            else:
                print(f"  跳过（重名）：{src.name} -> {new_name}")
                continue

        print(f"  重命名：{src.name} -> {target_name}")

        if not DRY_RUN:
            src.rename(target_path)

    if DRY_RUN:
        print("\n[试跑] 未实际改名。确认输出无误后，将 DRY_RUN = False 再运行。")
    else:
        print("\n[完成] 已重命名。")

if __name__ == "__main__":
    main()
