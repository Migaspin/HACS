import election
import copy

class hondtVote(election.Vote):
    pass

class hondtCandidate(election.Candidate):
    pass

def dhondtquotient(votes, seats):
    return votes / (seats + 1)

def dhondt(votes, candidates, seats):
    dHondtVotes = copy.deepcopy(votes)
    dHondtCandidates = copy.deepcopy(candidates)
    awardedseats = 0
    
    while awardedseats < seats:
        for dHondtCandidate in dHondtCandidates:
            dHondtCandidate.quotient = dhondtquotient(election.getVotesbyCandidate(dHondtCandidate.name, dHondtVotes), dHondtCandidate.elected)
        winner = max(dHondtCandidates, key = lambda x : x.quotient)
        winner.elected += 1
        awardedseats += 1
    return dHondtCandidates
