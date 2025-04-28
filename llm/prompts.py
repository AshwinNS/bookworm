from api.models import ReviewPublic, BookPublic

def generate_summary_prompt(reviews: ReviewPublic, book: BookPublic):
    """
    Generates a summary of the book using the Ollama client.
    Returns:
        str: The prompt for generating a summary.
    """
    prompt = f"""Write a short summary of the story that is NOT EXCEEDING 150 words long. 
                The summary should be based on its content and the rating provided by users. `DO NOT WRITE THE WHOLE STORY AGAIN OR MENTION TITLES`.
                If you think story content cannot be summarized, then mention only about the user reviews and ratings.
                The summary should be concise, capturing the main plot points and the overall sentiment reflected by the user ratings.

                Story: {book.story}

                User Ratings: {reviews}

                Output Format:
                Summary: <Provide the summary here>
                Aggregated Rating: <Provide the aggregated rating here>
            """

    return prompt


def generate_story_prompt():
    """
    Generates a prompt for the assistant to provide a story based on the book.
    Returns:
        str: The prompt for the assistant.
    """
    # Example prompt for generating a story
    prompt = """Write a random story that is exactly 200 words long. 
                The story can be about anything, but it should include unexpected twists and turns. Feel free to explore any genre, such as mystery, fantasy, or science fiction.
                Ensure the story is engaging and has a clear beginning, middle, and end.
            """

    return prompt


def assistant_prompt():
    """
    Generates a prompt for the assistant to provide a summary of the book.
    Returns:
        str: The prompt for the assistant.
    """
    # Example prompt for the assistant
    prompt = """You are an AI assistant. Who provides only details about books.
            Apart from greeting and DON'T ANSWER ANYTHING ELSE, SAY `I'm not programmed to answer this, please ask about books`.    
            """

    return prompt
