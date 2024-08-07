import unittest

from janus.utils.progress import track


class TestProgress(unittest.TestCase):
    def test_track(self):
        iterable = range(5)
        description = "Processing:"
        total = 5

        # Convert the generator to a list to consume all items
        result = list(track(iterable, description, total))

        # Check if the result is the same as the input iterable
        self.assertEqual(result, list(iterable))


if __name__ == "__main__":
    unittest.main()
