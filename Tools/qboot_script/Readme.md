# 内容说明
| 文件            | 作用                                                         |
| --------------- | ------------------------------------------------------------ |
| ./output_bins/* | bootloader.bin存放路径及脚本生成的文件                       |
| AdiDsp.py       | sigmastudio生成的*.dat文件转bin文件的脚本                    |
| BinMerge.py     | boot、app、dsp的bin文件合成的脚本                            |
| QBoot.py        | 生成[QBoot](https://gitee.com/qiyongzhong0/rt-thread-qboot)需要的文件头 |
| Main.py         | py脚本的main入口                                             |
| MakeAll.bat     | bat脚本，调用Main.py                                         |

# 使用说明
1. 运行MakeAll.bat

需要修改MakeAll.bat内 `python.exe` 路径。

```bat
@echo off

"C:\Users\xuwei\AppData\Local\Programs\Python\Python311\python.exe" .\Main.py

echo "(^_^) Press any key to close this window..."

pause > nul

```

### 2.生成固件说明

```bash
app.bin					# Debug/*.bin编译生成的app文件
app.rbl					# qboot支持的app升级包
bootloader.bin			# 启动文件，需要从bootloader工程生成的文件获得
factory_download.bin	# 工厂生产时的烧录文件
```