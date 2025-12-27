# Tasks: Phase-1 Todo App

**Feature**: Console-based Todo application with in-memory storage
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2025-12-28

## Implementation Strategy

**MVP Approach**: Start with Task entity and basic functionality (add/view tasks), then implement full CRUD operations and menu interface. This ensures a working application early with incremental feature additions.

**Phase 1**: Setup and foundational components
**Phase 2**: Core task management functionality
**Phase 3**: User Story 1 - Task Management Flow
**Phase 4**: User Story 2 - Task Update Flow
**Phase 5**: User Story 3 - Task Deletion Flow
**Phase 6**: Polish and integration

## Dependencies

- User Story 2 and 3 depend on User Story 1's foundational functionality
- All user stories require Phase 1 (setup) and Phase 2 (foundational) completion

## Parallel Execution Opportunities

- Task model and service can be developed in parallel [P]
- Unit tests can be written in parallel with implementation [P]
- Multiple user stories can have tests written in parallel [P]

---

## Phase 1: Setup (Project Initialization)

**Goal**: Initialize project structure and dependencies

- [X] T001 Create project directory structure (src/models, src/services, src/cli, tests/)
- [X] T002 Create requirements.txt with project dependencies
- [X] T003 Create main.py entry point file
- [X] T004 Create README.md with project documentation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Implement core data models and services needed by all user stories

- [X] T005 [P] Create Task model in src/models/task.py with ID, title, description, status, created properties
- [X] T006 [P] Create TaskList collection class in src/models/task.py with CRUD operations
- [X] T007 [P] Create TodoService in src/services/todo_service.py with add_task method per contract
- [X] T008 [P] Create TodoService get_all_tasks method per contract
- [X] T009 [P] Create TodoService get_task_by_id method per contract
- [X] T010 [P] Create TodoService update_task method per contract
- [X] T011 [P] Create TodoService delete_task method per contract
- [X] T012 [P] Create TodoService mark_task_status method per contract
- [X] T013 [P] Create unit tests for Task model in tests/unit/test_task.py
- [X] T014 [P] Create unit tests for TodoService in tests/unit/test_todo_service.py

---

## Phase 3: User Story 1 - Task Management Flow

**Goal**: Enable user to add, view, mark complete tasks as described in primary scenario

**Independent Test Criteria**: User can start the application, add a new task, view the task list, mark a task as complete, and exit

- [X] T015 [US1] Create console menu interface in src/cli/menu.py with basic structure
- [X] T016 [US1] Implement add task functionality in menu interface
- [X] T017 [US1] Implement view tasks functionality in menu interface
- [X] T018 [US1] Implement mark task complete/incomplete functionality in menu interface
- [X] T019 [US1] Implement exit functionality in menu interface
- [X] T020 [US1] Integrate menu interface with TodoService
- [X] T021 [US1] Create integration test for Task Management Flow in tests/integration/test_cli_flow.py
- [X] T022 [US1] Test full Task Management Flow with valid inputs

---

## Phase 4: User Story 2 - Task Update Flow

**Goal**: Enable user to update existing task's information

**Independent Test Criteria**: User can view existing tasks, select a task to update its description, and verify the changes

- [X] T023 [US2] Extend menu interface to include update task functionality
- [X] T024 [US2] Implement update task flow in menu interface
- [X] T025 [US2] Validate task ID exists before update operation
- [X] T026 [US2] Validate updated title is not empty
- [X] T027 [US2] Provide confirmation of successful updates
- [X] T028 [US2] Create integration test for Task Update Flow in tests/integration/test_cli_flow.py
- [X] T029 [US2] Test Task Update Flow with valid inputs

---

## Phase 5: User Story 3 - Task Deletion Flow

**Goal**: Enable user to delete tasks from the list

**Independent Test Criteria**: User can view the task list, select a task for deletion, confirm deletion, and verify it's removed

- [X] T030 [US3] Extend menu interface to include delete task functionality
- [X] T031 [US3] Implement delete task flow in menu interface with confirmation
- [X] T032 [US3] Validate task ID exists before deletion operation
- [X] T033 [US3] Provide confirmation before permanent deletion
- [X] T034 [US3] Update display after deletion
- [X] T035 [US3] Create integration test for Task Deletion Flow in tests/integration/test_cli_flow.py
- [X] T036 [US3] Test Task Deletion Flow with valid inputs

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Complete the application with error handling, validation, and user experience improvements

- [X] T037 Implement input validation across all menu operations
- [X] T038 Add error handling for invalid inputs with helpful messages
- [X] T039 Format task display with clear visual markers for completion status
- [X] T040 Handle invalid inputs gracefully without crashing
- [X] T041 Create contract tests in tests/contract/test_api_contracts.py
- [X] T042 Test performance with up to 1000 tasks
- [X] T043 Update README.md with usage instructions
- [X] T044 Run complete integration test suite
- [X] T045 Final end-to-end testing of all user scenarios