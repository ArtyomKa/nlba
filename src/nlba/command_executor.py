import subprocess

class CommandExecutor:
    def execute_command(self, command: str) -> tuple[str, str, int]:
        print(f"DEBUG: Executing command: '{command}'")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1
