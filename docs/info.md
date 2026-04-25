# Elevator Controller (Tiny Tapeout Project)

## 📌 Overview
This project implements a simple **FSM-based elevator controller** for a 3-floor system using Verilog. It processes floor requests and controls elevator movement while indicating status signals such as direction and door state.

---

## ⚙️ Features
- Supports **3 floors (0, 1, 2)**
- Finite State Machine with:
  - `IDLE`
  - `MOVE_UP`
  - `MOVE_DOWN`
- Moves **one floor per clock cycle**
- Handles:
  - Upward movement
  - Downward movement
  - Same-floor request (door opens)
- Compact Tiny Tapeout-compatible interface

---

## 🔌 Pin Configuration

### Inputs (`ui_in`)
| Bit | Name              | Description                  |
|-----|------------------|------------------------------|
| 0   | request_floor[0] | Floor select (LSB)           |
| 1   | request_floor[1] | Floor select (MSB)           |
| 2   | request_valid    | Request trigger              |
| 3–7 | —                | Unused                       |

### Outputs (`uo_out`)
| Bit | Name              | Description                  |
|-----|------------------|------------------------------|
| 0   | current_floor[0] | Current floor (LSB)          |
| 1   | current_floor[1] | Current floor (MSB)          |
| 2   | moving_up        | Elevator moving up           |
| 3   | moving_down      | Elevator moving down         |
| 4   | door_open        | Door open indicator          |
| 5–7 | —                | Unused                       |

### Bidirectional (`uio`)
Not used in this design.

---

## 🧠 Design Details
- The controller starts at **floor 0** after reset.
- When a valid request is received:
  - If target > current → moves up
  - If target < current → moves down
  - If equal → door opens
- Movement occurs **one floor per clock cycle**
- Door opens for **one clock cycle** on same-floor request

---

## ⏱️ Clock & Reset
- Clock frequency: **10 MHz** (recommended)
- Reset: **Active-low (`rst_n`)**

---

## 🧪 Testing
- Verified using **cocotb testbench**
- Tests include:
  - Move up (0 → 2)
  - Move down (2 → 0)
  - Same-floor request (door open)

---

## 🚀 Future Improvements
- Add **multiple request queue**
- Add **door open timer**
- Support **more floors**
- Implement **priority scheduling**

---

## 👤 Author
**subiksha**

---

## 📜 License
SPDX-License-Identifier: Apache-2.0
