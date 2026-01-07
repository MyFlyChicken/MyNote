import os
import subprocess
import sys
import time

# ================= 配置区域 =================

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 子脚本名称
SCRIPT_COMPILE = "keil_compile.py"
SCRIPT_MERGE = "fw_merge.py"
SCRIPT_FLASH = "jlink_flash.py"

# ===========================================

def run_step(script_name, description):
    """
    运行单个步骤脚本
    """
    script_path = os.path.join(SCRIPT_DIR, script_name)
    
    print("=" * 60)
    print(f"STEP: {description}")
    print(f"Script: {script_name}")
    print("=" * 60)
    
    if not os.path.exists(script_path):
        print(f"Error: Script not found: {script_path}")
        return False

    start_time = time.time()
    
    try:
        # 使用当前 Python 解释器运行子脚本
        # check=True 会在子进程返回非零退出码时抛出 CalledProcessError
        subprocess.run([sys.executable, script_path], check=True)
        
        elapsed = time.time() - start_time
        print(f"\n>>> {description} COMPLETED successfully in {elapsed:.2f}s.\n")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n!!! {description} FAILED with exit code {e.returncode}. !!!\n")
        return False
    except Exception as e:
        print(f"\n!!! {description} FAILED with exception: {e} !!!\n")
        return False

def main():
    print("Starting One-Click Build & Flash Process...")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    # 1. 编译工程
    if not run_step(SCRIPT_COMPILE, "Compile Projects"):
        print("Build process aborted due to compilation errors.")
        sys.exit(1)

    # 2. 合并固件
    if not run_step(SCRIPT_MERGE, "Merge Firmware"):
        print("Build process aborted due to merge errors.")
        sys.exit(1)

    # 3. 烧录固件
    if not run_step(SCRIPT_FLASH, "Flash Firmware"):
        print("Build process aborted due to flash errors.")
        sys.exit(1)

    print("=" * 60)
    print("ALL STEPS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
