# WorkItOut

(Developer: Darrach Barneveld)

![Mockup image](documentation/images/hero-image.png)

[WorkItOut Live Page](https://work-it-out-066ec18b52ea.herokuapp.com/)

WorkItOut is an all-in-one fitness app that allows you to enter and track your workouts effortlessly. It also provides personalized nutritional information based on your diet goals, including your BMI, daily calorie intake, and recommended macros. Stay on top of your fitness journey with WorkItOut's intuitive features and achieve a healthier lifestyle with ease.

## Table of Contents

1. [Project Goals](#project-goals)
   1. [Business Goals](#business-goals)
   2. [User Goals](#user-goals)
2. [UX](#UX)
   1. [Target Audience](#target-audience)
   2. [User Requirements and Expectations](#user-requirements-and-expectations)
   3. [User Stories](#user-stories)
   4. [Flow Chart](#flow-chart)
3. [Design](#design)
4. [Features](#features)
   1. [Current Features](#current-features)
   2. [Potential Features](#potential-features)
5. [Testing](#testing)
6. [Bugs](#Bugs)
7. [Deployment](#deployment)
8. [Credits](#credits)
9. [Technologies Used](#credits)
10. [Acknowledgements](#acknowledgements)

## Project Goals
The primary goal of WorkItOut is to provide an concise applicaion that allows users to easily enter and track their workouts. It also helps users develop a heavily life style by using a comprehensive nutrition database to offer customized nutritional information based on user and thier goals.

### Business Goals
1. The primary business goal for the WorkItOut app is to attract a significant number of users who are interested in fitness and nutrition.
2. Build a strong brand presence: Develop a strong brand identity for WorkItOut through consistent branding, engaging content, and positive user experiences.
3. Gather user data for research and insights: Leverage the anonymized and aggregated user data to conduct research and gain valuable insights into fitness trends, user preferences, and behavior patterns.
4. Expand the app's functionality and features: Continuously enhance and expand the app's capabilities to cater to the evolving needs of users.

### User Goals
1. Users want to set specific fitness goals, such as weight loss, muscle gain, or improved endurance, and track their progress over time. 
2. Users expect the app to have an intuitive and user-friendly interface that is easy to navigate and understand.
3. Users want the ability to track their workout performance, frequency and durations.
4. Users expect the ability to track dietary goals and get a better understanding of recommended nutritional information that is customised based on their current profile.
5. Users expect the app to continually evolve and improve based on user feedback and emerging fitness trends

[Back to Table of Contents](#table-of-contents)

## UX

### Target Audience
1. Individuals who are passionate about fitness, exercise, and maintaining an active lifestyle. 
2. People who prioritize their health and well-being.
3. Individuals who aim to lose weight, build muscle, or transform their bodies.


### User Requirements and Expectations
1. Users expect an intuitive and easy-to-navigate interface that allows them to quickly access and utilize the app's features.
2. Users require the ability to enter and track their workouts
3. Users require a log or history of their workouts for reference and progress tracking
4. Users expect the app to offer tools for tracking their daily food intake, including calories, macronutrients, and other nutritional information.

### User Stories

#### Website/Business Owner:
1. As a website/business owner, I want to attract a large user base to my fitness app website. 
2. As a website/business owner, I want to continuously improve the app based on user feedback.
3. As a website/business owner, I want to build a strong brand presence for the app. 


#### New Users:
1. As a new user, I want to easily understand the purpose and benefits of the fitness app.
2. As a new user, I want a simple and intuitive sign-up process.
3. As a new user, I want to track my progress easily. I expect the website to have a user-friendly interface that allows me to log my workouts., track my nutrition, and view my progress in a visually appealing and understandable format.
4. As a new user, I want to track my nutrition easily. I wish to have custom breakdowns that are tailored to my fitness goals displayed in an understandable format.

#### Existing Users:
1. As an existing user, I want the option to easily log into my account.
2. As an existing user, I want to track my ongoing progress. 
3. As an existing user, I want the app to continuously improve based on user feedback.
4. As an existing user, I want to be able to easily gain insight to my nutrition plan based on my current metrics.

[Back to Table of Contents](#table-of-contents)

## Design

As this was a terminal-based project colours were crafted using [Colourma](https://pypi.org/project/colorama/) which that provided a palette of colors to be used in the text. The website incorporated prominent colors such as red, blue, yellow, green, and white to create an engaging and visually appealing interface.

The intro hero banner was created using Ascii. The tool [Patrojk](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20) was used to convert text to a font in Ascii format so as to be printed to the terminal.

To present data in a clear and organized manner, the website utilized the [Tabulate](https://pypi.org/project/tabulate/) library, which allowed for easy formatting and creation of tables that were easy to read and comprehend. 

The combination of well-chosen colors and structured data tables enhanced the overall user experience and usability of the website.

[Back to Table of Contents](#table-of-contents)

## Features

### Current Features

1. Enter workout details:  Users can input the type of exercise performed and the duration to accurately track their workouts.
2. View all workouts: Users have access to a comprehensive view of their logged workouts, allowing them to review their workout history and monitor their progress.
3. BMI calculator: Calculator that enables users to calculate their Body Mass Index as an indicator of their overall health and fitness level.
4. Recommended calorie intake: Based on users' diet goals (weight loss, maintenance, or muscle gain), the application provides personalized recommendations for daily calorie intake to support their nutrition objectives.
5. Recommended macros: Customized macronutrient ratios (protein, carbohydrates, and fats) based on users' weight, height, age, gender and activity level, helping them optimize their nutrition and meet their fitness goals.

### Potential Features
1. Workout plans: Offer pre-designed workout plans tailored to different fitness goals, such as weight loss, muscle gain, or overall fitness. Users can follow these plans for structured and guided training.
2. Customizable meal plans: Provide the option to create personalized meal plans based on dietary preferences, restrictions, and fitness goals. Offer suggestions for balanced meals and portion sizes.
3. Nutritional tracking and logging: Allow users to log their daily food intake, track calories, macronutrients, and micronutrients, and view nutritional breakdowns for meals and snacks.

### Testing user stories



[Back to Table of Contents](#table-of-contents)

## Testing

### Testing user stories

#### Website/Business Owner

#### New Users:

#### Existing Users:


[Back to Table of Contents](#table-of-contents)

## Bugs

1. As of testing no bugs have been found. All bugs have been addressed via testing and consistant use of sites multiple features.

[Back to Table of Contents](#table-of-contents)

## Deployment

Code Institute Python Essentials Template for creating a terminal UI where the python code will generate its output to the user. 

Steps to reproduce:

1. Visit the [Code Institute Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template) and select use this template.
2. Select create a new repository.

### Deploying on Heroku

1. Create a Heroku account. 
2. Sign up with a student account for credits. (optional)
3. Once logged in select create new app.
4. Select an app name and region.
5. Select deployment method as connect to github.
6. Find the repo containing the python code created with the CI template and connect it.
7. Enable automatic deploys and select the main branch
8. In the settings tab select reveal config vars. Input the required hidden variables.
9. For this project a creds.json and RAPID_API_HOST, RAPID_API_KEY were created as config vars.
10. Select nodejs and python as the buildpack.
11. Deploy.

### Fork The Repository

1. Go to the GitHub repository
2. Click on Fork button in the upper right-hand corner
3. Edit the repository name and description if desired
4. Click the green create fork button

### Clone The Repository

1. Go to the GitHub repository
2. Locate the green Code button above the list of files and click it
3. Select if you prefer to clone using HTTPS, SSH, or Github CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash
5. Change the current working directory to the one where you want the cloned directory
6. Type git clone and paste the URL from the clipboard ($ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY)
7. Press Enter to create your local clone.

### Run The Repository Locally

1. Go to the GitHub repository
2. Locate the green Code button above the list of files and click it
3. From the dropdown menu select download Zip.
4. Download and open the zip file to run in an editor


[Back to Table of Contents](#table-of-contents)

## Credits

### Images

- Background Image [Background Image](https://slidesdocs.com/background/sports-running-dynamic-powerpoint-background_8c2cfd71f0)

### Favicon

- Favicon Barbell Image [Flaticon](https://www.flaticon.com/free-icon/barbell_2936886?term=gym&page=1&position=15&origin=tag&related_id=2936886)


### Code
Credit to [Berat Zorlu](https://github.com/beratzorlu/python-quiz) for the typing animation and colours. By understanding his code I was able to implement a typing and colour scheme to my project. 

Credit to [useriasminna](https://github.com/useriasminna/american_pizza_order_system) for the clearing console commands to give a fresh terminal screen to present user data.

Credit to [Dr Angela Yu](https://www.udemy.com/course/100-days-of-code/) and 100 days of Python for a greater understanding of error handling in python.

Credit to [Pylint](https://pylint.readthedocs.io/en/stable/) for helping me to indent and format code, document functions and modules and to follow python best practices.

[Back to Table of Contents](#table-of-contents)


## Technologies Used

- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [VS Code](https://code.visualstudio.com/)
- [Favicon.io - favicon generator](https://favicon.io/)
- [Coolors - Theme generator](https://coolors.co/)
- [Chat-GPT](https://chat.openai.com/)
- [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/)
- [W3C Markup Validation Service](https://validator.w3.org/)
- [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
- [PEP8 Validator](http://ww1.pep8online.com/)
- [Lucid Chart](https://www.lucidchart.com/)
- [Heroku](https://heroku.com/)



[Back to Table of Contents](#table-of-contents)


## Acknowledgements

[Back to Table of Contents](#table-of-contents)
