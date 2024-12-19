"""
    ADAU145x DSP export.
"""
import re
import sys
import struct

class DspEntry:
    def __init__(self, index, addr, data) -> None:
        self.index = index
        self.addr = addr
        self.data = data


class AdiDsp:
    def __init__(self, input_file) -> None:
        # 读取文件，按行转换
        with open(input_file, "r") as file:
            file_lines = file.readlines()

        # 开始转换数据
        self.__dsp_entries = []
        tmp_entry = DspEntry(0, [], [])
        cnt = 0

        for line in file_lines:
            index = self.__get_entry_index(line)
            if index < 0:
                # 本行是数据
                tmp_entry.data.extend(self.__get_hex(line))
            else:
                if cnt == 0:
                    # 第一行
                    pass
                else:
                    # 接收到完整的entry，保存后再处理下一个
                    self.__dsp_entries.append(DspEntry(tmp_entry.index, tmp_entry.addr, tmp_entry.data))

                cnt += 1

                # 本行是地址
                tmp_entry.index = index
                if self.__check_is_delay(line):
                    tmp_entry.addr = [255, 255] # 0xFF
                else:
                    tmp_entry.addr = self.__get_hex(line)

                tmp_entry.data = []

        # 保存最后一个entry
        self.__dsp_entries.append(DspEntry(tmp_entry.index, tmp_entry.addr, tmp_entry.data))


    def get_entry_sum(self):
        return len(self.__dsp_entries)


    def print_entry_info(self, index):
        tmp_entry = self.__dsp_entries[index]
        print(f"Entry({tmp_entry.index}) at addr({tmp_entry.addr}):")
        print(f"\tData: {tmp_entry.data}")


    def export_to_bin(self, output_file):
        """
        @output_file: The file to create
        Map Description:
        [addr] [len] [description]
        0      2     entry sum
        4*N    2     offset
        4*N+2  2     data length

        offset 2     regsiter addr
        offset+2 N   data
        """
        # 如果包数大于65535，报错
        entry_sum = self.get_entry_sum()
        if entry_sum > 65535:
            print(f"The num({entry_sum}) of entry is too large.")
            sys.exit()

        # 文件头部entry索引
        output_file_head = bytearray()

        # entry的数据区域
        output_file_data = bytearray()

        # entry数据区域的偏移，相对于整个文件的开头，因此起始地址是整个head之后
        data_offset = 4 * entry_sum + 2

        # entry总数
        output_file_head.extend(struct.pack('<H', entry_sum))

        for entry in self.__dsp_entries:
            output_file_head.extend(struct.pack('<H', data_offset))
            output_file_head.extend(struct.pack('<H', len(entry.data)))

            output_file_data.extend(entry.addr)
            data_offset += 2
            output_file_data.extend(entry.data)
            data_offset += len(entry.data)

        # 将数据保存到文件
        with open(output_file, "wb") as f:
            f.write(output_file_head)
            f.seek(0, 2)
            f.write(output_file_data)


    def __get_entry_index(self, line_str):
        """
        @line_str: The line to parse
        @ret: -1 for none and the other is the index
        """
        pattern = r'/\*\s\((\d+)\)\s.*\*/'
        match = re.search(pattern, line_str)
        
        if match:
            comment_number = int(match.group(1))
            return comment_number
        else:
            return -1


    def __get_hex(self, line_str):
        """
        @line_str: The str to translate
        @ret: The list of bytes
        """
        # 匹配注释
        pattern = r"/\*.*?\*/"

        # 去除注释
        cleaned_text = re.sub(pattern, "", line_str).strip()

        # 正则表达式模式，用于匹配十六进制字节
        pattern = r"0x[0-9A-Fa-f]{2}"

        # 使用 re.findall 进行匹配，返回匹配的列表
        hex_list = re.findall(pattern, cleaned_text)

        # 将每个十六进制字符串转换为单个字节（0-255 范围内的整数）
        num_list = [int(byte, 16) for byte in hex_list if 0 <= int(byte, 16) <= 255]

        return num_list


    def __check_is_delay(self, line_str):
        """
        @line_str: The str to check
        @ret: bool, check is delay entry
        """
        # 定义正则表达式模式
        pattern = r"Delay"
        
        # 使用 re.search 查找模式
        if re.search(pattern, line_str):
            return True
        else:
            return False


if __name__ == '__main__':
    dsp_dat = AdiDsp("../dsp_cfg/TxBuffer_IC_1.dat")
    dsp_dat.export_to_bin("../dsp_cfg/fal_dsp.bin")
