# Contributing
Contributing to the repository assumes that you have at least basic knowledge of GitHub workflows.

# Prerequisites
* [Python 3.11.6](https://www.python.org/downloads/release/python-3116/)

# Tools
* [JetBrains Pycharm](https://www.jetbrains.com/) (Note: Institutional accounts include a free year license of JetBrains All Products Pack)
* [Git](https://git-scm.com/) or [GitHub Desktop](https://desktop.github.com/) (Note: The contributing guide will only show examples for Git. GitHub Desktop will be at your own discretion.)

# Project Initialization
1. Clone the repository into your chosen directory `git clone https://github.com/sukaruta/EchoesOfTheHalls.git`
2. Install the required Python packages `pip install -r requirements.txt`

# Testing
1. Ensure the game runs with no errors.
2. Unless specified, make sure no features/functions stop working or stop working as intended.

# Commits
This repository follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
1. The commit name should follow conventional commit format: `feat: Add functional sprint bar in player script`
2. The commit name should complete the sentence "This commit will..."
3. Use the present tense, "Add feature" not "Added feature"
4. Use the imperative mood, "Fix crouch desync..." not "Fixing crouch desync..."

## Branching
Do not commit straight to the `main` branch. When implementing a change, create a separate branch prefixed with your GitHub username `sukaruta/` and shortly name it with what you intend to implement. 
`sukaruta/chase-entities`

## Making Pull Requests
Tasks in this repository are defined as issues. If you are tackling a specific task, create a Pull Request targeting that specific issue. You can link the PR in two ways:

Link the Issue to the PR by clicking on the Issue and then under "Linked pull requests", link the PR that you just made.
Add the keywords in the PR's description according to the GitHub docs.

When you want to do a task that isn't an existing Issue yet, you can create an Issue and work on it yourself.