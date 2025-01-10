import election
import copy

class droopVote(election.Vote):
    pass

class droopCandidate(election.Candidate):
    pass

def droopquota(votes, seats):
    return votes / (seats + 1)

def droop(votes, candidates, seats):
    droopVotes = copy.deepcopy(votes)
    droopCandidates = copy.deepcopy(candidates)
    totalVotes = 0
    awardedSeats = 0
    for vote in votes:
        totalVotes += vote.number
    quota = droopquota(totalVotes, seats)
    for droopCandidate in droopCandidates:
        for droopVote in droopVotes:
            if droopVote.candidate == droopCandidate.name:
                droopCandidate.quotient = droopVote.number / quota
        droopCandidate.elected = int(droopCandidate.quotient)
        awardedSeats += droopCandidate.elected
        droopCandidate.quotient = droopCandidate.quotient % 1
    while awardedSeats < seats:
        winner = max(droopCandidates, key = lambda x : x.quotient)
        winner.elected += 1
        winner.quotient = 0
        awardedSeats += 1
    return droopCandidates
