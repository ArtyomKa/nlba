

import argparse
import os
from nlba.llm_interface import LLMInterface
from nlba.command_executor import CommandExecutor

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

    args = parser.parse_args()

    llm = LLMInterface()
    executor = CommandExecutor()

    print(f"Your request: {args.request}")

    # Step 1: Generate bash command
    bash_command = llm.generate_bash_command(args.request)
    print(f"Generated command: {bash_command}")

    # Step 2: Confirm with user (unless --yes is used)
    if not args.yes:
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

if __name__ == "__main__":
    main()

