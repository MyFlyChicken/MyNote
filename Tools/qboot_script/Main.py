import shutil
import os
import sys
from AdiDsp import AdiDsp
from BinMerge import BinMerge
from QBoot import QBoot

def find_files(directory: str, suffix: str) -> list:
    """
    查找指定目录下以 .bin 结尾的文件

    :param directory: 要查找的目录路径
    :return: 以 .bin 结尾的文件列表
    """
    bin_files = []
    for filename in os.listdir(directory):
        if filename.endswith(suffix):
            bin_files.append(filename)
    return bin_files


if __name__ == "__main__":

    # {FAL_PART_MAGIC_WROD, "app",              "onchip_flash_bank0", 1024 *  60, 1024 * 144, 0},
    # {FAL_PART_MAGIC_WROD, "factory_app",      "onchip_flash_bank0", 1024 * 204, 1024 * 144, 0},
    # {FAL_PART_MAGIC_WROD, "download",         "onchip_flash_bank0", 1024 * 348, 1024 * 144, 0},
    # {FAL_PART_MAGIC_WROD, "tag",              "onchip_flash_bank0", 1024 * 492, 1024 *   2, 0},
    # {FAL_PART_MAGIC_WROD, "info",             "onchip_flash_bank0", 1024 * 494, 1024 *   2, 0},
    # {FAL_PART_MAGIC_WROD, "rsvd",             "onchip_flash_bank0", 1024 * 496, 1024 *  16, 0},

    # 需要与实际工程的Fal分区的地址相匹配
    factory_download_merge = [
        {"file": "./output_bins/bootloader.bin",    "offset": 0x00000000},
        {"file": "./output_bins/app.bin",           "offset": 0x0000F000},
        {"file": "./output_bins/app.rbl",           "offset": 0x00033000},
    ]   

    # 1 将bin文件拷贝到该目录
    bin_files = find_files("../Debug/", ".bin")
    if len(bin_files) < 1:
        print("Can't find file '*.bin' in the directory '../Debug/'.");
        sys.exit()

    shutil.copy("../Debug/" + bin_files[0], "./output_bins/app.bin")   

    # 2 将 app.bin 打包成qboot升级包 app.rbl
    app_rbl = QBoot("./output_bins/app.bin", "v1.0.0", "app", "010203040506070809")
    app_rbl.export_to_rbl("./output_bins/app.rbl")

    # 3 将 bootloader.bin 、 app.bin 、 app.rbl 组合成 factory_download.bin，这个是给工厂使用的烧录文件
    factory_download_bin = BinMerge()
    factory_download_bin.merge_bins("./output_bins/factory_download.bin", factory_download_merge)
    
