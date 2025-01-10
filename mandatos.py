from dhondt import dhondt
from saintelague import saintelague
from hare import hare
from droop import droop
from qpq import createVote, createCandidate, QPQ
import election
import os
import pandas as pd
import copy

totalSeats = 226
regularSeats = totalSeats
ano = "2024"

cwd = os.getcwd()
cwd = cwd + "\\data\\" + ano + "\\"

regionDirectory = cwd + "\\circulos.csv"

regionsDF = pd.read_csv(regionDirectory)

regionsNames = []
regionsPopulation = []

for _, row in regionsDF.iterrows():
    # Create an object using specific columns
    regionsNames.append(election.Candidate(row["district"]))
    regionsPopulation.append(election.Vote(row["district"], row["voters"]))

continueFlag = True

while continueFlag:
    regularSeats -= 1
    regionResults = droop(regionsPopulation, regionsNames, regularSeats)

    foo = 0
    bar = 0
    for candidate in regionResults:
        bar += candidate.elected
        foo += (candidate.elected**7/regularSeats)**(1/8)

    continueFlag = not(totalSeats**(3/4) >= foo)

print(regularSeats)
print(totalSeats - regularSeats)