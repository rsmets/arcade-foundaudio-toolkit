# Arcade Toolkit Presentation

Agenda

- Frame my decision-making
- Showcase tooling leveraged
- Present implementation
- Demo
- Toolkit development feedback

---

``

## README

The [README](./README.md) has most of the important details I want to touch on. Let's go there.

---

## Implementation

`get_audio_list`

Tool

- Intent-based implementation
- Use of context for secret management
- Graceful error handling with RetryableToolError

Tests

- Unit tests with external mocks to cover normal operation, input validation (e.g., limit boundaries), and error handling (e.g., missing secrets).

Evals

- Fairly extensive scenarios of how one would interface with the tool

---

### Gitops Workflow

- Metalinting with Trunk was done for every commit and push. Also confirmed in CI.
- Enforcing pull request repository rules with required CI test and eval status checks
- Encouraging proper use of semver versioning with the deploy CI/CD job

---

## Demo

I will show off the agent app in a moment, but first, let's look at the toolkit [in action](https://api.arcade.dev/dashboard/playground/chat)

---

## Toolkit development feedback

- Offering a toolkit dev kit in Typescript would have helped me personally
- Information around running evals was not very clear. I feel it should default to the remote eval server, api.arcade.dev
- Providing Github actions would have helpful for the gitops workflows
  - Allowing passing of apiKey directly to `arcade login` would have also helped
- Providing an official MCP documentation server is a nice touch
  - Providing a session based getting started guide/walk through I think would also help others

---
