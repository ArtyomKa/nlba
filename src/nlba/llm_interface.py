class LLMInterface:
    def generate_bash_command(self, natural_language_request: str) -> str:
        # In a real scenario, this would call an LLM API
        print(f"DEBUG: LLM received request: '{natural_language_request}'")
        # Simple mock for now
        if "list files" in natural_language_request:
            return "ls -l"
        elif "create directory" in natural_language_request:
            parts = natural_language_request.split()
            dir_name = parts[-1] if parts[-1] != "directory" else "new_directory"
            return f"mkdir {dir_name}"
        elif "remove file" in natural_language_request:
            parts = natural_language_request.split()
            file_name = parts[-1] if parts[-1] != "file" else "file_to_remove.txt"
            return f"rm {file_name}"
        else:
            return f"echo 'Could not generate command for: {natural_language_request}'"
