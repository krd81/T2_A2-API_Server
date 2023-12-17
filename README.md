# T2_A2-API_Server

---
## Contents
 [R1 Identification of the problem you are trying to solve by building this particular app](#r1-identification-of-the-problem-you-are-trying-to-solve-by-building-this-particular-app)


[R2 Why is it a problem that needs solving?](#r2-why-is-it-a-problem-that-needs-solving-1)


[R3 Why have you chosen this database system. What are the drawbacks compared to others?](#r3-why-have-you-chosen-this-database-system-what-are-the-drawbacks-compared-to-others)


[R4 Identify and discuss the key functionalities and benefits of an ORM](#r4---identify-and-discuss-the-key-functionalities-and-benefits-of-an-orm)


[R5 Document all endpoints for your API](#r5---document-all-endpoints-for-your-api)


[R6 Entity Relationship Diagram](#r6---entity-relationship-diagram)


[R7 Detail any third party services that your app will use](#r7---detail-any-third-party-services-that-your-app-will-use)


[R8 Describe your project's models in terms of the relationships they have with each other](#r8---describe-your-projects-models-in-terms-of-the-relationships-they-have-with-each-other)


[R9 Discuss the database relations to be implemented in your application](#r9---discuss-the-database-relations-to-be-implemented-in-your-application)


[R10 Describe the way tasks are allocated and tracked in your project](#r10---describe-the-way-tasks-are-allocated-and-tracked-in-your-project)

---


## R1 - Identification of the problem you are trying to solve by building this particular app

Many companies now offer flexible and hybrid working arrangements, which allows their employees to work from locations other than their designated office. Since workplaces have transitioned to a hybrid model, many have re-organised their offices so that employees do not have designated desks to allow for more flexibility. The downside of this is that there can be times when the office is busier than usual and there aren't enough desks for everybody there. If someone comes to the office, hoping there will be a desk available, time can be wasted while they try to find a desk and they may even have to go home and work remotely.

Other problems that can occur as a result of the hybrid model are that companies may find their office space is being under-utilised. This could prompt them to divert funds elsewhere if the expense of paying for office space, including furniture, utility bills, equipment etc is deemed unnecessary. There are some businesses however, that are unable to move to a fully remote operation (e.g. manufacturing, health care etc). These businesses may want visibility of how much the office is being utilised and/or whether employees are coming into the office in accordance with their policy.

## R2 - Why is it a problem that needs solving?

I have chosen to create an app which companies can use to provide their staff with a method to view and book available desks so that their team members know before coming to the office that they have a desk to use. A tool that allows employees to log into a website and book their desk for the day (or discover that there are none available which would allow them make other arrangements) would be beneficial to a lot of companies and their employees. By solving this problem, time will be saved, which will increase productivity and companies can adapt their resources according to the needs of their business. This has the possibility of reducing expenses and improving the bottom line profit. 

Some companies offer simple solutions to this issue, but from research among peers, they have found them to have issues with data inconsistency, cumbersome or difficult to use. By building a "best-in-class" solution that is feature-rich, reliable, scalable and fun to use, the app has the potential to be marketed as an integral tool for businesses requiring a system to help manage their hybrid workplace.

## R3 - Why have you chosen this database system. What are the drawbacks compared to others?
The database used is PostgreSQL, which lends itself well to the needs of this project due to its ability to handle complex queries, while allowing multiple users to simultaneously access the database and perform read-write actions. It is able to handle very large data sets, and so provides the assurance of scalability to medium or large businesses and even multinational corporations. PostgreSQL is open source and has an active community of developers consistently working on updates and improvements which mean it remains a popular choice for businesses and consistently in the top 5 of most popular databases, according to DB-Engines.

Below is a comparison of the features provided by PostgreSQL vs MySQL:

- Memory usage and disk requirements
Postgres takes a heavy toll on memory overhead due to its requirement to generate a new system process for every client connection. By comparison MySQL uses a single thread for each connection, requiring less memory allocation, which may provide a better performance for smaller or medium sized business requirements.


- ORDBMS
Postgres is an **object** relational database management system, compared with MySQL which is a standard relational DBMS - therefore Postgres has native capabilities for converting its entities into objects and also is inherently able to define inheritance relationships between tables. This assists its ability to handle complex relationships without sacrificing performance.

- Data Types & Structure
Postgres provides the ability to use complex and custom data types which offers increased functionality. MySQL by contrast has a more limited amount of data types and in terms of structure is less SQL-compliant compared with Postgres which means it can produce unpredictable results

- Data integrity
PostgreSQL uses multi-version concurrency control (MVCC), which is one of the primary reasons for its popularity for businesses. This ensures the integrity of data whilst multiple users are reading from and writing to the database simultaneously. MySQL does offer a solution but it is generally accepted that Postgres outperforms MySQL in handling MVCC.

### When MySQL could be chosen ahead of PostgreSQL
- Speed
MySQL is well-known to be one of the fastest performing databases, which is an important consideration factor, and one which places it ahead of Postgres. One of the reasons for this is MySQL's strong performance when dealing with read-only queries. In the case of this app which relies heavily on the full spectrum of CRUD operations, it may not be worth the trade-off. But for an application whose main purpose is *retrieving* data, MySQL would be a good choice.

- Simplicity
One of MySQL's attractions is its simplicity and ease of use. It was designed to be and remains lightweight and is quick to set up without the need for too many adjustments. However, it does offer extensibility features through a range of plug-ins. When the requirements of the project demand urgency, and the complexity level is low, MySQL is a good choice.



> Citations
> Engines ranking (no date) DB. Available at: https://db-engines.com/en/ranking (Accessed: 17 December 2023). 
> Smallcombe, M. (2019) PostgreSQL vs MySQL: The critical differences, Integrate.io. Available at: https://www.integrate.io/blog/postgresql-vs-mysql-which-one-is-better-for-your-use-case/#three (Accessed: 17 December 2023). 
> Salman Ravoof&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Salman Ravoof is a self-taught web developer (2023) PostgreSQL vs MySQL: Explore their 12 critical differences, Kinsta®. Available at: https://kinsta.com/blog/postgresql-vs-mysql/#postgresql-vs-mysql-headtohead-comparison (Accessed: 17 December 2023). 


## R4 - Identify and discuss the key functionalities and benefits of an ORM
An object relational mapper (ORM) is used to allow database entities to be treated as objects in an object-oriented paradigm. It takes away the need to write raw SQL queries to interact with the database and instead acts as an interpreter, converting instructions written in an object-oriented programming language into structured query language (SQL) so that an SQL database can process it. This enables programmers to focus on higher level concerns, such as business logic, implementing efficient and functional methods and functions etc, rather than being hindered by writing long and complex SQL queries. Additionally, the 'mapper' part of the ORM provides the function of mapping 'relationships' (e.g. one-to-one or one-to-many) and manages the integrity of the data between the relations. An ORM is 'database-agnostic', so it is not tied to one database or another. It is able to abstract the database engine, allowing for portability to another database management system in the future, if required, without needing to re-write the entire application.

## R5 - Document all endpoints for your API

### 1. /admin
- Description: Allows an admin to create and add a user to the database
- HTTP Request Verb: POST
- Required Data: employee id, first name, last name, email, password [between 8 and 14 characters], department
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created user (excluding password)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/USER%20-%20CREATE%20USER.png)

### 2. /user
- Description: Allows admin to view all users registered in database
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing all registered users, including their bookings, excluding passwords
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/USER%20-%20VIEW%20ALL.png)


### 3. /admin/\<string:employee_id>
- Description: Allows an admin to update a user's details (i.e. name, email address, password, department, admin status)
- HTTP Request Verb: PUT/PATCH
- Required Data: at least one of employee id, first name, last name, email, password, department
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated user (excluding password)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Updates to user cascade to any bookings associated with them

![](/docs/USER%20-%20Before%20Edit.png)
![](/docs/USER%20-%20EDIT.png)

### 4. /admin/\<string:employee_id>
- Description: Allows an admin to delete a user
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Deleting a user cascades to any booking with which the user is associated

![](/docs/USER%20-%20DELETE.png)



### 5. /user/\<string:employee_id>
- Description: Allows a user to see information about themselves (but not other users)
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing the user, including their bookings, excluding password and admin status
- Authentication Methods: Valid JWT with an admin's or user's credentials encoded, `authorise()` method checks the user is an admin or the user id being accessed matches the token's identity

![](/docs/USER%20-%20VIEW%20ONE.png)

### 6. /user
- Description: Allows a user to login
- HTTP Request Verb: POST
- Required Data: employee id, password
- Expected Response: HTTP response status 200 - OK, JSON object showing the user, including their bookings, excluding password and admin status
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/USER%20-%20LOGIN.png)

### 7. /user/\<string:employee_id>
- Description: Allows user to change their password
- HTTP Request Verb: PUT/PATCH
- Required Data: new password [must be between 8 and 14 characters]
- Expected Response: HTTP response status 200 - OK, JSON object showing the user, including their bookings, excluding password and admin status
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/USER%20-%20CHANGE%20PASSWORD.png)

### /user - missing routes:
- DELETE: There is no route which allows users to delete users - this function is available to admins via the admin route

### 8. /dept
- Description: Allows admin to view all departments
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing all departments (id, name, users in each dept)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/DEPT%20-%20VIEW%20ALL.png)

### 9. /dept
- Description: Allows admin to create new department
- HTTP Request Verb: POST
- Required Data: department name
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created department (id, name)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/DEPT%20-%20CREATE.png)

### 10. /dept/\<int:dept_id>
- Description: Allows admin to edit department name
- HTTP Request Verb: PUT/PATCH
- Required Data: department name
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated department (id, name, users in dept)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Updating a department name cascades to any users belonging to that department

![](/docs/DEPT%20-%20EDIT.png)

### 11. /dept/\<int:dept_id>
- Description: Allows admin to delete department
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
Note: Any user belonging to a department which has been deleted means their dept_id is set to `null`

![](/docs/DEPT%20-%20DELETE.png)

### 12. /desk
- Description: Allows admin to view all desks
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing all desks (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/DESK%20-%20VIEW%20ALL.png)

### 13. /desk/\<int:desk_id>
- Description: Allows admin to view a desk
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, JSON object showing an individual desk (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/DESK%20-%20VIEW%20ONE.png)

### 14. /desk
- Description: Allows admin to create new desk
- HTTP Request Verb: POST
- Required Data: desk id, status [optional]
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the created desk (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/DESK%20-%20CREATE.png)

### 15. /desk/\<int:desk_id>
- Description: Allows admin to edit desk
- HTTP Request Verb: PUT/PATCH
- Required Data: at least one of desk id, availability status
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated desk (id, status, bookings)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: If the desk_id or availability status is updated, this update cascades to any bookings associated with it

![](/docs/DESK%20-%20EDIT.png)

### 16. /desk/\<int:desk_id>
- Description: Allows admin to delete desk (desks which have bookings cannot be deleted)
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: Desks cannot be deleted if there are bookings associated, therefore there is no `ondelete` constraint for desk_id foreign keys

![](/docs/DESK%20-%20DELETE.png)

### 17. /user/\<string:employee_id>/booking
- Description: Allows user to view their bookings
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of their bookings (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/BOOKING%20-%20USER%20VIEW%20ALL.png)

### 18. /user/\<string:employee_id>/booking/\<int:booking_id>
- Description: Allows user to view an individual booking
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of the booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/BOOKING%20-%20USER%20VIEW%20ONE.png)

### 19. /user/\<string:employee_id>/booking
- Description: Allows user to create a new booking (the system prevents duplicate bookings for the same day/desk)
- HTTP Request Verb: POST
- Required Data: week_id [week number], weekday [mon, tue, wed, thu, fri], desk_id
- Expected Response: HTTP response status 201 - CREATED, a JSON object of the booking(booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/BOOKING%20-%20USER%20CREATE.png)

### 20. /user/\<string:employee_id>/booking/\<int:booking_id>
- Description: Allows user to edit their booking, ie. change the desk and/or week and/or day associated with the booking (fails if the chosen desk/day is unavailable)
- HTTP Request Verb: PUT PATCH
- Required Data: At least one of desk_id, week_id, weekday
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/BOOKING%20-%20USER%20EDIT.png)

### 21. /user/\<string:employee_id>/booking/\<int:booking_id>
- Description: Allows user to delete a booking
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/BOOKING%20-%20USER%20DELETE%20ONE.png)

### 22. /user/\<string:employee_id>/booking
- Description: Allows user to delete all their bookings
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.
- Note: while delete all is usually not recommended, it's provided here as an option in case a user realises they have made many bookings incorrectly, or perhaps they are away for a period of leave and want to delete their bookings

![](/docs/BOOKING%20-%20USER%20DELETE%20ALL.png)

### 23. /booking
- Description: Allows admin to view all bookings
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of all bookings (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/BOOKING%20-%20ADMIN%20VIEW%20ALL.png)

### 24. /booking/\<int:booking_id>
- Description: Allows admin to view an individual booking
- HTTP Request Verb: GET
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, a JSON object of the booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Requires employee id, which is matched against the database, if a match is found the hashed password is checked against the hashed password of the user found in the database. If successful a JWT is generated which allows the user to access all user level routes.

![](/docs/BOOKING%20-%20ADMIN%20VIEW%20ONE.png)

### 25. /booking/\<int:booking_id>
- Description: Allows admin to edit a booking (fails if the new day/desk is unavailable)
- HTTP Request Verb: PUT PATCH
- Required Data: At least one of employee id, desk_id, week_id, weekday
- Expected Response: HTTP response status 200 - OK, a JSON object of the updated booking (booking id, desk id, week id, weekday, user object excluding password/is_admin)
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/BOOKING%20-%20ADMIN%20EDIT.png)

