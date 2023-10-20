# USB相关知识点

USB是串行总线，所以数据是一位一位在数据线上传送的，USB使用的是LSB在前的方式，即先出来的是最低位的数据，接下来是次低位，最后是最高位（MSB）。

## USB描述符

标准的描述符有5种，USB为这些描述符定义了编号：

![描述符类型](./figures/描述符类型.png)

- [设备描述符](https://www.usbzh.com/article/detail-104.html)
- 配置描述符
- [字符串描述符](https://www.usbzh.com/article/detail-53.html)
- [接口描述符](https://www.usbzh.com/article/detail-64.html)
- [端点描述符](https://www.usbzh.com/article/detail-56.html)
- [HID描述符](https://www.usbzh.com/article/detail-62.html)
- [报表描述符](https://www.usbzh.com/article/detail-48.html)

- 限定描述符 DEVICE_QUALIFIER
- [其它速率配置描述符](https://www.usbzh.com/article/detail-88.html) OTHER_SPEED_CONFIGURATION
- 接口功率描述符 INTERFACE_POWER

### USB设备描述符关系

![描述符关系](./figures/描述符关系.png)

- 一个USB设备只有一个设备描述符。
- 一个USB设备可以有多个配置描述符（在设备描述符的bNumConfigurations下指定），但设备只能工作在一个配置描述符下。
- 一个配置描述符下可以有多个(在配置描述符的bNumInterfaces下指定)接口描述符。
- 一个接口描述符下可以有多个（在接口描述符的bNumEndPoints下指定）端点描述符。

## UBS-HID

HID的核心主要是报表描述符，以下着重介绍HID的报表描述符，以及如何利用报表描述符符合设备。

![HID描述符关系](./figures/HID描述符关系.png)

### HID描述符

| 偏移量 | 字段                   | 字节数 | 数值类型 | 说明                                   |
| ------ | ---------------------- | ------ | -------- | -------------------------------------- |
| 0      | bLength                | 1      | Numeric  | 描述符字节数                           |
| 1      | bDescriptorType        | 1      | Constant | 0x21 = HID 描述符                      |
| 2      | bcdHID                 | 2      | Numeric  | HID 规范版本号（BCD）                  |
| 4      | bCountryCode           | 1      | Numeric  | 硬件设备所在国家的国家代码             |
| 5      | bNumDescriptors        | 1      | Numeric  | 类别描述符数目（至少有一个报表描述符） |
| 6      | bDescriptorType        | 1      | Constant | 类别描述符的类型                       |
| 7      | wDescriptorLength      | 2      | Numeric  | 报表描述符的总长度                     |
| 9      | [bDescriptorType]...   | 1      | Constant | 附加的描述符的类型，可选的             |
| 10     | [wDescriptorLength]... | 2      | Numeric  | 附加的描述符的总长度，可选的           |

### HID报表描述符

报表描述符是报表描述项目（Item）的集合，每一个描述项目都有相对统一的数据结构，项目很多，通过编码实现。

- HID短项目字段结构

![HID短项目](./figures/HID短项目.png)

bSize，0为0字节，1为1字节，2为2字节，3为4字节。

bType，表示该条目的类型。**0为主条目，1为全局条目，2为局部条目**。

bTag，表示该条目的功能，具体参见下表

![HID短项目](./figures/bTag对照表.png)

- HID长项目字段结构

![HID长项目](./figures/HID长项目.png)

长项目一般不用，不做介绍（其实没学习）

#### 主条目

主条目用来**定义或者分组报告的数据域**，例如，可以使用输入主条目将输入报告划分为不同的数据域，以及指定该域的属性。

- Input、Output 和 Feature 项目的前缀字之后是 32 位描述数据，目前最多定义了 9 个位，余的位则是保留。位 0~8 的定义中只有位 7 不能应用于 Input 项目，除此之外其他的位定义都适应于 Input、utput 和 Feature 项目。

-  Collection 与 End Collection 项目来将相关的 Main 类型项目组成群组。这两个项目分别用于打开和关闭集合。项目之间的 Main 类型项目都是 Collection 的一部分。

#### 全局条目

主要用来选择用途页，定义数据域的长度、数量、报告ID等。**全局条目出现后对接下来的所有主条目都有效，除非遇到另一个全局条目来改变它。**

- 常用的全局条目有：Usage Page（用途页），Logical Minimum（逻辑最小值），Logical Maximum（逻辑最大值），Physical Minimum（物理最小值），Physical Maximum（物理最大值），Report Size（数据域大小，单位为位！），Report Count（数据域数量），Report ID（报告ID）。

其中Reprot Size 用来描述某个数据域有多少个位；Report Count用来描述这样的数据域有多少个；Logical Minimum和Logical Maximum用来描述数据域的取值范围。**Report Count不包含Report ID的大小**

#### 局部条目

用来定义控制的特性，例如，该数据域的用途、用途最小值、用途最大值。

- 常用的局部条目有：Usage(用途)、Usage Minimum(用途最小值)、Usage Maximum(用途最大值)。

简单来说，局部条目只是说明用途而已，标签Usage应该称为Usage ID，它搭配全局条目的Usage Page标签才形成所定义的用途。

### 键盘描述符，鼠标描述符

对于报表描述符，Usage在报表描述符内顺序排列，用于规定报告数据时数据的作用。**例如一个报表描述符内有Usage A，Usage B。同时Usage A，Usage B均为Report Size (8)，Report Count (1)，那么在上报数据时会先出现Usage A的数据项，再出现Usage B的数据项，假如这个描述符内有Report ID，那么上报数据时会先出现Report ID，再出现Usage A，Usage B的数据项。**

~~~c
//键盘描述符
0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
0x09, 0x06,        // Usage (Keyboard)
0xA1, 0x01,        // Collection (Application)
0x05, 0x07,        //   Usage Page (Kbrd/Keypad)
0x19, 0xE0,        //   Usage Minimum (0xE0)
0x29, 0xE7,        //   Usage Maximum (0xE7)
0x15, 0x00,        //   Logical Minimum (0)
0x25, 0x01,        //   Logical Maximum (1)
0x75, 0x01,        //   Report Size (1)
0x95, 0x08,        //   Report Count (8)
0x81, 0x02,        //   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x95, 0x01,        //   Report Count (1)
0x75, 0x08,        //   Report Size (8)
0x81, 0x03,        //   Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x95, 0x05,        //   Report Count (5)
0x75, 0x01,        //   Report Size (1)
0x05, 0x08,        //   Usage Page (LEDs)
0x19, 0x01,        //   Usage Minimum (Num Lock)
0x29, 0x05,        //   Usage Maximum (Kana)
0x91, 0x02,        //   Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
0x95, 0x01,        //   Report Count (1)
0x75, 0x03,        //   Report Size (3)
0x91, 0x03,        //   Output (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
0x95, 0x06,        //   Report Count (6)
0x75, 0x08,        //   Report Size (8)
0x15, 0x00,        //   Logical Minimum (0)
0x25, 0xFF,        //   Logical Maximum (-1)
0x05, 0x07,        //   Usage Page (Kbrd/Keypad)
0x19, 0x00,        //   Usage Minimum (0x00)
0x29, 0x65,        //   Usage Maximum (0x65)
0x81, 0x00,        //   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              // End Collection
// 63 bytes
~~~

~~~c
//鼠标描述符
0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
0x09, 0x02,        // Usage (Mouse)
0xA1, 0x01,        // Collection (Application)
0x09, 0x01,        //   Usage (Pointer)
0xA1, 0x00,        //   Collection (Physical)
0x05, 0x09,        //     Usage Page (Button)
0x19, 0x01,        //     Usage Minimum (0x01)
0x29, 0x03,        //     Usage Maximum (0x03)
0x15, 0x00,        //     Logical Minimum (0)
0x25, 0x01,        //     Logical Maximum (1)
0x95, 0x03,        //     Report Count (3)
0x75, 0x01,        //     Report Size (1)
0x81, 0x02,        //     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x95, 0x01,        //     Report Count (1)
0x75, 0x05,        //     Report Size (5)
0x81, 0x01,        //     Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x05, 0x01,        //     Usage Page (Generic Desktop Ctrls)
0x09, 0x30,        //     Usage (X)
0x09, 0x31,        //     Usage (Y)
0x09, 0x38,        //     Usage (Wheel)
0x15, 0x81,        //     Logical Minimum (-127)
0x25, 0x7F,        //     Logical Maximum (127)
0x75, 0x08,        //     Report Size (8)
0x95, 0x03,        //     Report Count (3)
0x81, 0x06,        //     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              //   End Collection
0x09, 0x3C,        //   Usage (Motion Wakeup)
0x05, 0xFF,        //   Usage Page (Reserved 0xFF)
0x09, 0x01,        //   Usage (0x01)
0x15, 0x00,        //   Logical Minimum (0)
0x25, 0x01,        //   Logical Maximum (1)
0x75, 0x01,        //   Report Size (1)
0x95, 0x02,        //   Report Count (2)
0xB1, 0x22,        //   Feature (Data,Var,Abs,No Wrap,Linear,No Preferred State,No Null Position,Non-volatile)
0x75, 0x06,        //   Report Size (6)
0x95, 0x01,        //   Report Count (1)
0xB1, 0x01,        //   Feature (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
0xC0,              // End Collection
// 74 bytes
~~~

~~~c
//自定义数据收发
0x06, 0x00, 0xFF,  // Usage Page (Vendor Defined 0xFF00)
0x09, 0x01,        // Usage (0x01)
0xA1, 0x01,        // Collection (Application)
0x85, 0x02,        //   Report ID (2)
0x09, 0x01,        //   Usage (0x01)
0x15, 0x00,        //   Logical Minimum (0)
0x26, 0xFF, 0x00,  //   Logical Maximum (255)
0x95, 0x3F,        //   Report Count (63)
0x75, 0x08,        //   Report Size (8)
0x81, 0x02,        //   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x85, 0x03,        //   Report ID (3)
0x09, 0x01,        //   Usage (0x01)
0x15, 0x00,        //   Logical Minimum (0)
0x26, 0xFF, 0x00,  //   Logical Maximum (255)
0x95, 0x3F,        //   Report Count (63)
0x75, 0x08,        //   Report Size (8)
0x91, 0x03,        //   Output (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
0xC0,              // End Collection
// 38 bytes

~~~

#### HID报表描述符复合设备

复合设备由report id进行区分。**一个报告描述符可以描述多个报告，不同的报告通过报告ID来识别。报告ID放到报告的最前面。当报告描述符中没有规定报告ID时，报告中就没有ID字段，开始就是数据。**

~~~c
//复合设备
~~~



## 参考资料

- [USB_HID协议中文版](.\资料\USB_HID协议中文版.pdf)

- [USB-HID设备6-HID报告描述符详解 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/41960639)

- [USB标准请求及描述符在线分析工具 - USB中文网 (usbzh.com)](https://www.usbzh.com/tool/usb.html))
