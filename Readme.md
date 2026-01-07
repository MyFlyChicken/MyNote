# 笔记目录

- [编码规范，参考esp32](https://docs.espressif.com/projects/esp-idf/zh_CN/v4.3.4/esp32/contribute/documenting-code.html#)

# 奇技淫巧
 - 使用[ringbuffer](https://github.com/cherry-embedded/CherryRB/tree/master)时，可以使用线性API来避免多次拷贝的问题，例如DMA传输或数据接收，都可以使用线性API来提高效率：
```c
// Example of using CherryRB linear API
extern void *chry_ringbuffer_linear_write_setup(chry_ringbuffer_t *rb, uint32_t *size);
extern void *chry_ringbuffer_linear_read_setup(chry_ringbuffer_t *rb, uint32_t *size);
extern uint32_t chry_ringbuffer_linear_write_done(chry_ringbuffer_t *rb, uint32_t size);
extern uint32_t chry_ringbuffer_linear_read_done(chry_ringbuffer_t *rb, uint32_t size);
```
 - 解耦
```
// 文件定义，depend用来定义模块依赖，adapter用来定义模块适配器
    module.c
    module_adapter.c
    module_adapter.h
    module_depend.c
    module_depend.h
```
