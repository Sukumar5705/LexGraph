"""
Convenience script to run the FastAPI backend locally.

Status: SKELETON.
"""
import subprocess
import sys


def main():
    # TODO: consider reading host/port from backend/config.py settings
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
        cwd="backend",
    )


if __name__ == "__main__":
    main()
