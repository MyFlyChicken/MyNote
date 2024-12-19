#ifndef _MR_CONFIG_H_
#define _MR_CONFIG_H_

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#define MR_USING_ASSERT
#define MR_CFG_HEAP_SIZE 4096
#define MR_USING_LOG_ERROR
#define MR_USING_LOG_WARN
#define MR_USING_LOG_INFO
#define MR_USING_LOG_DEBUG
#define MR_USING_LOG_SUCCESS
#define MR_CFG_PRINTF_BUFSZ 128
#define MR_CFG_PRINTF_DEV_NAME "serial1"
#define MR_USING_PRINTF_NONBLOCKING

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* _MR_CONFIG_H_ */
