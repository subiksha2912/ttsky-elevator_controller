`default_nettype none

module tt_um_elevator_controller (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

  // Extract inputs
  wire [1:0] current_floor = ui_in[1:0];
  wire [1:0] target_floor  = ui_in[3:2];

  // Logic
  wire up   = (target_floor > current_floor);
  wire down = (target_floor < current_floor);
  wire idle = (target_floor == current_floor);

  // Assign outputs
  assign uo_out[0] = up;
  assign uo_out[1] = down;
  assign uo_out[2] = idle;
  assign uo_out[7:3] = 0;

  // Not used
  assign uio_out = 0;
  assign uio_oe  = 0;

  wire _unused = &{ena, clk, rst_n, uio_in};

endmodule
