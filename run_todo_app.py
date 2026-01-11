#!/usr/bin/env python3
"""
Entry point for the CLI Todo App.
This script properly handles the Python path to run the application from the project root.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.cli import CLI


def main():
    """Main function to run the Todo App."""
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
        exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again or contact support if the problem persists.")
        exit(1)


if __name__ == "__main__":
    main()