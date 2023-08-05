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



