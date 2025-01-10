import election
import copy

class hareVote(election.Vote):
    pass

class hareCandidate(election.Candidate):
    pass

def harequota(votes, seats):
    return votes / seats

def hare(votes, candidates, seats):
    hareVotes = copy.deepcopy(votes)
    hareCandidates = copy.deepcopy(candidates)
    totalVotes = 0
    awardedSeats = 0
    for vote in votes:
        totalVotes += vote.number
    quota = harequota(totalVotes, seats)
    for hareCandidate in hareCandidates:
        for hareVote in hareVotes:
            if hareVote.candidate == hareCandidate.name:
                hareCandidate.quotient = hareVote.number / quota
        hareCandidate.elected = int(hareCandidate.quotient)
        awardedSeats += hareCandidate.elected
        hareCandidate.quotient = hareCandidate.quotient % 1
    while awardedSeats < seats:
        winner = max(hareCandidates, key = lambda x : x.quotient)
        winner.elected += 1
        winner.quotient = 0
        awardedSeats += 1
    return hareCandidates