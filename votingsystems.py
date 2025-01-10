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
compensationSeats = 79
regularSeats = totalSeats - compensationSeats
ano = "2024"

def sumElected(results):
    elected_counts = {}
    tempCandidates = copy.deepcopy(allCandidates)
    for result_list in results:
        for candidate in result_list:
            if candidate.name not in elected_counts:
                elected_counts[candidate.name] = 0
            elected_counts[candidate.name] += candidate.elected
    
    for candidate in tempCandidates:
        if candidate.name in elected_counts:
            candidate.elected = elected_counts[candidate.name]
    return tempCandidates

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

regionResults = dhondt(regionsPopulation, regionsNames, regularSeats)

regions = {region.name:region.elected for region in regionResults}

allCandidates = []
dHondtResults = []
sainteLagueResults = []
hareResults = []
droopResults = []

temporaryVotes = {}
allVotes = []

for region in regions:
    path = cwd + region + ".csv"
    data = pd.read_csv(path)
    candidates = []
    votes = []
    for _, row in data.iterrows():
        # Create an object using specific columns
        candidates.append(election.Candidate(row["Party"]))
        votes.append(election.Vote(row["Party"], row["Votes"]))
    
    for vote in votes:
        if vote.candidate not in temporaryVotes:
            temporaryVotes[vote.candidate] = 0
        temporaryVotes[vote.candidate] += vote.number
    
    all_candidate_names = {candidate.name for candidate in allCandidates}
    allCandidates.extend([candidate for candidate in candidates if candidate.name not in all_candidate_names])    
    dHondtResults.append(dhondt(votes, candidates, regions[region]))
    sainteLagueResults.append(saintelague(votes, candidates, regions[region]))
    hareResults.append(hare(votes, candidates, regions[region]))
    droopResults.append(droop(votes, candidates, regions[region]))

## Circulo de Compensação

for temporaryVote in temporaryVotes:
    allVotes.append(election.Vote(temporaryVote, temporaryVotes[temporaryVote]))

dHondtFinals = sumElected(dHondtResults)
sainteLagueFinals = sumElected(sainteLagueResults)
hareFinals = sumElected(hareResults)
droopFinals = sumElected(droopResults)

dHondtIdeals = dhondt(allVotes, allCandidates, totalSeats)
sainteLagueIdeals = saintelague(allVotes, allCandidates, totalSeats)
hareIdeals = hare(allVotes, allCandidates, totalSeats)
droopIdeals = droop(allVotes, allCandidates, totalSeats)

dHondtCompensations = []
sainteLagueCompensations = []
hareCompensations = []
droopCompensations = []

for dHondtIdeal in dHondtIdeals:
    for dHondtFinal in dHondtFinals:
        if dHondtFinal.name == dHondtIdeal.name:
            dHondtCompensations.append(election.Candidate(dHondtFinal.name, dHondtIdeal.elected - dHondtFinal.elected))

for sainteLagueIdeal in sainteLagueIdeals:
    for sainteLagueFinal in sainteLagueFinals:
        if sainteLagueFinal.name == sainteLagueIdeal.name:
            sainteLagueCompensations.append(election.Candidate(sainteLagueFinal.name, sainteLagueIdeal.elected - sainteLagueFinal.elected))

for hareIdeal in hareIdeals:
    for hareFinal in hareFinals:
        if hareFinal.name == hareIdeal.name:
            hareCompensations.append(election.Candidate(hareFinal.name, hareIdeal.elected - hareFinal.elected))

for droopIdeal in droopIdeals:
    for droopFinal in droopFinals:
        if droopFinal.name == droopIdeal.name:
            droopCompensations.append(election.Candidate(droopFinal.name, droopIdeal.elected - droopFinal.elected))

for i in range(compensationSeats):
    dHondtWinner = max(dHondtCompensations, key=lambda x: x.elected)
    dHondtWinner.elected -= 1
    for dHondtFinal in dHondtFinals:
        if dHondtFinal.name == dHondtWinner.name:
            dHondtFinal.elected += 1

    sainteLagueWinner = max(sainteLagueCompensations, key=lambda x: x.elected)
    sainteLagueWinner.elected -= 1
    for sainteLagueFinal in sainteLagueFinals:
        if sainteLagueFinal.name == sainteLagueWinner.name:
            sainteLagueFinal.elected += 1

    hareWinner = max(hareCompensations, key=lambda x: x.elected)
    hareWinner.elected -= 1
    for hareFinal in hareFinals:
        if hareFinal.name == hareWinner.name:
            hareFinal.elected += 1

    droopWinner = max(droopCompensations, key=lambda x: x.elected)
    droopWinner.elected -= 1
    for droopFinal in droopFinals:
        if droopFinal.name == droopWinner.name:
            droopFinal.elected += 1

# Resultados

votingsystems = {"dHondt":dHondtFinals, "Sainte Lague":sainteLagueFinals, "Hare":hareFinals, "Droop":droopFinals}

print("")
print("+", ano)

for votingsystem in votingsystems:
    print("")
    print("-", votingsystem)

    for candidate in votingsystems[votingsystem]:
        print(f"{candidate.name}: {candidate.elected}")
        
