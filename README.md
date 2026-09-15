# TaskEscrow — AI-Verified Task Completion on GenLayer

TaskEscrow is a GenLayer Intelligent Contract that uses AI and validator consensus to verify whether submitted web evidence proves that a task was completed.

The project demonstrates an onchain workflow for task creation, funding-state tracking, evidence submission, AI-assisted verification, and a final consensus-based decision.

## Agent Tank Hackathon

TaskEscrow is deployed on **GenLayer Studio Dev / Studio Next** for the Agent Tank Hackathon.

- Network: GenLayer Studio Dev / Studio Next
- Chain ID: `61997`
- Contract Address: `0x2Ca21453a7454bF1A2Ae5F77c4a83A6aE1A8dED9`

## Live Deployment

Contract Explorer:

https://explorer-studio-dev.genlayer.com/address/0x2Ca21453a7454bF1A2Ae5F77c4a83A6aE1A8dED9

Live Website:

https://rs0024.github.io/ai-task-verifier-intelligent-contract/

## How TaskEscrow Works

TaskEscrow follows a simple verification workflow:

1. A task is created with an employer, worker, task description, and configured reward amount.
2. `mark_funded()` changes the task state to `funded`.
3. The completed work is submitted using `submit_work(evidence_url)`.
4. `verify_task()` retrieves the public evidence.
5. GenLayer's nondeterministic AI execution evaluates whether the evidence proves completion.
6. Validators independently evaluate the result through GenLayer consensus.
7. The contract records the final result as `approved` or `rejected`.

## Contract Workflow

```text
created
   ↓
mark_funded()
   ↓
funded
   ↓
submit_work(evidence_url)
   ↓
submitted
   ↓
verify_task()
   ↓
approved / rejected
```

## AI Verification

The contract retrieves the submitted public evidence URL and provides its content to an AI verifier.

The verifier answers whether the evidence clearly proves that the specified task was completed.

The contract uses:

```python
gl.vm.run_nondet_default(
    leader_fn,
    validator_fn,
)
```

The validator independently performs the verification and compares its decision with the leader result.

This demonstrates how GenLayer Intelligent Contracts can use nondeterministic AI execution together with validator consensus.

## Public Contract Methods

### Write Methods

`mark_funded()`

Records the task as funded.

`submit_work(evidence_url)`

Stores the public evidence URL and changes the status to `submitted`.

`verify_task()`

Runs AI-assisted evidence verification and GenLayer validator consensus.

### View Methods

`get_status()`

Returns the current task status.

Possible states:

```text
created
funded
submitted
approved
rejected
```

`get_evidence_url()`

Returns the submitted evidence URL.

`get_task_description()`

Returns the task description.

`get_reward_amount()`

Returns the configured reward amount.

## Important Note

The current hackathon version demonstrates an **AI-verified task and settlement-decision workflow**.

`mark_funded()` records the funding state in the contract. The current version does not transfer or custody tokens automatically.

The configured reward amount represents the reward associated with the task and can be used by future versions to support full onchain escrow settlement.

## Example Workflow

```text
Task Created
      ↓
Funding State Recorded
      ↓
Worker Submits Public Evidence
      ↓
GenLayer AI Evaluates Evidence
      ↓
Validators Reach Consensus
      ↓
Approved or Rejected
```

## Example Task

Task:

```text
Build and submit a task completion report with verifiable evidence.
```

Reward:

```text
100
```

After evidence is submitted, `verify_task()` evaluates the evidence and the final consensus result is stored onchain.

## Repository Structure

```text
ai-task-verifier-intelligent-contract/
├── ai_task_verifier.py
├── index.html
├── README.md
├── evidence.md
└── tests/
```

## Technology

- GenLayer Intelligent Contracts
- Python
- GenLayer Studio Dev / Studio Next
- AI-assisted nondeterministic execution
- Validator consensus
- GitHub Pages

## Why TaskEscrow?

Traditional freelance and task platforms depend on a centralized party to decide whether work was completed correctly.

TaskEscrow demonstrates a different approach: submitted evidence can be evaluated through an Intelligent Contract, while GenLayer validators participate in reaching the final decision.

This creates a transparent and auditable foundation for future decentralized work verification, AI-agent commerce, milestone verification, and settlement systems.

## Current Deployment

**Chain ID:** `61997`

**Contract:**

```text
0x2Ca21453a7454bF1A2Ae5F77c4a83A6aE1A8dED9
```

**Explorer:**

https://explorer-studio-dev.genlayer.com/address/0x2Ca21453a7454bF1A2Ae5F77c4a83A6aE1A8dED9
