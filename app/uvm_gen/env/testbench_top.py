import os
from ..common import common 
from ..agent  import agent as import_agent

class testbench_top:


    def __init__(self, header, project_name, uvm_env):
        self.header                    = header
        self.testbench_top_name        = uvm_env["testbench"]
        self.environment_name          = project_name + "_env"
        self.environment_cfg_name      = project_name + "_env_cfg"
        self.environment_if_name       = project_name + "_env_if"
        self.scoreboard_name           = project_name + "_env_sb"
        self.coverage_name             = project_name + "_env_cov"
        self.virtual_sequence_name     = project_name + "_vir_seq"
        self.virtual_sequencer_name    = project_name + "_vir_seqr"
        self.testlib_name              = project_name + "_testlib"
        self.agent_setting             = uvm_env["agent"]
        self.clock                     = uvm_env["clock"]
        self.reset                     = uvm_env["reset"]

    def gen2(self):
        agent_dict      = {}
        tb_include_if   = "`include \"%s.sv\"\n" % (self.environment_if_name)
        tb_include_pkg  = ""
        tb_instance_if  = "  %-50s %s(%s, %s);\n" % (self.environment_if_name, self.environment_if_name, self.clock, self.reset)
        tb_import_pkg   = ""
        tb_cfg_db_agent = ""
        #tb_cfg_db_other = ""

        os.chdir("../model")
        for model in self.agent_setting:
            agent_name              = model["agent_name"]
            instance_name           = model["instance_name"]
            instance_num            = model["instance_num"]
            agent = import_agent.agent(self.header, agent_name, instance_name, instance_num)
            tb_instance_if  = tb_instance_if  + agent.gen_if_instance(self.clock, self.reset, 2)
            tb_cfg_db_agent = tb_cfg_db_agent + agent.gen_if_cfg_db_set_agent("uvm_test_top.env", 4)
            #tb_cfg_db_other = tb_cfg_db_other + agent.gen_if_cfg_db_set_other("uvm_test_top.env.env_cov", 4)
            if (agent_name not in agent_dict):          #Gen agent component
                common.create_dir(agent_name)
                os.chdir(agent_name)
                agent.gen_agent()
                tb_include_if  = tb_include_if   + agent.gen_include_if(0)
                tb_include_pkg = tb_include_pkg  + agent.gen_include_pkg(0)
                tb_import_pkg  = tb_import_pkg   + agent.gen_import_pkg(2)
                agent_dict[agent_name] = 1
                os.chdir("../")

        os.chdir("../env")
        fh = open(self.testbench_top_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.testbench_top_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.testbench_top_name.upper()))
        fh.write("`define _%s_\n" % (self.testbench_top_name.upper()))
        fh.write("\n")
        fh.write("%s" % (tb_include_if))
        fh.write("%s" % (tb_include_pkg))
        fh.write("\n")
        fh.write("module %s;\n" % (self.testbench_top_name))
        fh.write("\n")
        fh.write("%s" % (common.banner("ENVIRONMENT", 2)))
        fh.write("%s" % (tb_import_pkg))
        fh.write("\n")
        fh.write("  `include \"%s.sv\"\n" % (self.environment_cfg_name))
        fh.write("  `include \"%s.sv\"\n" % (self.virtual_sequencer_name))
        fh.write("  `include \"%s.sv\"\n" % (self.virtual_sequence_name))
        fh.write("  `include \"%s.sv\"\n" % (self.scoreboard_name))
        fh.write("  `include \"%s.sv\"\n" % (self.coverage_name))
        fh.write("  `include \"%s.sv\"\n" % (self.environment_name))
        fh.write("  `include \"%s.sv\"\n" % (self.testlib_name))
        fh.write("\n")
        fh.write("%s" % (common.banner("CLOCK & RESET GENERATOR", 2)))
        fh.write("  //CLOCK\n")
        fh.write("  parameter CLK_CYCLE = 40;\n")
        fh.write("  logic %s;\n" % (self.clock))
        fh.write("\n")
        fh.write("  initial begin\n")
        fh.write("    %s = 0;\n" % (self.clock))
        fh.write("  end\n")
        fh.write("\n")
        fh.write("  always #(CLK_CYCLE/2)\n")
        fh.write("    %s = ~%s;\n" % (self.clock, self.clock))
        fh.write("\n")
        fh.write("  //RESET\n")
        fh.write("  logic %s;\n" % (self.reset))
        fh.write("  assign %s = %s._reset_n;\n" % (self.reset, self.environment_if_name))
        fh.write("\n")
        fh.write("%s" % (common.banner("INTERFACE", 2)))
        fh.write("%s" % (tb_instance_if))
        fh.write("\n")
        fh.write("%s" % (common.banner("DUT CONNECTION", 2)))
        fh.write("\n")
        fh.write("%s" % (common.banner("WAVEFORM", 2)))
        fh.write("  `ifdef FSDB_ON\n")
        fh.write("    initial begin\n")
        fh.write("      $fsdbDumpfile(\"$testbench_name\");\n")
        fh.write("      $fsdbDumpvars(0, \"$testbench_name\");\n")
        fh.write("    end\n")
        fh.write("  `else\n")
        fh.write("    `ifdef VPD_ON\n")
        fh.write("    initial begin\n")
        fh.write("      $vcdpluson;\n")
        fh.write("      $vcdplusmemon;\n")
        fh.write("    end\n")
        fh.write("    `endif\n")
        fh.write("  `endif\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("Run UVM test", 2)))
        fh.write("  initial begin\n")
        fh.write("    uvm_config_db #(virtual %s)::set(uvm_root::get(), \"*\", \"env_if\", %s);\n" % (self.environment_if_name, self.environment_if_name))
        fh.write("%s" % (tb_cfg_db_agent))
        #fh.write("%s" % (tb_cfg_db_other))
        fh.write("    run_test();\n")
        fh.write("  end\n")
        fh.write("\n")
        fh.write("endmodule: %s\n" % (self.testbench_top_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.testbench_top_name.upper()))
        fh.close()

