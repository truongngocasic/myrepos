from ..common import common 

class environment_cfg:

    def __init__(self, header, project_name, uvm_env):
        self.header            = header
        self.agent_setting     = uvm_env["agent"]
        self.cfg_name          = project_name + "_env_cfg"

    def gen(self):
        cfg_declare = "  //Simulation timeout\n  time test_time_out=50000000;\n\n"
        cfg_build = ""

        cfg_declare = cfg_declare + "  //Agent config\n";
        for agent in self.agent_setting:
            agent_name          = agent["agent_name"]
            instance_name       = agent["instance_name"]
            instance_num        = agent["instance_num"]

            if (instance_num > 1):
                cfg_declare = cfg_declare + "  %-50s %s[%0d];\n" % (agent_name + "_cfg", instance_name + "_cfg", instance_num)
                cfg_build   = cfg_build   + "    for (int i=0; i<%0d; i++) begin\n" % (instance_num);
                cfg_build   = cfg_build   + "      %s[i] = new();\n" % (instance_name + "_cfg") 
                cfg_build   = cfg_build   + "    end\n"
            else:
                cfg_declare = cfg_declare + "  %-50s %s;\n" % (agent_name + "_cfg", instance_name + "_cfg")
                cfg_build   = cfg_build   + "    %s = new();\n" % (instance_name + "_cfg") 

        fh = open(self.cfg_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.cfg_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.cfg_name.upper()))
        fh.write("`define _%s_\n" % (self.cfg_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_object;\n" % (self.cfg_name))
        fh.write("\n")
        fh.write("%s" % (cfg_declare))
        fh.write("\n")
        fh.write("  `uvm_object_utils_begin(%s)\n" % (self.cfg_name))
        fh.write("    `uvm_field_int(test_time_out, UVM_ALL_ON)\n")
        fh.write("  `uvm_object_utils_end\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\");\n" % (self.cfg_name))
        fh.write("    super.new(name);\n")
        fh.write("%s" % (cfg_build))
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.cfg_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.cfg_name.upper()))
        fh.close()


