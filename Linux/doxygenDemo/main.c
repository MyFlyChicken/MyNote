/**
 * @file main.c
 * @author yuyf ()
 * @brief 测试模块
 * @version 0.1
 * @date 2024-04-08
 * 
 * @copyright Copyright (c) 2024 常山赵子龙
 * 
 * @section 打印学生信息模块
 * 打印传入的学生信息
 @code
student_t student = {.age = 18, .weight = 120, .height = 160};
print_sutdent((const student_t*) &student);
 @endcode
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2024-04-08 <td>v1.0     <td>chen     <td>内容
 * </table>
 */

#include "main.h"
#include <stdio.h>

/** @defgroup main主体
  * @{
  */

/** @defgroup 打印1
  * @{
  */

/**
 * @brief 输出字符串
 * 
 * @details 
 */
void print1(void)
{
  printf("this is printf1\r\n");
}

/**
  *@}
  */

/** @defgroup 打印2
  * @{
  */

/**
 * @brief 输出字符串
 * 
 * @details 
 */
void print2(void)
{
  printf("this is printf2\r\n");
}

/**
  *@}
  */

/** @defgroup 打印传入数据
  * @{
  */

/**
 * @brief 打印指定字符串
 * @param [in] str 指定字符串内容
 * 
 * @details 
 */
void print_arg(char * str)
{
  printf("%s\r\n", str);
}
/**
  *@}
  */

/** @addtogroup 打印学生信息
  * @{
  */

void print_sutdent(const student_t * p_stu)
{
  assert(p_stu);

  printf("age:%d\r\nheight:%d\r\nweight:%d\r\n", p_stu->age, p_stu->height, p_stu->weight);
}


/**
  *@}
  */



int main(void)
{
  student_t student = {.age = 18, .weight = 120, .height = 160};

  print1();
  print2();
  print_arg("Hello word");
  print_sutdent((const student_t*)&student);
  return 0;
}

/**
  *@}
  */

