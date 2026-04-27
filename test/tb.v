
`default_nettype none

module tb;

    reg  [7:0] ui_in;
    wire [7:0] uo_out;
    reg  [7:0] uio_in;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;
    reg  ena;
    reg  clk;
    reg  rst_n;

    // Instantiate DUT
    tt_um_example dut (
        .ui_in(ui_in),
        .uo_out(uo_out),
        .uio_in(uio_in),
        .uio_out(uio_out),
        .uio_oe(uio_oe),
        .ena(ena),
        .clk(clk),
        .rst_n(rst_n)
    );

    // Clock generation (10ns period)
    always #5 clk = ~clk;

    initial begin
        // Init
        clk = 0;
        rst_n = 0;
        ena = 1;
        ui_in = 0;
        uio_in = 0;

        // Reset pulse
        #20;
        rst_n = 1;

        // ----------------------------
        // Test 1: Request floor 2 (10)
        // ----------------------------
        #10;
        ui_in[1:0] = 2'b10; // target floor = 2
        ui_in[2]   = 1'b1;  // request_valid

        #10;
        ui_in[2]   = 1'b0;  // deassert request

        // Wait for movement
        #100;

        // ----------------------------
        // Test 2: Request floor 0 (down)
        // ----------------------------
        #10;
        ui_in[1:0] = 2'b00;
        ui_in[2]   = 1'b1;

        #10;
        ui_in[2]   = 1'b0;

        #100;

        // ----------------------------
        // Test 3: Same floor request
        // ----------------------------
        #10;
        ui_in[1:0] = uo_out[1:0]; // request current floor
        ui_in[2]   = 1'b1;

        #10;
        ui_in[2]   = 1'b0;

        #50;

    end

    // Monitor signals
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, tb_tt_um_example);

        $display("Time\tFloor\tUp\tDown\tDoor");
        $monitor("%0t\t%b\t%b\t%b\t%b",
            $time,
            uo_out[1:0],  // current_floor
            uo_out[2],    // moving_up
            uo_out[3],    // moving_down
            uo_out[4]     // door_open
        );
    end

endmodule
