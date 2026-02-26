import os
import django

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from school_schedule.models import Subject, Teacher, SchoolClass, Student, Schedule, Grade

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })

@app.post("/add_subject")
def add_subject(name: str = Form(...)):
    Subject.objects.create(name=name)
    return RedirectResponse("/", status_code=303)

@app.get("/subjects")
def get_subjects():
    subjects = Subject.objects.all()

    return [
        f"Id: {s.id} | {s.name}"
        for s in subjects
    ]

@app.post("/add_class")
def add_class(name: str = Form(...)):
    SchoolClass.objects.create(name=name)
    return RedirectResponse("/", status_code=303)

@app.get("/classes")
def get_subjects():
    classes = SchoolClass.objects.all()

    return [
        f"Id: {c.id} | {c.name}"
        for c in classes
    ]

@app.post("/add_teacher")
def add_teacher(
    first_name: str = Form(...),
    last_name: str = Form(...),
    subject: int = Form(...)
):
    Teacher.objects.create(
        first_name=first_name,
        last_name=last_name,
        subject=Subject.objects.get(id=subject)
    )
    return RedirectResponse("/", status_code=303)

@app.get("/teachers")
def get_teachers():
    teachers = Teacher.objects.select_related("subject")

    return [
        f"Id: {t.id} | {t.first_name} {t.last_name} | Subject: {t.subject.name}"
        for t in teachers
    ]

@app.post("/add_student")
def add_student(
    first_name: str = Form(...),
    last_name: str = Form(...),
    class_id: int = Form(...)
):
    Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        school_class=SchoolClass.objects.get(id=class_id)
    )
    return RedirectResponse("/", status_code=303)

@app.get("/students")
def get_students():
    students = Student.objects.select_related("school_class")

    return [
        f"Id: {s.id} | {s.first_name} {s.last_name} | Class: {s.school_class.name}"
        for s in students
    ]

@app.post("/add_lesson")
def add_lesson(
    day: str = Form(...),
    lesson_number: str = Form(...),
    subject: int = Form(...),
    teacher: int = Form(...),
    class_id: int = Form(...)
):
    Schedule.objects.create(
        day=day,
        lesson_number=lesson_number,
        subject=Subject.objects.get(id=subject),
        teacher=Teacher.objects.get(id=teacher),
        school_class=SchoolClass.objects.get(id=class_id)
    )
    return RedirectResponse("/", status_code=303)

@app.post("/add_grade")
def add_grade(
    student: int = Form(...),
    subject: int = Form(...),
    grade: int = Form(...)
):
    Grade.objects.create(
        student=Student.objects.get(id=student),
        subject=Subject.objects.get(id=subject),
        grade=grade
    )
    return RedirectResponse("/", status_code=303)

@app.get("/schedule", response_class=HTMLResponse)
def get_schedule(request: Request):
    lessons = Schedule.objects.select_related(
        "subject",
        "teacher",
        "school_class"
    ).all()

    return templates.TemplateResponse("schedule.html", {
        "request": request,
        "lessons": lessons
    })

@app.get("/diary", response_class=HTMLResponse)
def diary(request: Request):
    grades = Grade.objects.select_related(
        "student",
        "student__school_class",
        "subject"
    ).all()

    return templates.TemplateResponse("diary.html", {
        "request": request,
        "grades": grades
    })