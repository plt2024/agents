#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from target_acquisition.crew import TargetAcquisition

# Silence noisy third-party warnings similarly to stock_picker entrypoint
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Simple entrypoint to run the Target Acquisition crew.

    This mirrors the lightweight approach used by stock_picker's main.py:
    - Build a small inputs dict expected by the crew (industry, sector, geography, time_horizon).
    - Kick off the crew process using Crew.kickoff(inputs=...).
    - Print the crew result (raw output if available).
    """

    inputs = {
        "industry": os.environ.get("TA_INDUSTRY", "Marine Engineering and Industrial Manufacturing"),
        "sector": os.environ.get("TA_SECTOR", "Marine propulsion and thruster systems"),
        "geography": os.environ.get("TA_GEOGRAPHY", "Europe and Asia-Pacific"),
        "time_horizon": os.environ.get("TA_TIME_HORIZON", "12-24 months"),
        "current_date": str(datetime.now()),
    }

    # Create and run the crew. Many crew implementations expose .crew().kickoff(...)
    crew = TargetAcquisition().crew()
    # Kickoff may accept inputs and return a result object with .raw or similar
    try:
        result = crew.kickoff(inputs=inputs)
    except AttributeError:
        # Fallback: try common alternate entrypoints
        if hasattr(crew, "run"):
            result = crew.run(inputs=inputs)
        elif hasattr(crew, "start"):
            result = crew.start(inputs=inputs)
        else:
            raise

    # Print the result in a friendly form
    print("\n\n=== FINAL DECISION ===\n\n")
    # Many crew implementations attach the generated text to `.raw` or `.output`
    if hasattr(result, "raw"):
        print(result.raw)
    elif hasattr(result, "output"):
        print(result.output)
    else:
        # Fallback to printing the object representation
        print(result)


if __name__ == "__main__":
    run()

