from fastapi import APIRouter, HTTPException
from schemas import (
    LessonSchema,
    LessonCreate,
    LessonUpdate,
    QuestionSchema,
    QuestionCreate,
    AnswerSchema,
    AnswerCreate,
    TopicSchema,
    TopicCreate,
    TopicUpdate,
    UserCompletedTopicSchema,
    UserCompletedQuestionSchema,
    UserCompletedLessonSchema,
)
from repository import (
    LessonRepository,
    QuestionRepository,
    AnswerRepository,
    TopicRepository,
    UserProgressRepository,
)

router = APIRouter(prefix="/topics", tags=["topics"])


@router.post("", response_model=TopicSchema)
async def add_topic(topic: TopicCreate):
    try:
        topic_id = await TopicRepository.add_topic(topic)
        return await TopicRepository.get_topic(topic_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create topic")


@router.get("", response_model=list[TopicSchema])
async def get_topics():
    return await TopicRepository.all_topics()


@router.get("/{topic_id}/", response_model=TopicSchema)
async def get_topic(topic_id: int):
    topic = await TopicRepository.get_topic(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.delete("/{topic_id}/")
async def delete_topic(topic_id: int):
    res = await TopicRepository.delete_topic(topic_id)
    if not res:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"message": "Topic deleted successfully"}


@router.put("/{topic_id}/", response_model=TopicSchema)
async def update_topic(topic_id: int, topic: TopicUpdate):
    res = await TopicRepository.update_topic(topic_id, topic)
    if not res:
        raise HTTPException(status_code=404, detail="Topic not found or not updated")
    updated_topic = await TopicRepository.get_topic(topic_id)
    return updated_topic


# Уроки
lesson_router = APIRouter(prefix="/lessons", tags=["lessons"])


@lesson_router.post("/", response_model=LessonSchema)
async def add_lesson(body: LessonCreate):
    lesson = await LessonRepository.add_lesson(body)
    return lesson


@lesson_router.get("/{topic_id}/", response_model=list[LessonSchema])
async def get_lessons_by_topic(topic_id: int):
    lessons = await LessonRepository.get_lessons_by_topic(topic_id)
    return lessons


@lesson_router.get("/detail/{lesson_id}/", response_model=LessonSchema)
async def get_lesson(lesson_id: int):
    lesson = await LessonRepository.get_lesson(lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@lesson_router.put("/{lesson_id}/", response_model=LessonSchema)
async def update_lesson(lesson_id: int, lesson: LessonUpdate):
    res = await LessonRepository.update_lesson(lesson_id, lesson)
    if not res:
        raise HTTPException(status_code=404, detail="Lesson not found or not updated")
    updated_lesson = await LessonRepository.get_lesson(lesson_id)
    return updated_lesson


@lesson_router.delete("/{lesson_id}/")
async def delete_lesson(lesson_id: int):
    res = await LessonRepository.delete_lesson(lesson_id)
    if not res:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"deleted": True}


# Вопросы
question_router = APIRouter(prefix="/questions", tags=["questions"])


@question_router.post("/", response_model=QuestionSchema)
async def add_question(body: QuestionCreate):
    question = await QuestionRepository.add_question(body)
    return question


@question_router.get("/{lesson_id}/", response_model=list[QuestionSchema])
async def get_questions_by_lesson(lesson_id: int):
    questions = await QuestionRepository.get_questions_by_lesson(lesson_id)
    return questions


@question_router.delete("/{question_id}/")
async def delete_question(question_id: int):
    res = await QuestionRepository.delete_question(question_id)
    if not res:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"deleted": True}


@question_router.get("/detail/{question_id}/", response_model=QuestionSchema)
async def get_question(question_id: int):
    question = await QuestionRepository.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# Ответы
answer_router = APIRouter(prefix="/answers", tags=["answers"])


@answer_router.post("/", response_model=AnswerSchema)
async def add_answer(body: AnswerCreate):
    answer = await AnswerRepository.add_answer(body)
    return answer


@answer_router.get("/{question_id}/", response_model=list[AnswerSchema])
async def get_answers_by_question(question_id: int):
    answers = await AnswerRepository.get_answers_by_question(question_id)
    return answers


@answer_router.delete("/{answer_id}/")
async def delete_answer(answer_id: int):
    res = await AnswerRepository.delete_answer(answer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"deleted": True}


progress_router = APIRouter(prefix="/progress", tags=["progress"])


# ✅ Завершить урок
@progress_router.post("/lessons/")
async def complete_lesson(body: UserCompletedLessonSchema):
    progress = await UserProgressRepository.mark_lesson_completed(
        body.user_id, body.lesson_id
    )
    return {"id": progress.id}


# ✅ Получить пройденные уроки
@progress_router.get("/lessons/", response_model=list[UserCompletedLessonSchema])
async def get_completed_lessons(user_id: int):
    return await UserProgressRepository.get_completed_lessons(user_id)


# ✅ Завершить тему


@progress_router.post("/topics/")
async def complete_topic(body: UserCompletedTopicSchema):
    progress = await UserProgressRepository.mark_topic_completed(
        body.user_id, body.topic_id
    )
    return {"id": progress.id}


# ✅ Получить пройденные темы
@progress_router.get("/topics/", response_model=list[UserCompletedTopicSchema])
async def get_completed_topics(user_id: int):
    return await UserProgressRepository.get_completed_topics(user_id)


# ✅ Завершить вопрос
@progress_router.post("/questions/")
async def complete_question(body: UserCompletedQuestionSchema):
    progress = await UserProgressRepository.mark_question_completed(
        body.user_id, body.question_id, body.completed_at
    )
    return {"id": progress.id}


# ✅ Получить пройденные вопросы
@progress_router.get("/questions/", response_model=list[UserCompletedQuestionSchema])
async def get_completed_questions(user_id: int):
    return await UserProgressRepository.get_completed_questions(user_id)


@progress_router.delete("/lessons/")
async def remove_completed_lesson(user_id: int, lesson_id: int):
    success = await UserProgressRepository.remove_completed_lesson(user_id, lesson_id)
    if not success:
        raise HTTPException(status_code=404, detail="Completed lesson not found")
    return {"message": "Lesson completion removed"}


@progress_router.delete("/topics/")
async def remove_completed_topic(user_id: int, topic_id: int):
    success = await UserProgressRepository.remove_completed_topic(user_id, topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Completed topic not found")
    return {"message": "Topic completion removed"}


@progress_router.delete("/questions/")
async def remove_completed_question(user_id: int, question_id: int):
    success = await UserProgressRepository.remove_completed_question(
        user_id, question_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Completed question not found")
    return {"message": "Question completion removed"}
