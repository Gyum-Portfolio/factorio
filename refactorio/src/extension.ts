import * as vscode from 'vscode';
import {
    RefactoredContentProvider,
    REFACTORED_SCHEME,
} from './services/documentProvider';
import { ModelService } from './services/modelService';
import { GitService } from './services/gitService';
import { UIService } from './services/uiService';
import { RefactorioController } from './controllers/refactorioController';

export function activate(context: vscode.ExtensionContext) {
    console.log('Refactorio is now active!');

    // Initialize services
    const provider = new RefactoredContentProvider();
    const modelService = new ModelService();
    const gitService = new GitService();
    const uiService = new UIService();

    // Initialize controller
    const controller = new RefactorioController(
        modelService,
        gitService,
        uiService,
        provider
    );

    // Register provider
    context.subscriptions.push(
        vscode.workspace.registerTextDocumentContentProvider(
            REFACTORED_SCHEME,
            provider
        )
    );

    // Initialize controller
    controller.initialize();

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand(
            'refactorio.applyRefactoredChanges',
            async (editor) => await controller.applyRefactoredChanges(editor)
        ),
        vscode.commands.registerCommand(
            'refactorio.startListeningToGitChanges',
            () => controller.initialize()
        ),
        vscode.commands.registerCommand(
            'refactorio.viewRefactoredChanges',
            async () => await controller.viewRefactoredChanges()
        )
    );
}

// This method is called when your extension is deactivated
export function deactivate() {}
