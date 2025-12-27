# Data Model: Phase-1 Todo App

## Task Entity

### Properties
- **ID**: Unique sequential identifier (integer, auto-generated)
- **Title**: Task title/description (string, required, non-empty)
- **Description**: Detailed task information (string, optional)
- **Status**: Completion status (boolean, default: false/incomplete)
- **Created**: Timestamp of creation (datetime, auto-generated)

### Validations
- Title must not be empty or whitespace-only
- ID must be unique within the task collection
- Status must be boolean value (true for complete, false for incomplete)

### State Transitions
- New Task: Status starts as `false` (incomplete)
- Update Status: Can transition from `false` to `true` or `true` to `false`
- Delete: Task is removed from collection

## TaskList Collection

### Properties
- **Tasks**: Collection of Task entities stored in memory (list/dictionary)
- **Next ID**: Counter for generating unique sequential IDs (integer)

### Operations
- **Add Task**: Creates new task with auto-generated ID and current timestamp
- **Get All Tasks**: Returns all tasks in the collection
- **Get Task by ID**: Returns specific task matching the ID
- **Update Task**: Modifies existing task's title/description/status
- **Delete Task**: Removes task from collection
- **Mark Complete/Incomplete**: Updates task completion status

### Validation Rules
- Task ID must exist before update/delete operations
- Task title cannot be empty when adding/updating
- Cannot perform operations on non-existent tasks