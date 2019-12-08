class View:
    def __init__(self, view_number, leader):
        self.v = view_number
        self.leader = leader
        self.leader.propose(self)