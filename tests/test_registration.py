import pytest

from registration import enroll_student, summarize_batch_registrations

pytestmark = pytest.mark.unit


@pytest.mark.boundary
def test_empty_batch_returns_zero_count_and_zero_fees():
    assert summarize_batch_registrations([]) == (0, 0.0)


@pytest.mark.negative
def test_batch_with_only_rejected_request_adds_nothing():
    assert summarize_batch_registrations([(10, 3, False)]) == (0, 0.0)


@pytest.mark.positive
def test_batch_with_one_approved_request():
    assert summarize_batch_registrations([(12, 3, True)]) == (1, 1425.0)


@pytest.mark.positive
def test_batch_with_two_approved_requests_sums_fees():
    assert summarize_batch_registrations([(12, 3, True), (6, 2, True)]) == (2, 2225.0)


@pytest.mark.positive
@pytest.mark.negative
def test_batch_with_approved_and_rejected_requests():
    requests = [(12, 3, True), (10, 3, False), (0, 4, True)]
    assert summarize_batch_registrations(requests) == (2, 1825.0)


@pytest.mark.positive
def test_enroll_student_allowed_sends_confirmation(notifier):
    result = enroll_student(12, 3, True, notifier)
    assert result is True
    notifier.send_confirmation.assert_called_once_with(1425.0)
    notifier.send_rejection.assert_not_called()


@pytest.mark.negative
def test_enroll_student_rejected_sends_rejection(notifier):
    result = enroll_student(10, 3, False, notifier)
    assert result is False
    notifier.send_rejection.assert_called_once_with()
    notifier.send_confirmation.assert_not_called()
