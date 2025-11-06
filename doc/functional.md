Instructions:
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


#### Who are the users?
Neuroscientist with domain expertise but limited coding experience. They know the basics of python and how to work with a database, but not how to build their own database. They understand these types of common scientific experimental paradigms but need a relatively streamlined coding interface to access and use the data. They are familiar with common types of analysis and machine learning/decoding but not necessarliy how to build or apply them to data.

#### What information does the user want?
The neuroscientist wants to be able to access the data in the same way for both datasets and be able to apply common analysis with a function call. There should additionally be clear infrastrucure to extend on if the neuroscientist wants to change the paramters of the analysis or implement new analysis on the same data. There should be some basic data visualization to understand the results.

#### Use cases?
The user will clone this library to their local computer system, follow the instructions for downloading data, and then familiarize themeselves with the data and built-in analysis by running a tutorial notebook that walks them through the database and existing analysis. This will then allow them to utilize the existing functions and database to ask more specific questions or extend analysis.