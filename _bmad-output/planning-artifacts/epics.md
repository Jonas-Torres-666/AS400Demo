---
stepsCompleted: [1, 2, 3]
inputDocuments: ['_bmad-output/planning-artifacts/PRD.md', '_bmad-output/planning-artifacts/Architecture.md']
project_name: 'RPG Modernization PoC'
---

# Epics and Stories - RPG Modernization PoC

## 1. Extracted Requirements

### Functional Requirements (FRs)
FR1: Personalization via PSDS - The program shall retrieve the current IBM i User Profile from the Program Status Data Structure (PSDS) and prompt the user for their preferred display name using the `DSPLY` opcode.
FR2: Interactive Greeting and Joke - Upon receiving the user's name, the program shall display a personalized greeting followed by a random joke selected from a predefined set of at least three options.
FR3: Interaction Logging - The program shall log every execution, including the User ID retrieved from the PSDS, the preferred name provided, and a timestamp, to a Physical File (PF) or a Data Area for audit purposes.

### Non-Functional Requirements (NFRs)
NFR1: Performance on PUB400 - The program must execute with minimal resource overhead to ensure compatibility and stability within the shared PUB400 public server environment.
NFR2: Auditability - All user interactions must be persistently logged to enable system administrators to track usage patterns and ensure accountability.

### Additional Requirements (Architecture)
- **TD1: User Identification via PSDS** - The program will utilize the standard Program Status Data Structure (PSDS) to automatically retrieve the `USER` field (positions 254-263).
- **TD2: Console I/O via DSPLY** - The `DSPLY` opcode will be used for all user interactions to maintain simplicity and compatibility.
- **TD3: Interaction Logging** - A Physical File (PF) named `INTLOG` will be used to store interaction logs including User ID, Preferred Name, and System Timestamp.
- **Data Model:** A simple PF named `INTLOG` with fields `LOGUSER`, `LOGNAME`, and `LOGTIME`.
- **PSDS Structure:** Program must define the PSDS structure in the D-specs to extract positions 254-263.

### UX Design Requirements (N/A)
(No UI/UX document was provided, all interactions are terminal-based.)

## 2. Requirements Coverage Map
### FR Coverage Map

FR1: Epic 1 - Program retrieves IBM i User ID and prompts for a nickname.
FR2: Epic 1 - Program displays a personalized greeting and a random joke.
FR3: Epic 2 - Program writes the User ID, Nickname, and Timestamp to a log file (INTLOG).

## 3. Epics and Stories
## Epic List

### Epic 1: Interactive System-Aware Greeting
Modernize the legacy RPG "Hello World" into an interactive utility that automatically identifies the user and provides a personalized, engaging experience.
**FRs covered:** FR1, FR2

### Epic 2: Persistent Usage Audit Logging
Implement enterprise-grade tracking for the modernization PoC to ensure all user interactions are logged and auditable.
**FRs covered:** FR3

---

## Epic 1: Interactive System-Aware Greeting

### Story 1.1: Automatic System Identification

As a developer,
I want the program to automatically retrieve my IBM i User Profile from the system,
So that the interaction feels integrated and "aware" of the enterprise environment.

**Acceptance Criteria:**

**Given** the program is executed on PUB400,
**When** the RPG cycle starts,
**Then** the program retrieves the `USER` field from the Program Status Data Structure (PSDS).
**And** the program displays: "System ID: [USER ID]. What is your preferred name?"

### Story 1.2: Personalized Joke Delivery

As a user,
I want to receive a personalized greeting and a random joke after providing my name,
So that the application provides immediate value and a modern "delightful" experience.

**Acceptance Criteria:**

**Given** the user has entered their preferred name,
**When** the `DSPLY` input is processed,
**Then** the program displays: "Hi [Name]! Here is your joke of the day: [Random Joke]".
**And** the joke is randomly selected from a list of at least 3 predefined jokes.

---

## Epic 2: Persistent Usage Audit Logging

### Story 2.1: Audit Interaction Logging

As a system administrator,
I want every program execution to be recorded in a persistent log,
So that I can track usage patterns and ensure accountability on the shared public server.

**Acceptance Criteria:**

**Given** a user has completed the greeting and joke interaction,
**When** the program prepares to exit,
**Then** it writes a record to the `INTLOG` file (or Data Area).
**And** the record contains the System User ID, the Preferred Name, and a Current Timestamp.
