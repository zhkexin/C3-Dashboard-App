# C3 User Data Management Dashboard Application

write a description of the app

## Data Management

Test case documents can be found in the `test_case` folder.

## Demo
### Login and User Authentication
The following screenshots are the basic structure of the login portal of C3’s Web Portal.
Here is the login screen
<p align="center">
   <img src="./images/login_screen.png" width="400" align="center">
</p>

All workers can create an account using their username, first name, last name, work email address and confirming their password. 
There has also been a drop down option to clarify which department a user is a part of. 
<p align="center">
   <img src="./images/register_page.png" width="400" align="center">
</p>

Once the account is created, you will be able to see the created account in the database.
<p align="center">
   <img src="./images/account_creation.png" width="400" align="center">
</p>

Users who already have an account can login using the sign in page. A valid username and password must be inputted. 
If there is an invalid information inputted. The user will be redirected to the main login page with the following error message
<p align="center">
   <img src="./images/signin_page.png" width="400" align="center">
</p>

Once the user is logged in, they will be able to access the the subsystems that they were granted access for. If they are not granted permission, they will be prompted to log in. 
<details>

<summary>User authentication</summary>
   
   User with the id “sales” is under the sales department group, who can only access the sales subsystem.

   User with the id “dealership” is under the dealership department group, who can only access the dealership and sales subsystem.

   User with the id “management” is under the management department group, who can access all three of the subsystems. They will be classified as the superadmin.
</details>

| Subsystem  |                             Result                              |
| ---------- | --------------------------------------------------------------- |
| Sales      | <img src="./images/auth_sales.png" width="400" align="center">  |
| Claims     | <img src="./images/auth_claims.png" width="400" align="center"> |
| Reports    | <img src="./images/auth_reports.png" width="400" align="center">|

More details are included in the pdf file "build_information"

