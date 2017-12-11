class defines:

    def __init__(self, header, agent_setting):
        self.header            = header
        self.defines_name      = agent_setting["agent_name"] + "_defines"

    def gen(self):
        fh = open(self.defines_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.defines_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.defines_name.upper()))
        fh.write("`define _%s_\n" % (self.defines_name.upper()))
        fh.write("\n")
        fh.write("  //Add definitions\n")
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.defines_name.upper()))
        fh.close()


