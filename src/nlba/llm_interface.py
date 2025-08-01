import os
from abc import ABC, abstractmethod

PROMPT_TEMPLATE = (
    "Convert the following natural language request into a single, executable bash command. "
    "Format the response as:\nCOMMAND\nCLASSIFICATION\n"
    "Where CLASSIFICATION is either 'destructive' or 'non-destructive'. "
    "Do not include any explanations or additional text.\n\nRequest: {request}\nCommand:"
)

SUMMARY_PROMPT_TEMPLATE = (
    "Summarize the following command output in a single, user-friendly sentence. "
    "The original request was: '{request}'.\n\n"
    "Command: '{command}'\n\n"
    "Output:\n{output}\n\n"
    "Summary:"
)

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_command(self, natural_language_request: str) -> tuple[str, str]:
        """
        Generates a bash command from a natural language request.

        Args:
            natural_language_request: The user's request in natural language.

        Returns:
            A tuple containing the bash command and a classification ("destructive" or "non-destructive").
        """
        return "ls -l", "non-destructive"

    @abstractmethod
    def summarize_output(self, request: str, command: str, output: str) -> str:
        """
        Summarizes the output of a command.

        Args:
            request: The original natural language request.
            command: The executed bash command.
            output: The output of the command.

        Returns:
            A natural language summary of the output.
        """
        return f"The command '{command}' was executed."


class MockLLMProvider(BaseLLMProvider):
    """A mock LLM provider for testing and development."""

    def generate_command(self, natural_language_request: str) -> tuple[str, str]:
        """
        Generates a mock bash command based on the natural language request.
        """
        if "list files" in natural_language_request:
            return "ls -l", "non-destructive"
        elif "create directory" in natural_language_request:
            return "mkdir new_dir", "destructive"
        elif "remove file" in natural_language_request:
            return "rm test_file.txt", "destructive"
        elif "create a new folder called new_folder" in natural_language_request:
            return "mkdir new_folder", "destructive"
        else:
            return f"echo 'Mock command for: {natural_language_request}'", "non-destructive"

    def summarize_output(self, request: str, command: str, output: str) -> str:
        return f"This is a mock summary for the command: '{command}'"


class GeminiLLMProvider(BaseLLMProvider):
    """LLM provider using Google Gemini API."""

    def __init__(self):
        try:
            import google.generativeai as genai
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        except ImportError:
            raise ImportError("google-generativeai not installed. Please install it with 'pip install google-generativeai'")
        except Exception as e:
            raise RuntimeError(f"Failed to configure Gemini API: {e}")

    def generate_command(self, natural_language_request: str) -> tuple[str, str]:
        prompt = PROMPT_TEMPLATE.format(request=natural_language_request)
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            # print(f"Gemini response: {response_text}")
            lines = response_text.splitlines()
            if len(lines) >= 2:
                command = lines[0]
                classification = lines[1]
            else:
                command = response_text
                classification = "non-destructive"
            return command, classification
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")

    def summarize_output(self, request: str, command: str, output: str) -> str:
        prompt = SUMMARY_PROMPT_TEMPLATE.format(request=request, command=command, output=output)
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")


class OpenAILLMProvider(BaseLLMProvider):
    """LLM provider using OpenAI API."""

    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        except ImportError:
            raise ImportError("openai not installed. Please install it with 'pip install openai'")
        except Exception as e:
            raise RuntimeError(f"Failed to configure OpenAI API: {e}")

    def generate_command(self, natural_language_request: str) -> tuple[str, str]:
        prompt = PROMPT_TEMPLATE.format(request=natural_language_request)
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that converts natural language requests into bash commands."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.1,
            )
            response_text = response.choices[0].message.content.strip()
            print(f"OpenAI response: {response_text}")
            lines = response_text.splitlines()
            if len(lines) >= 2:
                command = lines[0]
                classification = lines[1]
            else:
                command = response_text
                classification = "non-destructive"
            return command, classification
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {e}")

    def summarize_output(self, request: str, command: str, output: str) -> str:
        prompt = SUMMARY_PROMPT_TEMPLATE.format(request=request, command=command, output=output)
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes command outputs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {e}")