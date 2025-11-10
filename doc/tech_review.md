# Instructions
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


## Format From Class Slides:

Next Tue. every project will present
Max 5 minutes – Natalie will cut you off

Everyone in the team will speak
- 1 min for intro and background including the three competing technologies you choose
- 1 min for tech option 1
- 1 min for tech option 2
- 1 min for tech option 3
- 1 min for summary of selection

# Brainstorm

### Technology review brainstorm:
1. Machine learning libraries: We will be using a library to perform Linear Discriminant Analysis, Logistic regression, PCA etc
    a. scikit-learn
    b. pynapple
    c. ???
2. Others??
3. Visualization/Database libraries
    a. NWB
    b. Spikeinterface
    c. Flatiron


# Selection: Scientic Computing toolbox
Script: ~100-150 words for ~1 minute of speech

## Background
We are attempting to understand the relationship between a neural dataset and behavioral dataset.  In the case of the monkey dataset, we are relating neural activity to hand movements and for the humans we are relating neural activity to elements of speech like tongue position and lip movement. There are a lot of potential computational techniques for relating these different types of data, so we've selected three common analysis that we're going to focus on for our project.  
Decoding movement onset with a classifier, tuning curve analysis that reveals directional preference of single neurons, and target decoding from neural population. We're going to evaluate each of the following potential libraries for whether they support these three analysis, how well they apply to the data 'out of the box' and how much potential for growth and new analysis for our end users.

Questions to answer:

1. Ease of use: is the library setup to work with neural data? Will we have to builda lot of code to format properly for the inputs/ouputs?

2. Movement detection: How well does the toolbox support logisitic, linear, or bayesian classifier. You train it by feeding 'motionless' neural data and 'movement' neural data that is labeled then testing it on held out data. Explanation of logisitc regression: https://compneuro.neuromatch.io/tutorials/W1D3_GeneralizedLinearModels/student/W1D3_Tutorial2.html

3. Tuning curve: Basically fitting a cosine equation to a set of firing rates/directions to show how well a single neuron responds to 'up' vs 'down'. Explanation: https://openbooks.library.northwestern.edu/neuroscienceconcepts/chapter/tuning-curves/ 

4. Similar to 1, just slightly more complicated in execution. See explanaintion in question 1, extended to multiple targets instead of only binary. 

5. Does it support new analysis for the user to explore?

## Scikit-learn
1. Sort of? Maybe medium on this one?
2. Yes, has linear and logisitc regression packages built in
3. Not prebuilt in, but we can construct it
4. Yes I think?

## Pynapple
1. Yes
2. Yes but only bayseian? Haven't looked through in that much detail
3. Yes built in
4. I think so?
5. Yes has more advanced analysis integrated into the package

## ???


## Summary and Conclusion
