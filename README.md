# T2_A2-API_Server

## R1 Identification of the problem you are trying to solve by building this particular app

Many companies now offer flexible and hybrid working arrangements, which allows their employees to work from locations other than their designated office. Since workplaces have transitioned to a hybrid model, many have re-organised their offices so that employees do not have designated desks to allow for more flexibility. The downside of this is that there can be times when the office is busier than usual and there aren't enough desks for everybody there. If someone comes to the office, hoping there will be a desk available, time can be wasted while they try to find a desk and they may even have to go home and work remotely.

Other problems that can occur as a result of the hybrid model are that companies may find their office space is being under-utilised. This could prompt them to divert funds elsewhere if the expense of paying for office space, including furniture, utility bills, equipment etc is deemed unneccesary. There are some business however, that are unable to move to a fully remote operation (e.g. manufacturing, health care etc). These businesses may want visibility of how much the office is being utilised and/or whether employees are coming into the office in accordance with their policy.

## R2 Why is it a problem that needs solving?

I have chosen to create an app which companies can use to provide their staff with a method to view and book available desks so that their team members know before coming to the office that they have a desk to use. A tool that allows employees to log into a website and book their desk for the day (or discover that there are none available which would allow them make other arrangements) would be beneficial to a lot of companies and their employees. By solving this problem, time will be saved, which will increase productivity and companies can adapt their resources according to the needs of their business. This has the possibility of reducing expenses and improving the bottom line profit.

## R3 Why have you chosen this database system. What are the drawbacks compared to others?
Database benefits


## R4 Identify and discuss the key functionalities and benefits of an ORM
ORM benefits (Marshmallow)

## R5 Document all endpoints for your API

### 1. /admin
- Description: Allows an admin to create and add a user to the database
- HTTP Request Verb: POST
- Required Data: employee id, first name, last name, email, password [between 8 and 14 characters], department
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created user (excluding password) and a JWT (JSON Web Token)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 2. /admin/\<string:employee_id>
- Description: Allows an admin to update a user's details (i.e. name, email address, password, department, admin status)
- HTTP Request Verb: PUT/PATCH
- Required Data: at least one of employee id, first name, last name, email, password, department
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated user (excluding password)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Updates to user cascade to any bookings associated with them


### 3. /admin/\<string:employee_id>
- Description: Allows an admin to delete a user
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Deleting a user cascades to any booking with which the user is associated

### /admin - missing routes:
- GET: There is no route via admin to view users - this route is available via user/employee_id 

### 4. /user
- Description: Allows admin to view all users registered in database
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing all registered users, including their bookings, excluding passwords
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status


### 5. /user/\<string:employee_id>
- Description: Allows a user to see information about themselves (but not other users)
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing the user, including their bookings, excluding password and admin status
- Authentication Methods: Valid JWT with an admin's or user's credentials encoded, `authorise()` method checks the user is an admin or the user id being accessed matches the token's identity

### 6. /user
- Description: Allows a user to login
- HTTP Request Verb: POST
- Required Data: employee id, password
- Expected Response: HTTP response status 200 - OK, JSON object showing the user, including their bookings, excluding password and admin status
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 7. /user/\<string:employee_id>
- Description: Allows user to change their password
- HTTP Request Verb: PUT/PATCH
- Required Data: new password [must be between 8 and 14 characters]
- Expected Response: HTTP response status 200 - OK, JSON object showing the user, including their bookings, excluding password and admin status
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### /user - missing routes:
- DELETE: There is no route which allows users to delete users - this function is available to admins via the admin route

### 8. /dept
- Description: Allows admin to view all departments
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing all departments (id, name, users in each dept)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status


### 9. /dept
- Description: Allows admin to create new department
- HTTP Request Verb: POST
- Required Data: department name
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created department (id, name)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 10. /dept/\<int:dept_id>
- Description: Allows admin to edit department name
- HTTP Request Verb: PUT/PATCH
- Required Data: department name
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated department (id, name, users in dept)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Updating a department name cascades to any users belonging to that department

### 11. /dept/\<int:dept_id>
- Description: Allows admin to delete department
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
Note: Any user belonging to a department which has been deleted means their dept_id is set to `null`

