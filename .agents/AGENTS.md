# Task Execution & Documentation Workflow

When executing tasks in this project, you MUST adhere to the following workflow and constraints:
1. **Clean Implementation Directories**: Create an individual directory for each task (e.g., `section_1/`, `section_2/`). These directories must **ONLY** contain the raw code and implementations intended for submission.
2. **Isolated Documentation**: Any explanations, write-ups, and handover documents (`handover.md`, `writeup.md`) must be placed in a separate directory structure completely outside of the implementation directories (e.g., `documentation/section_1/`). 
3. **Strict Compliance**: Ensure that all written tasks and code fully comply with the given requirements.
4. **Iterative Framework Approach**: Build the basic framework for the tasks first. Wait for the user to provide specific material for each task to test and refine the details iteratively.
5. **Local Progress Tracking**: All progress must be documented within the workspace, keeping everything self-contained.
6. **Continuous Documentation Sync**: Whenever code dependencies, environment variables, API keys, or execution steps change, you MUST immediately update all relevant documentation (e.g., `README.md`, `handover.md`) to reflect those changes. Documentation must always accurately represent the current state of the codebase.
7. **Explicit Process Termination**: Whenever providing instructions to run a continuous or long-running process (e.g., servers, agents, docker containers), you MUST explicitly include instructions on how to stop or kill the process (e.g., "Press `Ctrl+C` to stop").
8. **Comprehensive, Self-Contained README**: The `README.md` file must serve as the complete, standalone guide for evaluating the project. It must document the setup, execution, and testing of every task from A to Z (including virtual environment setup). **NEVER** mention or reference internal agent folders (e.g., `.agents/`) or artifacts in the README, as they will not be included in the final submission.
