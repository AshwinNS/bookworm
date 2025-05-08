from sqlmodel import SQLModel
from pydantic import field_validator


class ReviewBase(SQLModel):
    user_id: int
    review_text: str
    rating: int

    @field_validator("rating")
    def validate_rating(cls, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating
    
    @field_validator("user_id")
    def validate_user_id(cls, user_id):
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
        return user_id


class ReviewCreateModel(ReviewBase):
    pass


class ReviewResponseModel(ReviewBase):
    id: int
    book_id: int
