import subprocess

class CommandExecutor:
    """Executes bash commands and captures their output."""

    def execute_command(self, command: str) -> tuple[str, str, int]:
        """
        Executes a bash command.

        Args:
            command: The bash command to execute.

        Returns:
            A tuple containing stdout, stderr, and the exit code.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False  # Do not raise an exception for non-zero exit codes
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1