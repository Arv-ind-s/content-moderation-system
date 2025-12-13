import pytest
from src.utils.text_processing import clean_text, validate_text

class TestTextCleaning:
    @pytest.mark.parametrize("input_text, expected", [
        ("Hello\nWorld", "Hello World"),
        ("Hello\tWorld", "Hello World"),
        ("   Spaces   ", "Spaces"),
        ("Multiple    Spaces", "Multiple Spaces"),
        ("Check http://google.com link", "Check link"),
        ("Check www.google.com link", "Check link"),
        ("Email test@example.com here", "Email here"),
        ("IP 192.168.1.1 address", "IP address"),
        ("Wiki [[link]] style", "Wiki style"),
        ("", ""),
        (None, ""),
    ])
    def test_clean_text_cases(self, input_text, expected):
        """Test various text cleaning scenarios."""
        assert clean_text(input_text) == expected

    def test_clean_text_mixed(self):
        """Test a complex string with multiple issues."""
        text = "  Hello\nWorld!  Check http://site.com and test@mail.com "
        expected = "Hello World! Check and"
        assert clean_text(text) == expected

class TestTextValidation:
    def test_validate_valid_text(self):
        is_valid, error = validate_text("Valid text")
        assert is_valid is True
        assert error == ""

    def test_validate_empty(self):
        is_valid, error = validate_text("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_none(self):
        is_valid, error = validate_text(None)
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_too_long(self):
        long_text = "a" * 5001
        is_valid, error = validate_text(long_text, max_length=5000)
        assert is_valid is False
        assert "exceeds maximum length" in error

    def test_validate_empty_after_clean(self):
        # Text that becomes empty after cleaning (e.g., only URL)
        is_valid, error = validate_text("http://google.com")
        assert is_valid is False
        assert "empty after preprocessing" in error
