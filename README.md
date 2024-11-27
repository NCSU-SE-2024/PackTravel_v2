<div align="center">
  <img style="width: 120px; height: 120px;" src="./images/wolf2.svg" />
  <h1>NC State PackTravel</h1>
</div>

Welcome to PackTravel, your ultimate solution for escaping the confines of campus life and exploring the world beyond! 🚗💨 Tired of relying on the same old campus shuttle or waiting for a ride that never comes? Well, we've got your back!

PackTravel is here to revolutionize your off-campus travel experience, offering students without personal vehicles a hassle-free way to get where they need to go—whether it's a weekend getaway or just a quick trip to the nearest coffee shop (because let’s face it, sometimes the campus brew just doesn’t cut it). ☕🚀

Join our vibrant community, where convenience meets collaboration, and safety is always the top priority. With PackTravel, it’s not just about the ride—it’s about sharing the journey with fellow students, creating connections, and making your travel experience smarter and more fun!

So, pack your bags (or just your backpack), hop on board, and let’s make those off-campus adventures easier, cheaper, and a lot more exciting. Let’s get you where you need to go with PackTravel—your ride to freedom! 🌍🛣️


![alt text](https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/docs/HomePage.png)

NEW BADGES
missing badges:
1. codecov passing/failing
   
[![DOI](https://zenodo.org/badge/887482019.svg)](https://doi.org/10.5281/zenodo.14211208)
[![codecov](https://codecov.io/gh/KoruptTinker/PackTravel/graph/badge.svg?token=VbruFqYa0G)](https://codecov.io/gh/KoruptTinker/PackTravel)
[![Python Style Checker](https://github.com/NCSU-SE-2024/PackTravel_v2/actions/workflows/python_style_checker.yml/badge.svg)](https://github.com/NCSU-SE-2024/PackTravel_v2/actions/workflows/python_style_checker.yml)
[![Lint Python](https://github.com/NCSU-SE-2024/PackTravel_v2/actions/workflows/pylint.yml/badge.svg)](https://github.com/NCSU-SE-2024/PackTravel_v2/actions/workflows/pylint.yml)
[![Test cases](https://github.com/NCSU-SE-2024/PackTravel_v2/actions/workflows/testcases.yml/badge.svg)](https://github.com/NCSU-SE-2024/PackTravel_v2/actions/workflows/testcases.yml)
<a href="https://github.com/NCSU-SE-2024/PackTravel_v2/graphs/contributors" alt="Contributors"><img src = "https://img.shields.io/github/contributors/NCSU-SE-2024/PackTravel_v2"/></a>
<a href="https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/LICENSE" alt="License"><img src="https://img.shields.io/github/license/NCSU-SE-2024/PackTravel_v2" /></a>
<a href="https://github.com/NCSU-SE-2024/PackTravel_v2/issues" alt="Open Issues"><img src="https://img.shields.io/github/issues-raw/NCSU-SE-2024/PackTravel_v2" /></a>
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/NCSU-SE-2024/PackTravel_v2?style=plastic)
<a href="https://github.com/NCSU-SE-2024/PackTravel_v2/actions" alt="Build Status"><img src="https://img.shields.io/github/workflow/status/NCSU-SE-2024/PackTravel_v2/Build%20main" /></a>
[![Pull Requests](https://img.shields.io/github/issues-pr/NCSU-SE-2024/PackTravel_v2?style=for-the-badge)](https://github.com/NCSU-SE-2024/PackTravel_v2/pulls)
[![Commit Activity](https://img.shields.io/github/commit-activity/w/NCSU-SE-2024/PackTravel_v2?style=for-the-badge)](https://github.com/NCSU-SE-2024/PackTravel_v2/graphs/commit-activity)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/NCSU-SE-2024/PackTravel_v2)
<a href="https://github.com/NCSU-SE-2024/PackTravel_v2" alt="Repo Size"><img src="https://img.shields.io/github/repo-size/NCSU-SE-2024/PackTravel_v2"/></a>

## Pre-requisites
To run these scripts, you will require Python installed on your PC. Please visit [Python Installers](https://www.python.org/downloads/) to download the lastest python version. Apart from that, other requirements can be installed with the help of requirements.txt.

## Installation
Initially, you can check whether your system has Python pre-installed or not, usually nowadays in most of systems, be it Windows or MacOS, python is pre-installed. 

To check whether you have python installed or not, you can open CMD or a Terminal and run the command "python --version". If the CMD shows the version such as Python 3.10 then your system already has python installed and you just need to clone the repository and run the python scripts. 

If this is not the case, then you need to download python installer package from [Python Installers](https://www.python.org/downloads/) based on your system's operating system and install it and you can further clone this repository to execute the scripts.

You can refer [INSTALL.md](https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/INSTALL.md) for the complete installation steps based on your OS.

## Poster
![alt text](https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/docs/Poster.jpg)

## Contribution Code of Conduct

The rules listed below are to be followed by the ones who will be contributing to the code in the repository:

  - At least one review/approval is required from any other contributors of the project to merge a commit to the main branch.
  - It is recommended to delete the branch as soon as it is merged to the main branch to avoid stale branches in the repository.
  - It is encouraged to add name tags such as "feature-", "upd-" or "patch-" in the branches if it is used to add code patches or features in the project.

### Test Run Screenshot

![alt text](https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/docs/TestCasesRun.png)

### Code Coverage Screenshot

![alt text](https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/docs/CoverageRun.png)

### Discord Channel Screenshot
![alt_text](https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/docs/DiscordScreenshot.png)

### Video demonstrating the old functionalities
https://github.com/NCSU-SE-2024/PackTravel_v2/blob/main/docs/old%20Video.mp4

### Video demonstrating the new functionalities
TODO


### Issues in Previous Phase - 

- **Login and Logout Functionality**: The login and logout features were not functioning as expected; clicking on them did not trigger any action.
- **Unauthenticated Access**: Users were able to access several features, such as creating or searching for rides, without being logged in.
- **Homepage Background Image**: The background image on the homepage was not displaying correctly.
- **Database Updates**: The Users and Routes databases were not being updated properly.
- **Redirection After Login**: After logging in, users were not redirected to the correct homepage. Instead, they were directed to an index page.
- **Test Cases and Code Coverage**: The application lacked sufficient test cases, and the code coverage was inadequate, which limits the ability to detect errors and ensure system reliability.
- **Documentation Issues**: Several Python files lacked proper documentation, making it difficult to understand the code and its functionality.


# Quick look at the newly added features

* My Rides Section for Streamlined Ride Management:
A dedicated space where users can easily track, view, and delete the rides they've created. This feature offers enhanced convenience for managing personal rides, ensuring users have full control over their travel plans at all times.

* Popular Rides Section for Quick Access:
Users can now view the most frequently joined rides at a glance. This feature allows for quick discovery of popular travel options, helping users easily find and join well-frequented rides without hassle.

* Interactive Discussion Forum for Community Engagement:
The new discussion forum provides an interactive platform for users to share tips, exchange experiences, and discuss specific routes or trips. This fosters a vibrant community where users can collaborate and gain insights from fellow travelers.

* Email Notifications to Keep Users Informed:
Automated email alerts notify users when they successfully join a ride. This ensures users stay engaged and informed, with timely updates about their travel plans and any changes to the rides they are part of.

* Critical Bug Fixes for Improved User Experience:
Several key bugs have been resolved, including issues with login alerts, password confirmation mismatches, and background image loading problems. These fixes enhance the overall stability of the app, ensuring a smoother, more reliable user experience.


# Use Cases: 
1. Viewing My Rides
    * Actor: PackTravel User (Student)
    * Goal: View the rides they’ve created or joined.
    * Steps:
      - The user logs into the PackTravel platform.
      - They navigate to the "My Rides" section.
      - The system displays a list of their rides, including details such as ride time, destination, and participants.
      - The user selects a ride to view more detailed information.

    * Outcome: The user successfully tracks and views their rides, ensuring they are up to date with their travel plans.

2. Viewing Top Ride Picks
    * Actor: NCSU Student
    * Goal: Discover top-rated or highly recommended rides.
    * Steps:
      - The user logs into the PackTravel platform.
      - They navigate to the "Top Picks" section.
      - The system displays a list of top-rated or popular rides based on user feedback or ride popularity.
      - The user clicks on a ride for more information.
    * Outcome: The user easily discovers the best rides available, saving time in selecting a ride that suits their preferences.

3. Posting in the Discussion Forum
    * Actor: NCSU Student
    * Goal: Share travel experiences or discuss specific routes and trips with other users.
    * Steps:
      - The user logs into the PackTravel platform.
      - They access the "Discussion Forum" section.
      - The system displays a list of ongoing topics.
      - The user creates a new discussion topic or comments on an existing one.
      - The system updates the thread and notifies relevant users.
    * Outcome: The user contributes to the community by sharing their experiences or gaining insights on travel routes.

4. Viewing Latest Ride Options
    * Actor: NCSU Student
    * Goal: View the most recent ride options to different destinations.
    * Steps:
      - The user logs into the PackTravel platform.
      - They navigate to the "Latest Ride Options" section.
      - The system displays a list of new or upcoming rides to various locations.
      - The user can scroll through the list and select a ride that fits their schedule and destination.
    * Outcome: The user discovers fresh ride options and can quickly select a suitable ride for their trip.
  
5. Joining a Ride
    * Actor: PackTravel User (Student)
    * Goal: Join a ride that suits their destination and timing.
    * Steps:
      - The user logs into the PackTravel platform.
      - They browse or search for available rides to their desired destination.
      - The user selects a ride and clicks "Join."
      - The system confirms the user’s participation and updates the ride's participant list.
      - The user receives a confirmation notification about the ride.
Outcome: The user successfully joins a ride, ensuring a smooth and collaborative travel experience with fellow students.

6. Editing a Ride
    * Actor: PackTravel User (Student)
    * Goal: Edit an existing ride they created, such as adjusting the time or destination.
    * Steps:
      - The user logs into the PackTravel platform.
      - They navigate to the "My Rides" section.
      - The user selects a ride they have previously created.
      - The system allows them to edit details like the ride's time, destination, or available seats.
      - The user saves the changes, and the updated ride details are reflected in the system.
Outcome: The user successfully updates the ride information, allowing for better coordination with other participants.



**Built Using:**
</br>
<code><a href="https://www.python.org/" target="_blank"><img height="50" src="https://user-images.githubusercontent.com/111834635/194173533-37cd4997-55f3-4bb1-87bd-1a16a3af53aa.png"></a></code>
<code><a href="https://www.djangoproject.com/" target="_blank"><img height="50" src="https://user-images.githubusercontent.com/111834635/194172149-ff6a56be-3025-4d2c-8cdb-b9a7e3f87259.png"></a></code>
<code><a href="https://www.mongodb.com/" target="_blank"><img height="50" src="https://user-images.githubusercontent.com/111834635/194173280-628ecfc0-21ae-4870-8e22-711e6da83820.png"></a></code>
<code><a href="https://developer.mozilla.org/en-US/docs/Glossary/HTML5" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-ar21.svg"></a></code>
<code><a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/w3_css/w3_css-ar21.svg"></a></code>
<code><a href="https://www.javascript.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/javascript/javascript-ar21.svg"></a></code>
<code><a href="https://getbootstrap.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-ar21.svg"></a></code>



## Tools
- [Preetier Code Formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [JS-HTML-CSS Formatter](https://marketplace.visualstudio.com/items?itemName=lonefy.vscode-JS-CSS-HTML-formatter)
- [PyLint](https://pylint.org/)


## Roadmap
* [List of Roadmap and their corresponding open issues](https://github.com/NCSU-SE-2024/PackTravel_v2/issues)
  
## Team Members - Project 3
* Anish Dhage
* Gaurav Sheth
* Soham Gundewar
  


