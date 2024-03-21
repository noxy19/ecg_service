from src.domain.count_zero_crossings_service import CountZeroCrossingsService


def test_zero_crossings():
    zero_crossings_service = CountZeroCrossingsService()
    result = zero_crossings_service.count([1, -2, 3, -4, 5, -6])
    assert result == 5
