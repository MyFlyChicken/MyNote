# Linux记录

## Win安装Linux

### VMware 加Linux镜像

1. 下载VMware,需要安装的Linux镜像
2. 安装

### 基于Windows的WSL子系统安装

1. 参照[这里](https://docs.microsoft.com/zh-cn/windows/wsl/install-win10)安装WSL，安装后需要重启一下电脑
2. 点击[这里](https://github.com/yuk7/ArchWSL)下载ArchLinux，此处安装以ArchLinux为准

![image-20240220201139792](./assets/image-20240220201139792.png)

3. 安装证书*.cer，如果提示下图内容，则需要在安装证书时，将证书存储到受信任的区域里边

![image-20240219211338237](./assets/image-20240219211338237.png)

4. 切换到*.appx的路径，在shell内输入进行安装，如果提示突发安装，则可以百度相应的故障码进行搜索

   ![image-20240220201319838](./assets/image-20240220201319838.png)

5. 此时，系统已经可以识别到安装的Linux子系统，如果是其他系统，则图标可能是其它的

![image-20240220201547788](./assets/image-20240220201547788.png)

[视频参考连接](https://www.bilibili.com/video/BV1sW411v7VZ?p=1&vd_source=2e33a3cba9dea05126d330dcf100be27)

## 初装Linux需要进行的操作

1. 镜像源改为国内地址，也可以不更换

```
sudo vim  /etc/pacman.d/mirrorlist
```

2. 更新镜像

3. 将默认shell更换为fish

   ```
   sudo pacman -S fish
   chsh -s /bin/fish yf
   ```

4. 使用 VS Code + Clangd + CMake 搭建 C/C++开发环境参考链接

[Win10 下 WSL 的安装方法](https://docs.microsoft.com/zh-cn/windows/wsl/install-win10)

[ArchWSL 的下载与文档](https://github.com/yuk7/ArchWSL)

[VS Code 替换变量定义](https://code.visualstudio.com/docs/editor/variables-reference)

[Clangd](https://clangd.llvm.org/)

[VSCode-Clangd 插件](https://github.com/clangd/vscode-clangd)

[CMake-Tools 插件文档](https://github.com/microsoft/vscode-cmake-tools/tree/develop/docs)

[Clang-Format 代码整理选项](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)

[Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/)

[VS Code 的使用技巧与键位表等](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)

/usr/bin文件夹一般存放全家环境变量

tree 用来显示树形文件

![image-20240222203342138](./assets/image-20240222203342138.png)

which 用来搜索环境变量实际所在的位置

## GCC工具使用

[参考链接](https://www.cnblogs.com/kele-dad/p/9394568.html)

### add2line

```
addr2line -e test1.out -a 160b  -f -p -C -i
```

注意：map文件需要包含调试信息，在编译的时候需要设置gcc的编译标志''-g"，也需要设置map文件输出“-Wl,-Map,name.map”

## Linux指令教程

[参考网址](https://www.runoob.com/linux/linux-file-attr-permission.html)

## 动态库找不到怎么解决

![image-20240404092702819](./assets/image-20240404092702819.png)

下载相关库

```
sudo pacman -S llvm-libs
```

### 库找不到的原因

1. 下载的软件版本与之前已经安装的版本不匹配。所以找不到库，需要对原来的库进行更新
   - clang: error while loading shared libraries: libLLVM-17.so: cannot open shared object file: No such file or directory
   - sudo pacman -S llvm-libs

## Doxygen使用





## 文件权限

![img](./assets/file-llls22.jpg)

![363003_1227493859FdXT](./assets/363003_1227493859FdXT.png)

