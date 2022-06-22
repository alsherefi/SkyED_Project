import datetime
from secrets import choice
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid

MAXIMUM = 200

semester_choices = (
  (1, 'Fall'),
  (2, 'Spring'),
  (3, 'Summer'),
)

doc_types = (
  (1, 'towhom it may concern'),
  (2, 'transcript'),
)

announcement_status = (
  (1, 'Active'),
  (2, 'Active for students'),
  (3, 'Active for instructors'),
  (-1, 'Hidden'),
)

section_announcement_status = (
  (1, 'Active'),
  (-1, 'Hidden'),
)

# Create your models here.
class MyLoginManager(BaseUserManager):
  def create_user(self, email, first_name, middle_name, last_name, password=None):
    if not email:
      raise ValueError("Users must have an email address")
    if not first_name:
      raise ValueError("Users must have a first name")
    if not middle_name:
      raise ValueError("Users must have a middle name")
    if not last_name:
      raise ValueError("Users must have a last name")

    user = self.model(
      email=self.normalize_email(email),
      first_name=first_name,
      middle_name=middle_name,
      last_name=last_name,
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, first_name, middle_name, last_name, password=None):

    user = self.create_user(
      email=self.normalize_email(email),
      password=password,
      first_name=first_name,
      middle_name=middle_name,
      last_name=last_name,
    )

    user.is_admin = True
    user.save(using=self._db)
    return user

class Login(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=60, verbose_name='email', unique=True)
  first_name = models.CharField(verbose_name="first name", max_length=MAXIMUM)
  middle_name = models.CharField(verbose_name="middle name", max_length=MAXIMUM)
  last_name = models.CharField(verbose_name="last name", max_length=MAXIMUM)
  date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
  
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = MyLoginManager()

  # This the 'username' that the user will enter to sign in.
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']


  def __str__(self):
    return self.first_name + ' ' + self.last_name

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return self.is_admin


  class Meta:
    db_table = "login"
  
