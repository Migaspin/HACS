class Candidate():
    def __init__(self, name, elected = 0):
        self.name = name
        self.elected = elected
        self.quotient = 0

class Vote():
    def __init__(self, order, number):
        self.order = order.split()
        self.top = 0
        self.number = number
    @property
    def candidate(self):
        return self.order[self.top]

def getVotesByVotes(selectedVotes, votes):
    answer = 0
    for selectedVote in selectedVotes:
        answer += votes[selectedVote].number
    return answer

def selectVotesByCandidate(candidate, votes):
    answer = []
    for i in range(len(votes)):
        if votes[i].candidate == candidate:
            answer.append(i)
    return answer

def getVotesbyCandidate(candidate, votes):
    return getVotesByVotes(selectVotesByCandidate(candidate, votes), votes)

def getElected(candidates):
    answer = 0
    for candidate in candidates:
        answer += candidate.elected
    return answer

def getCandidateByName(name, candidates):
    for candidate in candidates:
        if candidate.name == name:
            return candidate