from ollama import AsyncClient, ResponseError


class OllamaClient:
    def __init__(self,  model_name: str, host: str = "ai"):
        """
        Initializes the Ollama client with the specified host.
        Args:
            host (str): The host address for the Ollama client.
        """
        self.model_name = model_name
        self.client = AsyncClient(host=host)


    async def is_model_available(self) -> bool:
        """
        Checks if a model is available in the Ollama client.
        Args:
            model_name (str): The name of the model to be checked.
        Returns:
            bool: True if the model is available, False otherwise.
        """
        is_available = True
        try:
            await self.client.show(self.model_name)
        except ResponseError as e:
            is_available = False
        return is_available


    async def pull_model(self):
        """
        Pulls a model from the Ollama client.
        Args:
            model_name (str): The name of the model to be pulled.
        """
        
        # Pull the specified model from the Ollama client
        await self.client.pull(self.model_name)


    async def chat(self, prompt: str, q: str):
        """
        Sends a chat request to the Ollama client using the specified prompt and user query.
        Args:
            prompt (str): The system prompt to guide the conversation.
            q (str): The user's query or input message.
        Returns:
            dict: A dictionary containing the response message content from the chat model.
        """     
        # Send a chat request to the Ollama client with the specified prompt and user query

        response = await self.client.chat(
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
