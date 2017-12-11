class interface:

    def __init__(self, header, interface_name, clock, reset):
        self.header                    = header
        self.interface_name            = interface_name
        self.clock                     = clock
        self.reset                     = reset

    def gen(self):
        fh = open(self.interface_name + ".sv", "w")
        fh.write(self.header)
        fh.write("`ifndef _%s_\n" % (self.interface_name.upper()))
        fh.write("`define _%s_\n" % (self.interface_name.upper()))
        fh.write("\n")
        fh.write("interface %s (input logic %s, input logic %s);\n" % (self.interface_name, self.clock, self.reset))
        fh.write("\n")
        fh.write("  //Add signal here\n")
        fh.write("\n")
        fh.write("endinterface: %s\n" % (self.interface_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.interface_name.upper()))
        fh.close()