### 26. /booking/\<int:booking_id>
- Description: Allows admin to delete a booking
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status

![](/docs/BOOKING%20-%20ADMIN%20DELETE.png)

### 27. /booking
- Description: Allows admin to delete all bookings
- HTTP Request Verb: DELETE
- Required Data: N/A
- Expected Response: HTTP response status 200 - OK, empty JSON object
- Authentication Methods: Valid JWT with admin's credentials encoded, `authorise()` method checks user has admin status
- Note: while delete all is usually not recommended, this route has been provided in case of some catastrophic event and provides a method for an admin to delete all bookings, rather than having to do this one by one

![](/docs/BOOKING%20-%20ADMIN%20DELETE%20ALL.png)

### /booking - missing routes:
- POST: there is no route to allow admins to create bookings as this should be done by users. If there was an occurence that required an admin to create a booking, they would have to do so via the user route

### Examples of error messages:
#### Desk ID must be unique
![](/docs/ERROR%20DESK%20-%20CREATE.png)

#### Desk cannot be deleted if bookings for it exist
![](/docs/ERROR%20-%20DELETE%20DESK.png)

#### User cannot access user route of another user
![](/docs/ERROR%20-%20USER%20ACCESSING%20ANOTHER%20USER.png)

### Examples of code to handle errors
![](/docs/ERROR%20HANDLING-1.png)

