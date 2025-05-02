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


def recommendations_prompt():
    """
    Generates a prompt for the assistant to provide book recommendations.
    Returns:
        str: The prompt for the assistant.
    """

    prompt = """You are an AI assistant. You will receive a user's watch history and a list of books.

You need to respond to 'Human Query'. You have been provided with 'Contexts' to generate a response.

based on the user's watch history, recommend books that may interest them. You can check the watched books genre and author to find similar books.

**Note:** The output should be in natural language, short, concise, and should only include the book title and author.

Input:
==
User Watch History: 
- 'The Explore' watched 2 times

Books Dataset: 
- {'book_title': 'The Explore', 'book_id': 1, 'author': 'Johnson', 'genre': 'Science Fiction'},
- {'book_title': 'The Great Adventure', 'book_id': 2, 'author': 'John Doe', 'genre': 'Adventure'},
- {'book_title': 'Mystery of the Lost City', 'book_id': 3, 'author': 'Jane Smith', 'genre': 'Mystery'},
- {'book_title': 'Journey to the Unknown', 'book_id': 4, 'author': 'Alice Brown', 'genre': 'Fantasy'},
- {'book_title': 'The Quantum Prophecy', 'book_id': 5, 'author': 'Emily J. Johnson', 'genre': 'Science Fiction'}
==

Output:
==
`The Quantum Prophecy` by `Emily J. Johnson`

Input:
==
{user_watch_history}
Books Dataset: {books_dataset}

Output:
==
            """
            
    

    return prompt
