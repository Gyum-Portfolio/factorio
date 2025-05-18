import * as vscode from 'vscode';

/**
 * Service for interacting with the AI model API.
 * Handles sending code for analysis and parsing responses.
 */
export class ModelService {
    private static readonly endpoint =
        'https://puqb636le2.execute-api.us-east-1.amazonaws.com/Prod/analyze';

    /**
     * Calls the AI model API to analyze code for potential refactoring.
     * @param code The source code to analyze
     * @param designPattern The design pattern to look for
     * @returns Promise resolving to the API response
     */
    async callModel(code: string, designPattern: string): Promise<Response> {
        console.log(`Calling endpoint with ${designPattern} design pattern`);

        return fetch(ModelService.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code,
                designPattern,
                model_provider: this.getModelProvider(),
            }),
        });
    }

    /**
     * Gets the configured AI model provider from VS Code settings.
     * @returns The model provider name, defaults to 'anthropic'
     */
    private getModelProvider(): string {
        return (
            vscode.workspace
                .getConfiguration('refactorio')
                .get<string>('modelProvider') || 'anthropic'
        );
    }

    /**
     * Parses the response from the AI model API to extract the refactored code.
     * Handles special cases like removing language tags.
     * @param responseText The raw response text from the API
     * @returns The extracted and cleaned code
     */
    parseResponseCode(responseText: string): string {
        const responseObject = JSON.parse(responseText);
        console.log(responseObject);
        const code = responseObject['body']['code'] as string;
        return code.startsWith('java\n') ? code.substring(5) : code;
    }
}
