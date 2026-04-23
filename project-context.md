# Project Context: RPG Modernization PoC

## Environment: PUB400.com
- **OS:** IBM i 7.5
- **Compiler:** ILE RPG (RPG IV)
- **Tooling:** Users typically use 5250 Emulators or VS Code with IBM i Projects.
- **Constraints:** Public system. No authority to system-level libraries (QSYS). Use personal library (e.g., USERLIB).

## Technical Standards
- **Language:** Fully Free-Form RPG (**FREE) is preferred.
- **I/O:** Use DSPLY for simple demo interactions.
- **Metadata:** Always define the Program Status Data Structure (PSDS) to retrieve system variables.
- **Logging:** Use Physical Files (PF) with simple native I/O (WRITE).

## BMAD Workflow Rules
- Always update sprint-status.yaml after completing a story.
- Use mad-create-story before implementation to ensure Gemini has full context of the architecture decisions.
