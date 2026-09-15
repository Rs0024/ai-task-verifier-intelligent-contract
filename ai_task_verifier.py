# v0.3.0
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }

import genlayer as gl


class TaskEscrow(gl.contract.Contract):
    employer: str
    worker: str
    task_description: str
    reward_amount: str
    evidence_url: str
    status: str

    def __init__(
        self,
        employer: str,
        worker: str,
        task_description: str,
        reward_amount: str,
    ):
        self.employer = employer
        self.worker = worker
        self.task_description = task_description
        self.reward_amount = reward_amount
        self.evidence_url = ""
        self.status = "created"

    @gl.public.write
    def mark_funded(self) -> None:
        self.status = "funded"

    @gl.public.write
    def submit_work(self, evidence_url: str) -> None:
        if self.status != "funded":
            raise gl.UserError("Task must be funded first")

        self.evidence_url = evidence_url
        self.status = "submitted"

    @gl.public.write
    def verify_task(self) -> None:
        if self.status != "submitted":
            raise gl.UserError("Submit work first")

        task = self.task_description
        evidence_url = self.evidence_url

        def leader_fn():
            page = gl.nondet.web.get(evidence_url)

            evidence_text = page.body.decode(
                "utf-8",
                errors="ignore",
            )[:8000]

            prompt = f"""
You are an independent task verifier.

TASK:
{task}

SUBMITTED EVIDENCE:
{evidence_text}

Decide whether the evidence clearly proves
that the stated task was completed.

Do not approve evidence merely because a URL exists.
Judge the actual evidence content.

Return JSON only:

{{"completed": true}}

or

{{"completed": false}}
"""

            return gl.nondet.exec_prompt(
                prompt,
                response_format="json",
            )

        def validator_fn(leader_result) -> bool:
            if not isinstance(
                leader_result,
                gl.vm.Return,
            ):
                return False

            my_result = leader_fn()

            return (
                my_result.get("completed")
                == leader_result.calldata.get("completed")
            )

        result = gl.vm.run_nondet_unsafe(
            leader_fn,
            validator_fn,
        )

        if result.get("completed") is True:
            self.status = "approved"
        else:
            self.status = "rejected"

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_evidence_url(self) -> str:
        return self.evidence_url

    @gl.public.view
    def get_task_description(self) -> str:
        return self.task_description

    @gl.public.view
    def get_reward_amount(self) -> str:
        return self.reward_amount
