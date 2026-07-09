`timescale 1ns/1ps
`include "traffic_light_controller.v"

module tb_traffic_light_controller;

  // Testbench signals
  reg clk, reset;
  wire [2:0] light;

  // Instantiate DUT
  traffic_light_controller uut (
    .clk(clk),
    .reset(reset),
    .light(light)
  );

  // Clock generation: 10ns period
  always #5 clk = ~clk;

  initial begin
    // VCD dump
    $dumpfile("traffic_light.vcd");
    $dumpvars(0, tb_traffic_light_controller);

    // Monitor signals
    $monitor("T=%0t | reset=%b | state_light=%b", $time, reset, light);

    // Initialize
    clk = 0;
    reset = 1;

    // Apply reset
    #12 reset = 0;

    // Run long enough to see multiple cycles
    #200 $finish;
  end

endmodule
