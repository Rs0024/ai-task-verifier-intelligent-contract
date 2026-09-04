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
    
    # A credible internal token ledger to simulate actual funding and withdrawal
    balances: TreeMap[Address, u256]
    escrowed_amount: u256

    def __init__(self, employer: Address, worker: Address, task_description: str, reward_amount: u256):
        self.employer = employer
        self.worker = worker
        self.task_description = task_description
        self.reward_amount = reward_amount
        self.evidence_url = ""
        self.status = "created"
        self.escrowed_amount = u256(0)
        
        # Mint initial tokens to the employer so they have real value to fund the escrow
        self.balances[employer] = reward_amount
        self.balances[worker] = u256(0)

    @gl.public.write
    def deposit(self) -> None:
        # Enforceable authorization
        if gl.msg.sender != self.employer:
            raise Exception("Only the assigned employer can deposit funds")
        if self.status != "created":
            raise Exception("Escrow is already funded or in progress")
        if self.balances[self.employer] < self.reward_amount:
            raise Exception("Insufficient token balance to fund escrow")
        
        # Value-bearing transfer: deduct tokens from employer and move to the escrow vault
        self.balances[self.employer] -= self.reward_amount
        self.escrowed_amount += self.reward_amount
        self.status = "funded"

    @gl.public.write
    def submit_work(self, evidence_url: str) -> None:
        # Enforceable authorization
        if gl.msg.sender != self.worker:
            raise Exception("Only the assigned worker can submit evidence")
        if self.status != "funded":
            raise Exception("Escrow must be funded before work is submitted")
            
        self.evidence_url = evidence_url
        self.status = "submitted"

    @gl.public.write
    def verify_and_settle(self) -> None:
        # Enforceable authorization: Only involved parties can trigger settlement
        if gl.msg.sender != self.employer and gl.msg.sender != self.worker:
            raise Exception("Only the employer or worker can trigger settlement")
        if self.status != "submitted":
            raise Exception("Work has not been submitted yet")
            
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
            return theirs.get("completed") == mine.get("completed")

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        # Credible value-bearing settlement path
        amount_to_settle = self.escrowed_amount
        self.escrowed_amount = u256(0)

        if result.get("completed") is True:
            # Pay the worker's ledger
            self.balances[self.worker] += amount_to_settle
            self.status = "completed_and_paid"
        else:
            # Refund the employer's ledger
            self.balances[self.employer] += amount_to_settle
            self.status = "rejected_and_refunded"

    @gl.public.view
    def get_details(self) -> dict:
        return {
            "status": self.status,
            "escrowed_vault": str(self.escrowed_amount),
            "employer_balance": str(self.balances[self.employer]),
            "worker_balance": str(self.balances[self.worker])
        }
