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
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    dut._log.info("✅ Reset Done")

    # -------------------------------
    # TEST: Move from floor 0 → 2
    # -------------------------------

    # request_floor = 2 (10), valid = 1
    dut.ui_in.value = 0b00000110   # [2]=valid, [1:0]=floor=2

    await ClockCycles(dut.clk, 1)

    # remove request
    dut.ui_in.value = 0

    # Wait for movement
    await ClockCycles(dut.clk, 3)

    output = dut.uo_out.value.integer

    current_floor = output & 0b11
    moving_up = (output >> 2) & 1

    dut._log.info(f"Floor={current_floor}, moving_up={moving_up}")

    assert moving_up == 1, "❌ Elevator should move UP"

    # Wait to reach floor
    await ClockCycles(dut.clk, 3)

    output = dut.uo_out.value.integer
    current_floor = output & 0b11

    dut._log.info(f"Final Floor={current_floor}")

    assert current_floor == 2, "❌ Elevator did not reach floor 2"

    dut._log.info("✅ TEST PASSED")
