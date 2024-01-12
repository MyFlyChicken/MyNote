import os
import sys
import zlib
import time
from creat_rbl import MyPacket

def get_file_crc_and_size(file_path):
    # 计算文件的 CRC32 校验和
    with open(file_path, "rb") as f:
        file_data = f.read()
        crc = zlib.crc32(file_data)

    # 获取文件的大小
    file_size = len(file_data)

    return crc, file_size

def prepend_to_bin_file(packet, dst_path, src_path):
    # 将 MyPacket 对象转换为二进制数据
    packet_data = packet.to_bin()

    # 读取已有的二进制文件
    with open(src_path, "rb") as f:
        existing_data = f.read()

    # 将 MyPacket 的二进制数据追加到已有的二进制数据的开头
    new_data = packet_data + existing_data

    # 将追加后的数据写入文件
    with open(dst_path, "wb") as f:
        f.write(new_data)


def merge_files(bin1_path, bin1_start, bin1_end, bin2_path, bin2_start, bin2_end, bin3_path, bin3_start, bin3_end, output_path):
    # 读取第一个二进制文件
    with open(bin1_path, 'rb') as f1:
        data1 = f1.read()

    # 读取第二个二进制文件
    with open(bin2_path, 'rb') as f2:
        data2 = f2.read()

    # 读取第三个二进制文件
    with open(bin3_path, 'rb') as f3:
        data3 = f3.read()
    data3_back = data3
    # 确定合并后的总长度
    total_len = len(data1) + len(data2) + len(data3)

    # 对于大小不足终止地址的文件，填充0xFF
    if len(data1) < bin1_end - bin1_start + 1:
        data1 += b'\xFF' * (bin1_end - bin1_start - len(data1))
    if len(data2) < bin2_end - bin2_start + 1:
        data2 += b'\xFF' * (bin2_end - bin2_start - len(data2))
    if len(data3) < bin3_end - bin3_start + 1:
        data3 += b'\xFF' * (bin3_end - bin3_start - len(data3))

    # 将三个二进制文件合并为一个文件
    data = data1 + data2 + data3

    # 将合并后的数据写入输出文件
    with open(output_path, 'wb') as f4:
        f4.write(data)

    new_path = os.path.join(os.path.dirname(output_path), "upgrade.rbl")
    with open(new_path, 'wb') as f5:
        f5.write(data3_back)

if __name__ == '__main__':
    # 获取命令行参数
    bin1_path   = sys.argv[1]
    bin1_start  = int(sys.argv[2], 16)
    bin1_end    = int(sys.argv[3], 16)
    bin2_path   = sys.argv[4]
    bin2_start  = int(sys.argv[5], 16)
    bin2_end    = int(sys.argv[6], 16)    
    bin3_start  = int(sys.argv[7], 16)
    bin3_end    = int(sys.argv[8], 16)
    output_path = sys.argv[9]

    #bin3_path 和bin2_path路径一样，实际文件为根据bin2_path生成的rbl文件
    print (bin2_path)
    crc, file_size = get_file_crc_and_size(bin2_path)
    #print(crc, file_size)
    timestamp = int(time.time())
    #print(timestamp)
    #RBL必须为大写，qboot会校验这个字符串
    packet = MyPacket("RBL", 0, 0, timestamp, "app", "v0.1.8", "00010203040506070809", crc, crc, file_size, file_size)
    bin3_path = bin2_path.replace(".bin", ".rbl")
    #print(bin3_path)
    prepend_to_bin_file(packet, bin3_path, bin2_path)
    # 合并文件
    merge_files(bin1_path, bin1_start, bin1_end, bin2_path, bin2_start, bin2_end, bin3_path, bin3_start, bin3_end, output_path)
    print("merge finished! ok")
    