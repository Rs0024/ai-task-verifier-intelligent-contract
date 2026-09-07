# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json


@gl.evm.contract_interface
class Recipient:
    class View:
        pass

    class Write:
        pass


class TaskEscrow(gl.Contract):
    employer: Address
    worker: Address
    task_description: str
    reward_amount: u256
    evidence_url: str
    status: str

    def __init__(
        self,
        employer: str,
        worker: str,
        task_description: str,
        reward_amount: u256
    ):
        self.employer = Address(employer)
        self.worker = Address(worker)
        self.task_description = task_description
        self.reward_amount = reward_amount
        self.evidence_url = ""
        self.status = "created"

    @gl.public.write.payable
    def deposit(self) -> None:
        if gl.message.sender_address != self.employer:
            raise gl.vm.UserError("Only employer can fund escrow")

        if self.status != "created":
            raise gl.vm.UserError("Escrow already funded")

        if gl.message.value != self.reward_amount:
            raise gl.vm.UserError("Send exactly the configured reward amount")

        if gl.message.value == u256(0):
            raise gl.vm.UserError("Reward must be greater than zero")

        self.status = "funded"

    @gl.public.write
    def submit_work(self, evidence_url: str) -> None:
        if gl.message.sender_address != self.worker:
            raise gl.vm.UserError("Only worker can submit evidence")

        if self.status != "funded":
            raise gl.vm.UserError("Escrow must be funded first")

        self.evidence_url = evidence_url
        self.status = "submitted"

    @gl.public.write
    def verify_and_settle(self) -> None:
        sender = gl.message.sender_address

        if sender != self.employer and sender != self.worker:
            raise gl.vm.UserError(
                "Only employer or worker can trigger settlement"
            )

        if self.status != "submitted":
            raise gl.vm.UserError("No submitted work to verify")

        task_desc = self.task_description
        url = self.evidence_url

        def leader_fn():
            page = gl.nondet.web.get(url)
            text = page.body.decode(
                "utf-8",
                errors="ignore"
            )[:8000]

            prompt = f"""
Task Description:
{task_desc}

Evidence:
{text}

Determine whether the evidence clearly proves
the task was completed.

Return ONLY JSON:
{{"completed": true}}
or
{{"completed": false}}
"""

            return json.loads(
                gl.nondet.exec_prompt(prompt)
            )

        def validator_fn(leader_result) -> bool:
            if not isinstance(
                leader_result,
                gl.vm.Return
            ):
                return False

            mine = leader_fn()
            theirs = leader_result.calldata

            return (
                theirs.get("completed")
                == mine.get("completed")
            )

        result = gl.vm.run_nondet_unsafe(
            leader_fn,
            validator_fn
        )

        amount = self.reward_amount

        if result.get("completed") is True:
            self.status = "completed_and_paid"

            Recipient(
                self.worker
            ).emit_transfer(
                value=amount
            )

        else:
            self.status = "rejected_and_refunded"

            Recipient(
                self.employer
            ).emit_transfer(
                value=amount
            )

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_contract_balance(self) -> u256:
        return self.balance
