
import unittest

from modules.content_standardizer import standardize_text


class TestContentStandardizer(unittest.TestCase):

    def test_employee_name_formatting(self):
        result = standardize_text("employee name : john smith")
        self.assertEqual(result, "Employee Name: John Smith")

    def test_email_lowercase(self):
        result = standardize_text("email id : JOHN@GMAIL.COM")
        self.assertEqual(result, "Email ID: john@gmail.com")

    def test_department_formatting(self):
        result = standardize_text("department - INFORMATION TECHNOLOGY")
        self.assertEqual(result, "Department: Information Technology")

    def test_status_formatting(self):
        result = standardize_text("status : ACTIVE")
        self.assertEqual(result, "Status: Active")

    def test_placeholder_is_preserved(self):
        result = standardize_text(
            "Remember to replace [insert owner] before publication."
        )
        self.assertIn("[insert owner]", result)


if __name__ == "__main__":
    unittest.main()
