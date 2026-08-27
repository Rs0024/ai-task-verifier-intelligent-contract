# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


class TaskEscrow(gl.Contract):

    worker: Address
    task_description: str
    reward_amount: u256
    evidence_url: str
    status: str

    def __init__(
        self,
        worker: Address,
        task_description: str,
        reward_amount: u256
    ):
        self.worker = worker
        self.task_description = task_description
        self.reward_amount = reward_amount
        self.evidence_url = ""
        self.status = "pending"

    @gl.public.write
    def submit_work(self, evidence_url: str) -> None:
        if self.status != "pending":
            raise Exception("Task already submitted or settled")
        self.evidence_url = evidence_url
        self.status = "submitted"

    @gl.public.write
    def verify_and_settle(self) -> None:
        if self.status != "submitted":
            raise Exception("No submission awaiting verification")
        task_description = self.task_description
        evidence_url = self.evidence_url

        def judge_completion() -> bool:
            page_content = gl.nondet.web.get(evidence_url, mode="text")
            result = gl.nondet.exec_prompt(
                "Task: " + task_description + " Evidence: " + page_content + " Completed? True or False only."
            )
            return "true" in result.lower()

        approved = gl.eq_principle_prompt_comparative(
            judge_completion,
            criteria="Validators must agree whether evidence satisfies the task.",
        )
        if approved:
            self.status = "released"
        else:
            self.status = "rejected"

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_details(self) -> dict:
        return {
            "worker": str(self.worker),
            "task_description": self.task_description,
            "reward_amount": self.reward_amount,
            "evidence_url": self.evidence_url,
            "status": self.status,
        }
