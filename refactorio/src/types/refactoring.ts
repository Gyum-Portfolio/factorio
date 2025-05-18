import * as vscode from 'vscode';

export interface RefactoringResult {
    originalUri: vscode.Uri;
    originalContent: string;
    refactoredContent: string;
}
