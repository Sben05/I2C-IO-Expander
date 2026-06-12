#include "pico/stdlib.h"
#include "hardware/i2c.h"

#define ADDR  0x20
#define IODIR 0x00
#define GPIO  0x09
#define OLAT  0x0A

#define HEARTBEAT_PIN 15

void writeReg(uint8_t addr, uint8_t reg, uint8_t val) {
    uint8_t buf[2] = {reg, val};
    i2c_write_blocking(i2c_default, addr, buf, 2, false);
}

uint8_t readReg(uint8_t addr, uint8_t reg) {
    uint8_t val;
    i2c_write_blocking(i2c_default, addr, &reg, 1, true);
    i2c_read_blocking(i2c_default, addr, &val, 1, false);
    return val;
}

int main() {
    stdio_init_all();

    i2c_init(i2c_default, 100 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);

    gpio_init(HEARTBEAT_PIN);
    gpio_set_dir(HEARTBEAT_PIN, GPIO_OUT);

    writeReg(ADDR, IODIR, 0b01111111);

    int tick = 0;
    bool hb = false;

    while (true) {
        uint8_t gpioVal = readReg(ADDR, GPIO);
        if ((gpioVal & 0x01) == 0) {
            writeReg(ADDR, OLAT, 0x80);
        } else {
            writeReg(ADDR, OLAT, 0x00);
        }

        tick++;
        if (tick >= 50) {
            tick = 0;
            hb = !hb;
            gpio_put(HEARTBEAT_PIN, hb);
        }

        sleep_ms(10);
    }
}