![](/docs/ERROR%20HANDLING-2.png)

## R6 - Entity Relationship Diagram
### ERD for Desk Easy Booking System Database 
The database contains the following tables:

1. The **Desks** table has a one to many relationship with bookings

1. The **Bookings** table is related to desks via the desk_id foreign key. A booking has a one to one relationship with a desk. Bookings is related to users via the **employee_id** foreign key; the relationship between booking and user is also one to one

1. The **Users** table has two identifiers: user_id and **employee_id** - the database calls exclusively use employee_id to search, select and manipulate users. Users have a one to many relationship with bookings and also relate to the department table via the foreign key dept_id. 

1. The **Depts** table contains each department within the company and has a one to many relationship with users. The diagram indicates it is mandatory for uses to have a department, which is true for creating users however, it is possible for users to become detached from the departments table, if their department is deleted by a DB administrator

![ERD](/docs/ERD_ver3.png)



## R7 - Detail any third party services that your app will use
### FLASK
Flask is a Python framework which is used to make creating web applications in Python easier. It is described as being flexible and lightweight, which means that while providing the tools and functionality to create both small, simple web applications and also larger, complex ones, it provides a range of customisable features and supports integration with other services needed to support the application, such as password encryption, Support Secure cookies and in-built error handling. It has its own development server, complete with debugger and a unit testing module which makes it a popular choice for web developers. Flask is capable of managing the HTTP request-response protocol and is particularly useful in creating RESTful APIs.

