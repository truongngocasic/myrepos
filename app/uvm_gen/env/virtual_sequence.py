from ..common import common 

class virtual_sequence:

    def __init__(self, header, project_name):
        self.header                    = header
        self.virtual_sequence_name     = project_name + "_vir_seq"
        self.virtual_sequencer_name    = project_name + "_vir_seqr"
        self.environment_interface_name= project_name + "_env_if"
        self.environment_config_name   = project_name + "_env_cfg"

    def gen(self):
        fh = open(self.virtual_sequence_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.virtual_sequence_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.virtual_sequence_name.upper()))
        fh.write("`define _%s_\n" % (self.virtual_sequence_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_sequence;\n" % (self.virtual_sequence_name))
        fh.write("  `uvm_declare_p_sequencer(%s)\n" % (self.virtual_sequencer_name))
        fh.write("\n")
        fh.write("  virtual %-42s env_if;\n" % (self.environment_interface_name))
        fh.write("  %-50s env_cfg;\n" % (self.environment_config_name))
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\");\n" % (self.virtual_sequence_name))
        fh.write("    super.new(name);\n")
        fh.write("    //Get interface\n")
        fh.write("    if(!uvm_config_db #(virtual %s)::get(uvm_root::get(), \"\", \"env_if\", env_if))\n" % (self.environment_interface_name))
        fh.write("      `uvm_fatal(\"vir_seq\",\"env_if is not set \");\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: pre_body", 2)))
        fh.write("  task pre_body();\n")
        fh.write("    if (starting_phase!=null) begin\n")
        fh.write("      `uvm_info(get_type_name(), $psprintf(\"\\n[INFO] %s pre_body() raising %s objection\",get_sequence_path(),starting_phase.get_name()), UVM_NONE);\n")
        fh.write("      starting_phase.raise_objection(this, get_type_name());\n")
        fh.write("    end\n")
        fh.write("\n")
        fh.write("    //Get env_cfg from p_sequencer\n")
        fh.write("    env_cfg = p_sequencer.env_cfg;\n")
        fh.write("\n")
        fh.write("    //Simulation run more 5 clocks (T=40ns) after drop the objection\n")
        fh.write("    starting_phase.phase_done.set_drain_time(this, 200);\n")
        fh.write("\n")
        fh.write("  endtask: pre_body\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: body", 2)))
        fh.write("  virtual task body();\n")
        fh.write("    //Add code here\n")
        fh.write("  endtask: body\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: post_body", 2)))
        fh.write("  task post_body();\n")
        fh.write("    if (starting_phase!=null) begin\n")
        fh.write("      `uvm_info(get_type_name(), $sformatf(\"\\n[INFO] %s post_body() dropping %s objection\",get_sequence_path(),starting_phase.get_name()), UVM_NONE);\n")
        fh.write("                starting_phase.drop_objection(this, get_type_name());\n")
        fh.write("    end\n")
        fh.write("  endtask: post_body\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.virtual_sequence_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.virtual_sequence_name.upper()))
        fh.close()
