# Statbotic

Statbotic is a command-line Python application for storing, viewing and exporting Support team statistics. To help Support Team Leads and Managers to keep track of how their team is performing.

[Live webpage](https://support-stats-bot.herokuapp.com/)

![Mockup image](docs/mockup.png)

## Table of contents

- [Statbotic](#statbotic)
  - [Table of contents](#table-of-contents)
- [UX](#ux)
  - [Strategy](#strategy)
    - [The problem](#the-problem)
    - [The solution](#the-solution)
    - [Target audience](#target-audience)
    - [The project goals](#the-project-goals)
  - [Scope](#scope)
    - [User stories](#user-stories)
  - [Structure](#structure)
  - [Skeleton + Surface](#skeleton--surface)
  - [Features](#features)
    - [Welcome banner](#welcome-banner)
    - [Login menu](#login-menu)
    - [Login](#login)
    - [Register](#register)
    - [Exit](#exit)
    - [Main menu](#main-menu)
    - [Add or update statistics](#add-or-update-statistics)
    - [View statistics](#view-statistics)
    - [Export stats](#export-stats)
    - [Exceptions](#exceptions)
  - [Technologies used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks and tools](#frameworks-and-tools)
  - [Validation](#validation)
    - [PEP8 validation](#pep8-validation)
    - [Testing user stories](#testing-user-stories)
  - [Bugs](#bugs)
  - [Deployment](#deployment)
  - [Python Libraries](#python-libraries)
    - [pymongo](#pymongo)
    - [tabulate](#tabulate)
    - [certifi](#certifi)
    - [pyfiglet](#pyfiglet)
  - [Credits](#credits)
    - [Code](#code)
    - [Reference material](#reference-material)

# UX

## Strategy

### The problem

Customer and technical support teams work hard to support their customers and their product. This means that, unless support statistics are being tracked, success or trends can go unnoticed. 

### The solution

Enter Statbotic! A simple, lightweight command-line application. Statistics, such as ticket solves and total live chats, can be stored for future reference. Historical date ranges can be viewed with averages over that range. And statistics can be exported to a JSON file to be used elsewhere - such as chart and graph software.

### Target audience

Anyone working on a customer or technical support team, where important statistics include solving tickets and handling live chats. Most likely in a managerial, supervisor or team lead role.

### The project goals

- To have a simple and lightweight way to record support team stats.
- To be able to view historical stat summaries.
- To be able to export the stats in other formats for use elsewhere.
- To be easy to navigate.

*Go back to the [top](#table-of-contents)*

---

## Scope

### User stories

As a manager/supervisor...

1. I want to input stats to be saved for future reference.
2. I want to view historical stats for a particular date/date range.
3. I want to see averages when viewing saved stats.
4. I want to export the data so I can use my charting software.
5. I want a login to provide some security.
6. I want a friendly application to help command-line be less scary.
7. I want to be able to navigate the application easily.
8. I want feedback on my actions.

## Structure

**App diagram**

The app consists of menus and "forms" (sequences of user input) for gathering information. The rest is "behind the scenes". The diagram below helps to understand how the app has been pieced together.

![App diagram](docs/planning/app-diagram.png)

**Database**

The app uses MongoDB. It's a non-relational database, with data being stored in documents. Each document can store any type of data, regardless of what was saved before, making it very flexible. It also has the perk of storing data in a JSON-like format, making it work really nicely with Python and this project.

## Skeleton + Surface

As a command-line app, there isn't any visual design as such. Space is created by inserting empty lines or clearing the terminal screen. There are also dashed lines to help titles to stand out, and borders for tables. Therefore, no wireframes were used, and no branding/visual design needed.

However, I will note the use of the cheeky robot (see the Features section). Being quite limited as to how to get any personality across with a mostly black and white text-based application, ascii art is an obvious choice. This allowed me to create a more interesting logo, and include a robot illustration.

*Go back to the [top](#table-of-contents)*

---

## Features

### Welcome banner

When arriving on the webpage and the mock terminal first loads, users are welcomed with a coloured logo, a cheeky robot and a welcome message. This provides a friendly introduction to the app, hopefully helping command line to be a slightly less scary place for those that have never used it, and injects some personality into an otherwise text-based application.

### Login menu

Beneath the welcome banner is the login menu. Users are given the options login, register or exit, followed by a prompt. Users are required to enter a number to choose a menu option.

![Welcome and login menu](docs/features/welcome-login-menu.png)

### Login

On selecting option 1 from the login menu, users enter the login workflow. The app asks for a username and password. The user has 3 tries to get these credentials correct. 

If the username is not found in the database, the app will let the user know and remove a try. If it is found, but the password doesn't match what's stored in the database, the app will again supply feedback to the user and remove a try. When all 3 tries have been used up, the app will return to the login menu.

If the correct credentials are provided, the user is taken to the application's main menu.

![Login](docs/features/login.png)

### Register

On selecting option 2 from the login menu, users enter the registration workflow to create a new login. The app asks for a username, and before continuing, will check if this username already exists in the database. If it does, the app will let the user know and prompt them for another username.

If the username they've chosen does not already exist in the database, the user is asked for a password, which is hashed and stored in the database. After this, they're returned to the login menu to login.

![Register](docs/features/register.png)

### Exit

If the user chooses option 0 from the login menu (or the main menu), the app exits. If this were running in an actual terminal, it would exit the app. But in the mock terminal, it exits, but doesn't appear to do anything, as there's nothing else for it to load.

### Main menu

Once a user is logged into the app, they're presented with the main menu where the main activity happens. They again have the option to exit by choosing 0. Or they can choose to add/update stats, view stats, or export stats. There's also a little personalised welcome message showing the user's username. Here's what happens when you choose to exit:

![Main menu and exit](docs/features/main-menu-exit.png)

### Add or update statistics

On choosing option 1 from the main menu, the user heads into the add/update stats workflow. The user is asked for a date, which is then checked in the database. If the date already exists, the user is asked if they'd like to overwrite the data. 

If it does not exist, they're taken to a "form" to collect the stats for that date. On completion of the form, the database is updated and the user is asked if they'd like to enter more stats. If the user chooses yes (y), the workflow is restarted. If they choose no (n), the user is returned to the main menu.

![Add or update stats](docs/features/add-update-stats.png)
![Enter new stats](docs/features/enter-new-stats.png)

### View statistics

When the user selects 2 from the main menu, this triggers the workflow for viewing historical statistics (i.e. those that have already been saved in the database). The user is asked for a date again, but this time it represents the beginning of a date range.

The user is then asked for the number of days to be included in the range. To see the statistics just for that date, they can enter 0. The database is checked to see if the data exists. If it does, a table of statistics is then displayed. The table shows totals for the input data, some average calculations for each, and lastly a number of public comments to solved ticket ratio.

It's quick to view the performance of a team using these statistics. The CSAT is the customer satisfaction rating, which is always good to look at over a range of time. The number of comments to solved ticket ratio is important for showing how efficient the team is with their explanations: the more accuracy in their responses, the more likely a ticket will be solved quickly (with less comments). 

In a perfect customer support world, the CSAT score would be 100%, and the comments vs solves ratio would be 1. A good goal would be 95% CSAT and 2 comments per solved ticket.

![View stats workflow](docs/features/view-stats.png)
![View stats table](docs/features/view-stats-table.png)

### Export stats

On selecting 3 from the main menu, the user is taken to the export workflow. This starts in the same way as the viewing workflow by asking for a date for the start of the range. This is then followed by an input for the number of extra days. The database is then checked to make sure the data exists. If it does, it's converted and exported to JSON behind the scenes, and the path to the file is provided to the user.

When running this app locally, the JSON files save to the exports/ directory in the root of the folder (as shown below). Sadly, this doesn't work the same on Heroku. If you copy and paste the provided path into the address bar in the browser, Heroku returns a 404. To get this to work properly on Heroku is outside the scope of this project.

![Export stats](docs/features/export.png)
![Exported stats as JSON](docs/features/exports-directory.png)

### Exceptions

Throughout the app, there are descriptive error messages that are displayed to the user should anything not go as planned. There are a few different inputs, such as strings, integers, and strings that need to be in a particular format (dates). Each has their own code that will raise an exception should the input be incorrect and redirect the user accordingly. See the example below.

There are also exceptions in place should anything go wrong with the database connection, or if data cannot be found.

![Example exception](docs/features/example-exception.png)

*Go back to the [top](#table-of-contents)*

---

## Technologies used

### Languages

- Python
- A little HTML/CSS

### Frameworks and tools

<details><summary>Research and planning</summary>
<ol>
   <li>VSCode (markdown)</li>
   <li>Code Institute lessons/notes</li>
</ol>
</details>

<details><summary>Development</summary>
<ol>
   <li>Git and GitHub</li>
   <li>VSCode</li>
   <li>Python libraries: pymongo, tabulate, certifi, pyfiglet</li>
</ol>
</details>

## Validation

### PEP8 validation

The [PEP8 Online](http://pep8online.com/) site was used to validate the Python of the app.

### Testing user stories

Sorry, I ran out of time to get this done before the submission time.

## Bugs

- BUG: FIXED: $round in the aggregator doesn't seem to work. Used Python instead.
- BUG: FIXED: Entering a number that isn't an option kicks you out of the program, when it should stay on the menu.
- BUG: FIXED: logging in after registering was returning False and kicking out of the program. Added login boolean.
- BUG: FIXED: Enter random string when asking for a date prompts the program to return "Please insert a number:". Added while loop.
- BUG: Typing something other than y/n at y/n questions will kick back to the menu.
- BUG: Registering will also log you in.

## Deployment

The website was deployed using GitHub to Heroku by following these steps:

1. Create an account at [heroku.com](https://.heroku.com/)
2. Create a new app, add app name and your region
3. Click on create app
4. Go to "Settings"
5. Under Config Vars, add your sensitive data (the MongoDB URL for example)
6. For this project, set buildpacks to <Python> and <NodeJS> in that order.
7. Go to "Deploy" and at "Deployment method", click on "Connect to Github"
8. Enter your repository name and click on it.
9. Choose the branch you want to buid your app from, and click "Deploy branch".

You can clone the repository by following these steps:

1. Go to the GitHub repository.
2. Locate the Code button above the list of files and click it.
3. Select if you prefere to clone using HTTPS, SSH, or Github CLI and click the copy button to copy the URL to your clipboard.
4. Open terminal locally.
5. Change the current working directory to the one where you want the cloned directory.
6. Type git clone and paste the URL from the clipboard ($ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY).
7. Press Enter to create your local clone.

## Python Libraries

### pymongo

### tabulate

### certifi

### pyfiglet

## Credits

### Code

- Reference for the menu structure: https://chunkofcode.net/how-to-implement-a-dynamic-command-line-menu-in-python/
- Reference for data classes: https://realpython.com/python-descriptors/

### Reference material

- MongoDB docs: https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
- Blog post on security to help with logins: https://martinheinz.dev/blog/59
- Blog post with hashlib: https://medium.com/@moinahmedbgbn/a-basic-login-system-with-python-746a64dc88d6
- Tabulate library for tables https://pypi.org/project/tabulate/
- Docs for setting up MongoDB with Heroku https://www.mongodb.com/developer/how-to/use-atlas-on-heroku/
- Blog post on errors and exceptions https://www.programiz.com/python-programming/exceptions
- Handy StackOverflow post to catch exceptions and see more info https://stackoverflow.com/questions/9823936/python-how-do-i-know-what-type-of-exception-occurred