### POSTGRESQL
PostgreSQL is an open-source relational database widely used for data storage in web applications. It has many powerful features and supports a range of popular programming languages. This app has specifically taken advantage of its ability to handle user-defined types, the referential integrity when using foreign keys, its ability to work well with plug-ins and extensions as well as its extensibility, meaning it has the scope to grow as the business requirements evolve.

### SQL ALCHEMY
SQL Alchemy is an Object Relational Mapper (ORM). It is used to allow access to and manipulation of the database without the need to enter SQL commands. It achieves this by converting the database objects (e.g. tables, rows, entity characteristics) to Python objects meaning the database is converted to an object-oriented paradigm which enables database queries to be executed within Python.

### PSYCOPG2
Psycopg2 is a database adapter that allows the ORM (SQL Alchemy) to connect to a PostgreSQL database. It is called as part of the initial database set up and contains a URL with important security information, such as the database "user" it will assume when accessing the database as well as the name of the Postgres database to which it needs to connect.

### MARSHMALLOW
Marshmallow is a Python library able to convert database object types into Python object types. It has powerful features allowing serialisation from JSON to Python and vice versa, making manipulating and extracting data from the database a much less labour intensive process. It comes with features that allow data validation, enforcing of mandatory fields and the nesting of data from join tables. It has its own error handling via its exception classes - this is particularly useful when targeting and handling Marshmallow specific errors.


