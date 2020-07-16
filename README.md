# GIULIA: Given Input factors, adjUst LIkert Acceptability judgments based on factor levels

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

### Input file

The script takes as input a tab-separated header-less file containing, for each line, the name of each factors and of its levels.

For instance, if you want to run a 2x2 experiment having telicity (levels = telic, atelic) and perfectivity (levels = perf, imperf) as factors, you would input:

| | | |
|-|-|-|
| telicity | telic | atelic
| perfectivity | perf | imperf

### Parameters

You may pass several optional parameters to the script:

    --factors, -f:       file containing your factors and levels of interest (defaults to input_factors.csv)
    --participants, -p:  number of participants to the experiment (defaults to 25)
    --output, -o:        output file with mock judgments (defaults to mock_judgments.csv)
    
To access the list of parameters in your terminal, run:    
    
    python3 giuliaJudgs.py -h

## How does it work?

It's easier done than said. First of all, it computes your factorial design (a.k.a. Cartesian product) using the awesome [DOEpy package](https://doepy.readthedocs.io/en/latest/) by Dr. Tirthajyoti Sarkar. Beware: it converts strings to numbers, so given the input provided before, you would get:

telicity | perfectivity
|-|-|
1 | 0
0 | 0
1 | 1
0 | 1

Then, the script creates a column for each participant, forcing them to provide high judgments (only 7s, since I'm using a 7-point Likert scale, or 6s and 7s if you comment a line). Say you have 3 participants:

telicity | perfectivity | prtp1 | prtp2 | prtp3
|-|-|-|-|-|
1 | 0 | 6 | 7 | 6
0 | 0 | 7 | 7 | 6
1 | 1 | 6 | 6 | 6
0 | 1 | 6 | 7 | 7

Then, the script updates these judgments based on the levels in your factors. In particular, for each line, it subtracts from each judgment the sum of the level values. It assumes that you want your 0-levels to make the sentences more acceptable than the 1-levels, the 1-levels more acceptable than the 2-levels (if any), and so on. The output will be:

telicity | perfectivity | prtp1 | prtp2 | prtp3
|-|-|-|-|-|
1 | 0 | 5 | 6 | 5
0 | 0 | 7 | 7 | 6
1 | 1 | 5 | 5 | 5
0 | 1 | 5 | 6 | 6

Now we add some noise in the data, replacing 20% of judgment values with random values within the Likert scale, and save the Pandas DataFrame to a csv file.

Done! May it provide optimal input for all your testing needs :mortar_board:
