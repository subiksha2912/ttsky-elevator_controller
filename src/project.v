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

    // -----------------------------
    // INPUT MAPPING
    // -----------------------------
    wire [1:0] request_floor = ui_in[1:0];
    wire request_valid       = ui_in[2];

    // -----------------------------
    // INTERNAL SIGNALS
    // -----------------------------
    wire [1:0] current_floor;
    wire moving_up;
    wire moving_down;
    wire door_open;

    // -----------------------------
    // INSTANTIATE YOUR FSM
    // -----------------------------
    elevator_controller core (
        .clk(clk),
        .reset(~rst_n),
        .request_floor(request_floor),
        .request_valid(request_valid),
        .current_floor(current_floor),
        .moving_up(moving_up),
        .moving_down(moving_down),
        .door_open(door_open)
    );

    // -----------------------------
    // OUTPUT MAPPING
    // -----------------------------
    assign uo_out[1:0] = current_floor;
    assign uo_out[2]   = moving_up;
    assign uo_out[3]   = moving_down;
    assign uo_out[4]   = door_open;
    assign uo_out[7:5] = 0;

    assign uio_out = 0;
    assign uio_oe  = 0;

    wire _unused = &{ena, uio_in};

endmodule
