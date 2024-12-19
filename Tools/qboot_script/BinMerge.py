"""
    Merge Bins
"""
from typing import List, Dict

class BinMerge:

    def merge_bins(self, output_file: str, dict_list_files: List[Dict[str, int]]) -> None:
        file_num = len(dict_list_files)
        print(f"{file_num} files will be merged")
        if file_num < 1:
            return

        # 创建输出文件并写入多个数据文件
        current_index = 0
        with open(output_file, "wb") as out:
            for file_info in dict_list_files:
                file = file_info['file']
                offset = file_info['offset']
                print(f"We will merge {file} at offset {offset}")

                # 填充0xFF
                if current_index < offset:
                    out.write(b'\xFF' * (offset - current_index))
                    current_index = offset

                # 移动到指定偏移位置
                out.seek(offset)

                # 读取源文件数据并写入到目标文件
                with open(file, "rb") as f:
                    data = f.read()
                    out.write(data)
                    current_index += len(data)


if __name__ == "__main__":
    merge_bins = [
        {"file": "./file1", "offset": 0},
        {"file": "./file2", "offset": 10}
    ]

    bin_merge = BinMerge()
    bin_merge.merge_bins("./out.bin", merge_bins)

