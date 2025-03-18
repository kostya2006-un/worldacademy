from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import delete, update
from models import (
    Topic,
    Lesson,
    Question,
    Answer,
    UserCompletedLesson,
    UserCompletedTopic,
    UserCompletedQuestion,
)
from schemas import (
    TopicSchema,
    TopicCreate,
    TopicUpdate,
    LessonSchema,
    LessonCreate,
    LessonUpdate,
    QuestionSchema,
    AnswerSchema,
    UserCompletedLessonSchema,
    UserCompletedTopicSchema,
    UserCompletedQuestionSchema,
    QuestionCreate,
    AnswerCreate,
)

from dp import async_session


class TopicRepository:
    @classmethod
    async def add_topic(cls, topic_data: TopicCreate) -> int:
        async with async_session() as session:
            topic = Topic(**topic_data.model_dump())
            session.add(topic)
            await session.flush()  # Тут появится topic.id
            await session.commit()
            return topic.id

    @classmethod
    async def get_topic(cls, topic_id: int):
        async with async_session() as session:
            query = select(Topic).where(Topic.id == topic_id)
            result = await session.execute(query)
            topic_model = result.scalar_one_or_none()
            return (
                TopicSchema.model_validate(topic_model.__dict__)
                if topic_model
                else None
            )

    @classmethod
    async def delete_topic(cls, topic_id: int) -> bool:
        async with async_session() as session:
            query = delete(Topic).where(Topic.id == topic_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def update_topic(cls, topic_id: int, topic_data: TopicUpdate) -> bool:
        async with async_session() as session:
            query = (
                update(Topic)
                .where(Topic.id == topic_id)
                .values(
                    **topic_data.model_dump(exclude_unset=True)
                )  # Обновляются только переданные поля
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def all_topics(cls) -> list[TopicSchema]:
        async with async_session() as session:
            query = select(Topic)
            result = await session.execute(query)
            topics = result.scalars().all()
            return [TopicSchema.model_validate(topic.__dict__) for topic in topics]


class LessonRepository:
    @classmethod
    async def add_lesson(cls, lesson_data: LessonCreate):
        async with async_session() as session:
            lesson = Lesson(**lesson_data.model_dump())
            session.add(lesson)
            await session.commit()
            await session.refresh(lesson)
            return lesson

    @classmethod
    async def get_lessons_by_topic(cls, topic_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Lesson).where(Lesson.topic_id == topic_id)
            )
            return result.scalars().all()

    @classmethod
    async def get_lesson(cls, lesson_id: int):
        async with async_session() as session:
            result = await session.execute(select(Lesson).where(Lesson.id == lesson_id))
            return result.scalar_one_or_none()

    @classmethod
    async def update_lesson(cls, lesson_id: int, lesson_data: LessonUpdate):
        async with async_session() as session:
            result = await session.execute(
                update(Lesson)
                .where(Lesson.id == lesson_id)
                .values(**lesson_data.model_dump(exclude_unset=True))
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def delete_lesson(cls, lesson_id: int):
        async with async_session() as session:
            result = await session.execute(delete(Lesson).where(Lesson.id == lesson_id))
            await session.commit()
            return result.rowcount > 0


class QuestionRepository:
    @classmethod
    async def add_question(cls, question_data: QuestionCreate):
        async with async_session() as session:
            question = Question(**question_data.model_dump())
            session.add(question)
            await session.commit()
            await session.refresh(question)
            return question

    @classmethod
    async def get_questions_by_lesson(cls, lesson_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Question).where(Question.lesson_id == lesson_id)
            )
            return result.scalars().all()

    @classmethod
    async def get_question(cls, question_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Question).where(Question.id == question_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def update_question(cls, question_id: int, question_data: QuestionSchema):
        async with async_session() as session:
            result = await session.execute(
                update(Question)
                .where(Question.id == question_id)
                .values(**question_data.model_dump())
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def delete_question(cls, question_id: int):
        async with async_session() as session:
            result = await session.execute(
                delete(Question).where(Question.id == question_id)
            )
            await session.commit()
            return result.rowcount > 0


class AnswerRepository:
    @classmethod
    async def add_answer(cls, answer_data: AnswerCreate):
        async with async_session() as session:
            answer = Answer(**answer_data.model_dump())
            session.add(answer)
            await session.commit()
            await session.refresh(answer)
            return answer

    @classmethod
    async def get_answers_by_question(cls, question_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Answer).where(Answer.question_id == question_id)
            )
            return result.scalars().all()

    @classmethod
    async def update_answer(cls, answer_id: int, answer_data: AnswerSchema):
        async with async_session() as session:
            result = await session.execute(
                update(Answer)
                .where(Answer.id == answer_id)
                .values(**answer_data.model_dump())
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def delete_answer(cls, answer_id: int):
        async with async_session() as session:
            result = await session.execute(delete(Answer).where(Answer.id == answer_id))
            await session.commit()
            return result.rowcount > 0


class UserProgressRepository:
    # ✅ Пометить урок как пройденный
    @staticmethod
    async def mark_lesson_completed(user_id: int, lesson_id: int):
        async with async_session() as session:
            progress = UserCompletedLesson(user_id=user_id, lesson_id=lesson_id)
            session.add(progress)
            await session.commit()
            await session.refresh(progress)
            return progress

    # ✅ Получить все пройденные уроки пользователя
    @classmethod
    async def get_completed_lessons(cls, user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(UserCompletedLesson).where(
                    UserCompletedLesson.user_id == user_id
                )
            )
            return result.scalars().all()

    # ✅ Пометить тему как пройденную
    @staticmethod
    async def mark_topic_completed(user_id: int, topic_id: int):
        async with async_session() as session:
            progress = UserCompletedTopic(user_id=user_id, topic_id=topic_id)
            session.add(progress)
            await session.commit()
            await session.refresh(progress)
            return progress

    # ✅ Получить все пройденные темы пользователя
    @classmethod
    async def get_completed_topics(cls, user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(UserCompletedTopic).where(UserCompletedTopic.user_id == user_id)
            )
            return result.scalars().all()

    # ✅ Пометить вопрос как пройденный
    @staticmethod
    async def mark_question_completed(
        user_id: int, question_id: int, completed_at: datetime
    ):
        async with async_session() as session:
            progress = UserCompletedQuestion(
                user_id=user_id, question_id=question_id, completed_at=completed_at
            )
            session.add(progress)
            await session.commit()
            await session.refresh(progress)
            return progress

    # ✅ Получить все пройденные вопросы пользователя
    @classmethod
    async def get_completed_questions(cls, user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(UserCompletedQuestion).where(
                    UserCompletedQuestion.user_id == user_id
                )
            )
            return result.scalars().all()
