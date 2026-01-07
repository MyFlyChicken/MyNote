import os
import subprocess
import datetime
import shutil
import sys

# Configuration
HEADER_FILE_PATH = os.path.join('applications', 'git_info.h')
BIN_FILE_NAME = 'rtthread.bin'
OUTPUT_DIR = 'build_output'  # Directory to store versioned binaries

def get_git_info():
    try:
        # Get commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        # Get branch name
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')
        # Get dirty status
        dirty = subprocess.call(['git', 'diff', '--quiet']) != 0
        dirty_str = "_dirty" if dirty else ""
        
        return commit_hash + dirty_str, branch_name
    except Exception as e:
        print(f"Warning: Could not get git info: {e}")
        return "unknown", "unknown"

def generate_header():
    commit_hash, branch_name = get_git_info()
    
    content = f"""#ifndef __GIT_INFO_H__
#define __GIT_INFO_H__

#define GIT_COMMIT_HASH "{commit_hash}"
#define GIT_BRANCH "{branch_name}"

#endif /* __GIT_INFO_H__ */
"""
    
    # Only write if content changed to avoid unnecessary rebuilds
    if os.path.exists(HEADER_FILE_PATH):
        with open(HEADER_FILE_PATH, 'r') as f:
            if f.read() == content:
                print("Git info header is up to date.")
                return

    with open(HEADER_FILE_PATH, 'w') as f:
        f.write(content)
    print(f"Generated {HEADER_FILE_PATH}")

def process_binary():
    if not os.path.exists(BIN_FILE_NAME):
        print(f"Error: {BIN_FILE_NAME} not found!")
        return

    commit_hash, branch_name = get_git_info()
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    # Create output directory if not exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    new_filename = f"dtu_app_{branch_name}_{commit_hash}_{now_str}.bin"
    dest_path = os.path.join(OUTPUT_DIR, new_filename)
    
    shutil.copy(BIN_FILE_NAME, dest_path)
    print(f"Binary copied to: {dest_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--pre':
            generate_header()
        elif sys.argv[1] == '--post':
            process_binary()
        else:
            print("Usage: python build_version.py [--pre | --post]")
    else:
        # Default behavior if no args (can be used for testing)
        print("No arguments provided. Running both steps for testing.")
        generate_header()
        process_binary()
