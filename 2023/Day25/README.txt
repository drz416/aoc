For part 1, I started creating a bruce force method that cut all combinations of 3 edges
    to find when the graph is split in 2
It worked for the sample set as it only had about 1000 combinations
But it didn't work for the data set as it had about a billion combinations
Also traversing the graph after each iteration was slow (an NP problem)

To solve part 1, I used code off of GitHub that plots network graphs, then I visualized my data
    and used the visual representation to easily find the 3 edges that split the graph in two