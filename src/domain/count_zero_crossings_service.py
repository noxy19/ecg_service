class CountZeroCrossingsService:
    def count(self, signal: list[int]) -> int:
        zero_crossings = 0
        for i in range(len(signal) - 1):
            if signal[i] * signal[i + 1] < 0:
                zero_crossings += 1

        return zero_crossings
