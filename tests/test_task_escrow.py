def deploy_escrow(direct_deploy, employer, worker):
    return direct_deploy(
        "ai_task_verifier.py",
        str(employer),
        str(worker),
        "Complete the assigned test task",
        100,
    )


def test_unauthorized_deposit_blocked(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
):
    escrow = deploy_escrow(
        direct_deploy,
        direct_alice,
        direct_bob,
    )

    with direct_vm.prank(direct_charlie):
        with direct_vm.expect_revert(
            "Only employer can fund escrow"
        ):
            escrow.deposit()


def test_only_worker_can_submit_work(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
):
    escrow = deploy_escrow(
        direct_deploy,
        direct_alice,
        direct_bob,
    )

    with direct_vm.prank(direct_charlie):
        with direct_vm.expect_revert(
            "Only worker can submit evidence"
        ):
            escrow.submit_work(
                "https://example.com/evidence"
            )


def test_employer_cannot_submit_worker_evidence(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
):
    escrow = deploy_escrow(
        direct_deploy,
        direct_alice,
        direct_bob,
    )

    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert(
            "Only worker can submit evidence"
        ):
            escrow.submit_work(
                "https://example.com/evidence"
            )


def test_unauthorized_settlement_blocked(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
):
    escrow = deploy_escrow(
        direct_deploy,
        direct_alice,
        direct_bob,
    )

    with direct_vm.prank(direct_charlie):
        with direct_vm.expect_revert(
            "Only employer or worker can trigger settlement"
        ):
            escrow.verify_and_settle()
