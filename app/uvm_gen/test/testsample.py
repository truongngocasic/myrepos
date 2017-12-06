from ..common import common 

class testsample:

    def __init__(self, header, project_name):
        self.header                    = header
        self.testbase_name             = project_name + "_testbase"
        self.testsample_name           = project_name + "_testsample"
        self.testlib_name              = project_name + "_testlib"
        self.virtual_sequence_name     = project_name + "_vir_seq"

    def gen(self):
        fh = open(self.testlib_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.testlib_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.testlib_name.upper()))
        fh.write("`define _%s_\n" % (self.testlib_name.upper()))
        fh.write("\n")
        fh.write("`include \"%s.sv\"\n" % (self.testbase_name))
        fh.write("`include \"%s.sv\"\n" % (self.testsample_name))
        fh.write("//Include test here\n")
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.testlib_name.upper()))
        fh.close()

        fh = open(self.testsample_name + ".sv", "w")
        fh.write(self.header.replace("file_name", self.testsample_name + ".sv"))
        fh.write("`ifndef _%s_\n" % (self.testsample_name.upper()))
        fh.write("`define _%s_\n" % (self.testsample_name.upper()))
        fh.write("\n")
        fh.write("//--------------------------------------------------\n")
        fh.write("//USER SEQUENCE\n")
        fh.write("//--------------------------------------------------\n")
        fh.write("class %s_vir_seq extends %s;\n" % (self.testsample_name, self.virtual_sequence_name))
        fh.write("  `uvm_object_utils(%s_vir_seq)\n" % (self.testsample_name))
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s_vir_seq\");\n" % (self.testsample_name))
        fh.write("    super.new(name);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("task: body", 2)))
        fh.write("  task body();\n")
        fh.write("  //Add code here\n")
        fh.write("  endtask: body\n")
        fh.write("\n")
        fh.write("endclass: %s_vir_seq\n" % (self.testsample_name))
        fh.write("\n")
        fh.write("//--------------------------------------------------\n")
        fh.write("//USER TEST\n")
        fh.write("//--------------------------------------------------\n")
        fh.write("class %s extends %s;\n" % (self.testsample_name, self.testbase_name))
        fh.write("  `uvm_component_utils(%s)\n" % (self.testsample_name))
        fh.write("\n")
        fh.write("%s" % (common.banner("function: new", 2)))
        fh.write("  function new(string name = \"%s\", uvm_component parent);\n" % (self.testsample_name))
        fh.write("    super.new(name, parent);\n")
        fh.write("  endfunction: new\n")
        fh.write("\n")
        fh.write("%s" % (common.banner("function: build_phase", 2)))
        fh.write("  function void build_phase(uvm_phase phase);\n")
        fh.write("    //Set default sequence\n")
        fh.write("    uvm_config_db #(uvm_object_wrapper)::set(this,\n")
        fh.write("      \"env.vir_seqr.run_phase\",\"default_sequence\",%s_vir_seq::type_id::get());\n" % (self.testsample_name))
        fh.write("    //Build test\n")
        fh.write("    super.build_phase(phase);\n")
        fh.write("\n")
        fh.write("  endfunction: build_phase\n")
        fh.write("\n")
        fh.write("endclass: %s\n" % (self.testsample_name))
        fh.write("\n")
        fh.write("`endif //_%s_\n" % (self.testsample_name.upper()))
        fh.close()
