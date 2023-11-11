## CherryUSB+SFUD+W25Q64模拟U盘无法格式化

在usbd_msc_sector_write接口函数内，写数据不对。W25Q64需要先擦除，再写入数据

```c
int usbd_msc_sector_write(uint32_t sector, uint8_t *buffer, uint32_t length)
{
    /* TODO 擦除前读出数据，将buffer写入付出缓冲，再写入缓冲，保证Flash内数据不被改变 */
    if (sector < BLOCK_COUNT)
    {
        nor_flash1.ops.erase(sector * BLOCK_SIZE, length);//先擦除
        nor_flash1.ops.write(sector * BLOCK_SIZE, buffer, length);//在写入
    }
ok:
    return 0;
error:
    return -1;    
}
```

## RTthread 如何挂载多个设备

1. 将一个存储设备挂载到一个根目录（“/”）

2. 在根目录创建一个文件夹NewFolder 
3. 将另一个（或更多）设备挂载到新创建的文件夹("/NewFolder")上
4. 挂载更多设备依此类推

## 判断摄像头数据是否正确

1. 查看手册，配置摄像头输出色条（ov2640 COM7 寄存器的bit2可以使能输出色条）
2. 根据实际输出的色块判断驱动是否有问题
## Keil全局变量分配的内存被OS内的molloc函数申请的内存覆盖，其它编译器类似
1. 首先检查keil的sct文件，检查是否分配了AXISRAM
2. 检查OS是否对AXISRAM区域的内存做了管理
3. 如果出现标题所述的现象，很有可能是全局变量分配内存与malloc函数申请内存重叠，导致全局变量被覆盖

## GPIO不够时可以采用的硬件设计方案

- keyADC检测
- IO组合，三个GPIO可以检测8(2的三次方)种按键
- 使用串转并或并转串的IC通过MCU外设进行扩展，如HC595

## 系统卡死、没有日志输出，但是系统并没有复位。排查办法

- 将shell调整至最大优先级
- 关闭看门狗
- 查看任务状态

- 连接仿真器，看程序一直在哪里运行，判断卡死位置

## HardWare 卡死



## MAP文件分析

map文件主要存储了编译文件内的数据存储结构，可以参看[Amap | Sergey Sikorskiy](https://www.sikorskiy.net/info/prj/amap/)进行文件分析

## 去除警告

功能写完一定要去除警告，可以避免出现未知的错误！
使用attribute可以修饰函数，将定义的函数却没有引用的函数警告进行修饰，可以避免编译器警告

如果提示missing braces around initializer，确实是缺少了括号，初始化时对结构体内部成员使用了一个错误的值

~~~c
struct apm32_adc
{
    const char *name;
    ADC_T *adc;
    ADC_Config_T adc_config;
    rt_base_t channel_pin[DRV_ADC_CHANNEL_MAX_NUM];
    struct rt_adc_device adc_dev;//为一个结构体
};

static struct apm32_adc adc_config[] =
{
    {
        "adc2",
        ADC2,
        {
            ADC_MODE_INDEPENDENT,
            DISABLE,
            DISABLE,
            ADC_EXT_TRIG_CONV_None,
            ADC_DATA_ALIGN_RIGHT,
            1
        },
        {
            GET_PIN(A, 0), GET_PIN(A, 1), GET_PIN(A, 2), GET_PIN(A, 3), GET_PIN(A, 4),
            GET_PIN(A, 5), GET_PIN(A, 6), GET_PIN(A, 7), GET_PIN(B, 0), GET_PIN(B, 1),
            GET_PIN(C, 0), GET_PIN(C, 1), GET_PIN(C, 2), GET_PIN(C, 3)
        },
        {}//正确实例，将结构体初始化为空，这样就避免了missing braces around initializer警告
    },
    {
        "adc1",
        ADC1,
        {
            ADC_MODE_INDEPENDENT,
            DISABLE,
            DISABLE,
            ADC_EXT_TRIG_CONV_None,
            ADC_DATA_ALIGN_RIGHT,
            1
        },
        {
            GET_PIN(A, 0), GET_PIN(A, 1), GET_PIN(A, 2), GET_PIN(A, 3), GET_PIN(A, 4),
            GET_PIN(A, 5), GET_PIN(A, 6), GET_PIN(A, 7), GET_PIN(B, 0), GET_PIN(B, 1),
            GET_PIN(C, 0), GET_PIN(C, 1), GET_PIN(C, 2), GET_PIN(C, 3)
        },
        RT_NULL//错误实例，将结构体赋值为RT_NULL
    },    
}
~~~



