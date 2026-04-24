---
stepsCompleted: [1]
inputDocuments: ['_bmad-output/brainstorming/brainstorming-session-2026-04-23-18-20.md']
workflowType: 'prd'
---

# Product Requirements Document - RPG Modernization PoC

**Author:** Gemini CLI
**Date:** 2026-04-23

## 1. Product Vision
To demonstrate a BMad-driven modernization of a legacy RPG "Hello World" program on the PUB400 platform. The goal is to transform a static greeting into a system-aware, interactive utility that personalizes the user experience and logs interactions for auditability, showcasing an end-to-end modernization workflow.

## 2. Functional Requirements
FR1: Personalization via PSDS - The program shall retrieve the current IBM i User Profile from the Program Status Data Structure (PSDS) and prompt the user for their preferred display name using the `DSPLY` opcode.
FR2: Interactive Greeting and Joke - Upon receiving the user's name, the program shall display a personalized greeting followed by a random joke selected from a predefined set of at least three options.
FR3: Interaction Logging - The program shall log every execution, including the User ID retrieved from the PSDS, the preferred name provided, and a timestamp, to a Physical File (PF) or a Data Area for audit purposes.

## 3. Non-Functional Requirements
NFR1: Performance on PUB400 - The program must execute with minimal resource overhead to ensure compatibility and stability within the shared PUB400 public server environment.
NFR2: Auditability - All user interactions must be persistently logged to enable system administrators to track usage patterns and ensure accountability.
