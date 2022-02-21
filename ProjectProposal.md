
# Project Proposal: OnBoard
#### Diya Yunus, Keerthana Nallamotu, Harini Arumugam, Eesha Ramkumar 

## Pitch
Booking transportation to and from Urbana-Champaign is cumbersome and confusing; students may feel overwhelmed by their many options (including Peoria Charter, the Amtrak, Greyhound) and scrolling through each website for time availability and cost appropriate choices can be a tedious task. OnBoard mitigates these challenges by providing a centralized space to book tickets, and creating opportunities for local transportation businesses to further their reach within their communities. 

## Functionality
- Using the web app, users can create accounts and login using their email addresses 
- Users can see a list of ticket availabilities for a specified date
- Users can purchase tickets for various public transportation from a single platform
- Users can view their past transactions in their transaction history
- Users can receive points proportional to each purchase 
- Users can accumulate points and get rewards (including discounts at local restaurants or shops) 

## Future goals:
- Local businesses can post discounts and advertisements that users can view in their feed
- Users can add friends to:
    - Share discounts and ticket pricing information
    - View a leaderboard of their friends’ points (creates incentive) 
- Expand to other states/countries
- Sync with existing accounts in transportation services.

## Components:
 - The page/database where users can see ticket availability
 - The local business side user interface where they can add discounts and advertisements
 - #### Backend: We will be using the Python Flask framework to connect front-end features such as the user interface, account sessions, and ticket selection platform to a backend SQL-Lite database that holds transportation service options and availability. We selected a Python-based framework since we all have previous experience working with the language and will easily be able to adapt our knowledge to Flask’s more specific requirements. This database will be updated in real-time by scraping ticket options from public transport websites at regular time intervals. 
    - Libraries: We will use the Curl library to transfer data to and from the server, flask-login for managing user accounts, flask-bootstrap library to integrate the bootstrap environment with flask, Flask-SqlAlchemy for integrating with SQLite Database, and pytest library for testing our application.
 - #### Frontend: We will be implementing the frontend of our web application using JavaScript and Bootstrap. We choose JavaScript because our team is familiar with it and it is a powerful language to apply in Bootstrap, an open-source web development environment. The frontend of our web app will contain the login page, main dashboard where users can see their accumulated points and earned rewards, and individual pages for viewing ticket availability for various transportation methods. It will interact with the backend and ticket/business databases to display the information to the users. 
    - Libraries: We will use UI Bootstrap library for additional UI elements, Bootstrap Datepicker for data choosing functionality, and bootstrap.bundle.js for JavaScript integration.
 - We will test our frontend manually and by letting potential users test and provide feedback.



## Weekly Planning
1. Collect potential transportation services and local businesses to partner with; start working on database for storage
2. Finish up the ticket platform; add tickets scraped in real-time from websites of previously researched services 
3. Create basic user dashboard design; build platform where they can see their accumulated points and discounts
4. Connect the user dashboard with backend so they can purchase tickets; build notification system receive point updates
5. Create basic local business dashboard design; build platform where they can post new discounts and advertisements
6. Connect the local business side to the main application, so changes made in the business account are updated on the user’s dashboard
7. Begin testing and debugging of all the components; refine the application 
    - Testing Plan: Because our main consumers are students at UIUC, we will offer the web application to them. Using a series of organized control groups and blind tests, we will record their feedback about the app and record their experience with the user interface (ie. did the flow make sense, was the booking process intuitive, were options clear and easy to find, did the text and instructions aid to the experience). Using their direct feedback, we will iterate on the application. Finally, once we release the web application, we will continue to monitor the feedback and comments section - making necessary updates and changes. 
8. Finish testing, debugging, and refinement of application; implement future goals with remaining time; Prepare for presentation

## Potential Risks
- It might be difficult to fetch real-time data from ticket servicing websites. However, we will research and find a way to provide users the most up-to-date information within the first week of our project.
- Local businesses might be unwilling to post on our app and provide discounts but we will encourage them by talking through the benefits of advertising on our platform by the end of the fourth week.
- Another challenge would be effectively following our schedule. If we have difficulties in finishing tasks for a week, the next week’s tasks will fall behind.  In order to avoid this issue, we will make sure each team member effectively finishes the required tasks every week through a check-in meeting on each Sunday.
- Accounting for user privacy will be a challenge to include in our web application, but we will ensure that we effectively ask user permission for access to their data and account for encrypting user personal information by week three when we finish building the user side of the application.

## Teamwork
We will be using the code hosting platform Github. This will allow us to keep all of the components of our project organized in one repository while enabling each of us to contribute from our preferred editors. Additionally, we will maintain documentation of our work and any errors we run into.

After finalizing our project plan and completing our initial research, we will divide up the tasks as follows: Eesha and Diya will tackle the frontend aspects of our application, from designing its visual elements and developing its user interface to implementing the various pages of our app including the user dashboard, points and discounts page, and local business advertisement page; Keerthana and Harini will tackle the backend component of our project by securing the app to a database with relevant transportation information for users to access as well as ensuring that information from local businesses is updated within this database. We will collectively work on testing and debugging our application. 

We believe collaborative contribution will be most efficient in furthering our project and its success. We will follow the sequence of the ‘Weekly Planning’ section and hold meetings regularly to ensure that we are on board with each step of the development process!
