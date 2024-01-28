import os
import struct
import argparse

def pad_bin_file(file_path):
    # 在文件末尾添加100字节的0xff
    with open(file_path, 'ab') as f:
        f.write(b'\xff' * 100)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pad binary file with 0xff')
    parser.add_argument('file', type=str, help='path to binary file')
    parser.add_argument('-o', '--overwrite', action='store_true', help='overwrite original file')

    args = parser.parse_args()

    file_path = args.file
    overwrite = args.overwrite

    # 如果不覆盖原文件，则在文件名后添加后缀'_pad'
    if not overwrite:
        file_path = os.path.splitext(file_path)[0] + '_pad.bin'

    pad_bin_file(args.file)

    # 如果覆盖原文件，则删除原文件并将填充后的文件重命名为原文件名
    if overwrite:
        os.remove(args.file)
        os.rename(file_path, args.file)

    print("padding ok")