### 12. /desk
- Description: Allows admin to view all desks
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing all desks (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 13. /desk/\<int:desk_id>
- Description: Allows admin to view a desk
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing an individual desk (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 14. /desk
- Description: Allows admin to create new desk
- HTTP Request Verb: POST
- Required Data: desk id, status [optional]
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created desk (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 15. /desk/\<int:desk_id>
- Description: Allows admin to edit desk
- HTTP Request Verb: PUT/PATCH
- Required Data: at least one of desk id, availability status
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated desk (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: If the desk_id or availability status is updated, this update cascades to any boookings associated with it

### 16. /desk/\<int:desk_id>
- Description: Allows admin to delete desk (desks which have bookings cannot be deleted)
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Desks cannot be deleted if there are bookings associated, therefore there is no `ondelete` constraint for desk_id foreign keys

### 17. /user/\<string:employee_id>/booking
- Description: Allows user to view their bookings
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of their bookings (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 18. /user/\<string:employee_id>/booking/\<int:booking_id>
- Description: Allows user to view an individual booking
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of the booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 19. /user/\<string:employee_id>/booking
- Description: Allows user to create a new booking (the system prevents duplicate bookings for the same day/desk)
- HTTP Request Verb: POST
- Required Data: week_id [week number], weekday [mon, tue, wed, thu, fri], desk_id
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the booking(booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 20. /user/\<string:employee_id>/booking/\<int:booking_id>
- Description: Allows user to edit their booking, ie. change the desk and/or week and/or day associated with the booking (fails if the chosen desk/day is unavailable)
- HTTP Request Verb: PUT PATCH
- Required Data: At least one of desk_id, week_id, weekday
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 21. /user/\<string:employee_id>/booking/\<int:booking_id>
- Description: Allows user to delete a booking
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 22. /user/\<string:employee_id>/booking
- Description: Allows user to delete all their bookings
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.
- Note: while delete all is usually not recommended, it's provided here as an option in case a user realises they have made many bookings incorrectly, or perhaps they are away for a period of leave and want to delete their bookings

### 23. /booking
- Description: Allows admin to view all bookings
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of all bookings (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 24. /booking/\<int:booking_id>
- Description: Allows admin to view an individual booking
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of the booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

### 25. /booking/\<int:booking_id>
- Description: Allows admin to edit a booking (fails if the new day/desk is unavailable)
- HTTP Request Verb: PUT PATCH
- Required Data: At least one of employee id, desk_id, week_id, weekday
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 26. /booking/\<int:booking_id>
- Description: Allows admin to delete a booking
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 26. /booking
- Description: Allows admin to delete all bookings
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: while delete all is usually not recommended, this route has been provided in case of some catastrophic event and provides a method for an admin to delete all bookings, rather than having to do this one by one

### /booking - missing routes:
- POST: there is no route to allow admins to create bookings as this should be done by users. If there was an occurance that required an admin to create a booking, they would have to do so via the user route

## R6 Entity Relationship Diagram

[ERD](ERD_ver3.png)



## R7 Detail any third party services that your app will use
Third party services

### POSTGRESQL
### SQL ALCHEMY
### FLASK
### MARSHMALLOW
### BCRYPT
### JWT
### PSYCOPG2

## R8 - Describe your project's models in terms of the relationships they have with each other

### User Model

The user model contains information about the user and connects to the department model via the foreign key `dept_id`. A user has a one-to-one relationship with department (i.e. a user can belong to only one department). The foreign key constraints: `onupdate="cascade"` and `ondelete="set null"` mean that users will be updated if their department name changes, but if the department itself is deleted, the user will still exist but with `null` as their department. There are relationships established using SQLAlchemy's `relationship()` method together with its `back_populates` argument. In the first instance, this is so that user information is populated within department - note if a user is deleted their entry will be deleted from the department. Secondly, user information is populated within the booking model and allows user data to be viewed within a booking. The `cascade="all, delete"` argument ensures that if a user is deleted, all of their bookings are deleted.


The user model contains multiple schemas, with varying requirements. `UserSchema` has no required fields but it does require any password that is entered to be between 8 and 14 characters long. The `CreateUserSchema` is called when a new user is being created and has several stipulations, as well as the password length criteria; it requires a new user in the system to have a first and last name, a properly formatted email and a department. SQLAlchemy's `fields.Nested` argument is called for department and bookings to allow Marshmallow to access the relevant Schemas and display the associated data within the user model. There is one further schema: `UserSchemaPassword`. This allows users to change their password; it enforces that a password (but nothing else) must be entered.

### Department Model

The department model has a one-to-many relationship with the user model, since one department can have many users. No foreign keys are required here, since the user model has the foreign key. The `relationship()` method is used so that department data `back_populates` the department field within user. `fields.Nested()` is used by the `DeptSchema`` to allow specified information about the users to be shown within each department to which they belomg.

### Desk Model

The desk model has a one-to-many relationship with the booking model, since one desk can be associated with many bookings. The desk model has no foreign keys as the booking side of the relationship takes care of that. However desk does employ the use of the `relationship()` method and `back_populates` the desk information within booking. To allow booking information to be shown within desks when a desk is displayed, `fields.Nested()` is called within `DeskSchema`.

### Booking Model

The booking model is the most integral of the models as it joins together users and bookings. A booking has a many-to-one relationship with users (users can have many bookings but each booking belongs to just one user) and a many-to-one relationship with desks (desks can belong to many bookings but each booking relates to just one desk). The booking model has foreign keys `user_id` and `desk_id` to establish exactly which user and desk are associated with the booking. The booking model also utilises SQLAlchemy's `relationship()` method so that the booking model `back_populates` the bookings field within both the user model and desk model. In both cases `onupdate="cascade"` is used - therefore if anything changes with the user or desk, the changes are reflected in the booking. `ondelete="cascade"` only applies to user though - if a user is deleted, the booking is deleted. Desk does not have this stipulation, since the controller has some functionality which does not allow desks to be deleted if there are bookings attached to it.

Defined within the booking model is a `get_booking_ref()` method, which is a simple concatenation of `desk_id`, `week_id`, `weekday`. This method is called by the booking controller when bookings are being created or amended to prevent double bookings since the desk, week, day must be unique amongst bookings, a request where all three match an existing booking will cause a 400 - Bad Request response.

The `BookingSchema` uses `fields.Nested()` to allow desk and user information to be shown with bookings. There is also validation on the `weekday` variable to ensure only valid days are accepted.



## R9 - Discuss the database relations to be implemented in your application

The database is called `desk_easy_db`. Within the database are four tables: users, departments, desks, bookings with each table relating to at least one other table.

The user table contains information strictly related to the user. The columns are `id, employee_id, f_name, l_name, email, password, is_admin, dept_id`. `id` is an auto-incremented id used only by the database. `employee_id` is the employer's reference number for the employee and the designated means of identifying a user within the application (e.g. when logging in). The users table is related to the departments table via the foreign key `dept_id`. Therefore the users table has visibility of the department to which each user belongs.

The departments table shows all of the company's available departments. There are two columns: `id, name`. Since this is a one-to-many relationship, where a department can have many employees, the users field acts as a join, enabling visibility of which users belong to which  departments.

The desks table shows information about desks which users can book. There are two columns: `id, available`. `id` accepts String values and would be provided by the particular company, but for this example the format is floor number, area, desk number, e.g. 2A-03 or level 2, zone A, desk 3. `available` accepts Boolean values and acts as a flag. There may be a reason for one or more desks to be "unavailable" (e.g. conference, maintenance, damage), so this variable allows admins to change the status and therefore prevent desks from being booked. There is a one-to-many relationship between desks and bookings, since one desk can have many bookings, therefore the bookings field acts as a join between the two tables. This means within the desks table, each desk has visibility of bookings with which it is associated.

The bookings table provides all necessary information about a booking via the following columns: `id, week_id, weekday, desk_id, user_id, date_created`. `id` is auto-incremented and is the designated means of identiying a booking. `date_created` is automatically generated using Python's datetime package. `week_id` is an Integer value representing the week number and `weekday` is a String value identifying the day of the week for which the booking has been made. The bookings table has a one-to-one relationship with both the desks and users tables, since each booking has just one desk and one user. This relationship is established using foreign keys and allows the bookings table to display the user and desk to which it is associated.

Setting up the database tables in this way means there is no overlap of information as each table has ownership for only what it needs and links to related tables to access any associated information. 


## R10 Describe the way tasks are allocated and tracked in your project
Project planning 