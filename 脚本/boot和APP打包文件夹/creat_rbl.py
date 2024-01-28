import sys
import struct
import time
import zlib

class MyPacket:
    def __init__(self, packet_type, algo, algo2, time_stamp, part_name, fw_ver, prog_code, pkg_crc, raw_crc, raw_size, pkg_size):
        self.packet_type = packet_type    #"rbl"
        self.algo = algo                  #算法选择 不压缩，不加密
        self.algo2 = algo2                #算法选择 不压缩，不加密
        self.time_stamp = time_stamp      #时间戳
        self.part_name = part_name        #固件分区名 “app”
        self.fw_ver = fw_ver              #固件版本 "v0.1.8" 需要可选
        self.prog_code = prog_code        #产品识别码 “00010203040506070809”
        self.pkg_crc = pkg_crc            #固件CRC
        self.raw_crc = raw_crc            #打包CRC
        self.raw_size = raw_size          #打包尺寸
        self.pkg_size = pkg_size          #固件尺寸
        self.hdr_crc = 0            #包头crc
    def to_bin(self):
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
        return packed_data
