# 音频开发笔记

## I2S、PCM、TDM、PDM简述

I2S（Inter-IC Sound）、PCM（Pulse Code Modulation）和TDM（Time Division Multiplexing）是数字音频传输协议，常用于将音频数据从一个设备传输到另一个设备。它们之间的区别如下：

1. I2S：I2S是一种串行音频接口协议，由Philips（现在的NXP Semiconductors）开发。它使用三个线路进行数据传输：时钟线（SCK）、帧同步线（LRCLK）和数据线（SD）。时钟线提供时钟信号，帧同步线指示左右声道，数据线传输音频样本。I2S适用于连接音频 DAC（数字模拟转换器）和音频处理器等设备。

2. PCM：PCM是一种数字音频编码方式，也是一种数字音频传输格式。PCM将模拟音频信号按照一定的采样率和位深度进行采样和量化，然后将其转换为数字音频数据。PCM音频数据可以通过多种传输方式进行传输，包括I2S、SPDIF（Sony/Philips Digital Interface）、HDMI（High-Definition Multimedia Interface）等。

3. TDM：TDM是一种多路复用技术，用于在共享传输介质上传输多个信号。在音频应用中，TDM可以用于同时传输多个音频通道的数据。TDM使用时分复用的原理，将每个音频通道的数据划分为不同的时隙，并按照时序依次发送。接收端根据时隙信息将数据还原为原始音频通道。TDM在音频设备之间传输多个通道的音频数据时很常见(**通俗讲就是在不同时间片内传输不同通道的数据**)

在应用PCM音频接口传输单声道数据（如麦克风）时，其接口名称为**PCM**；双声道经常使用**I2S**；而**TDM**则表示传输两个及以上声道的数据，同时区别于I2S特定的格式。

### I2S接口

|    接口    | 作用   |  备注 |
| :-------: | :--: | :--: |
| MCLK | 主设备发送时钟 | 在I2S总线中，任何设备都可以<br />通过提供时钟成为I2S的主控设备<br />主时钟（也名过采样率），一般是采样频率的128、或256、或384或512倍<br />即**MCLK = 128或者256或者512 * 采样频率** |
| BCLK/SCK | 同步信号，用于同步每一位的数据，<br />具体是哪一个BCLK/SCK边沿采样是可配置的 | 对应数字音频的每一位数据，该时钟都有一个脉冲<br />**即BCLK = 声道数 * 采样频率 * 采样位数** |
| LRCLK(WS) | 采样频率，也叫声道选则信号。 | **WS的频率与声音采样率一致** |
| SDIN | 数据输入信号 | **二进制补码**表示的音频数据 |
| SDOUT | 数据输出信号 | **二进制补码**表示的音频数据 |

**注** I2S的MCLK非必须，其一般用于同步主从设备的时钟

### I2S模式

无论什么模式，都是**先发送MSB**，先传送MSB是因为发送设备和接收设备的字长可能不同，当系统字长比数据发送端字长长的时候，数据传输就会出现截断的现象/Truncated，即**如果数据接收端接收的数据位比它规定的字长长的话，那么规定字长最低位（LSB: Least Significant Bit）以后的所有位将会被忽略**。**如果接收的字长比它规定的字长短，那么空余出来的位将会以0填补**。通过这种方式可以使音频信号的最高有效位得到传输，从而保证最好的听觉效果。

#### 标准模式

![标准模式时序图](.\picture\标准模式时序图.png)

#### 左对齐模式

![左对齐模式时序图](.\picture\左对齐时序图.png)

由于在WS变化后的第一个SCK上升沿就开始采样，它不需要关心左右声道数据的字长，只要WS的时钟周期足够长，左对齐的方式支持16-32bit字长格式。

#### 右对齐模式

![左对齐模式时序图](.\picture\右对齐时序图.png)



## PCM、TDM

PCM (Pulse Code Modulation) 是通过等时间隔（即采样率时钟周期）采样将模拟信号数字化的方法

![PCM采样量化](.\picture\pcm_samp.png)

注：图中的意思是一个正弦波被分为若干等份，每一份的幅值对应一个值。假设这个正弦波的周期为**1s**，那么**采样的次数对应PCM传输数据的采样率，每一份的值对应采样精度**。

TDM是PCM经过扩展得来的。一般情况下单声道使用PCM，双声道使用I2S，两个声道以上使用TDM。

### PCM、TDM接口

| 接口     | 作用             | 备注 |
| -------- | ---------------- | ---- |
| PCM_CLK  | 类似于I2S的BCLK  |      |
| PCM_SYNC | 类似于I2S的WS    |      |
| PCM_IN   | 类似于I2S的SDIN  |      |
| PCM_OUT  | 类似于I2S的SDOUT |      |

### PCM、TDM模式

根据SD相对帧同步时钟SYNC的位置，TDM分两种基本模式

#### TDM-ModeA

数据在FSYNC有效后，BCLK的第***2***个上升沿有效

![TDM-ModeA](.\picture\TDM-ModeA.png)

#### TDM-ModeB

数据在FSYNC有效后，BCLK的第**1**个上升沿有效

![TDM-ModeA](.\picture\TDM-ModeB.png)

在实际应用中，总是以**SYNC的上升沿**表示第一次传输的开始。**帧同步时钟的频率等于音频采样频率**。根据不同SYNC时钟的脉冲宽度差别，帧同步时钟分为两种模式

