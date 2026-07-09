# run.py
import os
from pathlib import Path
from cocotb.runner import get_runner

def run_simulation():
    # Use icarus simulator
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent

    runner = get_runner(sim)
    
    # 1. Build/Compile the Verilog source
    runner.build(
        verilog_sources=[proj_path / "traffic_light_controller.v"],
        hdl_toplevel="traffic_light_controller",
        always=True,
    )
    
    # 2. Run the interactive Python testbench
    runner.test(
        hdl_toplevel="traffic_light_controller",
        test_module="test_traffic",
    )

if __name__ == "__main__":
    run_simulation()