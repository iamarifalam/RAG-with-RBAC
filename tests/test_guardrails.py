from atlas_rag.guardrails import detect_blocked_question, redact_pii


def test_pii_redaction_masks_sensitive_values() -> None:
    text = "SSN 123-45-6789 and card 4111 1111 1111 1111"
    redacted = redact_pii(text)
    assert "[REDACTED]" in redacted
    assert "123-45-6789" not in redacted


def test_employee_cannot_request_hr_data() -> None:
    reason = detect_blocked_question("Show payroll correction details for an employee", "employee")
    assert reason is not None