### BCRYPT
Bcrypt is a password-storing tool, which uses complex algorithms to hash and salt passwords. This package enables users' passwords to be safely stored in the database, unable to be accessed by database administrators, and reducing the vulnerability in case of a cyber attack. The app is designed so that Bcrypt handles the password entered by a user, whether logging in or being created anew, immediately. It is a one way hash, so it is not possible to reverse the process and obtain the raw password. When the user logs in and enters their password, it is hashed in the same way as the original one, and the two hashed passwords are compared for similarity. Bcrypt handles each of these functions.


### Flask JWT Manager
The app uses JSON web tokens (JWTs) to manage the process of authenticating users and also for ensuring only users with the correct privileges access restricted routes. JWTs provide a simple and secure way of transmitting information between parties using a JSON object which contains digitally signed information used to identify the user. Flask JWT Extended provides functionality to create tokens, protect routes by labelling them as requiring a token and the ability to access specific information about a user via the token.

> Citation
> (No date) An Easy Introduction to Flask Framework for Beginners. Available at: https://www.analyticsvidhya.com/blog/2021/10/flask-python/. 


## R8 - Describe your project's models in terms of the relationships they have with each other

### User Model

The user model contains information about the user and connects to the department model via the foreign key `dept_id`. A user has a one-to-one relationship with department (i.e. a user can belong to only one department). The foreign key constraints: `onupdate="cascade"` and `ondelete="set null"` mean that users will be updated if their department name changes, but if the department itself is deleted, the user will still exist but with `null` as their department. There are relationships established using SQLAlchemy's `relationship()` method together with its `back_populates` argument. In the first instance, this is so that user information is populated within department - note if a user is deleted their entry will be deleted from the department. Secondly, user information is populated within the booking model and allows user data to be viewed within a booking. The `cascade="all, delete"` argument ensures that if a user is deleted, all of their bookings are deleted.


