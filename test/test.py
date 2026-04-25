# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def set_request(dut, floor, valid):
    """Set request_floor (ui_in[1:0]) and request_valid (ui_in[2])"""
    value = 0
    value |= (floor & 0b11)        # bits [1:0]
    value |= (valid & 0b1) << 2    # bit [2]
    dut.ui_in.value = value


def get_outputs(dut):
    """Decode uo_out signals"""
    val = dut.uo_out.value.integer
    current_floor = val & 0b11
    moving_up     = (val >> 2) & 1
    moving_down   = (val >> 3) & 1
    door_open     = (val >> 4) & 1
    return current_floor, moving_up, moving_down, door_open


async def wait_until_floor(dut, target, max_cycles=10):
    """Wait until elevator reaches target floor"""
    for _ in range(max_cycles):
        await ClockCycles(dut.clk, 1)
        floor, up, down, door = get_outputs(dut)
        if floor == target:
            return floor, up, down, door
    assert False, f"Timeout: did not reach floor {target}"


@cocotb.test()
async def test_elevator(dut):
    dut._log.info("🚀 Starting Elevator Test")

    # Clock (10 us period)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -----------------------
    # Reset
    # -----------------------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)  # stabilization

    # Check initial state
    floor, up, down, door = get_outputs(dut)
    assert floor == 0, "Initial floor should be 0"
    assert up == 0 and down == 0, "Elevator should be idle after reset"

    # ----------------------------------
    # Test 1: Move UP (0 → 2)
    # ----------------------------------
    dut._log.info("⬆️ Test: Move Up to floor 2")

    set_request(dut, floor=2, valid=1)
    await ClockCycles(dut.clk, 1)
    set_request(dut, floor=2, valid=0)

    # Check movement started
    await ClockCycles(dut.clk, 1)
    floor, up, down, door = get_outputs(dut)
    assert up == 1, "Elevator should be moving up"

    # Wait until floor reached
    floor, up, down, door = await wait_until_floor(dut, 2)
    assert floor == 2, f"Expected floor 2, got {floor}"

    # Ensure it stops
    await ClockCycles(dut.clk, 1)
    floor, up, down, door = get_outputs(dut)
    assert up == 0 and down == 0, "Elevator should stop at floor 2"

    # ----------------------------------
    # Test 2: Move DOWN (2 → 0)
    # ----------------------------------
    dut._log.info("⬇️ Test: Move Down to floor 0")

    set_request(dut, floor=0, valid=1)
    await ClockCycles(dut.clk, 1)
    set_request(dut, floor=0, valid=0)

    # Check movement started
    await ClockCycles(dut.clk, 1)
    floor, up, down, door = get_outputs(dut)
    assert down == 1, "Elevator should be moving down"

    # Wait until floor reached
    floor, up, down, door = await wait_until_floor(dut, 0)
    assert floor == 0, f"Expected floor 0, got {floor}"

    # Ensure it stops
    await ClockCycles(dut.clk, 1)
    floor, up, down, door = get_outputs(dut)
    assert up == 0 and down == 0, "Elevator should stop at floor 0"

    # ----------------------------------
    # Test 3: Same Floor Request (Door Open)
    # ----------------------------------
    dut._log.info("🚪 Test: Same Floor Door Open")

    set_request(dut, floor=0, valid=1)
    await ClockCycles(dut.clk, 1)

    floor, up, down, door = get_outputs(dut)
    assert door == 1, "Door should open on same floor request"

    set_request(dut, floor=0, valid=0)
    await ClockCycles(dut.clk, 2)

    dut._log.info("✅ All tests passed successfully!")
