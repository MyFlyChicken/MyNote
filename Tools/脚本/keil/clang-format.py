import os
import subprocess

# 设置 clang-format 的路径
CLANG_FORMAT_PATH = r".\clang-format.exe"

# 设置要格式化的多个文件夹或文件
ROOT_DIRS = [
    r"..\boot\applications",
    r"..\boot\board\ports",
    r"..\boot\board\ports",
    r"..\boot\board\CubeMX_Config\Src",
    r"..\boot\board\CubeMX_Config\Src",        
    r"..\boot\user",
    r"..\boot\bsp",
    r"..\app\applications",
    r"..\app\user",
    r"..\app\bsp",
]

FORMAT_FILES = [
    r"..\boot\board\board.c",
    r"..\boot\board\board.h",  
    r"..\app\board\board.c",
    r"..\app\board\board.h",  
]

# 设置 .clang-format 文件的路径
CLANG_FORMAT_FILE = r".\.clang-format"

def format_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.cpp', '.h', '.c')):
                file_path = os.path.join(root, file)
                print(f"Formatting {file_path}")
                subprocess.run([CLANG_FORMAT_PATH, '-i', '--style=file', 
                                '--assume-filename=' + file_path, 
                                '--style=' + 'file:'+ CLANG_FORMAT_FILE, 
                                file_path])            

for directory in ROOT_DIRS:
    format_files_in_directory(directory)

for file in FORMAT_FILES:
    if os.path.isfile(file):
        print(f"Formatting {file}")
        subprocess.run([CLANG_FORMAT_PATH, '-i', '--style=file', 
                        '--assume-filename=' + file, 
                        '--style=' + 'file:'+ CLANG_FORMAT_FILE, 
                        file])

print("Formatting completed.")
