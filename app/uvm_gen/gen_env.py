#Import setting
import os

from .agent import agent
from .env import virtual_sequence, virtual_sequencer, environment, environment_interface, environment_cfg, scoreboard, coverage, testbench_top
from .test import testbase, testsample
from .sim import makefile

def create_dir(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

#Create output folder structure
def gen(env_config):
    working_dir = os.getcwd()
    
    create_dir(env_config["output_folder"])
    create_dir(env_config["output_folder"] + "/model")
    
    create_dir(env_config["output_folder"] + "/env")
    os.chdir(env_config["output_folder"] + "/env")
    env_interface = environment_interface.environment_interface(env_config["header"], env_config["project_name"], env_config)
    env_interface.gen()
    
    vir_sequence = virtual_sequence.virtual_sequence(env_config["header"], env_config["project_name"])
    vir_sequence.gen()
    
    vir_sequencer = virtual_sequencer.virtual_sequencer(env_config["header"], env_config["project_name"], env_config)
    vir_sequencer.gen()
    
    env_cfg = environment_cfg.environment_cfg(env_config["header"], env_config["project_name"], env_config)
    env_cfg.gen()
    
    env_sb = scoreboard.scoreboard(env_config["header"], env_config["project_name"], env_config)
    env_sb.gen()
    
    env_cov = coverage.coverage(env_config["header"], env_config["project_name"], env_config)
    env_cov.gen()
    
    env = environment.environment(env_config["header"], env_config["project_name"], env_config)
    env.gen()
    
    tb_top = testbench_top.testbench_top(env_config["header"], env_config["project_name"], env_config)
    tb_top.gen2()
    
    os.chdir(working_dir)
    
    #Generate test
    create_dir(env_config["output_folder"] + "/tests")
    os.chdir(env_config["output_folder"] + "/tests")
    test_base = testbase.testbase(env_config["header"], env_config["project_name"])
    test_base.gen()
    test_sample = testsample.testsample(env_config["header"], env_config["project_name"])
    test_sample.gen()
    
    os.chdir(working_dir)
    
    #Generate sim/Makefile
    create_dir(env_config["output_folder"] + "/sim")
    os.chdir(env_config["output_folder"] + "/sim")
    make_file = makefile.makefile(env_config["header"], env_config["project_name"], env_config)
    make_file.gen()
    
    os.chdir(working_dir)
    
    #Generate rtl folder
    create_dir(env_config["output_folder"] + "/rtl")
    fh = open(env_config["output_folder"] + "/rtl/filelist", "w")
    fh.write("")
    fh.close()

