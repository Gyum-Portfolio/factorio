# Refactorio

Refactorio is a proactive VS Code extension that automatically identifies opportunities to implement design patterns in your Java code. It analyzes your code changes during git commits and suggests pattern-based improvements to enhance your codebase.

## Features

-   Automatically analyzes code during git commits to detect design pattern opportunities
-   Currently supports Factory Pattern detection and implementation
-   Generates optimized code refactoring suggestions in real-time
-   Provides side-by-side code review interface for suggested changes
-   Seamlessly integrates with VS Code's git workflow

## Getting Started

1. Install the extension in VS Code (`Extensions: Install from VSIX`)
2. Open any Java project with git version control
3. Make changes to your Java files and stage them for commit
4. When you commit changes, Refactorio will analyze the code
5. If improvements are detected, click "View" or use `refactorio.viewRefactoredChanges`
6. Review the suggestions and apply them with `refactorio.applyRefactoredChanges` (default: `Alt+Enter`).

## Configuration

The extension allows switching the model providers with the `refactorio.modelProvider` setting.

## Development Setup

To work on the extension:

1. Clone and open the `refactorio` folder in VS Code
2. Install dependencies with `npm install`
3. Compile the extension with `npm run compile`
4. Press F5 (`Debug: Start Debugging`) in the `extension.ts` file to start debugging
5. Test changes using the `examples` directory
6. Commit test files to trigger the extension
7. Check the debug console for detailed logs
8. Remember to revert test commits after debugging

## Troubleshooting

If you encounter issues during development:

-   Clear the extension cache by deleting the `out` directory
-   Rebuild with `npm run compile`
-   Check debug console for error messages
-   Ensure all dependencies are properly installed
