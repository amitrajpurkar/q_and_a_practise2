# Feature Specification: Offline Quiz Question Bank

**Feature Branch**: `001-offline-quiz`  
**Created**: 2025-12-08  
**Status**: Draft  
**Input**: User description: "Standalone offline quiz that uses a pre-defined list of questions and answers in a local text/CSV file. The user chooses a topic/subject and a difficulty level (easy, medium, hard). The application randomly picks questions from the chosen topic and difficulty, accepts answers, checks them against the question bank, keeps track of the user's score, and at the end shows a summary with score, time spent, and a review of incorrect questions with the correct answers."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Take quiz by topic and difficulty (Priority: P1)

As a student, I want to select a topic and a difficulty level and then answer a series of
questions so that I can practice specific material at an appropriate challenge level.

**Why this priority**: This is the core value of the application. Without the ability to
take a quiz by topic and difficulty, the rest of the functionality has no purpose.

**Independent Test**: Start a quiz session, select a topic and difficulty, answer a set
of questions, and verify that all questions shown match the selected topic and
difficulty, that answers are accepted, and that a score is tracked during the session.

**Acceptance Scenarios**:

1. **Given** the application has loaded a question bank from a local file and displays a
   list of topics, **When** the student chooses a topic and one of the three difficulty
   levels (easy, medium, hard) and starts a quiz, **Then** the system must present at
   least one question that matches the chosen topic and difficulty.
2. **Given** a quiz is in progress, **When** the student submits an answer for a
   displayed question, **Then** the system must record whether the answer is correct or
   incorrect and update the running score for the current session.

---

### User Story 2 - View quiz summary (Priority: P2)

As a student, I want to see a clear summary of my performance at the end of the quiz so
that I understand how many questions I answered correctly and how long I spent.

**Why this priority**: The summary provides immediate feedback and supports reflection,
which is important for learning and for IB-style evaluation.

**Independent Test**: Complete a quiz session and verify that the end-of-session screen
shows the total number of questions attempted, number correct, percentage score, and
total time spent in the session.

**Acceptance Scenarios**:

1. **Given** a quiz session has ended, **When** the summary is displayed, **Then** the
   student must see at least the total number of questions answered, the number of
   correct answers, and the overall percentage score.
2. **Given** a quiz session has ended, **When** the summary is displayed, **Then** the
   student must see the total time spent answering questions in that session.

---

### User Story 3 - Review incorrect questions (Priority: P3)

As a student, I want to see which questions I answered incorrectly along with the
correct answers so that I can review my mistakes and learn from them.

**Why this priority**: Reviewing incorrect answers supports deeper understanding and is
valuable evidence for learning and reflection.

**Independent Test**: Complete a quiz session with at least one incorrect answer and
verify that the review section lists each incorrect question, the student's answer, and
the correct answer from the question bank.

**Acceptance Scenarios**:

1. **Given** a quiz session has at least one incorrect answer, **When** the review
   section is shown, **Then** the student must see each incorrect question and the
   correct answer for that question.
2. **Given** a quiz session has no incorrect answers, **When** the review section is
   shown, **Then** the student must be informed that all questions were answered
   correctly and no corrections are needed.

---

### Edge Cases

- When there are no questions for the chosen combination of topic and difficulty, the
  system must prevent the quiz from starting and inform the student that no questions
  are available for that selection, asking them to choose another topic or difficulty.
- If the student provides an invalid topic or difficulty input (for example, a topic not
  on the list or a difficulty outside easy/medium/hard), the system must reject the
  input and prompt the student to choose from the valid options.
- When a student ends the quiz early (for example, quits before all planned questions
  are answered), the system must still show a partial summary and review for all
  questions that were answered in that session.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load a predefined question bank from a local text or CSV file
  at startup.
- **FR-002**: System MUST present the student with a list of available topics/subjects
  derived from the question bank.
- **FR-003**: System MUST allow the student to select exactly one topic and one of three
  difficulty levels (easy, medium, hard) before any quiz questions are shown.
- **FR-004**: System MUST randomly select questions that match the chosen topic and
  difficulty level from the question bank for the duration of the quiz session.
- **FR-005**: System MUST display each selected question and accept an answer from the
  student.
- **FR-006**: System MUST compare each submitted answer with the correct answer stored
  in the question bank and classify the response as correct or incorrect.
- **FR-007**: System MUST track the student's score during a quiz session, including at
  minimum the total number of questions asked and the number answered correctly.
- **FR-008**: System MUST measure the total time the student spends answering questions
  in a quiz session (from quiz start until the session ends).
- **FR-009**: At the end of a quiz session, System MUST display a summary that includes
  at least: total questions attempted, number of correct answers, percentage score, and
  total time spent.
- **FR-010**: At the end of a quiz session, System MUST provide a review section listing
  each question that was answered incorrectly, the student's answer, and the correct
  answer from the question bank.
- **FR-011**: System MUST end a quiz session after a fixed number of questions per
  session. This fixed number is defined by the application configuration or teacher
  instructions and is the same for all sessions unless explicitly changed outside the
  quiz flow.
- **FR-012**: System MUST allow a student to end a quiz session early (before the fixed
  number of questions has been reached) and still produce a summary and review for all
  questions that were answered.
- **FR-013**: System MUST treat each question as a multiple-choice item, where the
  question bank stores a set of answer options and identifies exactly one correct
  option for each question. The question bank file format MUST support storing these
  options and the correct answer in a consistent, parseable way.

### Key Entities *(include if feature involves data)*

- **Question**: Represents a single quiz question in the question bank.
  - Key attributes: identifier, topic/subject, difficulty level, question text, correct
    answer, and optionally a set of answer options.
- **Quiz Session**: Represents one run of the quiz for a student.
  - Key attributes: selected topic, selected difficulty, list of asked questions and
    responses, number of correct and incorrect answers, start time, end time, and
    derived summary data (score and duration).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student can select any available topic and one of the three difficulty
  levels and complete a quiz session without encountering missing or mismatched
  questions for that selection.
- **SC-002**: For a test session with a known set of questions and answers, the summary
  must report the correct total questions, correct answers, and percentage score with
  100% accuracy.
- **SC-003**: For sessions timed in controlled tests, the reported total time spent must
  be accurate within an acceptable small margin (for example, within a few seconds) of
  the measured real time.
- **SC-004**: In user testing, at least 90% of students report that the end-of-quiz
  summary and review make it clear which questions they answered incorrectly and what
  the correct answers were.
