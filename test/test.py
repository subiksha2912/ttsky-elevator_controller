import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_elevator(dut):

    dut._log.info("🚀 Starting Elevator Test")

    # Clock (10ns period)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # -------------------------
    # RESET
    # -------------------------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("✅ Reset Done")

    # -------------------------
    # REQUEST: Go to floor 2
    # -------------------------
    # ui_in mapping:
    # [1:0] = floor
    # [2]   = request_valid

    dut.ui_in.value = 0b00000110   # floor=2, valid=1

    await ClockCycles(dut.clk, 1)

    # REMOVE request (important!)
    dut.ui_in.value = 0

    # -------------------------
    # CHECK MOVING UP (exact cycle)
    # -------------------------
    await ClockCycles(dut.clk, 1)

    up = (dut.uo_out.value >> 2) & 1
    dut._log.info(f"Moving Up = {up}")

    assert up == 1, "❌ Elevator should be moving up"

    # -------------------------
    # NEXT CYCLE → FLOOR UPDATE
    # -------------------------
    await ClockCycles(dut.clk, 1)

    floor = dut.uo_out.value & 0b11
    dut._log.info(f"Current Floor = {floor}")

    # -------------------------
    # WAIT UNTIL REACH TARGET
    # -------------------------
    await ClockCycles(dut.clk, 2)

    floor = dut.uo_out.value & 0b11
    dut._log.info(f"Final Floor = {floor}")

    assert floor == 2, "❌ Elevator did not reach floor 2"

    dut._log.info("✅ TEST PASSED")
