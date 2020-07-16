# GIULIA: Given Input factors, adjUst LIkert Acceptability judgments based on levels

This very simple script may come in handy if you are a linguist and need mock data to test your model on before collecting acceptability judgments from actual people.

Given the factors of your interest and their levels, it computes the factorial design of your experiment and provides smart, constraint-based judgments for every item thus generated for how many participants as you want.

## Getting started

The script should run on Python 3.0+ and does not have to be installed. Runs fine on Python 3.8.2 in Ubuntu 20.10.

### Prerequisites

You need the following packages to make the script work:

    argparse>=1.1
    doepy
    pandas>=0.25.3
    numpy>=1.17.4
    random
    
To install these packages in Python 3, make sure you have installed pip3 and run:    
    
    pip3 install <package>
    
## Running the script

Make sure you have the script and the input file within the same folder before starting.
