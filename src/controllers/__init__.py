from controllers.admin_controller import admin
from controllers.admin_booking_controller import admin_booking
from controllers.booking_controller import booking
from controllers.dept_controller import dept
from controllers.desk_controller import desk
from controllers.user_controller import user


# Convenient to include all controllers here, once added to this list, they are automatically 
# accessible by app.py
registerable_controllers = [
    admin,
    admin_booking,
    booking,
    dept,
    desk,
    user
]