class sequencer:

    def __init__(self, header, agent_setting):
        self.header                    = header
        self.master_sequencer_name     = agent_setting.get("master_sequencer_name", agent_setting["agent_name"] + "_master_seqr")
        self.slave_sequencer_name      = agent_setting.get("slave_sequencer_name",  agent_setting["agent_name"] + "_slave_seqr")
        self.config_name               = agent_setting.get("config_name",           agent_setting["agent_name"] + "_cfg")
        self.transaction_name          = agent_setting.get("transaction_name",      agent_setting["agent_name"] + "_tr")
        self.config_ins                = agent_setting.get("config_instance",       "cfg")

    def master_sequencer_gen(self, transaction_name, config_name, config_ins, sequencer_name):
        fh = open(sequencer_name + ".sv", "w")
        fh.write(self.header.replace("file_name", sequencer_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (sequencer_name.upper()))
        fh.write("`define _%s_\n" % (sequencer_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_sequencer #(%s);\n" % (sequencer_name, transaction_name))
        fh.write("  `uvm_component_utils(%s)\n" % (sequencer_name))
        fh.write("\n")
        fh.write("  %-50s %s;\n" % (config_name, config_ins))
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: new\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (sequencer_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: build_phase\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (sequencer_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (sequencer_name.upper()))
        fh.close()

    def slave_sequencer_gen(self, transaction_name, config_name, config_ins, sequencer_name):
        fh = open(sequencer_name + ".sv", "w")
        fh.write(self.header.replace("file_name", sequencer_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (sequencer_name.upper()))
        fh.write("`define _%s_\n" % (sequencer_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_sequencer #(%s);\n" % (sequencer_name, transaction_name))
        fh.write("  `uvm_component_utils(%s)\n" % (sequencer_name))
        fh.write("\n")
        fh.write("  %-50s %s;\n" % (config_name, config_ins))
        fh.write("  %-50s peek_port;\n" % ("uvm_blocking_peek_port #(" + transaction_name + ")"))
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: new\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (sequencer_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: build_phase\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("    peek_port = new(\"peek_port\", this);\n")
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (sequencer_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (sequencer_name.upper()))
        fh.close()

    def sequencer_gen(self):
        self.master_sequencer_gen(self.transaction_name, self.config_name, self.config_ins, self.master_sequencer_name)
        self.slave_sequencer_gen(self.transaction_name, self.config_name, self.config_ins, self.slave_sequencer_name)
