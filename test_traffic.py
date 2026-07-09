import cocotb
from cocotb.triggers import Timer, RisingEdge

# Helper dictionary to decode the 3-bit light state and print colored emoji blocks
LIGHT_DECODER = {
    1: "\033[91m🔴 [RED]\033[0m   ",   # 3'b001
    2: "\033[92m🟢 [GREEN]\033[0m ",   # 3'b010
    4: "\033[93m🟡 [YELLOW]\033[0m"    # 3'b100
}

async def generate_clock(dut):
    """Generate clock cycles."""
    while True:
        dut.clk.value = 0
        await Timer(5, units="ns")
        dut.clk.value = 1
        await Timer(5, units="ns")

@cocotb.test()
async def traffic_interactive_test(dut):
    """Monitor and interactively step through the traffic light cycles."""
    # Start clock
    cocotb.start_soon(generate_clock(dut))
    
    # Apply Reset
    dut.reset.value = 1
    await Timer(15, units="ns")
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    
    print("\n=============================================")
    print("      TRAFFIC LIGHT CONTROLLER MONITOR       ")
    print("=============================================")
    print("Press [ENTER] to advance 1 clock cycle.")
    print("Type 'auto' to run a full cycle automatically.")
    print("Type 'q' to quit.")
    print("=============================================\n")

    auto_mode = False
    cycle_count = 0

    while True:
        # Read internal state and counter safely from the DUT
        current_state = dut.state.value
        counter_val = dut.i.value
        light_val = dut.light.value.integer
        
        light_string = LIGHT_DECODER.get(light_val, "⚪ [UNKNOWN]")
        
        # Display the dashboard status line
        print(f"Cycle: {cycle_count:03d} | State: S{current_state} | Timer: {counter_val:02d} | Light: {light_string}", end="")

        if auto_mode:
            await RisingEdge(dut.clk)
            await Timer(1, units="ns") # Allow signals to settle
            cycle_count += 1
            print() # Move to next line
            if cycle_count >= 20: # Stop auto-mode after 20 cycles (one full loop)
                auto_mode = False
                print("\n[Auto run finished. Back to manual step.]")
        else:
            # Wait for user interactivity
            user_input = input("") 
            
            if user_input.strip().lower() == 'q':
                break
            elif user_input.strip().lower() == 'auto':
                auto_mode = True
                cycle_count = 0
                print("Running simulation automatically...")
            else:
                # Step exactly one clock edge forward
                await RisingEdge(dut.clk)
                await Timer(1, units="ns")
                cycle_count += 1