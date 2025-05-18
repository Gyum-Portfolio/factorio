import * as vscode from 'vscode';
import { RefactoringResult } from '../types/refactoring';
import {
    RefactoredContentProvider,
    REFACTORED_SCHEME,
} from './documentProvider';

/**
 * Service responsible for handling all VS Code UI interactions including diff views,
 * notifications, and applying refactored changes to files.
 */
export class UIService {
    /**
     * Displays a diff view comparing the original and refactored code.
     * @param result The refactoring result containing original and refactored content
     * @param provider The content provider for the diff view
     */
    async showDiffView(
        result: RefactoringResult,
        provider: RefactoredContentProvider
    ) {
        try {
            const refactoredUri = result.originalUri.with({
                scheme: REFACTORED_SCHEME,
                path: result.originalUri.path,
            });

            provider.updateContent(refactoredUri, result.refactoredContent);

            await vscode.commands.executeCommand(
                'vscode.diff',
                result.originalUri,
                refactoredUri,
                'Original ↔ Refactored (Press Alt+Enter to apply changes)'
            );
        } catch (error) {
            this.handleError('Error showing diff:', error);
        }
    }

    /**
     * Shows a progress notification for a long-running operation.
     * @param message The message to display in the notification
     * @param operation The async operation to execute
     * @returns The result of the operation
     */
    async showProgressNotification<T>(
        message: string,
        operation: () => Promise<T>
    ): Promise<T> {
        return vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: message,
                cancellable: false,
            },
            operation
        );
    }

    /**
     * Shows a notification for multiple files with potential refactoring.
     * @param fileCount The number of files with potential refactoring
     * @returns Promise<boolean> True if user chooses to view changes
     */
    async showMultipleFilesNotification(fileCount: number): Promise<boolean> {
        const result = await vscode.window.showInformationMessage(
            `Found potential refactoring opportunities in ${fileCount} file${
                fileCount > 1 ? 's' : ''
            } (⌘⇧R to view)`,
            { modal: false },
            { title: 'View', isCloseAffordance: false }
        );

        return result?.title === 'View';
    }

    /**
     * Handles and displays error messages in a consistent way.
     * @param message The error message prefix
     * @param error The error object
     */
    private handleError(message: string, error: unknown) {
        console.error(message, error);
        if (error instanceof Error) {
            vscode.window.showErrorMessage(`${message} ${error.message}`);
        }
    }
}
