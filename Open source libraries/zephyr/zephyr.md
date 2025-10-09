# zephyr学习记录

## [环境搭建](https://docs.zephyrproject.org/latest/develop/getting_started/index.html)

### 注意事项
**下载完毕后，需要执行以下命令**
```
<!-- 如果修改文件存储路径，需要重新执行以下脚本 -->
<!-- 导出环境变量，方便设计zephyr独立程序 -->
source zephyr-env.sh
<!-- 设置工具链路径，否则会报错 -->
source setup.sh 
```
## [应用开发](https://docs.zephyrproject.org/latest/develop/application/index.html)

### [自定义板](https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html#create-your-board-directory)

自定义板时，**自定义板文件夹**需要包含以下文件
```
<!-- 注意：需要将 my_custom_board 替换为实际的板名称，同时自定义板文件夹名称需要与 my_custom_board 一致 -->
my_custom_board_defconfig
my_custom_board.dts
my_custom_board.yaml
board.cmake
board.h
CMakeLists.txt
doc/
Kconfig.my_custom_board
Kconfig.defconfig
support/
```

### [bindings文件](https://docs.zephyrproject.org/latest/build/dts/bindings-syntax.html)
