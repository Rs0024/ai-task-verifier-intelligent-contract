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
4. `verify_and_settle()` retrieves the evidence.
5. GenLayer's nondeterministic AI execution evaluates whether the evidence satisfies the task description.
6. Validators reach consensus on the result.
7. If the task is completed, the reward is transferred to the worker.
8. If the task is rejected, the escrow is refunded to the employer.

## Contract States

The contract follows these main states:

`created → funded → submitted → completed_and_paid`

or

`created → funded → submitted → rejected_and_refunded`

## Security / Authorization

The contract restricts important actions:

- Only the assigned employer can fund the escrow.
- Only the assigned worker can submit task evidence.
- Only the employer or worker can trigger verification and settlement.
- Settlement can only occur after evidence has been submitted.

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

Validators independently evaluate the result and use GenLayer consensus to determine the final outcome.

## Live Deployment

The contract has been successfully deployed and executed in GenLayer Studio.

Tested lifecycle:

`Deploy → Deposit GEN → Submit Evidence → AI Verification → Consensus → Settlement`

A test verification also demonstrated the rejection path, where insufficient evidence produced:

`completed: false`

and the contract correctly transitioned to:

`rejected_and_refunded`

## Built With

- GenLayer Intelligent Contracts
- Python
- GenLayer Studio
- GenLayer AI Consensus
- GitHub

## Purpose

This project explores trust-minimized task settlement where AI and decentralized validator consensus can determine whether submitted work satisfies predefined requirements.
