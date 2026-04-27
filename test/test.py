import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_elevator(dut):

    dut._log.info("🚀 Elevator Test Start")

    # Clock
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # ---------------- RESET ----------------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("✅ Reset Done")

    # ---------------- REQUEST FLOOR 2 ----------------
    # ui_in[1:0] = floor
    # ui_in[2]   = valid

    dut.ui_in.value = 0b00000110   # floor=2, valid=1
    await ClockCycles(dut.clk, 1)

    # IMPORTANT: clear request
    dut.ui_in.value = 0

    # ---------------- CHECK MOVE UP ----------------
    await ClockCycles(dut.clk, 1)

    uo = dut.uo_out.value

    moving_up = (uo >> 2) & 1
    dut._log.info(f"Moving Up = {moving_up}")

    assert moving_up == 1, "❌ Elevator should move up"

    # ---------------- NEXT STEP ----------------
    await ClockCycles(dut.clk, 1)

    floor = dut.uo_out.value & 0b11
    dut._log.info(f"Floor after move = {floor}")

    # ---------------- FINAL FLOOR ----------------
    await ClockCycles(dut.clk, 2)

    floor = dut.uo_out.value & 0b11
    dut._log.info(f"Final floor = {floor}")

    assert floor == 2, "❌ Elevator did not reach floor 2"

    dut._log.info("✅ TEST PASSED")
