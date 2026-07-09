# Simulator settings
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# Provide the path to your Verilog file
VERILOG_SOURCES += traffic_light_controller.v

# Top level module name inside the verilog file
TOPLEVEL = traffic_light_controller

# Python file name containing the @cocotb.test() wrapper
MODULE = test_traffic

# Include cocotb makefile rules
include $(shell cocotb-config --makefiles)/Makefile.sim