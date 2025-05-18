import * as vscode from 'vscode';
import { GitExtension, Repository, Change, API as GitAPI } from '../types/git';

/**
 * Service for interacting with Git functionality in VS Code.
 * Handles repository monitoring, commit analysis, and file filtering.
 */
export class GitService {
    private git?: GitAPI;

    constructor() {
        this.git = this.getGitExtension();
    }

    /**
     * Retrieves the VS Code Git extension API.
     * @returns The Git extension API or undefined if not found
     */
    private getGitExtension(): GitAPI | undefined {
        const gitExtension =
            vscode.extensions.getExtension<GitExtension>('vscode.git')?.exports;
        if (!gitExtension) {
            console.error('Git extension not found');
            return;
        }
        return gitExtension.getAPI(1);
    }

    /**
     * Sets up listeners for Git repository events.
     * Calls the provided callback for existing repositories and when new ones are opened.
     * @param callback Function to call with each repository
     */
    listenToRepositories(callback: (repo: Repository) => void) {
        if (!this.git) {
            return;
        }

        this.git.repositories.forEach(callback);
        this.git.onDidOpenRepository(callback);
        this.git.onDidCloseRepository((repository) => {
            console.log('Closed repository:', repository.rootUri.fsPath);
        });
    }

    /**
     * Filters a list of changes to only include Java files.
     * @param changes Array of file changes from Git
     * @returns Array of URIs for changed Java files
     */
    filterJavaFiles(changes: Change[]): vscode.Uri[] {
        return [
            ...new Set(
                changes
                    .filter((change) => change.uri.fsPath.endsWith('.java'))
                    .map((change) => change.uri)
            ),
        ];
    }

    /**
     * Gets the diff between the latest commit and its parent.
     * @param repository The Git repository to analyze
     * @returns Promise resolving to array of changes between commits
     */
    async getCommitDiff(repository: Repository): Promise<Change[]> {
        const commits = await repository.log({ maxEntries: 2 });
        if (commits.length < 2) {
            return [];
        }

        const [latestCommit, previousCommit] = commits;
        return repository.diffBetween(previousCommit.hash, latestCommit.hash);
    }
}
