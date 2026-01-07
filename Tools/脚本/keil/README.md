## 脚本说明
| 脚本名称 | 功能 | 使用说明 |
| --- | --- | --- |
| build_and_flash.py | 一次性实现编译，合并，烧录脚本 | 必须包含所有依赖脚本 |
| fw_merge.py | 固件合并脚本 | 配置后可单独使用 |
| jlink_flash.py | 固件烧录脚本 | 配置后可单独使用 |
| keil_compile.py | keil编译脚本 | 配置后可单独使用 |
| clang_format.py | 代码格式化脚本 | 依赖.clang-format与clang-format.exe |
| build_version.py | 版本号生成脚本 | 需要与keil工程放在同一目录，放在keil魔术棒user栏目下。编译前python build_version.py --pre，编译后python build_version.py --post |
| Keil2Json.py | keil工程转换脚本, 将工程转换为compile_commands.json | 需要与keil工程放在同一目录，keil魔术棒编译前 |

