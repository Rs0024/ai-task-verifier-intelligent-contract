def deploy_escrow(
    direct_deploy,
    employer,
    worker,
):
    return direct_deploy(
        "ai_task_verifier.py",
        employer,
        worker,
        "Complete the assigned test task",
        100,
    )


def test_employer_can_fund_escrow(
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

    direct_vm.deal(
        direct_alice,
        100,
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.deposit(
            value=100
        )

    assert (
        escrow.get_status()
        == "funded"
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

    direct_vm.deal(
        direct_charlie,
        100,
    )

    with direct_vm.prank(
        direct_charlie
    ):
        with direct_vm.expect_revert(
            "Only employer can fund escrow"
        ):
            escrow.deposit(
                value=100
            )


def test_worker_can_submit_work(
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

    direct_vm.deal(
        direct_alice,
        100,
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.deposit(
            value=100
        )

    with direct_vm.prank(
        direct_bob
    ):
        escrow.submit_work(
            "https://example.com/evidence"
        )

    assert (
        escrow.get_status()
        == "submitted"
    )


def test_unauthorized_submit_blocked(
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

    direct_vm.deal(
        direct_alice,
        100,
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.deposit(
            value=100
        )

    with direct_vm.prank(
        direct_charlie
    ):
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

    direct_vm.deal(
        direct_alice,
        100,
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.deposit(
            value=100
        )

    with direct_vm.prank(
        direct_alice
    ):
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

    with direct_vm.prank(
        direct_charlie
    ):
        with direct_vm.expect_revert(
            "Only employer or worker can trigger settlement"
        ):
            escrow.verify_and_settle()


def test_worker_can_trigger_settlement(
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

    direct_vm.deal(
        direct_alice,
        100,
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.deposit(
            value=100
        )

    with direct_vm.prank(
        direct_bob
    ):
        escrow.submit_work(
            "https://example.com/evidence"
        )

    direct_vm.mock_web(
        r".*example\.com/evidence.*",
        {
            "status": 200,
            "body":
                "The assigned task was completed successfully.",
        },
    )

    direct_vm.mock_llm(
        r".*Determine whether.*",
        '{"completed": true}',
    )

    with direct_vm.prank(
        direct_bob
    ):
        escrow.verify_and_settle()

    assert (
        escrow.get_status()
        == "completed_and_paid"
    )


def test_employer_can_trigger_refund(
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

    direct_vm.deal(
        direct_alice,
        100,
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.deposit(
            value=100
        )

    with direct_vm.prank(
        direct_bob
    ):
        escrow.submit_work(
            "https://example.com/evidence"
        )

    direct_vm.mock_web(
        r".*example\.com/evidence.*",
        {
            "status": 200,
            "body":
                "No proof of task completion.",
        },
    )

    direct_vm.mock_llm(
        r".*Determine whether.*",
        '{"completed": false}',
    )

    with direct_vm.prank(
        direct_alice
    ):
        escrow.verify_and_settle()

    assert (
        escrow.get_status()
        == "rejected_and_refunded"
    )
