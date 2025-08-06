import os
import shutil
import glob

download_dir = r"C:\Users\student\Downloads"
target_dirs = {
    "images": ["*.jpg", "*.jpeg"],
    "data": ["*.csv", "*.xlsx"],
    "docs": ["*.txt", "*.doc", "*.pdf"],
    "archive": ["*.zip"]
}

for folder, patterns in target_dirs.items():
    dest_path = os.path.join(download_dir, folder)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(download_dir, pattern)):
            try:
                shutil.move(file_path, dest_path)
                print(f"{os.path.basename(file_path)} → {folder} 폴더로 이동")
            except Exception as e:
                print(f"{file_path} 이동 실패: {e}")