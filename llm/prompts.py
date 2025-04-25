

def generate_summary_prompt():
    """
    Generates a summary of the book using the Ollama client.
    Returns:
        str: The prompt for generating a summary.
    """
    # Example prompt for generating a summary
    prompt = """You are an AI assistant and your task is to generate a summary of the book based on the provided information.
                Please check the context provided by the user.
                You should provide a concise and informative summary that captures the main themes and ideas of the book.
                If the summary is not available, please mention that in the response.
                Please do not include any personal opinions or interpretations.
                Please provide the summary in a single paragraph without any bullet points or lists.
                MAKE SURE TO INCLUDE THE BOOK TITLE AND AUTHOR NAME IN THE SUMMARY.
                ENSURE THE SUMMARY IS MAXIMUM 100 WORDS LONG.
            """

    return prompt


def assistant_prompt():
    """
    Generates a prompt for the assistant to provide a summary of the book.
    Returns:
        str: The prompt for the assistant.
    """
    # Example prompt for the assistant
    prompt = "You are an AI assistant."

    return prompt
