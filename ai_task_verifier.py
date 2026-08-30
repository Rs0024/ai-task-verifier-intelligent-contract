# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class TaskEscrow(gl.Contract):
    employer: Address
    worker: Address
    task_description: str
    reward_amount: u256
    evidence_url: str
    status: str
    
    # Internal Ledger for Escrow Mechanics
    employer_balance: u256
    worker_balance: u256
    escrow_balance: u256

    def __init__(
        self,
        employer: Address,
        worker: Address,
        task_description: str,
        reward_amount: u256
    ):
        self.employer = employer
        self.worker = worker
        self.task_description = task_description
        self.reward_amount = reward_amount
        self.evidence_url = ""
        self.status = "awaiting_deposit"
        
        # Initialize balances
        self.employer_balance = reward_amount
        self.worker_balance = u256(0)
        self.escrow_balance = u256(0)

    @gl.public.write
    def deposit_funds(self) -> None:
        if self.status != "awaiting_deposit":
            raise Exception("Funds already deposited or task in progress")
        
        # Lock funds in the escrow balance
        self.employer_balance -= self.reward_amount
        self.escrow_balance += self.reward_amount
        self.status = "pending"

    @gl.public.write
    def submit_work(self, evidence_url: str) -> None:
        if self.status != "pending":
            raise Exception("Task must be funded and pending before submission")
        self.evidence_url = evidence_url
        self.status = "submitted"

    @gl.public.write
    def verify_and_settle(self) -> None:
        if self.status != "submitted":
            raise Exception("No submission awaiting verification")
            
        task_desc = self.task_description
        url = self.evidence_url

        def leader_fn():
            page = gl.nondet.web.get(url)
            text = page.body.decode("utf-8", errors="ignore")[:8000]
            prompt = f"""
            Task Description: {task_desc}
            Evidence URL Content: {text}
            
            Evaluate if the evidence strictly satisfies the task description.
            Return ONLY JSON:
            {{
                "completed": true or false
            }}
            """
            return json.loads(gl.nondet.exec_prompt(prompt))

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            mine = leader_fn()
            theirs = leader_result.calldata
            
            # Consensus: all validators must agree on the boolean completion status
            return theirs.get("completed") == mine.get("completed")

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        # Escrow Settlement Logic based on Consensus
        if result.get("completed") is True:
            self.status = "released"
            self.escrow_balance -= self.reward_amount
            self.worker_balance += self.reward_amount
        else:
            self.status = "rejected"
            self.escrow_balance -= self.reward_amount
            self.employer_balance += self.reward_amount

    @gl.public.view
    def get_details(self) -> dict:
        return {
            "employer": str(self.employer),
            "worker": str(self.worker),
            "task_description": self.task_description,
            "reward_amount": str(self.reward_amount),
            "evidence_url": self.evidence_url,
            "status": self.status,
            "escrow_balance": str(self.escrow_balance),
            "worker_balance": str(self.worker_balance),
            "employer_balance": str(self.employer_balance)
        }
