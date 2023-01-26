import smartpy as sp
class Election(sp.Contract):
    def __init__(self):
        #this is to conduct an election for 2 candidates
        self.init(
            election_is_open=False,
            nomination_is_open=False,
            election_admin=sp.sender,
            candidates_votes=sp.map(tkey=sp.TAddress, tvalue=sp.TNat),
            security_deposit=sp.tez(0),
            voted=sp.set()
        )
    @sp.entry_point
    def set_security_deposit(self, value):
        sp.verify(sp.sender == self.data.election_admin, "Only election admin can change security deposit amount")
        sp.verify(~self.data.nomination_is_open, "Security deposit amount cannot be changed when nominations are open")
        sp.verify(~self.data.election_is_open, "Security deposit amount cannot be changed when election is open")
        self.data.security_deposit=sp.tez(value)
    @sp.entry_point
    def start_nomination(self):
        sp.verify(self.data.election_admin==sp.sender, "Only admin can allow to start nomination")
        sp.verify(~self.data.nomination_is_open, "Nomination is already open")
        sp.verify(~self.data.election_is_open, "Nomination cannot be started when election is getting conducted")
        sp.verify(self.data.security_deposit==sp.amo)
        self.data.nomination_is_open=True
    
    @sp.entry_point
    def file_nomination(self):
        sp.verify(~self.data.nomination_is_open, "Nominations are closed")
        sp.verify(~self.candidates_votes.contains(sp.sender), "Candidate already nominated! Cannot be nominated again.")
        sp.verify(sp.amount== security_deposit, "Send correct amount for nomination {}".format(self.data.security_deposit))
        self.data.candidates_votes[sp.sender]=0
    
    @sp.entry_point
    def start_election(self):
        sp.verify(sp.sender== self.data.election_admin, "Only an admin can start an election")
        sp.verify(~self.data.election_is_open, "Election is already open")
        self.data.nomination_is_open=False
        self.data.election_is_open=True

    @sp.entry_point
    def vote(self, candidate):
        sp.verify(~self.data.voted.contains(sp.sender), "Double voting not allowed")
        sp.verify(self.data.candidates_votes.contains(candidate), "This candidate has not filed any nomination")
        self.data.candidates_votes[candidate]+=1
        sp.data.voted.add(sp.sender)

        
