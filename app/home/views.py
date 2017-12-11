from flask import abort, render_template, request, send_file, flash
from flask_login import current_user, login_required

from . import home
import shutil
import uuid
import os
import json
import sys
from ..models import User, Project
from .. import db
from ..uvm_gen import gen_env

basedir = os.path.abspath(os.path.dirname(__file__))

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/generator', methods=['GET', 'POST'])
@login_required
def generator():
    """
    Render the env_gen template on the /envgen route
    """
    #For history project
    projects = Project.query.filter_by(user=current_user)[:10]
    return render_template('home/generator.html', title="Environment Generator", projects=projects)

@home.route('/load_project/<int:id>', methods=['GET', 'POST'])
@login_required
def load_project(id):
    """
    Return project config
    """
    #Load project
    ld_prj = Project.query.get_or_404(id)
    if (ld_prj.user != current_user):
        abort(404)

    #return prj.env_cfg
    return json.dumps({"project_name":ld_prj.name, "header":ld_prj.header, "agent":ld_prj.env_cfg})

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/generate', methods=['POST'])
@login_required
def env_gen():
    """
    Generate environment
    """
    working_dir = os.getcwd()
    json_result = request.get_json()
    uvm_env = { "output_folder" : "", "project_name" : "", "header" : "", "clock" : "clk", "reset" : "resetn", "testbench" : "testbench_top", "agent" : [] }
    uvm_env["project_name"]  = json_result["project_name"]
    uvm_env["header"]        = json_result["header"]
    uuid_val = str(uuid.uuid4())
    uvm_env_name = uvm_env["project_name"] + "_" + uuid_val
    uvm_env["output_folder"] = uvm_env_name
    for key, value in json_result["agent"].iteritems():
        value["instance_num"] = int(value["instance_num"])
        uvm_env["agent"].append(value)
    
    os.chdir(basedir + "/../output") 
    gen_env.gen(uvm_env)
    shutil.make_archive(uvm_env_name, 'zip', uvm_env_name)
    os.chdir(working_dir) 
    #Store project
    prj = Project.query.filter_by(name=json_result["project_name"]).first()
    if prj is not None:
        if prj.user.username == current_user.username:
            #Same user
            prj.env_cfg = json.dumps(json_result["agent"])
            prj.header  = json_result["header"]
        else:
            #Different user
            prj = Project(name=json_result["project_name"], env_cfg=json.dumps(json_result["agent"]), header=json_result["header"], user=current_user)
    else:
        prj = Project(name=json_result["project_name"], env_cfg=json.dumps(json_result["agent"]), header=json_result["header"], user=current_user)

    db.session.add(prj)
    db.session.commit()

    return uvm_env_name

@home.route('/download/<file_name>')
@login_required
def download(file_name):
    """
    Download environment
    """
    try:
        return send_file(basedir + '/../output/' + file_name + ".zip", mimetype="application/zip", as_attachment=True, attachment_filename=file_name + ".zip")
    except Exception as e:
        return str(e)

