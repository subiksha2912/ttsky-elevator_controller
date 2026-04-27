import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_elevator(dut):
    dut._log.info("🚀 Starting Elevator FSM Test")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    dut.ui_in.value = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # --------------------------------
    # REQUEST: GO TO FLOOR 2
    # --------------------------------
    dut._log.info("Request floor 2")

    dut.ui_in.value = (1 << 2) | 2   # valid=1, floor=2

    await ClockCycles(dut.clk, 1)

    # REMOVE request (important)
    dut.ui_in.value = 0

    # --------------------------------
    # WAIT FOR MOVEMENT
    # --------------------------------
    await ClockCycles(dut.clk, 5)

    out = dut.uo_out.value.integer

    moving_up = (out >> 2) & 1

    assert moving_up == 1, "Elevator should move UP"

    # --------------------------------
    # WAIT UNTIL REACH FLOOR
    # --------------------------------
    await ClockCycles(dut.clk, 5)

    out = dut.uo_out.value.integer

    floor = out & 0b11
    door  = (out >> 4) & 1

    assert floor == 2, "Should reach floor 2"
    assert door == 1, "Door should open"

    dut._log.info("✅ TEST PASSED")
