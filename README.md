# 521290S Distributed Systems - Design Document
## Distributed Secrets Management with Multi-Party Approval

## Summary
 This design document serves as a guide for the development of the Distributed Systems course project. The document includes information such as project team, overview, requirements, design considerations, system architecture, user interface design, security measures, testing strategies, and deployment plans. It aims to provide an understanding of the project’s scope, goals and technical details.

## Introduction
In the digital landscape, companies often safeguard sensitive information, referred to as secrets, containing data such as passwords, keys, configuration files, and credentials. Protecting these secrets is crucial, with access typically restricted to high-level employees to prevent potential disasters caused by unauthorized access.

Most companies do not have the funding for a separate cybersecurity team and thus common practices involve insecure handling of secrets, such as storing them in plaintext files, sharing via email or chat services, or even writing them down on paper. These methods lack the necessary access control and logging mechanisms, leaving organizations vulnerable to security breaches with no means of tracing who accessed which secret and for what purpose.

In response to this issue, our group has decided to design a distributed secret management system as the course project. This system will require users to obtain approval from their peers before accessing secrets, ensuring a common consensus and understanding of who accessed what. Event logging is implemented and plays a crucial role in providing a comprehensive audit trail to track every instance of secret access, along with the associated user and purpose.

## System Overview
The Distributed Secrets Management with Multi-Party Approval system's central idea is to ensure that sensitive information, or secrets, can only be accessed when several authorized individuals agree (common consensus). This way no single person can access cruicial data without approval from their peers.

The system maintains a thorough log of every instance when someone accesses a secret. This log captures important details like who accessed the secretm the purpose behind the access, and the exact time it occurred.

This combined approach, where decisions are collective and actions are recorded, provides a secure and transparent system. It guarantees that sensitive information is accessed with proper authorization, and the detailed log allows for review and verifying, promoting accountability and transparency.

## Requirements
System-level requirements given by the course are:
- The system shall address a real-world application or a research problem
- The system shall demonstrate selected distributed system functionalities
- The system shall have at least three nodes (e.g, containers)
- Each node shall have a role: client, server, peer, broker, etc.
- Participating nodes shall exchange information (messages)
- Participating nodes shall log their behavio understandably
- Each node shall be an independent entity and (partially) autonomus

Detailed requirements will be documented as individual tickets within the [Projects section of this repository](https://github.com/users/juskoski/projects/1/views/1).

### Architecture
The system architecture is outlined in the following image. Adjustments to the architecture may take place as the requirements are planned and development progresses.
![Architecture diagram](/img/DistributedSystemArchitectureV1.png)

## Development, Testing & Deployment
### Requirement/ticket naming, descriptions
Requirement shall be documented using tickets. Ticket naming shall be clear and concise. Use titles that clearly convey the essence of the task. Avoid vague terms and provide enough information to understand the ticket at a glance. Begin the title with an action verb to indicate what needs to be done. For example, "Implement feature X", "Fix problem Y", "Test feature Z". Prefixes "Feature" and "Fix" shall be used to give the ticket a category ("Feature" for a new feature, "Fix" for a bug).
Ticket description

Like the title, keep the description clear and consice. Start with a brief overview to provide context and explain why the ticket is necessary. The acceptance criteria shall be clearly outlined, bullet points can make it more readable.

Each ticket shall be given story points according to the following chart:
![Story points chart](/img/StoryPoints.png)  
Due to limitations with time, no ticket shall have more than 5 story points.

### Development
The development process will incorporate Scrum methodologies, with sprints lasting one week each. Prior to each sprint, a sprint planning session shall be held. Throughout the sprint, team members shall update other members on their completed tasks, current work, and any issues they may be facing. Following the completion of each sprint, a sprint review and retrospective shall be conducted to assess and ehance the team's processes and efficiency.
![Scrum cycle](/img/ScrumCycle.png)

### Testing
Given time constraints and limited expertise in developing distributed systems, manual testing will be the primary testing method. Recognizing the potential for errors, each developer is responsible for testing their own code. As a risk mitigation measure, developers are required to document the steps taken to test the functionality during the merge requst process.

### Branching & Commits
Every ticket will be handled in a dedicated branch, with the branch name incorporating the ticket's ID followed by its name. For example, the branch corresponding to the ticket "Implement secret access logging #24" should be named "24-implement-secret-access-logging". Note that the "#24" is automatically assigned by GitHub. This naming convention establishes a clear audit trail, allowing easy tracking of which features were merged at a specific stages in the project.

Commit messages must follow the 50/72 rule, with the title limited to a maximum of 50 characters and the description to 72 characters. The title should be written in imperative tense, such as "Add feature X" or "Fix bug Y". It is advisable to keep individual commits as small as possible. This approach helps prevent reviewer fatigue during the merge request review process.

### Merge Requests
Every branch must undergo a peer review before merging into the main branch. Once a developer completes a task, they push their branch to GitHub and initiate a merge request. In the request description, the author must detail how they verified the functionality and assign a reviewer. The reviewer shall be a different person than the author. The reviewer can add comments that must be addressed before the branch is merged. Upon the reviewer's approval, the author can proceed to merge the request and close the associated ticket.
