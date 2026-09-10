# AI Task Verifier Intelligent Contract

An AI-powered escrow and task verification Intelligent Contract built with GenLayer.

The contract allows an employer to create and fund a task escrow for a worker. The worker submits evidence of completed work, and GenLayer's AI-powered nondeterministic execution evaluates the evidence before settlement.

## How It Works

1. The contract is deployed with:
   - Employer address
   - Worker address
   - Task description
   - Reward amount

2. The employer funds the escrow with the configured reward amount.

3. The worker submits an evidence URL after completing the assigned task.

4. The contract retrieves the evidence from the submitted URL.

5. GenLayer's nondeterministic AI execution evaluates whether the evidence proves that the task was completed.

6. Validators independently verify the AI result.

7. If the task is verified as completed:
   - Status becomes `completed_and_paid`
   - The reward is transferred to the worker.

8. If the task is rejected:
   - Status becomes `rejected_and_refunded`
   - The reward is returned to the employer.

## Security Controls

The contract includes access and state protections:

- Only the employer can fund the escrow.
- The deposited amount must exactly match the configured reward.
- Zero-value rewards are rejected.
- Only the worker can submit evidence.
- Evidence can only be submitted after funding.
- Only the employer or worker can trigger settlement.
- Settlement requires submitted evidence.

## Contract Status Flow

```text
created
   |
   v
funded
   |
   v
submitted
   |
   +----------------------+
   |                      |
   v                      v
completed_and_paid   rejected_and_refunded
