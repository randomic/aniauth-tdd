from time import time


class MockTime:
    time_passed = 0.0

    def time(self):
        return time() + self.time_passed

    def sleep(self, seconds):
        self.time_passed += seconds

mock_time = MockTime()
