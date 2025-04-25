from ollama import Client, ResponseError, pull


class OllamaClient:
    def __init__(self,  model_name: str, host: str = "ai"):
        """
        Initializes the Ollama client with the specified host.
        Args:
            host (str): The host address for the Ollama client.
        """
        self.model_name = model_name
        self.client = Client(host=host)


    def is_model_available(self) -> bool:
        """
        Checks if a model is available in the Ollama client.
        Args:
            model_name (str): The name of the model to be checked.
        Returns:
            bool: True if the model is available, False otherwise.
        """
        is_available = True
        try:
            _ = self.client.show(self.model_name)
        except ResponseError as e:
            is_available = False
        return is_available


    def pull_model(self):
        """
        Pulls a model from the Ollama client.
        Args:
            model_name (str): The name of the model to be pulled.
        """
        
        # Pull the specified model from the Ollama client
        pull(self.model_name)



    def chat(self, prompt: str, q: str):
        """
        Sends a chat request to the Ollama client with the specified model and prompt.
        Args:
            model_name (str): The name of the model to be used for the chat.
            prompt (str): The prompt to be sent to the model.
        Returns:
            Response: The response from the Ollama client.
        """
        # Send a chat request to the Ollama client with the specified model and prompt
        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'system',
                    'content': prompt,
                },
                {
                    'role': 'user',
                    'content': q
                }
            ],
        )

        return {"response": response["message"]["content"]}
