from ..common import common 

class coverage:

    def __init__(self, header, project_name, uvm_env):
        self.header                     = header
        self.coverage_name              = project_name + "_env_cov"
        self.config_name                = project_name + "_env_cfg"
        self.environment_interface_name = project_name + "_env_if"
        self.agent_setting              = uvm_env["agent"]

    def gen(self):
        coverage_declare = "  //Ports that connect to agent\n"
        coverage_build   = ""
        function_decl    = ""
        #interface_decl   = ""
        #get_interface    = ""
        for agent in self.agent_setting:
            instance_name           = agent["instance_name"]
            instance_num            = agent["instance_num"]
            transaction_name        = agent["agent_name"] + "_tr"
            interface_name          = agent.get("interface_name",        agent["agent_name"] + "_if")
            if (instance_num > 1):
                #interface_decl = interface_decl + "  virtual %-42s %s[%0d];\n" % (interface_name, instance_name + "_if", instance_num)
                ii = 0
                while (ii < instance_num):
                    port_name = "%s%d_exp" % (instance_name, ii)
                    coverage_declare = coverage_declare + "  uvm_analysis_imp_%s #(%s, %s) %s;\n" % (port_name, transaction_name, self.coverage_name, port_name)
                    coverage_build   = coverage_build   + "    %s = new(\"%s\", this);\n" % (port_name, port_name)
                    function_decl      = function_decl + common.banner("function: write_%s" % (port_name), 2)
                    function_decl    = function_decl + "  function void write_%s(%s tr);\n" % (port_name, transaction_name)
                    function_decl    = function_decl + "    //Add code here\n"
                    function_decl    = function_decl + "  endfunction: write_%s\n" % (port_name)
                    function_decl    = function_decl + "\n"
                    #get_interface    = get_interface + "\n    if(!uvm_config_db #(virtual %s)::get(this, \"\", \"%s[%0d]\", %s[%0d]))\n" % (interface_name, instance_name + "_if", ii, instance_name + "_if", ii)
                    #get_interface    = get_interface + "      `uvm_fatal(\"NOVIF\",{\"virtual interface must be set for: \", get_full_name(),\".env_if\"});\n"
                    ii = ii + 1
            else:
                #interface_decl = interface_decl + "  virtual %-42s %s;\n" % (interface_name, instance_name + "_if")
                port_name = "%s_exp" % (instance_name)
                coverage_declare = coverage_declare + "  uvm_analysis_imp_%s #(%s, %s) %s;\n" % (port_name, transaction_name, self.coverage_name, port_name)
                coverage_build   = coverage_build   + "    %s = new(\"%s\", this);\n" % (port_name, port_name)
                function_decl      = function_decl + common.banner("function: write_%s" % (port_name), 2)
                function_decl    = function_decl + "  function void write_%s(%s tr);\n" % (port_name, transaction_name)
                function_decl    = function_decl + "    //Add code here\n"
                function_decl    = function_decl + "  endfunction: write_%s\n" % (port_name)
                function_decl    = function_decl + "\n"
                #get_interface    = get_interface + "\n    if(!uvm_config_db #(virtual %s)::get(this, \"\", \"%s\", %s))\n" % (interface_name, instance_name + "_if", instance_name + "_if")
                #get_interface    = get_interface + "      `uvm_fatal(\"NOVIF\",{\"virtual interface must be set for: \", get_full_name(),\".env_if\"});\n"

        fh = open(self.coverage_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.coverage_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.coverage_name.upper()))
        fh.write("`define _%s_\n" % (self.coverage_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_component;\n" % (self.coverage_name))
        fh.write("  `uvm_component_utils(%s)\n" % (self.coverage_name))
        fh.write("\n")
        fh.write("  virtual %-42s env_if;\n" % (self.environment_interface_name))
        #fh.write("%s\n" % (interface_decl))
        fh.write("  %-50s env_cfg;\n" % (self.config_name))
        fh.write("\n")
        fh.write("%s" % (coverage_declare)) 
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (self.coverage_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: build_phase", 2)))
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("    //Get interface\n")
        fh.write("    if(!uvm_config_db #(virtual %s)::get(this, \"\", \"env_if\", env_if))\n" % (self.environment_interface_name))
        fh.write("      `uvm_fatal(\"NOVIF\",{\"virtual interface must be set for: \", get_full_name(),\".env_if\"});\n")
        #fh.write("%s\n" % (get_interface))
        fh.write("\n")
        fh.write("    //Get env_cfg\n")
        fh.write("    if(!uvm_config_db #(%s)::get(this, \"\", \"env_cfg\", env_cfg))\n" % (self.config_name))
        fh.write("      `uvm_fatal(\"coverage\",\"env_cfg is not set\");\n")
        fh.write("\n")
        fh.write("%s" % (coverage_build)) 
        fh.write("\n")
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: connect_phase", 2)))
        fh.write("  function void connect_phase(uvm_phase phase);\n")
        fh.write("    super.connect_phase(phase);\n")
        fh.write("  endfunction: connect_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: run_phase", 2)))
        fh.write("  task run_phase(uvm_phase phase);\n")
        fh.write("\n")
        fh.write("  endtask: run_phase\n")
        fh.write("\n")
        fh.write("%s" % (function_decl)) 
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.coverage_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.coverage_name.upper()))
        fh.close()