class Document(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  doc_type = models.IntegerField(choices=doc_types)
  login = models.ForeignKey(Login, on_delete=models.CASCADE)
  document_date = models.DateField(auto_now_add=True)
  semester = models.ForeignKey('Semester', on_delete=models.CASCADE)

  def __str__(self):
    return str(self.login) + ': ' + self.get_doc_type_display() + ' ' + str(self.semester)
  
  class Meta:
    db_table = "document"

class Student(models.Model):
  login = models.OneToOneField(Login, primary_key=True, on_delete=models.CASCADE)

  gender = (
    ('M', 'Male'),
    ('F', 'Female')
  )

  sex = models.CharField(max_length=1, choices=gender)

  gpa = models.FloatField(blank=True, default=0)
  mgpa = models.FloatField(blank=True, default=0)
  credits = models.IntegerField(blank=True, default=0)
  major_credits = models.IntegerField(blank=True, default=0)

  passed_terms = models.IntegerField(default=0)

  semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
  
  registration_id = models.CharField(max_length=MAXIMUM, unique=True)

  # What is the best type for status
  student_status = (
    (1, 'Enrolled'),
    (2, 'Graduated'),
    (3, 'Dismissed'),
  )

  warning_status = (
    (0, 'No Warning'),
    (1, 'First Warning'),
    (2, 'Final Warning'),
  )

  status = models.IntegerField(choices=student_status, default=1)
  warning = models.IntegerField(default = 0, choices=warning_status)

  def __str__(self):
    return self.login.first_name + ' ' + self.login.last_name + ' - ' + self.registration_id

  class Meta:
    db_table = "student"  

class Instructor(models.Model):
  login = models.OneToOneField(Login, primary_key=True, on_delete=models.CASCADE)
  dept = models.ForeignKey('department', on_delete=models.CASCADE)
  registration_id = models.CharField(max_length=MAXIMUM, unique=True)

  def __str__(self):
    return self.login.first_name + ' ' + self.login.last_name +', ' + self.dept.name + ' - ' + self.registration_id

  class Meta:
    db_table = 'instructor'

class Department(models.Model):
  id = models.CharField(max_length=MAXIMUM, primary_key=True)
  name = models.CharField(max_length=MAXIMUM, unique=True)
  college = models.ForeignKey('College', on_delete=models.CASCADE)
  manager = models.OneToOneField(Instructor, on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
      return '(' + self.id + ') ' + self.name 

  class Meta:
    db_table = 'department'

class Segment(models.Model):
  name = models.CharField(max_length=MAXIMUM)
  year = models.IntegerField()
  credits = models.IntegerField(blank=True, null=True)
  courses = models.ManyToManyField('Course', blank=True)

  stypes = ((1, 'Required'), (2, 'Elective'))

  segment_type = models.IntegerField(choices=stypes)

  def __str__(self):
    return self.name + ' ' + str(self.year) + ' ' + self.get_segment_type_display()
class Program(models.Model):
  # title and year are unique together
  title = models.CharField(max_length=MAXIMUM)
  year = models.IntegerField()
  
  # What is the best type for program type?
  ptype = models.IntegerField(choices=((1, 'Major'), (2, 'General'), (3, 'Minor')))
  total_credits = models.IntegerField(blank=True, null=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

  students = models.ManyToManyField(Student, blank=True)
  segments = models.ManyToManyField(Segment, blank=True)

  def __str__(self):
    return self.title + ' ' + str(self.year)

  class Meta:
    db_table = 'program'
    unique_together = (('title', 'year'), )

class DeptAnnouncement(models.Model):
  department = models.ForeignKey(Department, on_delete=models.CASCADE)
  title = models.CharField(max_length=MAXIMUM) 
  info = models.CharField(max_length=MAXIMUM*4)
  adate = models.DateTimeField(auto_now_add=True)
  priority = models.IntegerField(default=2)

  status = models.IntegerField(choices=announcement_status, default=1)

  logins = models.ManyToManyField(Login, blank=True)

  def __str__(self):
    return self.department.name + ' ' + self.title + ' - ' + str(self.adate.date())

  class Meta:
    db_table = 'dept_announcement'

class College(models.Model):
  id = models.CharField(max_length=MAXIMUM, primary_key=True)
  college_name = models.CharField(max_length=MAXIMUM)
  dean = models.CharField(max_length=MAXIMUM, blank=True)

  def __str__(self):
    return '(' + self.id + ') ' + self.college_name
  
  class Meta:
    db_table = 'college'

# class Announcement
class Announcement(models.Model):
  college = models.ForeignKey(College, on_delete=models.CASCADE)
  title = models.CharField(max_length=MAXIMUM) 
  info = models.CharField(max_length=MAXIMUM*4)
  adate = models.DateTimeField(auto_now_add=True)
  priority = models.IntegerField(default=3)


  status = models.IntegerField(choices=announcement_status, default=1)

  logins = models.ManyToManyField(Login, blank=True)

  def __str__(self):
    return self.college.college_name + ' ' + str(self.id)

  class Meta:
    db_table = 'announcement'

# class Course
class Course(models.Model):
  course_id = models.CharField(max_length=MAXIMUM, primary_key=True)
  course_name = models.CharField(max_length=MAXIMUM)
  credits = models.IntegerField()
  department = models.ForeignKey(Department, on_delete=models.CASCADE)

  students = models.ManyToManyField(Student, through='StudentCoursePlan', blank=True)
  requisites = models.ManyToManyField('self', through="CourseRequisite", blank=True, symmetrical=False)

  def abbr(self):
    return self.department.name[:4].upper() + ' ' + self.course_id[-3: -1] + self.course_id[-1]

  def __str__(self):
    return self.course_id + ' ' + self.course_name

  class Meta:
    db_table = 'course'

class Semester(models.Model):
  year = models.IntegerField()

  semester = models.IntegerField(choices=semester_choices)

  registration_starts = models.DateTimeField()
  registration_ends = models.DateTimeField()
  
  semester_starts = models.DateField()
  semester_ends = models.DateField()

  exams_starts = models.DateField()
  exams_ends = models.DateField()

  grading_deadline = models.DateField()

  semester_status = (
    (1, 'Ongoing'),
    (2, 'Finished'),
    (3, 'New'),
  )

  status = models.IntegerField(choices=semester_status, default=3)

  def get_year(self):
    return str(self.year) + '/' + str(self.year + 1)

  def __str__(self):
    return str(self.year) + '/' + str(self.year+1) + ' ' + str(self.get_semester_display())

  class Meta:
    db_table= 'semester'
    unique_together=(('year', 'semester'), )


# class Section
class Section(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  snumber = models.CharField(max_length=MAXIMUM)
  # Ask Smaoui for the type of days
  days = models.CharField(max_length=MAXIMUM)
  start_time = models.TimeField()
  end_time = models.TimeField()
  
  semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

  instructor = models.ForeignKey(Instructor, null=True, blank=True, on_delete=models.CASCADE)

  building = models.CharField(max_length=MAXIMUM, null=True)
  room = models.CharField(max_length=MAXIMUM, null=True)

  gender = models.CharField(max_length=1)

  students = models.ManyToManyField(Student, through='StudentSection')

  def __str__(self):
    return self.snumber + ' ' + self.course.course_name + ' ' + self.semester.__str__()
 
  class Meta:
    db_table = 'section'

# class Section_Announcement
class SectionAnnouncement(models.Model):
  info = models.TextField(max_length=MAXIMUM * 2)
  title = models.CharField(max_length=MAXIMUM) 
  section = models.ForeignKey(Section, on_delete=models.CASCADE)
  adate = models.DateTimeField(auto_now_add=True)
  priority = models.IntegerField(default=1)

  status = models.IntegerField(choices=section_announcement_status, default=1)
  
  logins = models.ManyToManyField(Login, blank=True)

  def __str__(self):
    return str(self.id) + ' ' + self.section.snumber

  class Meta:
    db_table = 'section_announcement'


class StudentCoursePlan(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  grade = models.CharField(max_length=2, null=True, blank=True)

  year = models.IntegerField()

  semester = models.IntegerField(choices=semester_choices)

  def get_year(self):
    return str(self.year) + '/' + str(self.year + 1)

  def __str__(self):
    return str(self.student.login.student.registration_id) + ': ' + self.course.course_id

  class Meta:
    db_table = 'student_course_plan'
    unique_together = (('student', 'course'),)

class StudentSection(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  section = models.ForeignKey(Section, on_delete=models.CASCADE)
  grade = models.CharField(max_length=2, null=True, blank=True)

  def get_grade_points(self):
    grade_points = {
      "A":4,
      "A-":3.67,
      "B+":3.33,
      "B":3.0,
      "B-":2.67,
      "C+":2.33,
      "C":2.0,
      "C-":1.67,
      "D+":1.33,
      "D":1.0,
      "F":0
    }
    points = grade_points[self.grade] * self.section.course.credits
    return points

  def __str__(self):
    return self.student.login.first_name + ' ' +  self.student.login.last_name + ' ' + self.section.__str__()

  class Meta:
    db_table = 'student_section'
    unique_together = (('student', 'section'), )

class CourseRequisite(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  requisite = models.ForeignKey(Course, related_name="requisite", on_delete=models.CASCADE)

  requisite_type_status = (
    ('prerequisite', 'Prerequisite'),
    ('corequisite', 'Corequisite')
  )

  requisite_type = models.CharField(max_length=MAXIMUM, choices=requisite_type_status)
  

  def check_type(self):
    if self.requisite_type == 'prerequisite':
      return ' <--- '
    elif self.requisite_type == 'corequisite':
      return  ' <---> '
    else:
      return ' err '

  
  def __str__(self):
    return self.course.course_id + ' ' + self.course.course_name + self.check_type() + self.requisite.course_id + ' ' + self.requisite.course_name

  class Meta:
    db_table = 'course_requisite'
    unique_together = (('course', 'requisite'), )

