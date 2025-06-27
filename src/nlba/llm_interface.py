import os
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_command(self, natural_language_request: str) -> str:
        """
        Generates a bash command from a natural language request.

        Args:
            natural_language_request: The user's request in natural language.

        Returns:
            A string representing the generated bash command.
        """
        pass


class MockLLMProvider(BaseLLMProvider):
    """A mock LLM provider for testing and development."""

    def generate_command(self, natural_language_request: str) -> str:
        """
        Generates a mock bash command based on the natural language request.
        """
        if "list files" in natural_language_request:
            return "ls -l"
        elif "create directory" in natural_language_request:
            return "mkdir new_dir"
        elif "remove file" in natural_language_request:
            return "rm test_file.txt"
        elif "create a new folder called new_folder" in natural_language_request:
            return "mkdir new_folder"
        else:
            return f"echo 'Mock command for: {natural_language_request}'"


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

    def generate_command(self, natural_language_request: str) -> str:
        prompt = f"Convert the following natural language request into a single, executable bash command. Do not include any explanations or additional text, only the command.\n\nRequest: {natural_language_request}\nCommand:"
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

    def generate_command(self, natural_language_request: str) -> str:
        prompt = f"Convert the following natural language request into a single, executable bash command. Do not include any explanations or additional text, only the command.\n\nRequest: {natural_language_request}\nCommand:"
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that converts natural language requests into bash commands."}, # noqa
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {e}")