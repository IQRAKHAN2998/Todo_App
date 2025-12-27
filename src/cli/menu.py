"""
Console menu interface for the Todo application
Provides a menu-driven interface for task management
"""
from src.services.todo_service import TodoService
from colorama import init, Fore, Style
init(autoreset=True)  # Automatically reset color after each print

class TodoMenu:
    """Console menu interface for the Todo application."""

    def __init__(self):
        """Initialize the menu with a TodoService."""
        self.service = TodoService()

    def display_menu(self):
        """Display the main menu options."""
        print(Fore.CYAN + "\n--- Todo App Menu ---")
        print(Fore.GREEN + "1. Add Task")
        print(Fore.GREEN + "2. View Tasks")
        print(Fore.GREEN + "3. Update Task")
        print(Fore.RED + "4. Delete Task")
        print(Fore.GREEN + "5. Mark Task Complete/Incomplete")
        print(Fore.GREEN + "6. Exit")
        print("--------------------")

    def get_user_choice(self):
        """Get and validate user menu choice."""
        try:
            choice = input(Fore.MAGENTA + "\nEnter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                return None
        except KeyboardInterrupt:
            print("\n\nExiting application...")
            return '6'
        except EOFError:
            print("\n\nExiting application...")
            return '6'

    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()

        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = input("Enter task description (optional): ").strip()

        try:
            task_id = self.service.add_task(title, description)
            print(Fore.YELLOW + f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status_marker = "✓" if task.completed else "○"
            print(f"[{status_marker}] {task.id}. {task.title}")
            if task.description:
                print(f"    Description: {task.description}")
            print(f"    Created: {task.created.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

    def update_task(self):
        """Handle updating an existing task."""
        print("\n--- Update Task ---")

        if not self.service.get_all_tasks():
            print("No tasks available to update.")
            return

        self.view_tasks()

        try:
            task_id_input = input("Enter the ID of the task to update: ").strip()
            if not task_id_input:
                print("Error: Task ID cannot be empty.")
                return
            task_id = int(task_id_input)

            task = self.service.get_task_by_id(task_id)

            print(f"Current task: {task.title}")
            new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
            new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

            # Use current values if user doesn't provide new ones
            update_title = new_title if new_title else None
            update_description = new_description if new_description else None

            # If user enters empty string for title, set it to None to keep current
            if new_title == "":
                update_title = None
            elif not new_title:  # If they entered just whitespace, use the original
                update_title = None

            # Same for description
            if new_description == "":
                update_description = None
            elif not new_description:
                update_description = None

            try:
                result = self.service.update_task(task_id, update_title, update_description)
                if result:
                    print(Fore.YELLOW + "Task updated successfully!")
                else:
                    print("Failed to update task.")
            except ValueError as e:
                print(f"Error: {e}")

        except ValueError:
            print("Error: Please enter a valid task ID (number).")
        except KeyError as e:
            print(f"Error: {e}")

    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")

        if not self.service.get_all_tasks():
            print("No tasks available to delete.")
            return

        self.view_tasks()

        try:
            task_id_input = input("Enter the ID of the task to delete: ").strip()
            if not task_id_input:
                print("Error: Task ID cannot be empty.")
                return
            task_id = int(task_id_input)

            # Confirm deletion
            try:
                task = self.service.get_task_by_id(task_id)
                confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/n): ").strip().lower()

                if confirm in ['y', 'yes']:
                    result = self.service.delete_task(task_id)
                    if result:
                        print("Task deleted successfully!")
                    else:
                        print("Failed to delete task.")
                else:
                    print("Deletion cancelled.")

            except KeyError as e:
                print(f"Error: {e}")

        except ValueError:
            print("Error: Please enter a valid task ID (number).")

    def mark_task_status(self):
        """Handle marking a task as complete/incomplete."""
        print("\n--- Mark Task Status ---")

        if not self.service.get_all_tasks():
            print("No tasks available to update.")
            return

        self.view_tasks()

        try:
            task_id_input = input("Enter the ID of the task to update: ").strip()
            if not task_id_input:
                print("Error: Task ID cannot be empty.")
                return
            task_id = int(task_id_input)

            try:
                task = self.service.get_task_by_id(task_id)
                new_completed_status = not task.completed
                new_status_text = "Complete" if new_completed_status else "Incomplete"

                # current_status = "Complete" if task.completed else "Incomplete"
                # new_status = "Incomplete" if task.completed else "Complete"

                confirm = input(f"Mark task '{task.title}' as {new_status_text}? (y/n): ").strip().lower()

                if confirm in ['y', 'yes']:
                    # new_completed_status = not task.completed
                    result = self.service.mark_task_status(task_id,new_completed_status)
                    if result:
                        # Use checkmark / cross instead of True/False
                        status_symbol = "✅" if new_completed_status else "❌"
                        print(f"Task marked as {new_status_text} {status_symbol} successfully!")
                    else:
                        print("Failed to update task status.")
                else:
                    print("Status update cancelled.")

            except KeyError as e:
                print(f"Error: {e}")

        except ValueError:
            print("Error: Please enter a valid task ID (number).")

    def run(self):
        """Main loop for the menu interface."""
        print("Welcome to the Todo App!")
        print("Manage your tasks with this simple console application.")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.mark_task_status()
            elif choice == '6':
                print("\nThank you for using the Todo App!")
                print("Goodbye!")
                break