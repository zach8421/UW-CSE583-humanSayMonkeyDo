::::: site-header
:::: wrapper
[![](/images/logo.png){height="80px;"}Software Development for Data
Scientists (CSE 583)](/){.site-title}

[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMTggMTUiPgogICAgICAgICAgPHBhdGggZmlsbD0iIzQyNDI0MiIgZD0iTTE4LDEuNDg0YzAsMC44Mi0wLjY2NSwxLjQ4NC0xLjQ4NCwxLjQ4NEgxLjQ4NEMwLjY2NSwyLjk2OSwwLDIuMzA0LDAsMS40ODRsMCwwQzAsMC42NjUsMC42NjUsMCwxLjQ4NCwwIGgxNS4wMzFDMTcuMzM1LDAsMTgsMC42NjUsMTgsMS40ODRMMTgsMS40ODR6IiAvPgogICAgICAgICAgPHBhdGggZmlsbD0iIzQyNDI0MiIgZD0iTTE4LDcuNTE2QzE4LDguMzM1LDE3LjMzNSw5LDE2LjUxNiw5SDEuNDg0QzAuNjY1LDksMCw4LjMzNSwwLDcuNTE2bDAsMGMwLTAuODIsMC42NjUtMS40ODQsMS40ODQtMS40ODQgaDE1LjAzMUMxNy4zMzUsNi4wMzEsMTgsNi42OTYsMTgsNy41MTZMMTgsNy41MTZ6IiAvPgogICAgICAgICAgPHBhdGggZmlsbD0iIzQyNDI0MiIgZD0iTTE4LDEzLjUxNkMxOCwxNC4zMzUsMTcuMzM1LDE1LDE2LjUxNiwxNUgxLjQ4NEMwLjY2NSwxNSwwLDE0LjMzNSwwLDEzLjUxNmwwLDAgYzAtMC44MiwwLjY2NS0xLjQ4NCwxLjQ4NC0xLjQ4NGgxNS4wMzFDMTcuMzM1LDEyLjAzMSwxOCwxMi42OTYsMTgsMTMuNTE2TDE4LDEzLjUxNnoiIC8+CiAgICAgICAgPC9zdmc+)](#){.menu-icon}

::: trigger
[Home](/){.page-link} [Grading](/grading.html){.page-link}
[Projects](/projects.html){.page-link}
[Software](/software.html){.page-link}
[Syllabus](/syllabus.html){.page-link}
:::
::::
:::::

:::::: page-content
::::: wrapper
:::: post
::: post-header
# Projects {#projects .post-title}
:::

## Overview

The course project is a "capstone" that pulls together all elements of
the course: data, programming, coding style, version control, testing,
design, and team collaborations. This is a team effort, often with
members drawn from different disciplines.

Projects will address a science or business question of interest. For
example, a business question related to the bike sharing company Pronto
might be "How should bicycles be allocated among stations?" An
**analysis project** would seek data to answer this question directly.
However, you may choose not to answer the question yourself. Rather, you
might do a **tool project** that builds a tool to help others to answer
the question. For example, one such tool might be a package that better
organizes the Pronto data for analysis. Still another possibility is
that you will build a system that teaches others the skills needed to do
analysis, which we call an **instructional system project**. An example
here would be a system that teaches about logistics for businesses in
the sharing economy. Other types of projects are possible as well.

## Project Workflow

### Step 1: Pick Your Data

You should have two data sets so that you can demonstrate an ability to
join data with different characteristics (e.g., granularity in time
and/or space). The data must be available immediately, without concerns
about access rights for team members or the instructors.

### Ans:

#### Monkey Datasets:
https://dandiarchive.org/dandiset/000688

#### Human Datasets:
https://www.kaggle.com/competitions/brain-to-text-25/data

### Step 2: Define the Problem

Determine the type of project (e.g., analysis project) and the questions
of interest.

### Ans:
Both these datasets contain neural recordings from the same brain regions in motor cortex in macaque and human. The monkey data is during standard center out reaching task while the human recordings are taken during attempted speech. The goal of this project is to reformat the human dataset to resemble the trial structure during the reaching task and allow parallel analysis of reaching kinematics and tongue/mouth kinematics. We would like to apply 

### Step 3: Write the Functional Specification

#### Who are the users?
Neuroscientist with domain expertise but limited coding experience. They know the basics of python and how to work with a database, but not how to build their own database. They understand these types of common scientific experimental paradigms but need a relatively streamlined coding interface to access and use the data. They are familiar with common types of analysis and machine learning/decoding but not necessarliy how to build or apply them to data.

#### What information does the user want?
The neuroscientist wants to be able to access the data in the same way for both datasets and be able to apply common analysis with a function call. There should additionally be clear infrastrucure to extend on if the neuroscientist wants to change the paramters of the analysis or implement new analysis on the same data. There should be some basic data visualization to understand the results.

#### Use cases?
The user will clone this library to their local computer system, follow the instructions for downloading data, and then familiarize themeselves with the data and built-in analysis by running a tutorial notebook that walks them through the database and existing analysis. This will then allow them to utilize the existing functions and database to ask more specific questions or extend analysis.

### Steps 4 and beyond: Iteratively Develop And Refine the Project

#### Deliverables/Components:
1. Database
    a. Monkey database
        i. Function to reformat for easy use
    b. Human database
        i. Function to chunk data into trials
        ii. Function to convert phonemes into pseudo-kinematics
    c. Formated subset of data for examples
    d. Script to download and format full dataset
2. Analysis
    a. Movement onset detection
    b. Single neuron kinematic tuning
    c. Target position decoding
3. Visualization
    a. Graphically represent kinematics
    b. Peri-stimulus Spike rasters
    c. Decoding accuracy
    d. Tuning curves
4. Tutorial
    a. Downloading/formating walkthrough
    b. Dataset exploration/explanation
    c. Analysis examples

## Project Structure

Projects should have an online GitHub repository with the project name.
Top level folders/files within the repository include:

-   README.md file that gives an overview of the project
-   LICENSE file
-   setup.py file that initializes the project after it has been cloned
-   doc folder that contains documentation (including the functional
    specification, the design specification, and the final project
    presentation or poster)
-   python package folder (with the same name as the repository) that is
    structured as one or more python modules (e.g., with
    `__init__.py`{.language-plaintext .highlighter-rouge} files) and
    test files that begin with "test\_".
-   examples folder that contains examples of using the packages

## Design Documents

You will create two documents describing the design of your project.
These documents should be in your project `docs`{.language-plaintext
.highlighter-rouge} folder.

-   **Functional Specification**. The document should have the following
    sections:
    -   Background. The problem being addressed.
    -   User profile. Who uses the system. What they know about the
        domain and computing (e.g., can browse the web, can program in
        Python)
    -   Data sources. What data you will use and how it is structured.
    -   Use cases. Describing at least two use cases. For each,
        describe: (a) the objective of the user interaction (e.g.,
        withdraw money from an ATM); and (b) the expected interactions
        between the user and your system.
-   **Component Specification**. The document should have sections for.
    -   Software components. High level description of the software
        components such as: *data manager*, which provides a simplified
        interface to your data and provides application specific
        features (e.g., querying data subsets); and *visualization
        manager*, which displays data frames as a plot. Describe at
        least 3 components specifying: what it does, inputs it requires,
        and outputs it provides.
    -   Interactions to accomplish use cases. Describe how the above
        software components interact to accomplish at least one of your
        use cases.
    -   Preliminary plan. A list of tasks in priority order.

## Technology Review Presentation

The technology review is about making decisions about the choice of a
python library to address a technology need in the project. For example,
many projects make use of map visualizations. There are many python
libraries that support these visualizations such as
[Bokeh](https://bokeh.org/), [Plotly](https://plotly.com/python/), and
[googlemaps](https://pypi.org/project/googlemaps/). The libraries have
different capabilities, such as what (if any) interactions users can
have with the map. You will want to choose a library that: (a) addresses
the requirements of your project; (b) is compatible with other elements
of your project (e.g., runs on python 3); (c) is relatively easy to use;
(d) is computationally efficient for the scale of data you use; and (d)
doesn't have software bugs that will impair your use cases.

The technology review is a group presentation. It should be about 5-7
minutes in length. The presentation should address the following:

-   Brief background on the problem you're solving to motivate a
    technology for which you need a python library (e.g., interactive
    maps).
-   One slide description of a use case in which the technology is
    required.
-   One slide that describes at least two python libraries that
    potentially address your technology requirement.
-   One slide side-by-side comparisons of the technologies. This will
    require that you actually install and use the technologies.


### Technology review brainstorm:
1. Machine learning libraries: We will be using a library to perform Linear Discriminant Analysis, Logistic regression, PCA etc
    a. scikit-learn
    b. statsmodels
    c. Pytorch
2. Others??
3. Visualization/Database libraries
    a. NWB
    b. Spikeinterface
    c. Flatiron

## Final Project Presentation

We will likely use a poster presentation format for this year. In the
past, we have done oral presentations.

### Instructions for oral presentations (likely not for 2022)

Teams will present their projects using slides in 10 minute oral
presentation. The presentation should include:

-   Background. Describe the problem or area being addressed.
-   Data used. What data did you use? How was it obtained? What are its
    limitations?
-   Use cases. How users will interact with your system in a way that
    addresses the problem area.
-   Demo. Demonstrate your software.
-   Design. Describe the components and how they interact to accomplish
    the use cases.
-   Project Structure. Show the structure of your GitHub repository.
-   Lessons learned and future work. Focus on *software engineering*
    lessons.

You should post a PDF of your presentation in the docs folder of your
project.

## Grading Rubric

Projects will be evaluated based on the following criteria:

-   Organized as described in the section on project structure
-   Quality of the documentation (especially the functional
    specification and design specification)
-   Uses at least two data sources
-   Code quality, especially consistent coding standard (e.g.,
    `pylint`{.language-plaintext .highlighter-rouge}).
-   Test coverage
-   Quality of the example of using the package (in the examples folder
    of the project repository)
-   Implements continuous integration (e.g., via travis-CI), and all
    tests pass.
-   Completeness of the setup.py script
-   Creativity and technical challenge

## Examples of previous projects

These examples are fantastic, though they may not be perfect. They
should be considered examples of what kinds of projects are possible and
not necessarily exa mples to be precisely emulated. The examples below
include an analysis project, a visualization project and a reusable data
project.

### Spring, 2018

-   [Crash Data Analysis
    Tools](https://github.com/johnash1990/crashDataAnalysisTools) - This
    set of tools takes several different traffic data sets and merges
    them as well as providing an easy interface for interacting with the
    data.

### Spring, 2017

-   [First Stop](https://github.com/sliwhu/UWHousingTeam) - First Stop
    for First-time home buyers; This tool would be most helpful to
    first-time home buyers to set up expectations, plan budgets and make
    an informed decision on expenses before they even go through the
    exhaustive house-hunting process given current real-estate market
    status.
-   [Searching For
    Success](https://github.com/khyatiparekh/Searching-for-Success) is a
    template project that can help an amateur investor to visualize
    search trends on Google for selected company and get probability
    that the stock price will increase when the quarterly reports will
    be released for that company.
-   [Ax/Wx](https://github.com/rexthompson/axwx) - Ax/Wx is a collision
    and weather analysis tool that can enhance the WSP collision
    database with objective observations from nearby personal weather
    stations.
-   [HomeIn](https://github.com/hanghu/HomeIn) - HomeIn provides a
    visualization tool for housing data, prices, and crime rates on a
    multiple-layered map.
-   [How is Uber changing Taxi in New York
    City?](https://github.com/HWNi/DATA515-Project) Uber is a new riding
    model which connects drivers and passengers and provides
    ride-sharing service with a fair rate. This visualization tool
    enables user to analyze and compare Uber and taxi traffic of
    neighbors in NYC.
-   [AirbnbViz](https://github.com/wangbeiqi199159/AirbnbVizTool) aims
    to provide more information and insights to guests of Airbnb in
    Seattle to help them have a deeper understanding of what factors
    influence the listing price most, which neighborhood has
    higher/lower listing price and which neighborhood has higher and
    lower guests' rating via our different interactive visualizations.
    On the other hand, As hosts of Airbnb, they will have more ideas
    that how other hosts priced around them relative to dimensions such
    as amenities and location and what is the average listing prices of
    different neighborhoods in Seattle.

**ALL INFORMATION MUST BE POSTED TO YOUR REPO BY THE DEADLINE**
::::
:::::
::::::

::::::: wrapper
## Software Development for Data Scientists (CSE 583) {#software-development-for-data-scientists-cse-583 .footer-heading}

:::::: footer-col-wrapper
::: {.footer-col .footer-col-1}
-   Software Development for Data Scientists (CSE 583)
-   [](mailto:)
:::

::: {.footer-col .footer-col-2}
-   [[
    ![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMTYgMTYiPgogICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsPSIjODI4MjgyIiBkPSJNNy45OTksMC40MzFjLTQuMjg1LDAtNy43NiwzLjQ3NC03Ljc2LDcuNzYxIGMwLDMuNDI4LDIuMjIzLDYuMzM3LDUuMzA3LDcuMzYzYzAuMzg4LDAuMDcxLDAuNTMtMC4xNjgsMC41My0wLjM3NGMwLTAuMTg0LTAuMDA3LTAuNjcyLTAuMDEtMS4zMiBjLTIuMTU5LDAuNDY5LTIuNjE0LTEuMDQtMi42MTQtMS4wNGMtMC4zNTMtMC44OTYtMC44NjItMS4xMzUtMC44NjItMS4xMzVjLTAuNzA1LTAuNDgxLDAuMDUzLTAuNDcyLDAuMDUzLTAuNDcyIGMwLjc3OSwwLjA1NSwxLjE4OSwwLjgsMS4xODksMC44YzAuNjkyLDEuMTg2LDEuODE2LDAuODQzLDIuMjU4LDAuNjQ1YzAuMDcxLTAuNTAyLDAuMjcxLTAuODQzLDAuNDkzLTEuMDM3IEM0Ljg2LDExLjQyNSwzLjA0OSwxMC43NiwzLjA0OSw3Ljc4NmMwLTAuODQ3LDAuMzAyLTEuNTQsMC43OTktMi4wODJDMy43NjgsNS41MDcsMy41MDEsNC43MTgsMy45MjQsMy42NSBjMCwwLDAuNjUyLTAuMjA5LDIuMTM0LDAuNzk2QzYuNjc3LDQuMjczLDcuMzQsNC4xODcsOCw0LjE4NGMwLjY1OSwwLjAwMywxLjMyMywwLjA4OSwxLjk0MywwLjI2MSBjMS40ODItMS4wMDQsMi4xMzItMC43OTYsMi4xMzItMC43OTZjMC40MjMsMS4wNjgsMC4xNTcsMS44NTcsMC4wNzcsMi4wNTRjMC40OTcsMC41NDIsMC43OTgsMS4yMzUsMC43OTgsMi4wODIgYzAsMi45ODEtMS44MTQsMy42MzctMy41NDMsMy44MjljMC4yNzksMC4yNCwwLjUyNywwLjcxMywwLjUyNywxLjQzN2MwLDEuMDM3LTAuMDEsMS44NzQtMC4wMSwyLjEyOSBjMCwwLjIwOCwwLjE0LDAuNDQ5LDAuNTM0LDAuMzczYzMuMDgxLTEuMDI4LDUuMzAyLTMuOTM1LDUuMzAyLTcuMzYyQzE1Ljc2LDMuOTA2LDEyLjI4NSwwLjQzMSw3Ljk5OSwwLjQzMXoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)
    ]{.icon .icon--github}
    [UWSEDS]{.username}](https://github.com/UWSEDS)
-   [[
    ![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMTYgMTYiPgogICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsPSIjODI4MjgyIiBkPSJNMTUuOTY5LDMuMDU4Yy0wLjU4NiwwLjI2LTEuMjE3LDAuNDM2LTEuODc4LDAuNTE1YzAuNjc1LTAuNDA1LDEuMTk0LTEuMDQ1LDEuNDM4LTEuODA5CiAgICAgICAgICAgICAgICAgIGMtMC42MzIsMC4zNzUtMS4zMzIsMC42NDctMi4wNzYsMC43OTNjLTAuNTk2LTAuNjM2LTEuNDQ2LTEuMDMzLTIuMzg3LTEuMDMzYy0xLjgwNiwwLTMuMjcsMS40NjQtMy4yNywzLjI3IGMwLDAuMjU2LDAuMDI5LDAuNTA2LDAuMDg1LDAuNzQ1QzUuMTYzLDUuNDA0LDIuNzUzLDQuMTAyLDEuMTQsMi4xMjRDMC44NTksMi42MDcsMC42OTgsMy4xNjgsMC42OTgsMy43NjcgYzAsMS4xMzQsMC41NzcsMi4xMzUsMS40NTUsMi43MjJDMS42MTYsNi40NzIsMS4xMTIsNi4zMjUsMC42NzEsNi4wOGMwLDAuMDE0LDAsMC4wMjcsMCwwLjA0MWMwLDEuNTg0LDEuMTI3LDIuOTA2LDIuNjIzLDMuMjA2IEMzLjAyLDkuNDAyLDIuNzMxLDkuNDQyLDIuNDMzLDkuNDQyYy0wLjIxMSwwLTAuNDE2LTAuMDIxLTAuNjE1LTAuMDU5YzAuNDE2LDEuMjk5LDEuNjI0LDIuMjQ1LDMuMDU1LDIuMjcxIGMtMS4xMTksMC44NzctMi41MjksMS40LTQuMDYxLDEuNGMtMC4yNjQsMC0wLjUyNC0wLjAxNS0wLjc4LTAuMDQ2YzEuNDQ3LDAuOTI4LDMuMTY2LDEuNDY5LDUuMDEzLDEuNDY5IGM2LjAxNSwwLDkuMzA0LTQuOTgzLDkuMzA0LTkuMzA0YzAtMC4xNDItMC4wMDMtMC4yODMtMC4wMDktMC40MjNDMTQuOTc2LDQuMjksMTUuNTMxLDMuNzE0LDE1Ljk2OSwzLjA1OHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)
    ]{.icon .icon--twitter}
    [uwescience]{.username}](https://twitter.com/uwescience)
:::

::: {.footer-col .footer-col-3}
Course at the University of Washington, Software Development for Data
Scientists
:::
::::::
:::::::
