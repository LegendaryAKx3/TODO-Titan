# TODO-Titan

#### Video Demonstration: <insert url>

### Description
To-do list webapp written with flask. Users are able to log in to unique and secure accounts and create, move and complete their own tasks. Follows the CRUD list and stores data in SQLite.

#### Register
Consists of a form for users to submit with a field for username, password and for password confirmation, which is standard across all websites. Username was chosen instead of email because email was deemed not nessecary for this service, and would add an extra layer of complication to the process. The information gathered from the user is verified as legitimate then added to the users database. This page also has a link redirecting to the login page, in case someone with an account is directed here by mistake. 

#### Login
Users input username and password into corresponding fields, then submit form. Information is then checked against user database, and if verified, the user is logged in with ther user id stored in their session. Having this user id stored will allow the user to access all portions of the app where login is required, enforced by the login_required function.

#### Logout
Clears the session information and redirects user to the login page. Button is located within the homepage.

#### Layout/homepage
The homepage is the core of any app. This app has the homepage as one of three screens (others being login and register). This page has all the sections, tasks, and buttons to manage your list. Any addition or deletion of section or task redirects you back to the homepage and updates the html to reflect the user's change. The homepage has a logout button in the top, giving ways for a user to sign out of the current account. There is a popup form for creating tasks (if we were to do this project again, we would probably remove that). The form uses javascript to update an attribute that shows the form when the "Add Task" button is clicked. The form code is contained in a script tag. In the layout, we chose to use Jinja to override css links so we could break down css into multiple files and have one for each html page. We also include titles, call Bootstrap, and template out the "body" block.

#### Creating tasks
To create tasks, a form is submitted containing the name of the task and the section that the task is going to be added to. The section is read from the sections database when the page loads. Once a task is submitted, it is added to the tasks database under that user's id, and given a unique id that is used until the task is completed. If the section selected is main, the section_id value is set to null. Otherwise, it is set to the value of the corresponding section's id. After this action is executed, the page is refreshed to reflect changes.

#### Moving tasks
In the options section of each task, there is a drop down to move the task into a different section, alongside a button to submit it. The form contains hidden fields iwth the task and destination section id. The button submits the form and modifies the section of the database entry corresponding to the task id. The page is then refreshed to update changes.

#### Completing tasks
Each task consists of a form with a checkmark button from Bootstrap submitting the form and a hidden element containing the tasks id, as well as a visible task name section.

#### Sections
When the section form is submitted, a new section is created under that name with a unique id. Tasks are added to sections in the creating tasks form, and this is done by id, not by name, to prevent duplicate name conflicts. Sections also have buttons to delete the section and delete the section and send all the remaining tasks to the main section, or delete the section with all the tasks in it.


**Sqlite startup commands**

- `CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);`

- `CREATE TABLE tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, task_text TEXT NOT NULL, uuid INTEGER NOT NULL, section_id INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);`

- `CREATE TABLE sections (section_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, uuid INTEGER NOT NULL, section_name TEXT NOT NULL);`
