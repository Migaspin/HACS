import election
import copy

class sainteLagueVote(election.Vote):
    pass

class sainteLagueCandidate(election.Candidate):
    pass

def saintelaguequotient(votes, seats):
    return votes / (2 * seats + 1)

def saintelague(votes, candidates, seats):
    sainteLagueVotes = copy.deepcopy(votes)
    sainteLagueCandidates = copy.deepcopy(candidates)
    awardedseats = 0
    
    while awardedseats < seats:
        for sainteLagueCandidate in sainteLagueCandidates:
            sainteLagueCandidate.quotient = saintelaguequotient(election.getVotesbyCandidate(sainteLagueCandidate.name, sainteLagueVotes), sainteLagueCandidate.elected)
        winner = max(sainteLagueCandidates, key = lambda x : x.quotient)
        winner.elected += 1
        awardedseats += 1
    return sainteLagueCandidates
