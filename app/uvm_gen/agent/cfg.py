class cfg:

    def __init__(self, header, agent_setting):
        self.header            = header
        self.cfg_name          = agent_setting.get("config_name",           agent_setting["agent_name"] + "_cfg")
        self.interface_name    = agent_setting.get("interface_name",        agent_setting["agent_name"] + "_if")
        self.interface_ins     = agent_setting.get("interface_instance",    "vif")

    def gen(self):
        fh = open(self.cfg_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.cfg_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.cfg_name.upper()))
        fh.write("`define _%s_\n" % (self.cfg_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_object;\n" % (self.cfg_name))
        fh.write("  `uvm_object_utils(%s)\n" % (self.cfg_name))
        fh.write("\n")
        fh.write("  virtual %s %s;\n" % (self.interface_name, self.interface_ins))
        fh.write("\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  //function: new\n")
        fh.write("  //--------------------------------------------------\n")
        fh.write("  function new(string name = \"%s\");\n" % (self.cfg_name))
        fh.write("    super.new(name);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.cfg_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.cfg_name.upper()))
        fh.close()


