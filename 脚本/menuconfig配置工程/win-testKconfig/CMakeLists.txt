cmake_minimum_required(VERSION 3.10)

project(test)

set(srcs "test1.c")

if(CONFIG_TEST2)    
    list(APPEND srcs "test2.c")
    message("TEST2")
endif()

if(CONFIG_TEST3)
    list(APPEND srcs "test3.c")
    message("TEST3")
endif()

list(APPEND srcs main.c)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

message(${srcs})

add_executable(test ${srcs})


#######################  GPT生成文件  ########################
# cmake_minimum_required(VERSION 3.10)

# project(MyProject)

# # 添加源文件
# set(SRCS test1.c test2.c test3.c main.c)

# # 添加头文件目录
# include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# add_executable(MyExecutable ${SRCS})
