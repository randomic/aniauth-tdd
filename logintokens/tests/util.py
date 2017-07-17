"""utility functions for testing logintokens app

"""
from time import time


class MockTime:
    """Provide mocked time and sleep methods to simulate the passage of time.

    """
    time_passed = 0.0

    def time(self):
        """Return current time with a consistent offset.

        """
        return time() + self.time_passed

    def sleep(self, seconds):
        """Increase the offset to make it seem as though time has passed.

        """
        self.time_passed += seconds

mock_time = MockTime()
