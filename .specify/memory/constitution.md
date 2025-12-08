<!-- Sync Impact Report
Version change: N/A to 1.0.0

Modified principles (template placeholders to concrete principles):
- Template principle 1 to P1. Minimal Files & Simplicity
- Template principle 2 to P2. IB Computer Science SL Alignment
- Template principle 3 to P3. Core Python Construct Coverage
- Template principle 4 to P4. PEP8-Compliant Python Style
- Template principle 5 to P5. Learnability & Transparency

Added sections:
- Additional Constraints for IB CS SL Project
- Development Workflow & Review Process

Removed sections:
- None (all template sections have been given concrete content)

Templates requiring updates or checks:
- .specify/templates/plan-template.md [OK]: Constitution Check section will list IB SL
  and construct gates per feature; no template structure changes required.
- .specify/templates/spec-template.md [OK]: Requirements and entity sections will record
  IB SL alignment and chosen constructs where relevant.
- .specify/templates/tasks-template.md [OK]: Tasks will reference constructs and PEP8
  where helpful; no structural changes required.
- .specify/templates/commands/* [PENDING]: commands directory not present in this repo.

Follow-up TODOs:
- None.
-->

# Q and A Practise 2 Constitution

## Core Principles

### P1. Minimal Files & Simplicity

The application MUST be implemented using the minimum number of Python, template, and
HTML files needed to satisfy the specification and IB assessment requirements.

- The default structure is a single main Python file (for example, `main.py`) plus only
  those additional files that are clearly essential (for example, one HTML/template file
  and/or one data file).
- Introducing additional Python modules, packages, or templates MUST be justified in the
  feature plan as strictly necessary for clarity or functionality.
- Complex, multi-package architectures (for example, many subpackages under `src/`) are
  discouraged for this project and MUST only appear if required by the IB teacher or
  rubric.

Rationale: A minimal, non-modular structure keeps the code easy to inspect, understand,
and grade in the context of an IB Computer Science SL internal assessment.

### P2. IB Computer Science SL Alignment

The project MUST be designed, implemented, and documented as an IB Computer Science SL
style application.

- User scenarios, requirements, and explanations MUST be understandable to an IB CS SL
  student and examiner.
- Features and data structures SHOULD map directly to IB syllabus topics (for example,
  arrays/lists, records/objects, selection, iteration, OOP concepts).
- The specification and plan MUST explicitly state how the application demonstrates
  relevant IB CS SL concepts.

Rationale: The primary goal of the project is to support learning and assessment under
the IB CS SL curriculum, not to optimize for industrial-scale software architecture.

### P3. Core Python Construct Coverage

The final application MUST demonstrably use **at least 15** of the following Python
constructs and concepts in meaningful, non-trivial ways:

1. Arrays (Python lists used as collections)
2. User-defined objects (instances of custom classes)
3. Objects as data records (for example, simple classes or data classes storing fields)
4. Simple selection (if/else)
5. Complex selection (nested if, multiple conditions with `and`/`or`)
6. Loops (for/while)
7. Nested loops
8. User-defined methods/functions
9. User-defined methods with parameters
10. User-defined methods with return values
11. Sorting (for example, using `sort`, `sorted`, or a manual algorithm)
12. Searching (for example, linear search or binary search)
13. File input/output (reading from or writing to files)
14. Use of sentinels or flags to control loops or state
15. Recursion
16. Merging of two or more sorted data structures
17. Polymorphism (for example, different classes implementing a common interface or
    method name)
18. Inheritance (for example, a subclass extending a base class)
19. Encapsulation (for example, grouping related state and behavior inside classes,
    controlling access via methods)
20. Parsing a text file (for example, reading lines and extracting structured data)

Project plans and specifications MUST:

- List which constructs from the above set are targeted for the feature or project.
- Indicate in which functions, classes, or files each construct will appear.
- Ensure that by project completion, at least 15 constructs are implemented.

Rationale: This ensures the application provides rich evidence of programming skills
aligned with IB CS SL while remaining focused and coherent.

### P4. PEP8-Compliant Python Style

All Python code in the project MUST adhere to Python PEP8 style guidelines.

- Names, indentation, line length, and imports MUST follow PEP8 unless the IB teacher
  explicitly requires an exception.
- Where practical, a formatting or linting tool MAY be used, but the primary goal is
  clear, consistent, human-readable code for assessors.
- Code reviews and self-checks MUST include verifying PEP8-style issues (for example,
  via a checklist or linting output).

Rationale: PEP8 compliance supports readability, maintainability, and professional
standards, which benefits both learning and assessment.

### P5. Learnability & Transparency

The codebase MUST be easily understandable by IB CS SL students and examiners.

- Functions and classes SHOULD have clear, descriptive names and, where appropriate,
  concise docstrings explaining purpose and parameters.
- Each usage of the required constructs (for example, recursion, inheritance) SHOULD be
  located in well-isolated functions or classes so it is easy to point to in
  documentation and reflection.
- Any non-obvious algorithmic choices MUST be briefly explained in accompanying
  documentation (for example, README or quickstart instructions).

Rationale: The project is both an application and a learning/assessment artifact, so
clarity and openness are critical.

## Additional Constraints for IB CS SL Project

This section refines how the required constructs are applied within the project.

- **Arrays / Lists**: Use Python lists to store and process collections of items (for
  example, questions, scores, or records).
- **User-defined objects & data records**: Define at least one custom class used as a
  record type (for example, `Question`, `Student`, or similar) with attributes and
  behavior.
- **Selection & iteration**: Implement both simple and complex selection, loops, and
  nested loops in core logic (for example, menu handling, processing question banks).
- **User-defined methods with parameters and returns**: Core logic MUST be broken into
  reusable functions/methods with parameters and return values, not only inline code in
  `main`.
- **Sorting & searching**: At least one core feature MUST rely on sorting or searching
  over a collection (for example, finding a record, ordering results).
- **File I/O & parsing**: At least one feature MUST read from and/or write to a file,
  and parse text into structured data (for example, load questions from a text file
  with a defined format).
- **Sentinels / flags**: At least one loop MUST use a sentinel value or flag variable to
  control termination or state transitions.
- **Recursion**: At least one function MUST be implemented recursively in a way that is
  relevant to the problem domain or demonstrates a clear algorithmic idea.
- **Merging sorted data structures**: At least one operation MUST merge two or more
  sorted lists or similar structures, preserving sort order.
- **Object-oriented concepts (polymorphism, inheritance, encapsulation)**: At least one
  small hierarchy of classes MUST demonstrate inheritance and encapsulation, with
  polymorphic behavior via common methods.

Every feature plan and specification MUST include a short "Construct Coverage" note
indicating how it contributes to the overall 15-construct requirement.

## Development Workflow & Review Process

The following rules govern how the constitution is applied during planning,
implementation, and review:

- The **"Constitution Check"** section in each `plan.md` MUST confirm:
  - The project still uses a minimal, non-modular structure.
  - The feature aligns with IB CS SL goals.
  - Planned constructs and their locations are listed and counted toward the 15+ total.
  - PEP8 compliance will be maintained for all new or modified Python code.
- Feature specifications MUST trace user stories and requirements back to IB CS SL
  concepts where relevant.
- Tasks in `tasks.md` SHOULD reference PEP8 checks and construct implementation where it
  improves clarity (for example, explicit tasks to implement recursion or inheritance).

During code review (or self-review where formal reviews are not used):

- Changes MUST be checked against all five core principles.
- Any new module or file MUST include a short justification that the additional file is
  essential.
- If a construct is removed or replaced, the overall 15-construct coverage MUST be
  re-validated.

## Governance

This constitution defines the non-negotiable development rules for the **Q and A
Practise 2** project.

- It supersedes ad-hoc practices or preferences when there is a conflict.
- Any deviation from these rules MUST be explicitly justified in planning documents and
  approved by the supervising teacher or project owner.

### Versioning and Amendments

- The constitution uses semantic versioning: **MAJOR.MINOR.PATCH**.
  - **MAJOR**: Backward-incompatible changes to principles or governance.
  - **MINOR**: New principles or materially expanded guidance.
  - **PATCH**: Clarifications, wording fixes, or non-semantic refinements.
- Amendments MUST be made by editing `.specify/memory/constitution.md`, updating the
  version number and **Last Amended** date, and summarizing changes in the Sync Impact
  Report at the top of this file.

### Compliance Expectations

- Each new feature plan MUST complete the "Constitution Check" gate before
  implementation work begins.
- When reviewing features or preparing final submission, the team (or individual
  student) MUST verify:
  - Minimal file structure is still respected.
  - IB CS SL alignment is clear in spec and documentation.
  - At least 15 constructs from the defined list are present.
  - Python code remains PEP8-compliant.
- Non-compliant changes MUST either be revised to comply or explicitly documented and
  accepted as exceptions by the supervising teacher.

**Version**: 1.0.0 | **Ratified**: 2025-12-08 | **Last Amended**: 2025-12-08
