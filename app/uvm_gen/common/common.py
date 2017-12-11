import os

def banner(message, space_num):
    ret_str = ""
    ret_str = ret_str + space_num * " " + "//--------------------------------------------------\n"
    ret_str = ret_str + space_num * " " + "//%s\n" % (message)
    ret_str = ret_str + space_num * " " + "//--------------------------------------------------\n"
    return ret_str
    
def space(num):
    ret_str = num * " "
    return ret_str
    
def create_dir(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

