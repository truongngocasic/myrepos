from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db
from ..models import User, Project


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Department Views


#j@admin.route('/departments', methods=['GET', 'POST'])
#j@login_required
#jdef list_departments():
#j    """
#j    List all departments
#j    """
#j    check_admin()
#j
#j    departments = Department.query.all()
#j
#j    return render_template('admin/departments/departments.html',
#j                           departments=departments, title="Departments")
#j
#j
#j@admin.route('/departments/add', methods=['GET', 'POST'])
#j@login_required
#jdef add_department():
#j    """
#j    Add a department to the database
#j    """
#j    check_admin()
#j
#j    add_department = True
#j
#j    form = DepartmentForm()
#j    if form.validate_on_submit():
#j        department = Department(name=form.name.data,
#j                                description=form.description.data)
#j        try:
#j            # add department to the database
#j            db.session.add(department)
#j            db.session.commit()
#j            flash('You have successfully added a new department.')
#j        except:
#j            # in case department name already exists
#j            flash('Error: department name already exists.')
#j
#j        # redirect to departments page
#j        return redirect(url_for('admin.list_departments'))
#j
#j    # load department template
#j    return render_template('admin/departments/department.html', action="Add",
#j                           add_department=add_department, form=form,
#j                           title="Add Department")
#j
#j
#j@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
#j@login_required
#jdef edit_department(id):
#j    """
#j    Edit a department
#j    """
#j    check_admin()
#j
#j    add_department = False
#j
#j    department = Department.query.get_or_404(id)
#j    form = DepartmentForm(obj=department)
#j    if form.validate_on_submit():
#j        department.name = form.name.data
#j        department.description = form.description.data
#j        db.session.commit()
#j        flash('You have successfully edited the department.')
#j
#j        # redirect to the departments page
#j        return redirect(url_for('admin.list_departments'))
#j
#j    form.description.data = department.description
#j    form.name.data = department.name
#j    return render_template('admin/departments/department.html', action="Edit",
#j                           add_department=add_department, form=form,
#j                           department=department, title="Edit Department")
#j
#j
#j@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
#j@login_required
#jdef delete_department(id):
#j    """
#j    Delete a department from the database
#j    """
#j    check_admin()
#j
#j    department = Department.query.get_or_404(id)
#j    db.session.delete(department)
#j    db.session.commit()
#j    flash('You have successfully deleted the department.')
#j
#j    # redirect to the departments page
#j    return redirect(url_for('admin.list_departments'))
#j
#j    return render_template(title="Delete Department")


# Users Views

@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


#@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
#@login_required
#def assign_employee(id):
#    """
#    Assign a department and a role to an employee
#    """
#    check_admin()
#
#    employee = Employee.query.get_or_404(id)
#
#    # prevent admin from being assigned a department or role
#    if employee.is_admin:
#        abort(403)
#
#    form = EmployeeAssignForm(obj=employee)
#    if form.validate_on_submit():
#        employee.department = form.department.data
#        employee.role = form.role.data
#        db.session.add(employee)
#        db.session.commit()
#        flash('You have successfully assigned a department and role.')
#
#        # redirect to the roles page
#        return redirect(url_for('admin.list_employees'))
#
#    return render_template('admin/employees/employee.html',
#                           employee=employee, form=form,
#                           title='Assign Employee')

@admin.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user from the database
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the departments page
    return redirect(url_for('admin.list_users'))

    return render_template(title="Delete User")