The user model contains multiple schemas, with varying requirements. `UserSchema` has no required fields but it does require any password that is entered to be between 8 and 14 characters long. The `CreateUserSchema` is called when a new user is being created and has several stipulations, as well as the password length criteria; it requires a new user in the system to have a first and last name, a properly formatted email and a department. SQLAlchemy's `fields.Nested` argument is called for department and bookings to allow Marshmallow to access the relevant Schemas and display the associated data within the user model. There is one further schema: `UserSchemaPassword`. This allows users to change their password; it enforces that a password (but nothing else) must be entered.

### Department Model

The department model has a one-to-many relationship with the user model, since one department can have many users. No foreign keys are required here, since the user model has the foreign key. The `relationship()` method is used so that department data `back_populates` the department field within user. `fields.Nested()` is used by the `DeptSchema`` to allow specified information about the users to be shown within each department to which they belong.

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

The bookings table provides all necessary information about a booking via the following columns: `id, week_id, weekday, desk_id, user_id, date_created`. `id` is auto-incremented and is the designated means of identifying a booking. `date_created` is automatically generated using Python's datetime package. `week_id` is an Integer value representing the week number and `weekday` is a String value identifying the day of the week for which the booking has been made. The bookings table has a one-to-one relationship with both the desks and users tables, since each booking has just one desk and one user. This relationship is established using foreign keys and allows the bookings table to display the user and desk to which it is associated.

Setting up the database tables in this way means there is no overlap of information as each table has ownership for only what it needs and links to related tables to access any associated information. 


## R10 - Describe the way tasks are allocated and tracked in your project
For the planning of this project, I used the project management tool available within GitHub. I initially added the following states: To Do, In Progress, Add Ons, Complete. The 'Add Ons' section was to include "nice to have" or additional features, not necessary for the initial pass (in this case, the assignment rubric, in reality this would be the minimum viable product). In "To Do", I placed several items which I knew would need to be done, or at least considered, early on. Some examples of these tasks were planning the database design, creating an initial ERD and answering the first few questions which were all useful in terms of directing the early stages. At the start of the day or upon completing a task, I would go back to the plan and move items as necessary and review what to start on next.

The plan was continuously evolving - as new learnings were made, I would make changes or additions to the task list. It also served as a useful reminder - if an idea popped into my head, I'd add it to the to-do list. This helped to keep the focus on the task at hand, but ensure a new idea wouldn't be forgotten. When clicking into a task card, it is possible to make more detailed comments - this was another feature I found particularly useful as under one task, I often included a number of sub-points, which I could tick off along the way. 
See image for reference:
![](/docs/GITHUB%20PROJECT%20-%20ADDITIONAL%20COMMENT.png)

When making comments in the daily standup Discord channel, I used the project plan as a reminder on what had been completed in the last day and a guide on what I'd be working on that day. There were times when a particular issue would be taking longer than expected, so rather than lose sight of the bigger picture I would seek help from others, or leave it to one side to continue making progress on other areas. One of the many benefits of using a project planning tool is having a visual representation of the progress that has been made. It's all too easy to forget how far you've come from an empty code repository to a fully functioning application. I took screenshots along the way to document my progress.

[Link to GitHub Project Plan](https://github.com/users/krd81/projects/2)

#### Project Status at 7 Dec
![](/docs/GITHUB%20PROJECT%20-%2007.12.23.png)

#### Project Status at 10 Dec
![](/docs/GITHUB%20PROJECT%20-%2010.12.23.png)

#### Project Status at 12 Dec
![](/docs/GITHUB%20PROJECT%20-%2012.12.23.png)

#### Project Status at 14 Dec
![](/docs/GITHUB%20PROJECT%20-%2014.12.23.png)

#### Project Status at 16 Dec
![](/docs/GITHUB%20PROJECT%20-%2016.12.23.png)



