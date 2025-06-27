

import argparse
import os
from nlba.llm_interface import MockLLMProvider, GeminiLLMProvider, OpenAILLMProvider
from nlba.command_executor import CommandExecutor

def run_nlba(request: str, provider: str = "mock", skip_confirmation: bool = False):
    if provider == "mock":
        llm_provider = MockLLMProvider()
    elif provider == "gemini":
        llm_provider = GeminiLLMProvider()
    elif provider == "openai":
        llm_provider = OpenAILLMProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

    executor = CommandExecutor()

    print(f"Your request: {request}")

    # Step 1: Generate bash command
    bash_command = llm_provider.generate_command(request)
    print(f"Generated command: {bash_command}")

    # Step 2: Confirm with user (unless --yes is used or skip_confirmation is True)
    if not skip_confirmation:
        confirmation = input("Execute this command? (y/N): ").strip().lower()
        if confirmation != 'y':
            print("Command execution cancelled.")
            return

    # Step 3: Execute command
    stdout, stderr, exit_code = executor.execute_command(bash_command)

    print("\n--- Command Output ---")
    if stdout:
        print("STDOUT:")
        print(stdout)
    if stderr:
        print("STDERR:")
        print(stderr)
    print(f"Exit Code: {exit_code}")
    print("----------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Natural Language Bash Assistant (NLBA)"
    )
    parser.add_argument(
        "request",
        type=str,
        help="Your natural language request (e.g., 'list all files')"
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation and execute command directly"
    )

    parser.add_argument(
        "--provider",
        type=str,
        default="mock",
        choices=["mock", "gemini", "openai"],
        help="Specify the LLM provider to use (e.g., 'gemini', 'openai', 'mock')"
    )

    args = parser.parse_args()
    run_nlba(args.request, args.provider, args.yes)

if __name__ == "__main__":
    main()

