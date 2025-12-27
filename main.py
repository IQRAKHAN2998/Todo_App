#!/usr/bin/env python3
"""
Todo App - Console-based Todo application with in-memory storage
Main entry point for the application
"""

from src.cli.menu import TodoMenu


def main():
    """Main entry point for the Todo application."""
    print("Welcome to the Todo App!")
    print("A console-based application for managing your tasks.")
    print()

    menu = TodoMenu()
    menu.run()


if __name__ == "__main__":
    main()