/**
 * @file main.h
 * @author yuyf ()
 * @brief 测试模块
 * @version 0.1
 * @date 2024-04-08
 * 
 * @copyright Copyright (c) 2024 常山赵子龙
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2024-04-08 <td>v1.0     <td>chen     <td>第一次测试
 * </table>
 */

 #include <stdint.h>
 #include <stdlib.h>
 #include <assert.h>
/**
 * @brief 定义学生类
 * 
 * @details 包含了学生的身高，体重，年龄信息
 */
typedef struct {
    uint8_t age;
    uint8_t weight;
    uint8_t height;
}student_t;
