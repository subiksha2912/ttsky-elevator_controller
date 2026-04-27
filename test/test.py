import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_elevator(dut):
    dut._log.info("🚀 Starting Elevator Test")

    # Clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # -------------------------
    # TEST 1: MOVE UP
    # current = 0, target = 2
    # -------------------------
    dut._log.info("⬆️ Test: Move Up")

    current = 0
    target = 2
    dut.ui_in.value = (target << 2) | current

    await ClockCycles(dut.clk, 1)

    out = dut.uo_out.value.integer
    up   = (out >> 0) & 1
    down = (out >> 1) & 1
    idle = (out >> 2) & 1

    assert up == 1, "UP should be 1"
    assert down == 0, "DOWN should be 0"
    assert idle == 0, "IDLE should be 0"

    # -------------------------
    # TEST 2: MOVE DOWN
    # -------------------------
    dut._log.info("⬇️ Test: Move Down")

    current = 3
    target = 1
    dut.ui_in.value = (target << 2) | current

    await ClockCycles(dut.clk, 1)

    out = dut.uo_out.value.integer
    up   = (out >> 0) & 1
    down = (out >> 1) & 1
    idle = (out >> 2) & 1

    assert up == 0
    assert down == 1
    assert idle == 0

    # -------------------------
    # TEST 3: IDLE
    # -------------------------
    dut._log.info("⏸️ Test: Idle")

    current = 2
    target = 2
    dut.ui_in.value = (target << 2) | current

    await ClockCycles(dut.clk, 1)

    out = dut.uo_out.value.integer
    up   = (out >> 0) & 1
    down = (out >> 1) & 1
    idle = (out >> 2) & 1

    assert up == 0
    assert down == 0
    assert idle == 1

    dut._log.info("✅ ALL TESTS PASSED")
