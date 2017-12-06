class interface:

    def __init__(self, header, agent_setting):
        self.header                    = header
        self.interface_name            = agent_setting["agent_name"] + "_if"
        self.defines_name              = agent_setting["agent_name"] + "_defines"
        self.clock                     = agent_setting["clock"]
        self.reset                     = agent_setting["reset"]

    def gen(self):
        fh = open(self.interface_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.interface_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.interface_name.upper()))
        fh.write("`define _%s_\n" % (self.interface_name.upper()))
        fh.write("\n")
        fh.write("`include \"%s.sv\"\n" % (self.defines_name))
        fh.write("\n")
        fh.write("interface %s (input logic %s, input logic %s);\n" % (self.interface_name, self.clock, self.reset))
        fh.write("\n")
        fh.write("  //Add signal here\n")
        fh.write("\n")
        fh.write("endinterface: %s\n" % (self.interface_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.interface_name.upper()))
        fh.close()


