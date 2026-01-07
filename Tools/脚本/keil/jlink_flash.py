import os
import subprocess
import sys

# ================= 配置区域 =================

# JLink.exe 路径
# 请根据实际安装位置修改此路径
# 常见路径:
# C:\Program Files\SEGGER\JLink\JLink.exe
# C:\Program Files (x86)\SEGGER\JLink\JLink.exe
JLINK_EXE_PATH = r"C:\Program Files\SEGGER\JLink\JLink.exe"

# 目标芯片型号
# 如果连接失败，请尝试 "Cortex-M4"
DEVICE_NAME = "GD32F470VE"

# 接口类型: SWD 或 JTAG
INTERFACE = "SWD"

# 速度 (kHz)
SPEED = 4000

# 烧录起始地址 (Flash Base Address)
FLASH_ADDR = "0x08000000"

# 固件文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FW_PATH = os.path.join(SCRIPT_DIR, "..", "fw", "merged_firmware.bin")

# ===========================================

def flash_firmware():
    # 检查 JLink 路径
    if not os.path.exists(JLINK_EXE_PATH):
        print(f"Error: JLink.exe not found at: {JLINK_EXE_PATH}")
        print("Please update 'JLINK_EXE_PATH' in the script to point to your JLink installation.")
        return

    # 检查固件文件
    if not os.path.exists(FW_PATH):
        print(f"Error: Firmware file not found at: {FW_PATH}")
        print("Please run 'fw_merge.py' first to generate the firmware.")
        return

    print(f"Preparing to flash firmware...")
    print(f"  Firmware: {FW_PATH}")
    print(f"  Device:   {DEVICE_NAME}")
    print(f"  Interface:{INTERFACE}")
    print(f"  Speed:    {SPEED} kHz")
    print(f"  Address:  {FLASH_ADDR}")

    # 处理路径中的反斜杠，JLink 脚本中建议使用正斜杠或双反斜杠
    fw_path_safe = FW_PATH.replace("\\", "/")

    # 创建 JLink 命令脚本内容
    # r: Reset
    # h: Halt
    # loadbin: Load binary file
    # g: Go (Start CPU)
    # q: Quit
    jlink_script_content = f"""
r
h
loadbin "{fw_path_safe}", {FLASH_ADDR}
r
g
q
"""
    
    script_file = os.path.join(SCRIPT_DIR, "flash_cmd.jlink")
    
    try:
        with open(script_file, "w") as f:
            f.write(jlink_script_content)
    except Exception as e:
        print(f"Error creating JLink script file: {e}")
        return

    # 构造 JLink 命令
    cmd = [
        JLINK_EXE_PATH,
        "-device", DEVICE_NAME,
        "-if", INTERFACE,
        "-speed", str(SPEED),
        "-autoconnect", "1",
        "-CommanderScript", script_file
    ]

    print("\nExecuting JLink command...")
    print("-" * 50)
    
    try:
        # 执行命令
        result = subprocess.run(cmd, check=False)
        
        print("-" * 50)
        if result.returncode == 0:
            print("Flash operation completed successfully.")
        else:
            print(f"Flash operation failed with exit code: {result.returncode}")
            sys.exit(result.returncode)
            
    except FileNotFoundError:
        print(f"Error: Could not execute {JLINK_EXE_PATH}. Please check the path.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        # 清理临时脚本文件
        if os.path.exists(script_file):
            try:
                os.remove(script_file)
            except:
                pass

if __name__ == "__main__":
    flash_firmware()
