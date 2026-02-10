# 韦东山FreeRtos

[视频链接](https://www.bilibili.com/video/BV1Ar4y1C7En?spm_id_from=333.788.player.switch&vd_source=2e33a3cba9dea05126d330dcf100be27&p=3)

## 常用汇编

| 汇编                | 例子            | 说明                                                         |
| ------------------- | --------------- | ------------------------------------------------------------ |
| LDR(load register)  | LDR R3,[R2,#00] | R3为**目标寄存器**，R2原寄存器地址，#00为偏移。例子表示加载R2寄存器到R3寄存器 |
| STR(store register) | STR R3,[R2,#00] | 例子为设置R3的值到R2寄存器                                   |
| PUSH                | PUSH  {r3,lr}   | 将寄存器值压入栈，压入顺序按照寄存器编号从大到小进行写入。和括号内的顺序无关 |
| POP                 | POP    {r3,lr}  | 将栈的数据取出，顺序从低地址开始取出。即先获得R3值，SP+4后在获取LR的值 |
| MOV                 | mov	r5, r0   | r5:目标寄存器，r0源寄存器/立即数，mov将源寄存器/立即数的值赋值给目标寄存器 |

## 栈的作用

用来保存现场与恢复现场。

### 如何保存现场？

当程序出现中断时，需要保存当前的R0~R15，xPSR寄存器到SP内。**注意，SP（R13）不需要保存到栈里边，因为其本身就是栈**

当退出中断时，需要将保存的R0~R15,xPSR寄存器从SP内恢复到各自寄存器。

其中R0~R4,R12,LR,PC,XPSR由内核自动入栈，出栈。

软件保存或取出R5~R11。

#### rtos保存现场流程：

这个流程**一般在PendSV**内进行

| **步骤**        | **动作类型** | **执行内容**                  | **结果**               |
| --------------- | ------------ | ----------------------------- | ---------------------- |
| **1. 异常触发** | 硬件         | 压入 R0-R3, R12, LR, PC, xPSR | 保护了 C 运行环境      |
| **2. 汇编代码** | 软件         | 执行 `STMDB SP!, {R4-R11}`    | 保护了剩余寄存器       |
| **3. 更新 TCB** | 软件         | `TCB_Old->SP = SP`            | **封存**旧任务现场     |
| **4. 切换任务** | 软件         | `SP = TCB_New->SP`            | **激活**新任务现场     |
| **5. 汇编代码** | 软件         | 执行 `LDMIA SP!, {R4-R11}`    | 恢复新任务的手动寄存器 |
| **6. 异常返回** | 硬件         | 自动弹出 R0-xPSR              | 任务 B 恢复执行        |

### 什么情况下会保存现场？

| **情况**     | **普通函数调用**    | **硬件中断**             | **RTOS 任务切换**        |
| ------------ | ------------------- | ------------------------ | ------------------------ |
| **触发方式** | 代码主动调用        | 外部信号（按键、定时器） | 系统调度器触发（PendSV） |
| **保存位置** | 当前栈              | 当前栈 (MSP/PSP)         | 该任务专属的栈           |
| **保存程度** | 部分寄存器 (按协议) | 关键寄存器 (硬件全包)    | **所有**通用寄存器 + SP  |

## 任务状态转换

```mermaid
graph TD
    %% 状态定义
    New((新任务创建))
    Ready[就绪态 Ready]
    Running[运行态 Running]
    Blocked[阻塞态 Blocked]
    Suspended[挂起态 Suspended]
    Deleted((任务删除))

    %% 转换逻辑
    New -->|vTaskCreate| Ready
    
    Ready -->|调度器切换/高优先级抢占| Running
    Running -->|时间片用完/被更高优先级抢占| Ready
    
    Running -->|等待事件: 延时/信号量/队列| Blocked
    Blocked -->|事件发生: 延时到期/收到信号| Ready
    
    Running -->|vTaskSuspend| Suspended
    Ready -->|vTaskSuspend| Suspended
    Blocked -->|vTaskSuspend| Suspended
    Suspended -->|vTaskResume| Ready
    
    Running -->|vTaskDelete| Deleted
    Ready -->|vTaskDelete| Deleted
    Blocked -->|vTaskDelete| Deleted
```

## 优先级翻转举例

![image-20260208165411507](./assets/image-20260208165411507.png)

## 队列

用来传递数据

### 队列如何实现互斥访问

队列内部会有一个临界区，读写数据时会对操作的数据进行保护。

```mermaid
sequenceDiagram
    participant T as 任务 Task
    participant Q as 队列 Queue
    participant S as 调度器 Scheduler

    T->>Q: 尝试发送数据 (xQueueSend)
    Note over Q: 1. 进入临界区 (关中断)
    alt 队列未满
        Q->>Q: 拷贝数据至缓冲区
        Q->>Q: 更新指针和计数
        Note over Q: 2. 退出临界区 (开中断)
        Q-->>T: 返回成功
    else 队列已满
        Note over Q: 2. 检查阻塞时间 (Timeout)
        T->>S: 任务进入阻塞态
        S->>Q: 将任务挂入 xTasksWaitingToSend 链表
        Note over Q: 3. 退出临界区，切换至其他任务
    end
```

### 队列使用方式

- 一对一，一个生产者，一个消费者
- 多对一，多个生产者，一个消费者

- 一对多，一个生产者，多个消费者，消费者根据优先级获取队列数据（弊端，无法保证数据准确送给指定的消费者）
- 多对多，多个生产者，多个消费者（不建议这样使用）

## 信号量

### 二值信号量/计数信号量

```mermaid
graph TD
    Start((信号量操作)) --> Op{操作类型}
    
    Op -->|Give / 释放| Give[计数器 +1]
    Give --> Max{是否达到最大值?}
    Max -->|是| GFail[释放失败: 信号量已满]
    Max -->|否| GWake[检查阻塞链表: 唤醒等待任务]
    
    Op -->|Take / 获取| Take[计数器是否 > 0?]
    Take -->|是| TSub[计数器 -1]
    TSub --> TSuccess[获取成功: 任务继续运行]
    
    Take -->|否| TBlock{设置了阻塞等待?}
    TBlock -->|否| TFail[立即返回: 获取失败]
    TBlock -->|是| TSleep[任务进入阻塞态: 挂入等待链表]
    TSleep -->|超时或被唤醒| Take
```

### 互斥量

```mermaid
graph TD
    M_Start((任务 A 尝试获取 Mutex)) --> M_Check{Mutex 是否空闲?}
    
    M_Check -->|是| M_Take[获取成功: 记录所有者为任务 A]
    
    M_Check -->|否| M_Prio{当前任务 A 优先级 > <br>当前占有者 B?}
    
    M_Prio -->|是| M_Inh[<b>优先级继承</b>: <br>临时提升任务 B 的优先级至 A 的水平]
    M_Inh --> M_Wait[任务 A 进入阻塞等待]
    
    M_Prio -->|否| M_Wait
    
    M_Release((任务 B 释放 Mutex)) --> M_Rest[恢复任务 B 的原始优先级]
    M_Rest --> M_Wake[唤醒阻塞链表中的任务 A]
```

```mermaid
sequenceDiagram
    participant H as 高优先级 Task H
    participant M as 中优先级 Task M
    participant L as 低优先级 Task L
    participant Mutex as 互斥量 (Mutex)

    L->>Mutex: 获取锁
    Note over L: L 以低优先级运行
    H->>Mutex: 尝试获取锁 (失败)
    Note over H: H 阻塞
    Note right of L: 优先级继承：L 提升至 H 的级别
    
    M->>M: M 任务就绪
    Note over M: M 优先级低于当前的 L，无法抢占
    
    L->>L: L 快速完成工作
    L->>Mutex: 释放锁
    Note right of L: 优先级恢复：L 回到原始低级别
    
    Mutex->>H: 锁交给 H
    H->>H: H 立即抢占并运行
    H->>H: H 运行完毕
    M->>M: M 终于得到机会运行
```

## 应用场景

### 线程通讯

| **需求**                  | **推荐方案**   | **理由**                           |
| ------------------------- | -------------- | ---------------------------------- |
| **中断通知任务**          | 二值信号量     | 简单、开销极低、实时性高           |
| **保护打印机、总线**      | 互斥量 (Mutex) | 只有它支持优先级继承，防止死锁     |
| **我有 5 个空闲内存块**   | 计数信号量     | 内置计数器，自动管理资源数         |
| **等 A 且等 B 发生**      | 事件组 (AND)   | 信号量无法实现复杂的逻辑组合       |
| **等 A 或等 B 发生**      | 事件组 (OR)    | 避免开多个任务去等不同的信号量     |
| **一个信号唤醒 3 个任务** | 事件组         | 信号量释放一次通常只能唤醒一个任务 |

如果你是在管**“资源”**或者**“一对一”**发通知，选**信号量**；如果你是在处理**“逻辑组合”**或者**“广播通知”**，选**事件组**。

### 数据处理

| **特性**     | **数据队列 (Queue)**                 | **消息邮箱 (Mailbox)**                 |
| ------------ | ------------------------------------ | -------------------------------------- |
| **容量**     | 较大（支持多个消息排队）             | 通常为 1                               |
| **数据流向** | 强调“流”（Stream），所有数据都要处理 | 强调“值”（Value），通常只关心最新值    |
| **典型长度** | 5, 10, 50 ...                        | 1                                      |
| **满时行为** | 发送者通常阻塞等待空位               | 通常直接覆盖旧数据（取决于 RTOS 实现） |
| **内存开销** | 较高（取决于长度 * 单元大小）        | 极低                                   |

## 临界资源的访问方法

- 关中断，开中断
- 互斥量

