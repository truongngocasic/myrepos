from ..common import common 

class scoreboard:

    def __init__(self, header, project_name, uvm_env):
        self.header                    = header
        self.environment_name          = project_name + "_env"
        self.interface_name            = project_name + "_env_if"
        self.scoreboard_name           = project_name + "_env_sb"
        self.environment_config_name   = project_name + "_env_cfg"
        self.agent_setting             = uvm_env["agent"]

    def gen(self):
        scoreboard_declare = ""
        scoreboard_declare = scoreboard_declare + "  //Environment interface\n"
        scoreboard_declare = scoreboard_declare + "  virtual %-42s env_if;\n\n" % (self.interface_name)
        scoreboard_declare = scoreboard_declare + "  //Environment config\n"
        scoreboard_declare = scoreboard_declare + "  %-50s env_cfg;\n\n" % (self.environment_config_name)
        analysis_imp_decl  = ""
        scoreboard_build   = ""
        function_decl      = ""

        scoreboard_declare = scoreboard_declare + "  //Ports that connect to agent\n"
        for agent in self.agent_setting:
            instance_name           = agent["instance_name"]
            instance_num            = agent["instance_num"]
            transaction_name        = agent["agent_name"] + "_tr"

            if (instance_num > 1):
                ii = 0
                while (ii < instance_num):
                    port_name = "%s%d_exp" % (instance_name, ii)
                    analysis_imp_decl  = analysis_imp_decl  + "`uvm_analysis_imp_decl(_%s)\n" % (port_name)
                    scoreboard_declare = scoreboard_declare + "  uvm_analysis_imp_%s #(%s, %s) %s;\n" % (port_name, transaction_name, self.scoreboard_name, port_name)
                    scoreboard_build   = scoreboard_build   + "    %s = new(\"%s\", this);\n" % (port_name, port_name)
                    function_decl      = function_decl + common.banner("function: write_%s" % (port_name), 2)
                    function_decl      = function_decl + "  function void write_%s(%s tr);\n" % (port_name, transaction_name)
                    function_decl      = function_decl + "    //Add code here\n"
                    function_decl      = function_decl + "  endfunction: write_%s\n" % (port_name)
                    function_decl      = function_decl + "\n"
                    ii = ii + 1
            else:
                port_name = "%s_exp" % (instance_name)
                analysis_imp_decl  = analysis_imp_decl  + "`uvm_analysis_imp_decl(_%s)\n" % (port_name)
                scoreboard_declare = scoreboard_declare + "  uvm_analysis_imp_%s #(%s, %s) %s;\n" % (port_name, transaction_name, self.scoreboard_name, port_name)
                scoreboard_build   = scoreboard_build   + "    %s = new(\"%s\", this);\n" % (port_name, port_name)
                function_decl      = function_decl + common.banner("function: write_%s" % (port_name), 2)
                function_decl      = function_decl + "  function void write_%s(%s tr);\n" % (port_name, transaction_name)
                function_decl      = function_decl + "    //Add code here\n"
                function_decl      = function_decl + "  endfunction: write_%s\n" % (port_name)
                function_decl      = function_decl + "\n"

        fh = open(self.scoreboard_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.scoreboard_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.scoreboard_name.upper()))
        fh.write("`define _%s_\n" % (self.scoreboard_name.upper()))
        fh.write("\n")
        fh.write("%s" % (analysis_imp_decl)) 
        fh.write("\n")
        fh.write("class %s extends uvm_scoreboard;\n" % (self.scoreboard_name))
        fh.write("  `uvm_component_utils(%s)\n" % (self.scoreboard_name))
        fh.write("\n")
        fh.write("%s" % (scoreboard_declare)) 
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (self.scoreboard_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: build_phase", 2)))
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("    //Get interface\n")
        fh.write("    if(!uvm_config_db #(virtual %s)::get(this, \"\", \"env_if\", env_if))\n" % (self.interface_name))
        fh.write("      `uvm_fatal(\"NOVIF\",{\"virtual interface must be set for: \", get_full_name(),\".env_if\"});\n")
        fh.write("\n")
        fh.write("    //Get env_cfg\n")
        fh.write("    if(!uvm_config_db #(%s)::get(this, \"\", \"env_cfg\", env_cfg))\n" % (self.environment_config_name))
        fh.write("      `uvm_fatal(\"scoreboard\",\"env_cfg is not set\");\n")
        fh.write("\n")
        fh.write("%s" % (scoreboard_build)) 
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: connect_phase", 2)))
        fh.write("  function void connect_phase(uvm_phase phase);\n")
        fh.write("    super.connect_phase(phase);\n")
        fh.write("  endfunction: connect_phase\n")
        fh.write("\n")
        fh.write("%s" % (function_decl)) 
        fh.write("%s" % (common.banner("task: run_phase", 2)))
        fh.write("  task run_phase(uvm_phase phase);\n")
        fh.write("  endtask: run_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: check_phase", 2)))
        fh.write("  function void check_phase(uvm_phase phase);\n")
        fh.write("  endfunction: check_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: report_phase", 2)))
        fh.write("  function void report_phase(uvm_phase phase);\n")
        fh.write("  endfunction: report_phase\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.scoreboard_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.scoreboard_name.upper()))
        fh.close()
