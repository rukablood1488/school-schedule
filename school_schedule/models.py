from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
class SchoolClass(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.school_class}"
    
class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    lesson_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.day} - {self.lesson_number} - {self.subject}"
    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.subject} : {self.grade}"