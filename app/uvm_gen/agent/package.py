import defines
import interface
import cfg
import transaction
import sequencer
import sequence
import driver
import monitor
import callback
import agent

class package:

    def __init__(self, header, agent_setting):
        self.header                    = header
        self.agent_setting             = agent_setting
        self.package_name              = agent_setting["agent_name"] + "_pkg"
        self.defines_name              = agent_setting["agent_name"] + "_defines"
        self.master_agent_name         = agent_setting.get("master_agent_name",     agent_setting["agent_name"] + "_master_agent")
        self.master_driver_name        = agent_setting.get("master_driver_name",    agent_setting["agent_name"] + "_master_drv")
        self.master_sequencer_name     = agent_setting.get("master_sequencer_name", agent_setting["agent_name"] + "_master_seqr")
        self.master_sequence_name      = agent_setting.get("master_sequence_name",  agent_setting["agent_name"] + "_master_seq")
        self.slave_agent_name          = agent_setting.get("slave_agent_name",      agent_setting["agent_name"] + "_slave_agent")
        self.slave_driver_name         = agent_setting.get("slave_driver_name",     agent_setting["agent_name"] + "_slave_drv")
        self.slave_sequencer_name      = agent_setting.get("slave_sequencer_name",  agent_setting["agent_name"] + "_slave_seqr")
        self.slave_sequence_name       = agent_setting.get("slave_sequence_name",   agent_setting["agent_name"] + "_slave_seq")
        self.monitor_name              = agent_setting.get("monitor_name",          agent_setting["agent_name"] + "_mon")
        self.callback_name             = agent_setting.get("callback_name",         agent_setting["agent_name"] + "_mon_callback")
        self.cov_callback_name         = agent_setting.get("cov_callback_name",     agent_setting["agent_name"] + "_mon_cov_callback")
        self.config_name               = agent_setting.get("config_name",           agent_setting["agent_name"] + "_cfg")
        self.transaction_name          = agent_setting.get("transaction_name",      agent_setting["agent_name"] + "_tr")

    def gen(self):
        fh = open(self.package_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.package_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.package_name.upper()))
        fh.write("`define _%s_\n" % (self.package_name.upper()))
        fh.write("\n")
        fh.write("package %s;\n" % (self.package_name))
        fh.write("  import uvm_pkg::*;\n")
        fh.write("\n")
        fh.write("  `include \"%s.sv\"\n" % (self.defines_name))
        fh.write("  `include \"%s.sv\"\n" % (self.config_name))
        fh.write("  `include \"%s.sv\"\n" % (self.transaction_name))
        fh.write("  `include \"%s.sv\"\n" % (self.config_name))
        fh.write("  `include \"%s.sv\"\n" % (self.callback_name))
        fh.write("  `include \"%s.sv\"\n" % (self.cov_callback_name))
        fh.write("  `include \"%s.sv\"\n" % (self.master_driver_name))
        fh.write("  `include \"%s.sv\"\n" % (self.master_sequencer_name))
        fh.write("  `include \"%s.sv\"\n" % (self.master_sequence_name))
        fh.write("  `include \"%s.sv\"\n" % (self.slave_driver_name))
        fh.write("  `include \"%s.sv\"\n" % (self.slave_sequencer_name))
        fh.write("  `include \"%s.sv\"\n" % (self.slave_sequence_name))
        fh.write("  `include \"%s.sv\"\n" % (self.monitor_name))
        fh.write("  `include \"%s.sv\"\n" % (self.master_agent_name))
        fh.write("  `include \"%s.sv\"\n" % (self.slave_agent_name))
        fh.write("\n")
        fh.write("endpackage: %s\n" % (self.package_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.package_name.upper()))
        fh.close()

        #Generate agent components
        agent_defines = defines.defines(self.header, self.agent_setting)
        agent_defines.gen()
        
        agent_interface = interface.interface(self.header, self.agent_setting)
        agent_interface.gen()
        
        agent_cfg = cfg.cfg(self.header, self.agent_setting)
        agent_cfg.gen()
        
        agent_transaction = transaction.transaction(self.header, self.agent_setting)
        agent_transaction.gen()

        agent_sequencer = sequencer.sequencer(self.header, self.agent_setting)
        agent_sequencer.sequencer_gen()
        
        agent_sequence = sequence.sequence(self.header, self.agent_setting)
        agent_sequence.sequence_gen()
        
        agent_drv = driver.driver(self.header, self.agent_setting)
        agent_drv.master_driver_gen()
        agent_drv.slave_driver_gen()
        
        agent_mon = monitor.monitor(self.header, self.agent_setting)
        agent_mon.monitor_gen()
        
        agent_callback = callback.callback(self.header, self.agent_setting)
        agent_callback.callback_gen()
        agent_callback.cov_callback_gen()
        
        agent_agent = agent.agent(self.header, self.agent_setting)
        agent_agent.agent_gen()
    


