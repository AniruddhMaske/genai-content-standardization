import tempfile
import unittest
from pathlib import Path

from modules.ai_reviewer import build_review_prompt
from modules.content_standardizer import standardize_text
from modules.quality_checker import check_quality
from modules.text_cleaner import clean_text


class TextCleanerTests(unittest.TestCase):
    def test_normalizes_whitespace_without_rewriting_words(self):
        self.assertEqual(
            clean_text("\ufeff  Hello\t  world!\r\n\r\n\r\nNext line.  "),
            "Hello world!\n\nNext line.",
        )

    def test_standardization_is_idempotent(self):
        content = "  Keep   these words!\n\n\nAnd this line?"
        once = standardize_text(content)
        self.assertEqual(standardize_text(once), once)


class QualityCheckerTests(unittest.TestCase):
    def test_reports_duplicate_placeholder_and_long_line(self):
        text = (
            "Repeated paragraph.\n\n"
            "Repeated paragraph.\n\n"
            "Replace [insert owner] after reading this line, "
            + ("x" * 100)
        )
        issues = check_quality(text, max_line_length=80)
        codes = [issue.code for issue in issues]
        self.assertIn("duplicate_paragraph", codes)
        self.assertIn("placeholder", codes)
        self.assertIn("long_line", codes)

    def test_empty_text_has_one_clear_finding(self):
        issues = check_quality(" \n ")
        self.assertEqual([issue.code for issue in issues], ["empty"])


class CopilotPromptTests(unittest.TestCase):
    def test_prompt_preserves_supplied_content_and_review_boundaries(self):
        prompt = build_review_prompt("Revenue was $12.")
        self.assertIn("Revenue was $12.", prompt)
        self.assertIn("Do not add facts", prompt)
        self.assertIn("human verification", prompt)


if __name__ == "__main__":
    unittest.main()
