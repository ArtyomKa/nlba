

import argparse
import os
from nlba.llm_interface import MockLLMProvider, GeminiLLMProvider, OpenAILLMProvider
from nlba.command_executor import CommandExecutor
from nlba.config_manager import load_config, save_config

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
    bash_command, classification = llm_provider.generate_command(request)
    if classification.lower() == "destructive":
        color_code = "\033[91m"  # Red
    else:
        color_code = "\033[92m"  # Green
    print(f"Generated command: {color_code}{bash_command}\033[0m")

    # Step 2: Confirm with user (unless --yes is used or skip_confirmation is True)
    if not skip_confirmation:
        confirmation = input("Execute this command? (y/N): ").strip().lower()
        if confirmation != 'y':
            print("Command execution cancelled.")
            return

    # Step 3: Execute command
    stdout, stderr, exit_code = executor.execute_command(bash_command)

    if classification == "destructive":
        color_code = "\033[91m"  # Red
    else:
        color_code = "\033[92m"  # Green
    # Determine color for output based on classification
    if classification.lower() == "destructive":
        color_code = "\033[91m"  # Red
    else:
        color_code = "\033[92m"  # Green

    print("\n--- Command Output ---")
    if stdout:
        print("STDOUT:")
        print(f"{color_code}{stdout}\033[0m")
    if stderr:
        print("STDERR:")
        print(f"{color_code}{stderr}\033[0m")
    print(f"Exit Code: {color_code}{exit_code}\033[0m")
    print("----------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Natural Language Bash Assistant (NLBA)"
    )
    parser.add_argument(
        "request",
        type=str,
        nargs="?",  # Make request optional for --set-provider
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
        choices=["mock", "gemini", "openai"],
        help="Specify the LLM provider to use (e.g., 'gemini', 'openai', 'mock'). Overrides saved config."
    )

    parser.add_argument(
        "--set-provider",
        type=str,
        choices=["mock", "gemini", "openai"],
        help="Save the specified LLM provider as default for future interactions."
    )

    args = parser.parse_args()

    config = load_config()
    
    # Handle --set-provider
    if args.set_provider:
        config['nlba'] = {'provider': args.set_provider}
        save_config(config)
        print(f"Default provider set to: {args.set_provider}")
        return # Exit after setting provider

    # Determine the provider to use
    provider_to_use = args.provider or config.get('nlba', {}).get('provider', 'mock')

    if not args.request:
        parser.error("the following arguments are required: request (unless --set-provider is used)")

    run_nlba(args.request, provider_to_use, args.yes)

if __name__ == "__main__":
    main()
