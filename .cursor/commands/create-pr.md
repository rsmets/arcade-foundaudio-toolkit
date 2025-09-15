# Command

Create a pull request based on changes from the current branch vs main:

1. **Analyze the changes:**
   - Get the git diff between current branch and main
   - Identify modified, added, and deleted files
   - Categorize changes by type (features, bug fixes, refactoring, tests, docs, etc.)

2. **Generate PR title:**
   - Use conventional commit format when possible
   - Be descriptive and concise
   - Include the main change type (feat, fix, refactor, test, docs, etc.)

3. **Generate PR description with sections:**
   - **Summary:** Brief overview of what changed
   - **Changes:** Detailed list of modifications organized by category
   - **Testing:** What testing was done or needs to be done
   - **Breaking Changes:** Any breaking changes (if applicable)
   - **Additional Notes:** Any other relevant information

4. **Include relevant context:**
   - Reference any related issues or tickets
   - Mention any dependencies or prerequisites
   - Note any configuration changes needed

5. **Format the output:**
   - Use proper markdown formatting
   - Include code snippets for significant changes
   - Add checkboxes for review checklist items
   - Make it ready to copy-paste into GitHub/GitLab

6. **Provide next steps:**
   - Suggest reviewers based on changed files
   - Recommend any additional testing
   - Mention any deployment considerations
