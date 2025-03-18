from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


class TopicBase(BaseModel):
    title: str


class TopicCreate(TopicBase):
    pass


class TopicSchema(TopicBase):
    id: int


class TopicUpdate(BaseModel):
    title: str | None = None


class LessonSchema(BaseModel):
    id: int
    topic_id: int
    title: str
    content: str


class LessonCreate(BaseModel):
    topic_id: int
    title: str
    content: str


class LessonUpdate(BaseModel):
    topic_id: int | None = None
    title: str | None = None
    content: str | None = None


class QuestionSchema(BaseModel):
    id: int
    lesson_id: int
    question_text: str


class QuestionCreate(BaseModel):
    lesson_id: int
    question_text: str


class AnswerSchema(BaseModel):
    id: int
    question_id: int
    answer_text: str
    is_correct: bool


class AnswerCreate(BaseModel):
    question_id: int
    answer_text: str
    is_correct: bool


class UserCompletedLessonSchema(BaseModel):
    user_id: int
    lesson_id: int


class UserCompletedTopicSchema(BaseModel):
    user_id: int
    topic_id: int


class UserCompletedQuestionSchema(BaseModel):
    user_id: int
    question_id: int
    completed_at: datetime
