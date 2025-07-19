

import argparse
import os
from nlba.llm_interface import MockLLMProvider, GeminiLLMProvider, OpenAILLMProvider
from nlba.command_executor import CommandExecutor
from nlba.config_manager import load_config, save_config, log_request, get_history_file_path, get_history_entry

def run_nlba(request: str, provider: str = "mock", skip_confirmation: bool = False, summarize: bool = False):
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
    
    log_request(request)

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

    if summarize:
        summary = llm_provider.summarize_output(request, bash_command, stdout)
        print("\n--- Summary ---")
        print(summary)
        print("---------------")

def run_interactive_shell(provider: str = "mock", summarize: bool = False):
    if provider == "mock":
        llm_provider = MockLLMProvider()
    elif provider == "gemini":
        llm_provider = GeminiLLMProvider()
    elif provider == "openai":
        llm_provider = OpenAILLMProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

    executor = CommandExecutor()

    print("Entering NLBA interactive shell. Type 'exit' or 'quit' to leave.")
    display_history()
    while True:
        try:
            request = input("> ").strip()
            if request.lower() in ("exit", "quit"):
                print("Exiting NLBA interactive shell.")
                break
            if not request:
                continue

            if request.startswith('!'):
                try:
                    index = int(request[1:])
                    history_request = get_history_entry(index)
                    if history_request:
                        print(f"Re-executing: {history_request}")
                        request = history_request
                    else:
                        print(f"History entry !{index} not found.")
                        continue
                except (ValueError, IndexError):
                    print(f"Invalid history command: {request}")
                    continue

            print(f"Your request: {request}")

            # Step 1: Generate bash command
            bash_command, classification = llm_provider.generate_command(request)
            if classification.lower() == "destructive":
                color_code = "\033[91m"  # Red
            else:
                color_code = "\033[92m"  # Green
            print(f"Generated command: {color_code}{bash_command}\033[0m")

            # Step 2: Confirm with user
            confirmation = input("Execute this command? (y/N): ").strip().lower()
            if confirmation != 'y':
                print("Command execution cancelled.")
                continue
            
            log_request(request)

            # Step 3: Execute command
            stdout, stderr, exit_code = executor.execute_command(bash_command)

            print("\n--- Command Output ---")
            if stdout:
                print(f"{color_code}{stdout}\033[0m")
            if stderr:
                print(f"{color_code}{stderr}\033[0m")
            print(f"Exit Code: {color_code}{exit_code}\033[0m")
            print("----------------------")

            if summarize:
                summary = llm_provider.summarize_output(request, bash_command, stdout)
                print("\n--- Summary ---")
                print(summary)
                print("---------------")

        except KeyboardInterrupt:
            print("\nExiting NLBA interactive shell.")
            break
        except EOFError:
            print("\nExiting NLBA interactive shell.")
            break

def display_history():
    history_file = get_history_file_path()
    if not history_file.exists():
        print("No history found.")
        return
    
    print("\n--- Command History ---")
    with open(history_file, 'r') as f:
        for i, line in enumerate(f, 1):
            print(f"{i}: {line.strip()}")
    print("----------------------\n")


def main():
    parser = argparse.ArgumentParser(
        description="Natural Language Bash Assistant (NLBA)"
    )
    parser.add_argument(
        "request",
        type=str,
        nargs="?",  # Make request optional for --set-provider or interactive shell
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

    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Enable command output summarization."
    )
    
    parser.add_argument(
        "--history",
        action="store_true",
        help="Display command history."
    )

    args = parser.parse_args()

    if args.history:
        display_history()
        return

    config = load_config()
    
    # Handle --set-provider
    if args.set_provider:
        config['nlba'] = {'provider': args.set_provider}
        save_config(config)
        print(f"Default provider set to: {args.set_provider}")
        return # Exit after setting provider

    # Determine the provider to use
    provider_to_use = args.provider or config.get('nlba', {}).get('provider', 'mock')
    summarize_output = args.summarize or config.get('nlba', {}).get('summarize', False)

    if not args.request:
        # No request given, enter interactive shell mode
        run_interactive_shell(provider_to_use, summarize_output)
    else:
        run_nlba(args.request, provider_to_use, args.yes, summarize_output)

if __name__ == "__main__":
    main()

