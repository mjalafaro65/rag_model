# Code Review Guidelines
**Northlane Systems — Engineering**
**Effective Date:** February 2026
**Document ID:** ENG-STD-003

## Purpose
Consistent code review practices improve code quality, share knowledge across the team, and catch defects before they reach production.

## Required Reviewers
All pull requests to protected branches (`main`, `release/*`) require at least one approval from a reviewer outside the author's immediate sub-team. Changes touching authentication, billing, or data-deletion logic require an additional approval from a senior engineer or the security champion for that team.

## What Reviewers Should Check
- **Correctness:** Does the code do what the PR description claims?
- **Test coverage:** Are new code paths covered by unit or integration tests? PRs that lower overall test coverage require justification in the description.
- **Readability:** Can a new team member understand this code without extensive context?
- **Security:** Does the change introduce injection risks, unvalidated input, or exposed secrets? See the Secure Coding Checklist (ENG-STD-006).
- **Performance:** Are there obvious inefficiencies (N+1 queries, unnecessary re-renders, unbounded loops)?

## Review Turnaround
Reviewers are expected to provide initial feedback within 1 business day for standard PRs and within 4 hours for PRs tagged `urgent` or `hotfix`. If a reviewer cannot meet this window, they should reassign or flag the delay in the team channel.

## Handling Disagreements
If author and reviewer disagree on an approach, the default is to resolve via a short synchronous conversation rather than prolonged comment threads. Unresolved disagreements after discussion should be escalated to the tech lead for a final decision, which is then documented in the PR for future reference.

## Merge Requirements
A PR may only be merged once:
- All required approvals are obtained
- CI checks (build, lint, tests) pass
- Any requested changes are resolved or explicitly acknowledged by the reviewer

## Self-Merging
Authors may self-merge only for documentation-only changes or dependency version bumps flagged as low-risk by automated tooling. All other changes require reviewer approval before merge, even for urgent fixes.

## Policy Owner
VP of Engineering, Northlane Systems
