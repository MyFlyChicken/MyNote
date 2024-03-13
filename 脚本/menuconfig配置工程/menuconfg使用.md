# menuconfig使用

为了方便程序配置及模块化，menuconfig是必须的

## windows使用menuconfig

### 环境搭建

1. 安装python
2. 安装Kconfiglib

```
 pip install windows-curses
 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple kconfiglib
```

3. 编写Kconfig
4. 编写C语言头文件生成脚本kconfig.py

```
import re
import pip


def log_print(level, text):
    # Log level colors
    LEVEL_COLORS = {
        'error': '\033[31m',
        'success': '\033[32m',
        'warning': '\033[33m',
        'info': '\033[34m',
    }
    RESET_COLOR = '\033[0m'
    # Log level name
    LEVEL_NAME = {
        'error': 'ERROR',
        'success': 'SUCCESS',
        'warning': 'WARNING',
        'info': 'INFO',
    }
    print(LEVEL_COLORS[level] + LEVEL_NAME[level] + ': ' + text + RESET_COLOR)


def install_package(package):
    log_print('info', "%s package installing..." % package)
    pip.main(['install', package])


try:
    from kconfiglib import Kconfig
except ImportError:
    install_package('kconfiglib')
    from kconfiglib import Kconfig

try:
    import curses
except ImportError:
    install_package('windows-curses')
    import curses


def generate_config(kconfig_file, config_in, config_out, header_out):
    kconf = Kconfig(kconfig_file, warn=False, warn_to_stderr=False)

    # Load config
    kconf.load_config(config_in)
    kconf.write_config(config_out)
    kconf.write_autoconf(header_out)

    with open(header_out, 'r+') as header_file:
        content = header_file.read()
        header_file.truncate(0)
        header_file.seek(0)

        # Remove CONFIG_ and MR_USING_XXX following number
        content = content.replace("#define CONFIG_", "#define ")
        content = re.sub(r'#define MR_USING_(\w+) (\d+)', r'#define MR_USING_\1', content)

        # Add the micro
        header_file.write("#ifndef _MR_CONFIG_H_\n")
        header_file.write("#define _MR_CONFIG_H_\n\n")

        header_file.write("#ifdef __cplusplus\n")
        header_file.write("extern \"C\" {\n")
        header_file.write("#endif /* __cplusplus */\n\n")

        # Write back the original data
        header_file.write(content)

        # Add the micro
        header_file.write("\n#ifdef __cplusplus\n")
        header_file.write("}\n")
        header_file.write("#endif /* __cplusplus */\n\n")
        header_file.write("#endif /* _MR_CONFIG_H_ */\n")

        header_file.close()
        log_print('success', "menuconfig %s make success" % header_out)


def main():
    kconfig_file = ''#Kconfig的路径
    config_in = '.config'
    config_out = '.config'
    header_out = 'config.h'#输出头文件路径
    generate_config(kconfig_file, config_in, config_out, header_out)


if __name__ == "__main__":
    main()
```

### 使用步骤

1. 在Kconfig同目录下使用menuconfig

![image-20240313103803102](./assets/image-20240313103803102.png)

2. 保存变更，生成config头文件

```
python kconfig.py
```

```
#ifndef _MR_CONFIG_H_
#define _MR_CONFIG_H_

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#define MR_USING_ASSERT
#define MR_CFG_HEAP_SIZE 4096
#define MR_USING_LOG_ERROR
#define MR_USING_LOG_WARN
#define MR_USING_LOG_INFO
#define MR_USING_LOG_DEBUG
#define MR_USING_LOG_SUCCESS
#define MR_CFG_PRINTF_BUFSZ 128
#define MR_CFG_PRINTF_DEV_NAME "serial1"
#define MR_USING_PRINTF_NONBLOCKING

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* _MR_CONFIG_H_ */

```

3. 工程引用config.h头文件实现menuconfig配置

### 参考文档

[kconfiglib](https://pypi.org/project/kconfiglib/#installation-with-pip)

[mr-library](https://github.com/Mac-Rsh/mr-library)

[menuconfig在windows上安装](https://blog.csdn.net/qq_33229007/article/details/129340204)

[Kconfig语法](https://www.rt-thread.org/document/site/#/development-tools/build-config-system/Kconfig)

[Kconfig语法](https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html)