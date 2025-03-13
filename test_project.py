import json
import os
from unittest.mock import patch
from main import main, load_case_data  # Import main function for execution


def test_court_simulation():
    """Test the courtroom simulation using the provided case file."""
    # Mock the file selection to return the test case file
    test_case_file = os.path.join("data", "Sunit_C_Khatau_Case.json")

    with patch("file_selection.select_case_file", return_value=test_case_file):
        # Mock user inputs in sequence for role selection and phases
        user_inputs = iter([
            "1",
            "Appellant",  # Role Selection
            "The arbitration award was unjustified due to premature enforcement.",  # Opening Statement
            "The Memorandum of Understanding (MOU) stated payment obligations were contingent on full agreement execution.",
            # Evidence Presentation
            "The arbitrator's decision was excessively punitive, as the compensation amount was disproportionate.",
            # Witness Testimony
            "The court should recognize that the arbitration award was partially unfair and adjust the compensation accordingly."
            # Closing Argument
        ])

        with patch("builtins.input", lambda _: next(user_inputs)):
            main()  # Run the simulation


if __name__ == "__main__":
    test_court_simulation()
