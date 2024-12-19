/**
 * @file file.h
 * @author yuyf ()
 * @brief
 * @version 0.1
 * @date 2024-04-09
 *
 * @copyright Copyright (c) 2024 常山赵子龙
 *
 * @par 修改日志:
 * <table>
 * <caption id="multi_row1">Complex table</caption>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2024-04-09 <td>v1.0     <td>chen     <td>内容
 * </table>
 * @section
 * @code
 * @endcode
 */

#include <cstdint>
#include <stdint.h>
#include <stdlib.h>

/**
 * @brief 测试调用关系
 *
 * @details 包含了三个成员
 */
typedef struct {
  uint8_t t1; /*!< t1 */
  uint8_t t2; /*!< t2 */
  uint8_t t3; /*!< t3 */
} aaa_t;

extern void file1(void);

extern void file2(void);
