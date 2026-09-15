# TaskEscrow — AI-Verified Task Completion on GenLayer

TaskEscrow is a GenLayer Intelligent Contract that uses AI and validator consensus to verify whether submitted web evidence proves that a task was completed.

The project demonstrates an onchain workflow for task creation, evidence submission, AI-assisted verification, and consensus-based settlement decisions.

## Studio Dev Deployment

**Network:** GenLayer Studio Dev  
**Chain ID:** 61997

**Contract Address:**

`0x5E934B5f06222648Af54c0384a9Fd5916de1f57F`

**Explorer:**

https://explorer-studio-dev.genlayer.com/address/0x5E934B5f06222648Af54c0384a9Fd5916de1f57F

The deployment was finalized successfully through GenLayer consensus.

## How It Works

### 1. Create Task

The contract is deployed with:

- Employer
- Worker
- Task description
- Reward amount

Initial status:

`created`

### 2. Mark Task as Funded

Call:

`mark_funded()`

The contract status changes:

`created → funded`

The current Studio Dev version records the funding state but does not transfer funds.

### 3. Submit Work

The worker provides a public evidence URL using:

`submit_work(evidence_url)`

The contract stores the evidence URL and changes the status:

`funded → submitted`

### 4. AI Verification

Call:

`verify_task()`

The Intelligent Contract:

1. Retrieves the submitted web evidence using `gl.nondet.web.get()`.
2. Extracts the evidence content.
3. Sends the task description and evidence to an AI model.
4. Asks the model whether the evidence clearly proves task completion.
5. Uses GenLayer validator consensus to independently evaluate the result.

If the evidence is accepted:

`submitted → approved`

If the evidence is rejected:

`submitted → rejected`

## Contract Read Methods

- `get_status()`
- `get_evidence_url()`
- `get_task_description()`
- `get_reward_amount()`

## Contract Write Methods

- `mark_funded()`
- `submit_work(evidence_url)`
- `verify_task()`

## AI Verification

TaskEscrow does not trust a URL simply because it exists.

The contract retrieves the actual web content and asks AI validators to determine whether that content proves completion of the specified task.

The verification result is accepted through GenLayer's consensus mechanism.

## Current Deployment Test

Deployment was successfully finalized on GenLayer Studio Dev.

Initial onchain state was verified using:

`get_status()`

Result:

`created`

## Technology

- GenLayer Intelligent Contracts
- Python
- GenLayer Studio Dev
- GenLayer AI / LLM execution
- Web evidence retrieval
- Validator consensus

## Contract Source

The Intelligent Contract is located at:

`ai_task_verifier.py`

## Hackathon

TaskEscrow is being developed for the GenLayer Agent Tank Hackathon.

The project explores AI-verifiable task completion for future-of-work and agentic commerce applications.
