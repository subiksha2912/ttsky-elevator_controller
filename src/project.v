`default_nettype none

//--------------------------------------
// TOP MODULE (TinyTapeout Wrapper)
//--------------------------------------
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
    // CORE FSM
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
    assign uo_out[7:5] = 3'b000;

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Prevent unused warnings
    wire _unused = &{ena, uio_in, ui_in[7:3], 1'b0};

endmodule


//--------------------------------------
// ELEVATOR CONTROLLER FSM
//--------------------------------------
module elevator_controller (
    input clk,
    input reset,
    input [1:0] request_floor,
    input request_valid,
    output reg [1:0] current_floor,
    output reg moving_up,
    output reg moving_down,
    output reg door_open
);

    // States
    parameter IDLE      = 2'b00,
              MOVE_UP   = 2'b01,
              MOVE_DOWN = 2'b10;

    reg [1:0] state;
    reg [1:0] target_floor;

    always @(posedge clk) begin
        if (reset) begin
            state <= IDLE;
            current_floor <= 2'b00;
            target_floor <= 2'b00;
            moving_up <= 0;
            moving_down <= 0;
            door_open <= 0;
        end 
        else begin
            // Default outputs
            moving_up <= 0;
            moving_down <= 0;
            door_open <= 0;

            case (state)

                //----------------------------------
                // IDLE STATE
                //----------------------------------
                IDLE: begin
                    door_open <= 1; // door open when idle

                    if (request_valid) begin
                        target_floor <= request_floor;
                        door_open <= 0;

                        if (request_floor > current_floor)
                            state <= MOVE_UP;
                        else if (request_floor < current_floor)
                            state <= MOVE_DOWN;
                        else
                            door_open <= 1; // already there
                    end
                end

                //----------------------------------
                // MOVE UP
                //----------------------------------
                MOVE_UP: begin
                    moving_up <= 1;

                    if (current_floor == target_floor) begin
                        state <= IDLE;
                    end 
                    else begin
                        current_floor <= current_floor + 1;
                    end
                end

                //----------------------------------
                // MOVE DOWN
                //----------------------------------
                MOVE_DOWN: begin
                    moving_down <= 1;

                    if (current_floor == target_floor) begin
                        state <= IDLE;
                    end 
                    else begin
                        current_floor <= current_floor - 1;
                    end
                end

            endcase
        end
    end

endmodule
