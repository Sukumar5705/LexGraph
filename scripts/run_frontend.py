"""
Convenience script to run the React frontend dev server locally.

Status: SKELETON.
"""
import subprocess


def main():
    subprocess.run(["npm", "run", "dev"], cwd="frontend")


if __name__ == "__main__":
    main()
