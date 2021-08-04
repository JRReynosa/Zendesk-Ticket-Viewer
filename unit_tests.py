import unittest
from main import get_multiple_tickets, get_ticket_by_id


class UnitTests(unittest.TestCase):
    print()

    def test_multiple(self):
        # Tickets 0 - 25
        actual_json, actual_prevURL, actual_nextURL = get_multiple_tickets()

        self.assertEqual(len(actual_json['tickets']), 25, "Should be 25")
        self.assertEqual(actual_prevURL, "", "Should be an empty string")
        self.assertNotEqual(actual_nextURL, "", "Should be a valid URL")

        # Tickets 26 - 50
        actual_json, actual_prevURL, actual_nextURL = get_multiple_tickets(actual_nextURL)

        self.assertEqual(len(actual_json['tickets']), 25, "Should be 25")
        self.assertNotEqual(actual_prevURL, "", "Should be a valid URL")
        self.assertNotEqual(actual_nextURL, "", "Should be a valid URL")

        # Tickets 51 - 75
        actual_json, actual_prevURL, actual_nextURL = get_multiple_tickets(actual_nextURL)

        # Tickets 76 - 100
        actual_json, actual_prevURL, actual_nextURL = get_multiple_tickets(actual_nextURL)

        # Ticket 101
        actual_json, actual_prevURL, actual_nextURL = get_multiple_tickets(actual_nextURL)
        self.assertEqual(len(actual_json['tickets']), 1, "Should be 1")
        self.assertNotEqual(actual_prevURL, "", "Should be a valid URL")
        self.assertEqual(actual_nextURL, "", "Should be an empty string")


    def test_individual(self):
        actual = get_ticket_by_id("1")

        self.assertEqual(actual['ticket']['id'], 1, "Should be 1")
        self.assertEqual(actual['ticket']['submitter_id'], 1900383340524, "Should be 1")

        actual = get_ticket_by_id("125")
        self.assertEqual(actual, None, "Should be None")


if __name__ == '__main__':
    unittest.main()
