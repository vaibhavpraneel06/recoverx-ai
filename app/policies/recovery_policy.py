def decide_recovery_action(
    probability,
    failure_reason,
    retry_count,
    amount
):
    """
    Decide the safest recovery strategy for a failed payment.

    This is a deterministic policy layer that sits
    on top of the ML prediction.
    """

    # --------------------------------------------------------
    # 1. Avoid repeatedly retrying payments
    # --------------------------------------------------------

    if retry_count >= 3:
        return {
            "action": "STOP_RETRYING",
            "reason": (
                "Multiple previous retries detected. "
                "Further retries may have low value."
            )
        }

    # --------------------------------------------------------
    # 2. Customer-action failures
    # --------------------------------------------------------

    if failure_reason == "INSUFFICIENT_FUNDS":

        return {
            "action": "CUSTOMER_ACTION",
            "reason": (
                "The payment likely requires customer "
                "action before another attempt."
            )
        }

    # --------------------------------------------------------
    # 3. Limit-related failures
    # --------------------------------------------------------

    if failure_reason == "LIMIT_EXCEEDED":

        return {
            "action": "ALTERNATE_METHOD",
            "reason": (
                "The current payment route may not accept "
                "another attempt. Suggest another method."
            )
        }

    # --------------------------------------------------------
    # 4. Temporary technical failures
    # --------------------------------------------------------

    if failure_reason in [
        "TIMEOUT",
        "NETWORK_ERROR"
    ]:

        if probability >= 70:

            return {
                "action": "RETRY",
                "reason": (
                    "The failure appears temporary and "
                    "the predicted recovery probability is high."
                )
            }

        elif probability >= 40:

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "The failure may be temporary, but "
                    "the recovery probability is moderate."
                )
            }

    # --------------------------------------------------------
    # 5. Bank decline
    # --------------------------------------------------------

    if failure_reason == "BANK_DECLINE":

        if probability >= 70:

            return {
                "action": "ALTERNATE_METHOD",
                "reason": (
                    "The bank declined the transaction. "
                    "Using another payment method may improve "
                    "the recovery opportunity."
                )
            }

        return {
            "action": "CUSTOMER_ACTION",
            "reason": (
                "The issuing bank declined the payment. "
                "Customer intervention may be required."
            )
        }

    # --------------------------------------------------------
    # 6. High-value transactions
    # --------------------------------------------------------

    if amount >= 40000 and probability >= 60:

        return {
            "action": "PRIORITY_REVIEW",
            "reason": (
                "High-value transaction with a meaningful "
                "recovery probability."
            )
        }

    # --------------------------------------------------------
    # 7. Default
    # --------------------------------------------------------

    return {
        "action": "DO_NOT_RETRY",
        "reason": (
            "Current evidence does not justify another "
            "automatic recovery attempt."
        )
    }


# ============================================================
# TEST THE POLICY
# ============================================================

if __name__ == "__main__":

    test_cases = [
        {
            "probability": 82,
            "failure_reason": "TIMEOUT",
            "retry_count": 1,
            "amount": 25000
        },
        {
            "probability": 70,
            "failure_reason": "LIMIT_EXCEEDED",
            "retry_count": 1,
            "amount": 45000
        },
        {
            "probability": 35,
            "failure_reason": "INSUFFICIENT_FUNDS",
            "retry_count": 2,
            "amount": 10000
        },
        {
            "probability": 85,
            "failure_reason": "NETWORK_ERROR",
            "retry_count": 3,
            "amount": 30000
        }
    ]

    print("\n===== RECOVERX POLICY ENGINE =====\n")

    for case in test_cases:

        decision = decide_recovery_action(
            case["probability"],
            case["failure_reason"],
            case["retry_count"],
            case["amount"]
        )

        print(
            f"Failure: {case['failure_reason']}"
        )

        print(
            f"Probability: {case['probability']}%"
        )

        print(
            f"Retries: {case['retry_count']}"
        )

        print(
            f"Decision: {decision['action']}"
        )

        print(
            f"Reason: {decision['reason']}"
        )

        print("-" * 60)