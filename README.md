# TODO-Titan

#### Video Demonstration: <insert url>

### Description

To-do list webapp written with flask. Users are able to log in to unique and secure accounts and create, move and complete their own tasks.

#### Register
Consists of a form for users to submit with a field for username, password and for password confirmation, which is standard across all websites. Username was chosen instead of email because email was deemed not nessecary for this service, and would add an extra layer of complication to the process. The information gathered from the user is verified as legitimate then added to the users database. This page also has a link redirecting to the login page, in case someone with an account is directed here by mistake. 

#### Login



#### Logout
Clears the session information and redirects user to the login page

#### Layout/homepage

#### Creating tasks
To create tasks, a form is submitted containing the name of the task and the section that the task is going to be added to. The section is read from the sections database when the page loads. Once a task is submitted, it is added to the tasks database under that user's id, and given a unique id that is used until the task is completed.

#### Moving tasks

#### Completing tasks


#### Sections
