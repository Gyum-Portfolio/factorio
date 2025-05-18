import * as vscode from 'vscode';

export const REFACTORED_SCHEME = 'refactored-version';

/**
 * Provides content for the diff view when comparing original and refactored code.
 * Implements VS Code's TextDocumentContentProvider interface to serve virtual documents
 * containing refactored code versions.
 */
export class RefactoredContentProvider implements vscode.TextDocumentContentProvider {
    private _onDidChange = new vscode.EventEmitter<vscode.Uri>();
    private _content = new Map<string, string>();

    onDidChange = this._onDidChange.event;

    /**
     * Required implementation of TextDocumentContentProvider interface.
     * Returns the content for a given URI from the internal content map.
     * @param uri The URI of the virtual document to provide content for
     * @returns The stored content for the URI, or empty string if none exists
     */
    provideTextDocumentContent(uri: vscode.Uri): string {
        return this._content.get(uri.path) || '';
    }

    /**
     * Updates the stored content for a URI and notifies VS Code of the change.
     * @param uri The URI of the virtual document to update
     * @param content The new content to store
     */
    updateContent(uri: vscode.Uri, content: string) {
        this._content.set(uri.path, content);
        this._onDidChange.fire(uri);
    }
}
