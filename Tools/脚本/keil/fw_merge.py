import os
import sys

# ================= 配置区域 =================

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 目录配置 (支持相对路径或绝对路径)
# Bootloader 构建输出目录
BOOT_BUILD_DIR = os.path.join(SCRIPT_DIR, "..", "project", "boot", "build_output")
# Application 构建输出目录
APP_BUILD_DIR = os.path.join(SCRIPT_DIR, "..", "project", "app", "build_output")
# 合并固件输出目录
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "fw")

# 固件参数配置 (单位: 字节, 1KB = 1024 Bytes)
# Bootloader 最大允许大小 (超过此大小将报错)
BOOT_MAX_SIZE = 0x20000  # 128KB

# App 最大允许大小 (超过此大小将报错)
APP_MAX_SIZE = 0xE0000  # 896KB

# App 在合并文件中的起始偏移地址
# Bootloader 之后、此偏移之前的数据将填充 0xFF
APP_OFFSET = 0x20000     # 128KB

# 输出文件名 (如果为 None，则自动根据源文件名生成)
OUTPUT_FILENAME = "merged_firmware.bin"

# ===========================================

def find_latest_bin(directory):
    """
    在指定目录下查找修改时间最新的 .bin 文件
    """
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return None
        
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.bin')]
    if not files:
        print(f"Error: No .bin files found in {directory}")
        return None
        
    # 按修改时间排序，获取最新的
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def merge_firmware():
    print("Starting firmware merge process...")
    
    # 1. 查找最新的 Bootloader bin
    boot_bin_path = find_latest_bin(BOOT_BUILD_DIR)
    if not boot_bin_path:
        sys.exit(1)
    print(f"Latest Bootloader: {os.path.basename(boot_bin_path)}")

    # 2. 查找最新的 App bin
    app_bin_path = find_latest_bin(APP_BUILD_DIR)
    if not app_bin_path:
        sys.exit(1)
    print(f"Latest Application: {os.path.basename(app_bin_path)}")

    # 3. 读取文件内容
    try:
        with open(boot_bin_path, 'rb') as f:
            boot_data = f.read()
        
        with open(app_bin_path, 'rb') as f:
            app_data = f.read()
    except Exception as e:
        print(f"Error reading input files: {e}")
        sys.exit(1)

    boot_len = len(boot_data)
    app_len = len(app_data)
    
    print(f"Bootloader size: {boot_len} bytes ({boot_len/1024:.2f} KB)")
    print(f"Application size: {app_len} bytes ({app_len/1024:.2f} KB)")

    # 4. 检查大小限制
    if boot_len > BOOT_MAX_SIZE:
        print(f"Error: Bootloader size ({boot_len}) exceeds limit ({BOOT_MAX_SIZE})!")
        sys.exit(1)

    if app_len > APP_MAX_SIZE:
        print(f"Error: Application size ({app_len}) exceeds limit ({APP_MAX_SIZE})!")
        sys.exit(1)

    if boot_len > APP_OFFSET:
        print(f"Error: Bootloader size ({boot_len}) overlaps with App Offset ({APP_OFFSET})!")
        sys.exit(1)

    # 5. 合并数据
    # 创建输出 buffer
    # 大小 = App 偏移 + App 大小
    total_size = APP_OFFSET + app_len
    merged_data = bytearray(total_size)
    
    # 初始化全为 0xFF
    for i in range(total_size):
        merged_data[i] = 0xFF

    # 写入 Bootloader 数据到开头
    merged_data[0:boot_len] = boot_data

    # 写入 App 数据到偏移位置
    merged_data[APP_OFFSET:APP_OFFSET+app_len] = app_data

    # 6. 写入输出文件
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    
    try:
        with open(output_path, 'wb') as f:
            f.write(merged_data)
        print(f"\nSuccess! Merged firmware saved to:\n{output_path}")
        print(f"Total size: {len(merged_data)} bytes ({len(merged_data)/1024:.2f} KB)")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    merge_firmware()
