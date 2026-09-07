# AI Task Verifier – GenLayer Intelligent Contract

An intelligent escrow contract built on GenLayer that uses AI-powered consensus to verify task completion before releasing a reward.

## Overview

This project demonstrates how GenLayer Intelligent Contracts can be used to create an AI-assisted task escrow system.

An employer creates a task and assigns a worker. The reward is deposited into the contract, the worker submits evidence of completed work, and GenLayer validators evaluate the evidence against the original task description.

Depending on the consensus result, the contract either releases the escrowed GEN to the worker or refunds it to the employer.

## How It Works

1. Employer and worker are assigned during contract deployment.
2. Employer funds the escrow using `deposit()`.
3. Worker submits an evidence URL using `submit_work()`.
4. `verify_and_settle()` retrieves the submitted evidence.
5. GenLayer's nondeterministic AI execution evaluates whether the evidence satisfies the task description.
6. Validators reach consensus on the verification result.
7. If the task is completed, the escrowed reward is transferred to the worker.
8. If the task is rejected, the escrowed reward is refunded to the employer.

## Contract States

The contract follows these main states:

`created → funded → submitted → completed_and_paid`

or:

`created → funded → submitted → rejected_and_refunded`

## Security / Authorization

The contract restricts important actions:

- Only the assigned employer can fund the escrow.
- Only the assigned worker can submit task evidence.
- Only the employer or worker can trigger verification and settlement.
- Settlement can only occur after evidence has been submitted.
- GEN remains under contract custody while the task is being evaluated.

## Tests

The `tests/test_task_escrow.py` test suite covers authorized and unauthorized contract interactions, including:

- Employer escrow funding
- Unauthorized deposit attempts
- Worker evidence submission
- Unauthorized evidence submission
- Employer attempting to submit worker evidence
- Unauthorized settlement attempts
- Contract state transitions

## GenLayer AI Verification

The contract uses GenLayer nondeterministic execution to retrieve evidence from a submitted URL and ask an AI model whether the evidence satisfies the task description.

Validators independently evaluate the result and GenLayer consensus determines the final verification outcome.

The verification result controls whether the escrowed reward is released to the worker or returned to the employer.

## Live Deployment

### Deployed Contract

Contract Address:

`0x1BEfbCa71186AE3fa708C4D69b1BB8272F9eA5b3`

The contract was deployed and tested using GenLayer Studio with GEN custody and AI-based consensus verification.

### Tested Lifecycle

`Deploy → Deposit GEN → Submit Evidence → AI Verification → Consensus → Settlement`

During testing, the employer successfully funded the contract and the contract transitioned to:

`funded`

The worker then submitted evidence and the state transitioned to:

`submitted`

The AI verification and validator consensus process was then triggered successfully.

A test verification returned:

```json
{
  "completed": false
}
