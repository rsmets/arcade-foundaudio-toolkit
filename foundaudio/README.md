<div style="display: flex; justify-content: center; align-items: center;">
  <img
    src="https://docs.arcade.dev/images/logo/arcade-logo.png"
    style="width: 250px;"
  >
</div>

<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
  <img src="https://img.shields.io/github/v/release/rsmets/foundaudio" alt="GitHub release" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" style="margin: 0 2px;">
  <img src="https://img.shields.io/pypi/v/foundaudio" alt="PyPI version" style="margin: 0 2px;">
  <img src="https://github.com/rsmets/foundaudio/workflows/CI/badge.svg" alt="CI Status" style="margin: 0 2px;">
</div>
<div style="display: flex; justify-content: center; align-items: center;">
  <a href="https://github.com/rsmets/foundaudio" target="_blank">
    <img src="https://img.shields.io/github/stars/rsmets/foundaudio" alt="GitHub stars" style="margin: 0 2px;">
  </a>
  <a href="https://github.com/rsmets/foundaudio/fork" target="_blank">
    <img src="https://img.shields.io/github/forks/rsmets/foundaudio" alt="GitHub forks" style="margin: 0 2px;">
  </a>
</div>


<br>
<br>

# Arcade foundaudio Toolkit
interface with found audio
## Features

- The foundaudio toolkit does not have any features yet.

## CI/CD

This project uses GitHub Actions for continuous integration and deployment:

- **CI Workflow**: Runs on every push to `main` and on pull requests
- **PR Checks**: Additional checks for pull requests including pre-commit hooks
- **Multi-Python Support**: Tests against Python 3.10, 3.11, 3.12, and 3.13
- **Code Quality**: Automated linting, type checking, and testing
- **Coverage**: Code coverage reporting with minimum 80% threshold

### Running CI Locally

You can test the CI workflow locally using the provided script:

```bash
./scripts/test-ci-locally.sh
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

## Development

Read the docs on how to create a toolkit [here](https://docs.arcade.dev/home/build-tools/create-a-toolkit)