# T2_A2-API_Server

## R1
Many companies now offer flexible and hybrid working arrangements, which allows their employees to work from locations other than their designated office. Since workplaces have transitioned to a hybrid model, many have re-organised their offices so that employees do not have designated desks to allow for more flexibility. The downside of this is that there can be times when the office is busier than usual and there aren't enough desks for everybody there. If someone comes to the office, hoping there will be a desk available, time can be wasted while they try to find a desk and they may even have to go home and work remotely.

Other problems that can occur as a result of the hybrid model are that companies may find their office space is being under-utilised. This could prompt them to divert funds elsewhere if the expense of paying for office space, including furniture, utility bills, equipment etc is deemed unneccesary. There are some business however, that are unable to move to a fully remote operation (e.g. manufacturing, health care etc). These businesses may want visibility of how much the office is being utilised and/or whether employees are coming into the office in accordance with their policy.

## R2
I have chosen to create an app which companies can use to provide their staff with a method to view and book available desks so that their team members know before coming to the office that they have a desk to use. A tool that allows employees to log into a website and book their desk for the day (or discover that there are none available which would allow them make other arrangements) would be beneficial to a lot of companies and their employees. By solving this problem, time will be saved, which will increase productivity and companies can adapt their resources according to the needs of their business. This has the possibility of reducing expenses and improving the bottom line profit.

## R3
Database benefits


## R4
ORM benefits (Marshmallow)

## R5 - GO THROUGH DELETE AND EXPLAIN CASCADE

### 1. /admin
- Description: Allows an admin to create and add a user to the database
- HTTP Request Verb: POST
- Required Data: employee id, first name, last name, email, password [between 8 and 14 characters], department
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created user (excluding password & is_admin) and a JWT (JSON Web Token)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

### 2. /admin/\<string:employee_id>
- Description: Allows an admin to update a user's details (i.e. name, email address, password, department, admin status)
- HTTP Request Verb: PUT/PATCH
- Required Data: at least one of employee id, first name, last name, email, password, department
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated user (excluding password & is_admin)
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
- Expected Response: HTTP response status 200 - OK, JSON object showing all registered users, including their bookings, excluding passwords and admin status
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status


### 5. /user/\<string:employee_id>
- Description: Allows a user to see their information
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
- Expected Response: HTTP response status 200 - OK, JSON object showing all departments (id, name)
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
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated department (id, name)
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
- Required Data: week_id , weekday [mon, tue, wed, thu, fri], desk_id
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

## R6
ERD
[ERD](ERD_ver1.png)



## R7
Third party services

## R8
Models (Alchemy) - foreign keys/back populate/nested fields etc

## R9
Related to the database itself (SQL)

## R10
Project planning 