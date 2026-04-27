/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

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

    // Internal signals
    wire [1:0] request_floor = ui_in[1:0];
    wire request_valid = ui_in[2];
    wire reset = ~rst_n;

    reg [1:0] current_floor;
    reg moving_up;
    reg moving_down;
    reg door_open;

    // State encoding
    parameter IDLE      = 2'b00,
              MOVE_UP   = 2'b01,
              MOVE_DOWN = 2'b10;

    reg [1:0] state;
    reg [1:0] target_floor;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            state <= IDLE;
            current_floor <= 2'b00;
            target_floor <= 2'b00;
            moving_up <= 0;
            moving_down <= 0;
            door_open <= 0;
        end else begin
            // Default outputs
            moving_up <= 0;
            moving_down <= 0;
            door_open <= 0;

            case (state)

                IDLE: begin
                    if (request_valid) begin
                        target_floor <= request_floor;

                        if (request_floor > current_floor)
                            state <= MOVE_UP;
                        else if (request_floor < current_floor)
                            state <= MOVE_DOWN;
                        else
                            door_open <= 1;
                    end
                end

                MOVE_UP: begin
                    moving_up <= 1;
                    current_floor <= current_floor + 1;

                    if (current_floor + 1 == target_floor)
                        state <= IDLE;
                end

                MOVE_DOWN: begin
                    moving_down <= 1;
                    current_floor <= current_floor - 1;

                    if (current_floor - 1 == target_floor)
                        state <= IDLE;
                end

            endcase
        end
    end

    // Output mapping
    assign uo_out[1:0] = current_floor;
    assign uo_out[2]   = moving_up;
    assign uo_out[3]   = moving_down;
    assign uo_out[4]   = door_open;

    // Unused outputs
    assign uo_out[7:5] = 3'b000;

    // No bidirectional IO used
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Prevent unused warnings
    wire _unused = &{ena, uio_in, 1'b0};

endmodule
