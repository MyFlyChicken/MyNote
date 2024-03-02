## 安装pack

1. pyocd pack -i (芯片支持包的索引)
2. 查看log是否下载成功
3. pyocd pack -f (芯片)，查看Installed是否成功
4. 如果为TRUE则说明下载成功，为FALSE则失败。需要手动下载pack包放置在对应的路径

![image-20240103162922432](./assets/image-20240103162922432.png)

~~~
pyocd pack -f apm32
pyocd pack -i APM32E103CE
Pyocd pack -s 
~~~

## pyocd_user.py

文件作用参考[这里](https://github.com/pyocd/pyOCD/blob/main/docs/user_scripts.md)

demo：自定义FLM下载算法，参考[这里](https://forum.electro-smith.com/t/anyone-using-pyocd/1330/4)

```
# For Daisy Seed
def will_connect():

    # For STM32H750xB devices: a 128-Kbyte user Flash memory block containing one
    # user sector of 128 Kbytes (4 K Flash words).
    # 256 bit write = page_size of 32 Bytes
    # see /data/daisy/cmsis/Keil.STM32H7xx_DFP.pdsc
    internal_flash = target.memory_map.get_first_matching_region(name="FLASH_Bank1")
    LOG.info("Updating %s settings", internal_flash.name)
    flash = pyocd.core.memory_map.FlashRegion(
                                        name=internal_flash.name,
                                        start=0x08000000,
                                        length=0x200000,
                                        blocksize=0x800,
                                        page_size=0x20,
                                        access='rx',
                                        is_boot_memory=True,
                                        flm="./STM32H7x_2048.FLM"
                                        )
    target.memory_map.remove_region(internal_flash)
    target.memory_map.add_region(flash)
    LOG.info("===>>>%s", repr(flash))

    # Create the new 64M SDRAM region
    #sdram = pyocd.core.memory_map.RamRegion(
    #                                    name="sdram",
    #                                    start=0xc0000000,
    #                                    length=0x4000000,
    #                                    is_default=False,
    #                                    is_powered_on_boot=False
    #                                    )
#
    ## Add the SDRAM region to the memory map.
    #target.memory_map.add_region(sdram)
#
    ## Create QSPIFLASH - took blocksize from libdaisy/src/per/qspi.c
    ## TODO: No ALGO for this - can't keep code in it yet 
    #qspiflash = pyocd.core.memory_map.FlashRegion(
    #                                    name="qspiflash",
    #                                    start=0x90000000,
    #                                    length=0x800000,
    #                                    blocksize=0x1000
    #                                    )
#
    ## Add the SDRAM region to the memory map.
    #target.memory_map.add_region(qspiflash)

#
# Don't know if this is 100% needed 
#
# The DBGMCU registers are not reset by a system reset, only by a power on reset. They are
# accessible to the debugger via the APB-D bus at base address 0xE00E1000. They are also
# accessible by the processor core at base address 0x5C001000.
# Note: the DBGMCU is not a standard CoreSight component. Therefore, it does not appear
# in the system ROM table.
#
# DBGMCU configuration register (DBGMCU_CR)
# Address offset: 0x004
# Reset value: 0x0000 0000
# 
# See also CMSIS/Debug/STM32H742_743_753_750.dbgconf
# and /data/daisy/cmsis/Keil.STM32H7xx_DFP.pdsc

#DBGMCU_CR = 0xE00E1004
#DBGMCU_APB3FZ1 = 0xE00E1034
#DBGMCU_APB1LFZ1 = 0xE00E103C
#DBGMCU_APB2FZ1 = 0xE00E104C
#DBGMCU_APB4FZ1 =  0xE00E1054#

#def did_connect():
#    # Set STANDBY, STOP, and SLEEP bits all to 1.
#    # set preset values (enable all debug clocks by default)
#    # DBGMCU_CR[18] CKDBGD3EN, [17] CKDBGD2EN, [16] CKDBGD1EN
#    # DBGMCU_CR[22] D3DBGCKEN, [21] D1DBGCKEN
#    # 
#    # From DM00314099.pdf:
#    # D3DBGCKEN: bit 22
#    # D1DBGCKEN: bit 21
#    # TRACECLKEN: bit 20
#    val = target.read32(DBGMCU_CR)
#    val |= (0x00700000 | 0x00000007)
#    LOG.info("Setting DBGMCU_CR to 0x%x after connect", val)
#    target.write32(DBGMCU_CR, val)
#    target.write32(DBGMCU_APB3FZ1, 0x0)
#    target.write32(DBGMCU_APB1LFZ1, 0x0)
#    target.write32(DBGMCU_APB2FZ1, 0x0)
#    target.write32(DBGMCU_APB4FZ1, 0x0)

```



