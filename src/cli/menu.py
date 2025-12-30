"""
Console menu interface for the Todo application
Provides a menu-driven interface for task management
"""
from datetime import datetime
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
        print(Fore.YELLOW + "6. Filter Tasks")
        print(Fore.YELLOW + "7. Search Tasks")
        print(Fore.CYAN + "8. View Statistics")
        print(Fore.GREEN + "9. Exit")
        print("--------------------")

    def get_user_choice(self):
        """Get and validate user menu choice."""
        try:
            choice = input(Fore.MAGENTA + "\nEnter your choice (1-9): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
                return None
        except KeyboardInterrupt:
            print("\n\nExiting application...")
            return '9'
        except EOFError:
            print("\n\nExiting application...")
            return '9'

    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()

        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = input("Enter task description (optional): ").strip()

        # Get priority
        priority = input("Enter priority (low/medium/high, default: medium): ").strip().lower()
        if priority not in ["low", "medium", "high"]:
            priority = "medium"  # default to medium if invalid

        # Get due date
        due_date_str = input("Enter due date (YYYY-MM-DD, optional): ").strip()
        due_date = None
        if due_date_str:
            try:
                from datetime import datetime
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Date will be set to None.")
                due_date = None

        # Get category
        category = input("Enter category (optional, default: General): ").strip()
        if not category:
            category = "General"

        # Get recurrence pattern
        recurrence_pattern = input("Enter recurrence pattern (daily/weekly/monthly/yearly, optional): ").strip().lower()
        if recurrence_pattern and recurrence_pattern not in ["daily", "weekly", "monthly", "yearly"]:
            print("Invalid recurrence pattern. It will be set to None.")
            recurrence_pattern = None

        # Calculate next occurrence if recurrence pattern is provided
        next_occurrence = None
        if recurrence_pattern:
            if due_date:
                # If due date is provided, next occurrence is the due date
                next_occurrence = due_date
            else:
                # If no due date, use current date as the next occurrence
                next_occurrence = datetime.now()

        # Get reminder datetime
        reminder_datetime = None
        reminder_input = input("Enter reminder date and time (YYYY-MM-DD HH:MM, optional): ").strip()
        if reminder_input:
            try:
                reminder_datetime = datetime.strptime(reminder_input, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid datetime format. Reminder will be set to None.")
                reminder_datetime = None

        try:
            task_id = self.service.add_task(title, description, priority, due_date, category, recurrence_pattern, next_occurrence, reminder_datetime)
            print(Fore.YELLOW + f"Task added successfully with ID: {task_id}")
            if recurrence_pattern:
                print(Fore.CYAN + f"Task will repeat {recurrence_pattern} starting from {next_occurrence.strftime('%Y-%m-%d') if next_occurrence else 'now'}")
            if reminder_datetime:
                print(Fore.MAGENTA + f"Reminder set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')}")
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
            # Check if task is overdue
            is_overdue = False
            if task.due_date and task.due_date < datetime.now() and not task.completed:
                is_overdue = True

            status_marker = "✓" if task.completed else "○"
            priority_marker = {"high": "❗", "medium": "🔸", "low": "🔹"}[task.priority]

            # Format due date
            due_date_str = f" (Due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""
            if is_overdue:
                due_date_str += " ⚠️ OVERDUE"

            print(f"[{status_marker}] {priority_marker} {task.id}. {task.title} [{task.category}]{due_date_str}")
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

            # Update priority
            new_priority = input(f"Enter new priority (low/medium/high, or press Enter to keep '{task.priority}'): ").strip().lower()
            update_priority = new_priority if new_priority in ["low", "medium", "high"] else None
            if new_priority == "":
                update_priority = None

            # Update due date
            new_due_date_str = input(f"Enter new due date (YYYY-MM-DD, or press Enter to keep current '{task.due_date.strftime('%Y-%m-%d') if task.due_date else None}'): ").strip()
            update_due_date = None
            if new_due_date_str:
                try:
                    update_due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Date will not be updated.")
                    update_due_date = None
            elif new_due_date_str == "":
                update_due_date = None

            # Update category
            new_category = input(f"Enter new category (or press Enter to keep '{task.category}'): ").strip()
            update_category = new_category if new_category else None
            if new_category == "":
                update_category = None

            # Update recurrence pattern
            new_recurrence = input(f"Enter new recurrence pattern (daily/weekly/monthly/yearly, or press Enter to keep '{task.recurrence_pattern or 'None'}'): ").strip().lower()
            update_recurrence = new_recurrence if new_recurrence in ["daily", "weekly", "monthly", "yearly"] else None
            if new_recurrence == "":
                update_recurrence = ""  # Empty string to indicate no change

            # Update reminder datetime
            current_reminder = task.reminder_datetime.strftime('%Y-%m-%d %H:%M') if task.reminder_datetime else 'None'
            new_reminder_input = input(f"Enter new reminder date and time (YYYY-MM-DD HH:MM, or press Enter to keep '{current_reminder}'): ").strip()
            update_reminder = None
            if new_reminder_input:
                try:
                    update_reminder = datetime.strptime(new_reminder_input, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Invalid datetime format. Reminder will not be updated.")
                    update_reminder = None
            elif new_reminder_input == "":
                update_reminder = None  # No change

            try:
                result = self.service.update_task(task_id, update_title, update_description, update_priority, update_due_date, update_category, update_recurrence, None, update_reminder)
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

    def filter_tasks(self):
        """Handle filtering tasks by various criteria."""
        print("\n--- Filter Tasks ---")
        print("1. Filter by status (completed/pending)")
        print("2. Filter by priority")
        print("3. Filter by category")
        print("4. Show overdue tasks")
        print("5. Back to main menu")

        try:
            filter_choice = input("Enter your choice (1-5): ").strip()

            if filter_choice == '1':
                status_choice = input("Show (c)ompleted or (p)ending tasks? (c/p): ").strip().lower()
                if status_choice in ['c', 'completed']:
                    tasks = self.service.get_tasks_by_status(completed=True)
                    print("\n--- Completed Tasks ---")
                elif status_choice in ['p', 'pending']:
                    tasks = self.service.get_tasks_by_status(completed=False)
                    print("\n--- Pending Tasks ---")
                else:
                    print("Invalid choice.")
                    return
            elif filter_choice == '2':
                priority_choice = input("Enter priority (low/medium/high): ").strip().lower()
                if priority_choice in ["low", "medium", "high"]:
                    tasks = self.service.get_tasks_by_priority(priority_choice)
                    print(f"\n--- {priority_choice.capitalize()} Priority Tasks ---")
                else:
                    print("Invalid priority level.")
                    return
            elif filter_choice == '3':
                category = input("Enter category: ").strip()
                tasks = self.service.get_tasks_by_category(category)
                print(f"\n--- Tasks in '{category}' Category ---")
            elif filter_choice == '4':
                tasks = self.service.get_overdue_tasks()
                print("\n--- Overdue Tasks ---")
            elif filter_choice == '5':
                return
            else:
                print("Invalid choice.")
                return

            if not tasks:
                print("No tasks found.")
                return

            for task in tasks:
                # Check if task is overdue
                is_overdue = False
                if task.due_date and task.due_date < datetime.now() and not task.completed:
                    is_overdue = True

                status_marker = "✓" if task.completed else "○"
                priority_marker = {"high": "❗", "medium": "🔸", "low": "🔹"}[task.priority]

                # Format due date
                due_date_str = f" (Due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""
                if is_overdue:
                    due_date_str += " ⚠️ OVERDUE"

                print(f"[{status_marker}] {priority_marker} {task.id}. {task.title} [{task.category}]{due_date_str}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Created: {task.created.strftime('%Y-%m-%d %H:%M:%S')}")
                print()

        except Exception as e:
            print(f"Error filtering tasks: {e}")

    def search_tasks(self):
        """Handle searching tasks by title or description."""
        print("\n--- Search Tasks ---")
        query = input("Enter search query: ").strip()

        if not query:
            print("Search query cannot be empty.")
            return

        tasks = self.service.search_tasks(query)

        if not tasks:
            print("No tasks found matching your search.")
            return

        print(f"\n--- Search Results for '{query}' ---")
        for task in tasks:
            # Check if task is overdue
            is_overdue = False
            if task.due_date and task.due_date < datetime.now() and not task.completed:
                is_overdue = True

            status_marker = "✓" if task.completed else "○"
            priority_marker = {"high": "❗", "medium": "🔸", "low": "🔹"}[task.priority]

            # Format due date
            due_date_str = f" (Due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""
            if is_overdue:
                due_date_str += " ⚠️ OVERDUE"

            print(f"[{status_marker}] {priority_marker} {task.id}. {task.title} [{task.category}]{due_date_str}")
            if task.description:
                print(f"    Description: {task.description}")
            print(f"    Created: {task.created.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

    def view_statistics(self):
        """Display task statistics and productivity metrics."""
        print("\n--- Task Statistics ---")
        stats = self.service.get_statistics()

        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"Completed Tasks: {stats['completed_tasks']}")
        print(f"Pending Tasks: {stats['pending_tasks']}")
        print(f"Completion Rate: {stats['completion_rate']}%")
        print(f"Overdue Tasks: {stats['overdue_tasks']}")
        print(f"Recurring Tasks: {stats['recurring_tasks']}")
        print()

        print("--- Priority Breakdown ---")
        for priority, count in stats['priority_breakdown'].items():
            print(f"{priority.capitalize()}: {count}")
        print()

        print("--- Category Breakdown ---")
        for category, count in stats['category_breakdown'].items():
            print(f"{category}: {count}")

    def process_recurring_tasks(self):
        """Process recurring tasks and create new instances when needed."""
        new_tasks_count = self.service.process_recurring_tasks()
        if new_tasks_count > 0:
            print(f"\n{Fore.GREEN}Created {new_tasks_count} new recurring task(s).{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}No recurring tasks needed to be processed.{Style.RESET_ALL}")

    def check_upcoming_reminders(self, within_minutes: int = 60):
        """Check and display upcoming reminders."""
        upcoming_reminders = self.service.get_upcoming_reminders(within_minutes)
        if upcoming_reminders:
            print(f"\n{Fore.RED}[ALARM] Upcoming Reminders (within {within_minutes} minutes):{Style.RESET_ALL}")
            for task in upcoming_reminders:
                time_diff = task.reminder_datetime - datetime.now()
                minutes_left = int(time_diff.total_seconds() // 60)
                print(f"{Fore.RED}[ALARM] {minutes_left} min - {task.title} (ID: {task.id}){Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}No upcoming reminders.{Style.RESET_ALL}")

    def run(self):
        """Main loop for the menu interface."""
        print("Welcome to the Todo App!")
        print("Manage your tasks with this simple console application.")

        # Load tasks from file on startup
        self.service.load_from_file('tasks.json')

        while True:
            # Process recurring tasks before showing the menu
            self.process_recurring_tasks()

            # Check for upcoming reminders
            self.check_upcoming_reminders(30)  # Check for reminders within 30 minutes

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
                self.filter_tasks()
            elif choice == '7':
                self.search_tasks()
            elif choice == '8':
                self.view_statistics()
            elif choice == '9':
                # Save tasks to file before exiting
                self.service.save_to_file('tasks.json')
                print("\nThank you for using the Todo App!")
                print("Goodbye!")
                break