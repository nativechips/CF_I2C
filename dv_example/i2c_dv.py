from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import VirtualGPIOModel
import cocotb
from cocotb.triggers import RisingEdge
from caravel_cocotb.caravel_interfaces import I2C_Slave
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, First


@cocotb.test()
@report_test
async def i2c_dv(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=561831)
    cocotb.log.info("[TEST] Starting I2C master-slave communication test")
    cocotb.log.info("[TEST] Firmware will test both simple slave and M24AA64 EEPROM")

    virtual_gpio = VirtualGPIOModel(caravelEnv)
    virtual_gpio.start()

    await virtual_gpio.wait_output(1)
    #caravelEnv.dut.gpio9_en.value = 1
    await cocotb.start(I2C_Slave(caravelEnv.dut.gpio8_monitor, caravelEnv.dut.gpio9_monitor, caravelEnv.dut.gpio9, caravelEnv.dut.gpio9_en, {0x7A:0x2, 0x1B:0x5d}).run())
    await virtual_gpio.wait_output(2)
    await ClockCycles(caravelEnv.clk, 20000)
    await virtual_gpio.wait_output(3)

