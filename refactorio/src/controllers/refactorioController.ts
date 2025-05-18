import * as vscode from 'vscode';
import { Repository } from '../types/git';
import { ModelService } from '../services/modelService';
import { GitService } from '../services/gitService';
import { UIService } from '../services/uiService';
import {
    RefactoredContentProvider,
    REFACTORED_SCHEME,
} from '../services/documentProvider';
import { RefactoringResult } from '../types/refactoring';

/**
 * Main controller for the Refactorio extension.
 * Orchestrates the interaction between Git monitoring, code analysis, and UI updates.
 * Manages the workflow of detecting, analyzing, and presenting potential refactoring opportunities.
 */
export class RefactorioController {
    private refactoringResults: Map<string, RefactoringResult> = new Map();

    constructor(
        private modelService: ModelService,
        private gitService: GitService,
        private uiService: UIService,
        private provider: RefactoredContentProvider
    ) {}

    /**
     * Initializes the controller by setting up Git repository monitoring.
     * Should be called when the extension activates.
     */
    initialize() {
        this.gitService.listenToRepositories((repo) =>
            this.handleNewRepository(repo)
        );
    }

    /**
     * Sets up commit monitoring for a new repository.
     * @param repository The Git repository to monitor
     */
    private async handleNewRepository(repository: Repository) {
        console.log('Listening to new repository:', repository.rootUri.fsPath);
        repository.onDidCommit(() => this.handleCommitChanges(repository));
    }

    /**
     * Handles new commits in a repository by analyzing changed Java files
     * for potential refactoring opportunities.
     * @param repository The repository where the commit occurred
     */
    private async handleCommitChanges(repository: Repository) {
        try {
            const changes = await this.gitService.getCommitDiff(repository);
            const javaFiles = this.gitService.filterJavaFiles(changes);

            if (javaFiles.length === 0) {
                return;
            }

            // Process all files in parallel with a single progress notification
            const results = await this.uiService.showProgressNotification(
                `Analyzing ${javaFiles.length} file(s) for potential refactoring`,
                async () => {
                    const processingPromises = javaFiles.map((file) =>
                        this.getRefactoredCode(file)
                    );
                    return Promise.allSettled(processingPromises);
                }
            );

            let hasValidResults = false;
            results.forEach((result, index) => {
                if (result.status === 'fulfilled' && result.value) {
                    const uri = javaFiles[index];
                    const refactoringResult = result.value;

                    // Only store results that have actual refactoring changes
                    if (refactoringResult.refactoredContent !== '') {
                        this.refactoringResults.set(
                            uri.toString(),
                            refactoringResult
                        );
                        hasValidResults = true;
                    } else {
                        console.log(
                            `No refactoring needed for ${uri.toString()}`
                        );
                    }
                }
            });

            if (hasValidResults) {
                await vscode.commands.executeCommand(
                    'setContext',
                    'refactorioHasChanges',
                    true
                );
                await this.notifyMultipleChanges();
            }
        } catch (error) {
            console.error('Error handling commit:', error);
            if (error instanceof Error) {
                vscode.window.showErrorMessage(`Git error: ${error.message}`);
            }
        }
    }

    /**
     * Sends file content to the AI model for analysis and creates a RefactoringResult.
     * @param uri The URI of the file to analyze
     * @returns Promise resolving to RefactoringResult if successful, undefined otherwise
     */
    private async getRefactoredCode(
        uri: vscode.Uri
    ): Promise<RefactoringResult | undefined> {
        try {
            const document = await vscode.workspace.openTextDocument(uri);
            const originalContent = document.getText();

            const response = await this.modelService.callModel(
                originalContent,
                'Factory'
            );
            const refactoredText = await response.text();
            const refactoredContent =
                this.modelService.parseResponseCode(refactoredText);

            return {
                originalUri: uri,
                originalContent,
                refactoredContent,
            };
        } catch (error) {
            console.error('Error getting refactored code:', error);
            return undefined;
        }
    }

    /**
     * Returns all current refactoring results.
     * @returns Map of file URIs to their RefactoringResults
     */
    getRefactoringResults(): Map<string, RefactoringResult> {
        return this.refactoringResults;
    }

    /**
     * Applies refactored changes from the diff view to the original file.
     * Handles saving the file, closing the diff view, and showing success/error messages.
     * @param editor The VS Code text editor containing the refactored code
     */
    async applyRefactoredChanges(editor: vscode.TextEditor) {
        if (editor.document.uri.scheme === REFACTORED_SCHEME) {
            const originalUriStr = editor.document.uri
                .with({ scheme: 'file' })
                .toString();
            if (!this.refactoringResults.has(originalUriStr)) {
                vscode.window.showErrorMessage(
                    'No refactoring result found for this file'
                );
                return;
            }
            try {
                const originalUri = editor.document.uri.with({
                    scheme: 'file',
                });
                const newContent = editor.document.getText();
                const originalDoc = await vscode.workspace.openTextDocument(
                    originalUri
                );
                const edit = new vscode.WorkspaceEdit();
                const fullRange = new vscode.Range(
                    originalDoc.positionAt(0),
                    originalDoc.positionAt(originalDoc.getText().length)
                );
                edit.replace(originalUri, fullRange, newContent);
                await vscode.workspace.applyEdit(edit);
                await originalDoc.save();
                await vscode.commands.executeCommand(
                    'workbench.action.closeActiveEditor'
                );
                await vscode.window.showTextDocument(originalDoc);

                vscode.window.showInformationMessage(
                    'Changes applied successfully'
                );
                this.refactoringResults.delete(originalUriStr);

                if (this.refactoringResults.size === 0) {
                    await vscode.commands.executeCommand(
                        'setContext',
                        'refactorioHasChanges',
                        false
                    );
                }
            } catch (error) {
                console.error('Error applying changes:', error);
                if (error instanceof Error) {
                    vscode.window.showErrorMessage(
                        `Error applying changes: ${error.message}`
                    );
                }
            }
        }
    }

    private async notifyMultipleChanges() {
        const shouldViewChanges =
            await this.uiService.showMultipleFilesNotification(
                this.refactoringResults.size
            );
        if (shouldViewChanges) {
            await this.viewRefactoredChanges();
        }
    }

    /**
     * Shows the diff view for refactoring changes.
     * If multiple files have changes, shows a quick pick to select which file to view.
     */
    async viewRefactoredChanges() {
        if (this.refactoringResults.size === 0) {
            return;
        }

        let resultToShow: RefactoringResult | undefined;

        if (this.refactoringResults.size === 1) {
            resultToShow = this.refactoringResults.values().next().value;
        } else {
            const items = Array.from(this.refactoringResults.entries()).map(
                ([uri, result]) => ({
                    label: vscode.workspace.asRelativePath(result.originalUri),
                    result,
                })
            );

            const selected = await vscode.window.showQuickPick(items, {
                placeHolder: 'Select a file to view changes',
            });

            if (!selected) {
                return;
            }

            resultToShow = selected.result;
        }

        if (resultToShow) {
            await this.uiService.showDiffView(resultToShow, this.provider);
        }
    }
}
