#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from target_acquisition.crew import TargetAcquisition

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "industry": "Marine Engineering and Industrial Manufacturing",
        "sector": "Marine propulsion and thruster systems",
        "geography": "Europe and Asia-Pacific",
        "time_horizon": "12-24 months"
    }

    result= TargetAcquisition().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)

if __name__ == "main":
    run()    