**SLOT概念**：SLOT在TDM中表示的是传输单个声道所占用的位数。注意，Slot的位数并不一定等于音频的量化深度。比如Slot可能为***32 bit\***，其中包括***24 bit\***有效数据位（Audio Word） + ***8 bit\***零填充（Zero Padding）。不同厂商对Slot的叫法可能有所区别，比如Circus Logic称之为Channel Block

#### 长帧同步

SYNC脉冲宽度等于一个SLOT长度

![长帧同步](D:\02_data\github\笔记\MyNote\Audio\picture\长帧同步.png)

#### 短帧同步

SYNC脉冲宽度等于一个BCLK长度

![短帧同步](D:\02_data\github\笔记\MyNote\Audio\picture\短帧同步.png)

**如果需要更详细的理解PCM、TDM协议，请参考[pcmconfigv2_1.xls](./pcmconfigv2_1/pcmconfigv2_1.xls)，或利用开发板运行Demo，利用示波器或者逻辑分析仪进行抓包**



## PDM(Pulse Density Modulation)

PDM使用远高于PCM采样率的时钟采样调制模拟分量，只有1位输出，要么为0，要么为1。因此通过PDM方式表示的数字音频也被称为Oversampled 1-bit Audio。相比**PDM**一连串的0和1，**PCM**的量化结果更为直观简单。

![PDM](D:\02_data\github\笔记\MyNote\Audio\picture\PDM.png)

注：图中的正弦波经PDM采样后，输出值要么为0，要么为1



## 优缺点

| 协议     | 优点 | 缺点 |
| -------- | ---- | ---- |
| I2S      |      |      |
| PCM、TDM |      |      |
| PDM      |      |      |

## DRC(Dynamic Range Control)

DRC全称Dynamic Range Control，通常用来**调整音频信号的动态范围**，保证信号不至于过大或过小。DRC的原理其实很简单，就是根据输入信号的大小，对其施加一个增益：当检测到大信号时，施加一个负向增益，以降低信号幅值；当检测到小信号时，施加一个正向增益，以提升信号幅值。

### DRC作用

#### 抑制底噪

检测到db值小的噪音不让其输出，即负增益

#### 限幅

检测到db值大时，施加一个负增益

#### 放大

感觉声音小时，施加一个正增益

#### 相关参数

- **Threshold**（阈值）

  如果压缩器的振幅超过某个阈值，则压缩器会降低其电平。阈值（threshold）通常是以分贝为单位。通常低阈值(e.g. -60)意味着大部分的信号会被衰减。当信号低于阈值时，对输入的信号不做任何处理，这就意味着，-5db的衰减结果就是压缩少，处理的少。

- **Ratio**

  ratio是总的增益衰减，反映到图表中即为斜率。一个4：1的ratio增益系数，意味着输入信号高于阈值4db的话，输出信号把这个信号衰减为高于阈值1db,输出的增益这就会被衰减了3db

- **Energy、Attack、decay**

DRC需要提供一些系数来表述它的相应速度。**Energy、Attack、decay**可以进行表示。

energy为检测信号的周期系数

attack 就是DRC增益小数开始生效到稳定的周期系数

decay(release)就是DRC增益系数释放的时候从开始释放到稳定的周期系数

![TI-DRC](./picture/DRCFilter.png)

![TI-DRC](./picture/DRCtime示波器对比.png)

![TI-DRC](./picture/TI-Drc.png)

![TI-DRC](./picture/DRCtime.png)

## AEC(Acoustic Echo Cancellation)

一种音频处理技术，旨在**消除语音通信中出现的回声**。当音频信号从扬声器播放出来时，可能会经过麦克风被再次捕获，形成回声。这种回声会导致通话质量下降，使得对方听到自己的声音回音，影响通话的清晰度和可理解性。

音频AEC的目标是通过实时分析和处理音频信号，将扬声器输出的回声信号从麦克风输入中抵消或减弱，使得通话双方能够更清晰地听到对方的声音。它在语音通信中尤其重要，例如电话会议、网络电话、语音聊天等场景。

## AGC(Automatic Gain Control)

一种音频处理技术，旨在自动调整音频信号的增益（音量）水平，以确保信号的一致性和可听性。AGC常用于音频设备和系统中，以应对不同音量水平的输入信号并实现统一的输出级别。

音频AGC的主要目标是在不损失重要信号细节的同时，将输入信号的动态范围限制在一个适当的范围内。它通过实时监测音频信号的强度，并根据设定的目标增益水平自动调整信号的增益来实现。

## 参考资料

[I2S/PCM - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/353520173)

[数字音频接口 I2S、PCM、TDM 、PDM比较_tdm接口](https://blog.csdn.net/yangjizhen1533/article/details/113758138)

[音频接口：TDM，PDM，I2S，PCM 简介_51CTO博客_i2s mclk](https://blog.51cto.com/u_12810168/2450275)

[数字音频接口 – 第22条军规 (wangdali.net)](http://www.wangdali.net/i2s/)

[请问Energy Filter，Attack Filters ，Decay Filters该怎么理解？ - TI论坛 - 电子技术论坛 - 广受欢迎的专业电子论坛! (elecfans.com)](https://bbs.elecfans.com/jishu_1826197_1_1.html)







