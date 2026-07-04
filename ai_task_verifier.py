from genlayer import IntelligentContract, Field, event

class AITaskVerifier(IntelligentContract):
    manager = Field(address=True)
    worker = Field(address=True)
    reward = Field(int, default=0)
    task_submitted = Field(bool, default=False)
    approved = Field(bool, default=False)

    @event
    def initialize(self, manager, worker, reward):
        self.manager = manager
        self.worker = worker
        self.reward = reward

    @event
    def submit_task(self):
        assert self.sender == self.worker, "Only worker can submit task"
        self.task_submitted = True

    @event
    def approve_task(self):
        assert self.sender == self.manager, "Only manager can approve"
        assert self.task_submitted, "Task not submitted yet"
        self.approved = True

    @event
    def release_reward(self):
        assert self.sender == self.manager, "Only manager can release reward"
        assert self.approved, "Task not approved yet"
        self.transfer(self.worker, self.reward)
