"""
    qboot
"""

import sys
import struct
import time
import zlib

class QBoot:

    def __init__(self, input_file, version, part_name, prog_code) -> None:

        with open(input_file, "rb") as f:
            file_data = f.read()
            file_size = len(file_data)
            file_crc = zlib.crc32(file_data)

            self.input_file = input_file

            self.packet_type = "RBL"                # "rbl"
            self.algo = 0                           # 算法选择 不压缩，不加密
            self.algo2 = 0                          # 算法选择 不压缩，不加密
            self.time_stamp = int(time.time())      # 时间戳
            self.part_name = part_name              # 固件分区名
            self.fw_ver = version                   # 固件版本 "v0.1.8" 需要可选
            self.prog_code = prog_code              # 产品识别码，最大24字节
            self.pkg_crc = file_crc                 # 固件CRC
            self.raw_crc = file_crc                 # 打包CRC
            self.raw_size = file_size               # 打包尺寸
            self.pkg_size = file_size               # 固件尺寸
            self.hdr_crc = 0                        # 包头crc


    def export_to_rbl(self, output_file):
        # 将各个字段按照顺序打包为二进制数据
        # 使用 struct 模块来完成二进制打包
        # 格式说明：
        #   > 表示大端字节序
        #   4s 表示长度为 4 的字符串
        #   H 表示 unsigned short，即 16 位无符号整数
        #   I 表示 unsigned int，即 32 位无符号整数
        #   16s 表示长度为 16 的字符串
        #   24s 表示长度为 24 的字符串
        #   Q 表示 unsigned long long，即 64 位无符号整数
        #   f 表示 float，即单精度浮点数
        #   返回结果为 bytes 类型
        packed_data = struct.pack(
            "<4sHHI16s24s24sIIII",
            self.packet_type.encode(),
            self.algo,
            self.algo2,
            self.time_stamp,
            self.part_name.encode(),
            self.fw_ver.encode(),
            self.prog_code.encode(),
            self.pkg_crc,
            self.raw_crc,
            self.raw_size,
            self.pkg_size,            
        )

        self.hdr_crc = zlib.crc32(packed_data)
        packed_data += struct.pack("<I",self.hdr_crc)

        with open(self.input_file, "rb") as f:
            file_data = f.read()

        with open(output_file, "wb") as out:
            out.write(packed_data)
            out.write(file_data)
