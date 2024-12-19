# CMakeLists 工程编译步骤

```shell
# 构建编译输出目录
mkdir build
# 切换到输出目录
cd build
# 生成Makefile文件
cmake ../CMakeLists.txt
# 编译
make all
```

**注：CMakeLists.txt与.config无直接关系，如果需要使用.config控制CMakeLists.txt，则需要编写函数将.config内的变量读取出来**
