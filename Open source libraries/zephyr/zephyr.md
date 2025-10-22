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

#### 传递自定义板路径
```
west build -b <board name> -- -DBOARD_ROOT=<path to boards>

cmake -Bbuild -GNinja -DBOARD=<board name> -DBOARD_ROOT=<path to boards> .
ninja -Cbuild
```

#### 指定文件夹
```
#指定build文件夹
west build -b <board name> -- -DBOARD_ROOT=<path to boards> -d <build directory>
#指定烧录文件夹
west flash -d <build directory>
```

### [bindings文件](https://docs.zephyrproject.org/latest/build/dts/bindings-syntax.html)

### [DTS文件](https://docs.zephyrproject.org/latest/build/dts/index.html)

- [C/C++使用dts生成的文件](https://docs.zephyrproject.org/latest/build/dts/api-usage.html)

- [DTS参考链接](https://www.cnblogs.com/jayant97/articles/17209392.html#1-%E5%89%8D%E8%A8%80)
- 注意事项:
  name@x: 这里的x表示设备的地址，必须是十六进制数(x没有0x前缀，如果节点没有reg属性，则可以省略@x部分)
  reg属性首地址必须与name@x中的x值一致，且地址必须加0x前缀
- compatible属性必须与bindings文件夹下的yaml文件中的compatible值一致
- *.overlay文件用于覆盖dts配置，有app.overlay和board.overlay两种，默认情况下app.overlay优先级高于board.overlay。其中，app.overlay用于应用层的覆盖（例如，节点修改），board.overlay用于板级的覆盖（例如，引脚修改）。
- *.conf文件用于覆盖Kconfig，有prj.conf和${boardname}.conf两种，默认情况下app.conf优先级高于${boardname}.conf。其中，prj.conf用于应用层的覆盖（例如，部分功能开启/关闭），${boardname}.conf用于板级的覆盖（例如，外设修改）。
- 注意编写overlay文件时，不允许重复定义节点，否则会报错
