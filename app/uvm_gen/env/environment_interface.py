from ..common import common 
from ..agent import agent as import_agent

class environment_interface:

    def __init__(self, header, project_name, uvm_env):
        self.header                    = header
        self.interface_name            = project_name + "_env_if"
        self.agent_setting             = uvm_env["agent"]
        self.clock                     = uvm_env["clock"]
        self.reset                     = uvm_env["reset"]

    def gen(self):
        tb_instance_if  = ""
        for model in self.agent_setting:
            agent_name              = model["agent_name"]
            instance_name           = model["instance_name"]
            instance_num            = model["instance_num"]
            agent = import_agent.agent(self.header, agent_name, instance_name, instance_num)
            tb_instance_if  = tb_instance_if  + agent.gen_if_instance(self.clock, self.reset, 2)

        fh = open(self.interface_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.interface_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.interface_name.upper()))
        fh.write("`define _%s_\n" % (self.interface_name.upper()))
        fh.write("\n")
        fh.write("interface %s (input logic %s, input logic %s);\n" % (self.interface_name, self.clock, self.reset))
        fh.write("\n")
        fh.write("  //Reset\n")
        fh.write("  logic _reset_n;\n")
        fh.write("\n")
        fh.write("  //Error counter\n")
        fh.write("  logic _error_cnt;\n")
        fh.write("\n")
        fh.write("  //Agent interface\n")
        fh.write("%s" % (tb_instance_if))
        fh.write("\n")
        fh.write("  //Add more signals here\n")
        fh.write("\n")
        fh.write("endinterface: %s\n" % (self.interface_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.interface_name.upper()))
        fh.close()

