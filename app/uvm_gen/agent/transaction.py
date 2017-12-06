class transaction:

    def __init__(self, header, agent_setting):
        self.header                    = header
        self.transaction_name          = agent_setting.get("transaction_name",      agent_setting["agent_name"] + "_tr")
        self.clock                     = agent_setting.get("clock", "clk")
        self.reset                     = agent_setting.get("reset", "resetn")

    def gen(self):
        fh = open(self.transaction_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.transaction_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.transaction_name.upper()))
        fh.write("`define _%s_\n" % (self.transaction_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_sequence_item;\n" % (self.transaction_name))
        fh.write("\n")
        fh.write("  `uvm_object_utils_begin(%s)\n" % (self.transaction_name))
        fh.write("  `uvm_object_utils_end\n")
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: new\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function new(string name = \"%s\");\n" % (self.transaction_name))
        fh.write("    super.new(name);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: pre_randomize\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function void pre_randomize();\n")
        fh.write("  endfunction: pre_randomize\n")
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: post_randomize\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function void post_randomize();\n")
        fh.write("  endfunction: post_randomize\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.transaction_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.transaction_name.upper()))
        fh.close()


