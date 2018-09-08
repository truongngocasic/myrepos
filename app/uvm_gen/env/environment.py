from ..common import common 

class environment:

    def __init__(self, header, project_name, uvm_env):
        self.header                    = header
        self.environment_name          = project_name + "_env"
        self.virtual_sequencer_name    = project_name + "_vir_seqr"
        self.scoreboard_name           = project_name + "_env_sb"
        self.coverage_name             = project_name + "_env_cov"
        self.config_name               = project_name + "_env_cfg"
        self.interface_name            = project_name + "_env_if"
        self.agent_setting             = uvm_env["agent"]
        self.reset                     = uvm_env["reset"]

    def gen(self):
        environment_declare = ""
        environment_build   = ""
        environment_connect = ""
        
        environment_declare = environment_declare + "  //Environment interface\n"
        environment_declare = environment_declare + "  virtual %-42s env_if;\n\n" % (self.interface_name)
        environment_declare = environment_declare + "  //Environment config\n"
        environment_declare = environment_declare + "  %-50s env_cfg;\n\n" % (self.config_name)
        environment_declare = environment_declare + "  //Environment scoreboard\n"
        environment_declare = environment_declare + "  %-50s env_sb;\n\n" % (self.scoreboard_name)
        environment_declare = environment_declare + "  //Environment coverage\n"
        environment_declare = environment_declare + "  %-50s env_cov;\n\n" % (self.coverage_name)
        environment_declare = environment_declare + "  //Virtual sequencer\n"
        environment_declare = environment_declare + "  %-50s vir_seqr;\n\n" % (self.virtual_sequencer_name)
        environment_declare = environment_declare + "  //Agents\n"
        #environment_build   = environment_build   + "    env_cfg = new();\n"
        environment_build   = environment_build   + "    env_sb = %s::type_id::create(\"env_sb\", this);\n" % (self.scoreboard_name)
        environment_build   = environment_build   + "    env_cov = %s::type_id::create(\"env_cov\", this);\n" % (self.coverage_name)
        environment_build   = environment_build   + "    vir_seqr = %s::type_id::create(\"vir_seqr\", this);\n" % (self.virtual_sequencer_name)

        for agent in self.agent_setting:
            agent_type                    = agent["agent_type"]
            if (agent_type == "Master"):
                agent_name                = agent["agent_name"] + "_master_agent"
            if (agent_type == "Slave"):
                agent_name                = agent["agent_name"] + "_slave_agent"

            instance_name                 = agent["instance_name"]
            instance_num                  = agent["instance_num"]
            if (agent["agent_active"] == "Active"):
                is_active                 = "UVM_ACTIVE"
            else:
                is_active                 = "UVM_PASSIVE"

            if (instance_num > 1):
                environment_declare = environment_declare + "  %-50s %s[%0d];\n" % (agent_name, instance_name, instance_num)
                environment_build   = environment_build   + "    for (int i=0; i<%0d; i++) begin\n" % (instance_num);
                environment_build   = environment_build   + "      %s[i] = %s::type_id::create($psprintf(\"%s\", i), this);\n" % (instance_name, agent_name, instance_name + "[%0d]")
                environment_build   = environment_build   + "      %s[i].is_active  = %s;\n" % (instance_name, is_active)
                environment_build   = environment_build   + "      %s[i].cfg = env_cfg.%s[i];\n" % (instance_name, instance_name + "_cfg")
                environment_build   = environment_build   + "    end\n"
                environment_connect = environment_connect + "    for (int i=0; i<%0d; i++) begin\n" % (instance_num);
                environment_connect = environment_connect + "      vir_seqr.%s[i] = %s[i].seqr;\n" % (instance_name + "_seqr", instance_name)
                environment_connect = environment_connect + "    end\n"
                ii = 0
                while (ii < instance_num):
                    scoreboard_port_name = "%s%d_exp" % (instance_name, ii)
                    coverage_port_name   = "%s%d_exp" % (instance_name, ii)
                    environment_connect  = environment_connect + "    %s[%d].monitor_ap.connect(env_sb.%s);\n" % (instance_name, ii, scoreboard_port_name)
                    environment_connect  = environment_connect + "    %s[%d].monitor_ap.connect(env_cov.%s);\n" % (instance_name, ii, coverage_port_name)
                    ii = ii + 1
            else:
                environment_declare  = environment_declare + "  %-50s %s;\n" % (agent_name, instance_name)
                environment_build    = environment_build   + "    %s = %s::type_id::create(\"%s\", this);\n" % (instance_name, agent_name, instance_name)
                environment_build    = environment_build   + "    %s.is_active  = %s;\n" % (instance_name, is_active)
                environment_build    = environment_build   + "    %s.cfg = env_cfg.%s;\n" % (instance_name, instance_name + "_cfg")
                scoreboard_port_name = "%s_exp" % (instance_name)
                coverage_port_name   = "%s_exp" % (instance_name)
                environment_connect  = environment_connect + "    vir_seqr.%s = %s.seqr;\n" % (instance_name + "_seqr", instance_name)
                environment_connect  = environment_connect + "    %s.monitor_ap.connect(env_sb.%s);\n" % (instance_name, scoreboard_port_name)
                environment_connect  = environment_connect + "    %s.monitor_ap.connect(env_cov.%s);\n" % (instance_name, coverage_port_name)

        fh = open(self.environment_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.environment_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.environment_name.upper()))
        fh.write("`define _%s_\n" % (self.environment_name.upper()))
        fh.write("\n")
        fh.write("class %s extends uvm_env;\n" % (self.environment_name))
        fh.write("  `uvm_component_utils(%s)\n" % (self.environment_name))
        fh.write("\n")
        fh.write("%s" % (environment_declare)) 
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (self.environment_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: build_phase", 2)))
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("    //Get interface\n")
        fh.write("    if(!uvm_config_db #(virtual %s)::get(this, \"\", \"env_if\", env_if))\n" % (self.interface_name))
        fh.write("      `uvm_fatal(\"NOVIF\",{\"virtual interface must be set for: \", get_full_name(),\".env_if\"});\n")
        fh.write("\n")
        fh.write("    //Get env_cfg\n")
        fh.write("    if(!uvm_config_db #(%s)::get(this, \"\", \"env_cfg\", env_cfg))\n" % (self.config_name))
        fh.write("      `uvm_fatal(\"env\",\"env_cfg is not set\");\n")
        fh.write("\n")
        fh.write("%s" % (environment_build)) 
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: connect_phase", 2)))
        fh.write("  function void connect_phase(uvm_phase phase);\n")
        fh.write("    super.connect_phase(phase);\n")
        fh.write("%s" % (environment_connect)) 
        fh.write("  endfunction: connect_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: run_phase", 2)))
        fh.write("  task run_phase(uvm_phase phase);\n")
        fh.write("  endtask: run_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: main_phase", 2)))
        fh.write("  task main_phase(uvm_phase phase);\n")
        fh.write("  endtask: main_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: configure_phase", 2)))
        fh.write("  task configure_phase(uvm_phase phase);\n")
        fh.write("  endtask: configure_phase\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: reset_phase", 2)))
        fh.write("  task reset_phase(uvm_phase phase);\n")
        fh.write("    phase.raise_objection(this);\n")
        fh.write("    env_if._reset_n <= 1'b0;\n")
        fh.write("    #($urandom_range(10,500));   //Async reset\n")
        fh.write("    env_if._reset_n <= 1'b1;\n")
        fh.write("    #($urandom_range(10,50));    //Delay to start driving traffic\n")
        fh.write("    phase.drop_objection(this);\n")
        fh.write("  endtask: reset_phase\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.environment_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.environment_name.upper()))
        fh.close()
