cmake_minimum_required(VERSION 3.13)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(HW3 C CXX ASM)
set(CMAKE_C_STANDARD 11)

pico_sdk_init()

add_executable(HW3 main.c)

target_link_libraries(HW3
    pico_stdlib
    hardware_i2c
)

pico_add_extra_outputs(HW3)
