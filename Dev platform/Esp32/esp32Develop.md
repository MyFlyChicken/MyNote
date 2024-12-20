# esp32Develop

记录对esp32学习

## esp32开发环境配置

- 安装esp-idf，点击[Windows 平台工具链的标准设置 - ESP32 - — ESP-IDF 编程指南 release-v5.1 文档 (espressif.com)](https://docs.espressif.com/projects/esp-idf/zh_CN/release-v5.1/esp32/get-started/windows-setup.html)

| 开发环境                     | 备注                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| 利用ESP-IDF Eclipse 插件开发 | 参考 [idf-eclipse-plugin/README_CN.md ](https://github.com/espressif/idf-eclipse-plugin/blob/master/README_CN.md) |
| Vscode Espressif IDF插件     | 参考 [VSCode Extension](https://github.com/espressif/vscode-esp-idf-extension/blob/master/docs/tutorial/install.md) |
| esp-idf 命令行开发           | 实际为在Vscode内编写代码，在命令行内编译下载                 |

## esp-idf工具参考

- [工具 - ESP32 - — ESP-IDF 编程指南 release-v5.1 文档 ](https://docs.espressif.com/projects/esp-idf/zh_CN/release-v5.1/esp32/api-guides/tools/index.html)



## [编译第一个工程 ](https://docs.espressif.com/projects/esp-idf/zh_CN/release-v5.1/esp32/get-started/windows-setup.html#get-started-windows-first-steps)

- 运行ESP-IDF 5.0 CMD或ESP-IDF 5.0 PowerShell(如果直接在Windows  PowerShell或CMD内运行idf.py指令，会提示命令未知，**待解决**)
- 切换至工程目录
- 设置目标版(idf.py set-target esp32c3)
- 编译(idf.py build)
- 烧录(idf.py flash)

## build目录

![build目录](./编译文件.png)

## 程序下载

- cmd或power shell 下载

编译后使用命令

```cmd
idf.py -p COM5 flash
```

下载程序，下载后会出现一系列日志

![download-log](./download-log.png)

- flash_download_Tool下载

根据编译输出的日志

```cmd
D:\InstallSoft\Espressif\python_env\idf5.0_py3.11_env\Scripts\python.exe ..\..\..\InstallSoft\Espressif\frameworks\esp-idf-v5.0.2\components\esptool_py\esptool\esptool.py -p (PORT) -b 460800 --before default_reset --after hard_reset --chip esp32c3  write_flash --flash_mode dio --flash_size 2MB --flash_freq 80m 0x0 build\bootloader\bootloader.bin 0x8000 build\partition_table\partition-table.bin 0x10000 build\hello_world.bin
```

得到文件对应的地址

| 文件                | 地址    |
| ------------------- | ------- |
| bootloader.bin      | 0x0     |
| partition-table.bin | 0x8000  |
| hello_world.bin     | 0x10000 |

根据[Flash_Download_Tool__cn](./flash_download_tool_3.9.5/doc/Flash_Download_Tool__cn.pdf)烧录文件

## menuconfig配置



## esp32移植btstack

1. 前往[btstack](git@github.com:bluekitchen/btstack.git)下载源码
2. 打开esp-idf CMD或esp-idf PowerShell，将运行目录切换至btstack内的port\esp32
3. 参考btstack内的port\esp32内的README.md文件进行移植

## Linux开发esp32记录

本地的子模块与当前分支或tag一定要与esp32git发布的一致，否则会出现奇怪的错误。

错误：**子模块与tag不匹配**

![image-20240630135913146](./assets/image-20240630135913146.png)

出现这个现象时，可以使用git命令，将子模块切换到与tag匹配的HEAD

```shell
git submodule update --init --recursive
```

正确：没有出现不匹配的子模块

![image-20240630135736882](./assets/image-20240630135736882.png)

一定要注意编译警告！！！





