from ..common import common 

class virtual_sequencer:

    def __init__(self, header, project_name, uvm_env):
        self.header                    = header
        self.virtual_sequencer_name    = project_name + "_vir_seqr"
        self.agent_setting             = uvm_env["agent"]
        self.environment_config_name   = project_name + "_env_cfg"

    def gen(self):
        sequencer_declare = "  %-50s env_cfg;\n\n" % (self.environment_config_name)
        for agent in self.agent_setting:
            instance_num = agent["instance_num"]
            if (instance_num > 1):
              sequencer_declare = sequencer_declare + "  %-50s %s[%0d];\n" % ("uvm_sequencer #(" + agent["agent_name"] + "_tr)", agent["instance_name"] + "_seqr", instance_num)
            else:
              sequencer_declare = sequencer_declare + "  %-50s %s;\n" % ("uvm_sequencer #(" + agent["agent_name"] + "_tr)", agent["instance_name"] + "_seqr")

        fh = open(self.virtual_sequencer_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.virtual_sequencer_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.virtual_sequencer_name.upper()))
        fh.write("`define _%s_\n" % (self.virtual_sequencer_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_sequencer;\n" % (self.virtual_sequencer_name))
        fh.write("  `uvm_component_utils(%s)\n" % (self.virtual_sequencer_name))
        fh.write("\n")
        fh.write(sequencer_declare)
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (self.virtual_sequencer_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: build_phase", 2)))
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("\n")
        fh.write("    //Get env_cfg\n")
        fh.write("    if(!uvm_config_db #(%s)::get(this, \"\", \"env_cfg\", env_cfg))\n" % (self.environment_config_name))
        fh.write("      `uvm_fatal(\"vir_seqr\",\"env_cfg is not set\");\n")
        fh.write("\n")
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.virtual_sequencer_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.virtual_sequencer_name.upper()))
        fh.close()
