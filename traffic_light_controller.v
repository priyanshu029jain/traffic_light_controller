module traffic_light_controller(
    input clk, reset,
    output reg [2:0] light
  );

  parameter s0 = 2'b00, s1 = 2'b01, s2 = 2'b10;
  parameter RED = 3'b001, GREEN = 3'b010, YELLOW = 3'b100;
  parameter red_delay = 10, green_delay = 5, yellow_delay = 2;

  reg [1:0] state;
  reg [8:0] i;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= s0;
      i <= 0;
      light <= RED;
    end
    else
    begin
      case(state)
        s0 :
        begin
          light <= RED;
          if(i == red_delay)
          begin
            state <= s1;
            i <= 0;
          end
          else
            i <= i + 1;
        end
        s1 :
        begin
          light <= GREEN;
          if(i == green_delay)
          begin
            state <= s2;
            i <= 0;
          end
          else
            i <= i + 1;
        end
        s2 :
        begin
          light <= YELLOW;
          if(i == yellow_delay)
          begin
            state <= s0;
            i <= 0;
          end
          else
            i <= i + 1;
        end
        default :
        begin
          light <= RED;
          state <= s0;
          i <= 0;
        end
      endcase
    end
  end
endmodule
