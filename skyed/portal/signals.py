from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.db.models import Q, Sum

from .models import *
from datetime import datetime

# This is a trigger that changes some columns in Student table. The following function changes:
# 	GPA
#		MGPA
#		Credits
#		Major Credits
		
@receiver(post_save, sender=StudentSection)
def update_student_status(sender, instance, created, **kwargs):

	grade = instance.grade
	student = instance.student

	if grade:

		try:
			department = student.program_set.get(ptype=1).department
		except:
			department = None

		mgpa = 0.0
		major_credits = 0
		gpa = 0.0
		credits = 0
		student_sections = StudentSection.objects.filter(student=student, grade__isnull=False).order_by('section__course__course_name', 'section__semester__year', 'section__semester__semester')
		repeated = False # This is used to check for repeated courses
		previous_course = None # Stores the previous course to check later if repeated
		previous_grade = None # Stores the previous grade to remove later from the gpa if repeated
		
		 # Every student have one chance to replace the previous grade.
		 # If repeated for the third time, the new subject is counted as a new course
		given_chance = True

		for student_section in student_sections:
			print(student_section.section.course, student_section.grade)
			if previous_course and previous_course == student_section.section.course:
				if given_chance:
					repeated = True
			else:
				given_chance = True

			if repeated:
				gpa -= previous_grade
				credits -= previous_course.credits
				given_chance = False
				
			grade = student_section.get_grade_points()
			gpa += grade
			credits += student_section.section.course.credits

			if student_section.section.course.department == department:
				if repeated:
					mgpa -= previous_grade
					major_credits -= previous_course.credits

				mgpa += grade
				major_credits += student_section.section.course.credits

			previous_course = student_section.section.course
			previous_grade = grade
			repeated = False


		gpa = round(gpa/credits, 2)
		mgpa = round(mgpa/major_credits, 2)

		# Updating the Student Object
		student.gpa = gpa
		student.mgpa = mgpa
		student.credits = credits
		student.major_credits = major_credits

		# Sending the updated Object to the Database (updating the row)
		student.save()

		#Checking if values are correct
		print('gpa updated:', student.gpa)
		print('mgpa updated:', student.mgpa)
		print('credits:', student.credits)
		print('major credts:', student.major_credits)


@receiver(post_save, sender=StudentSection)
def update_passed_terms(sender, instance, created, **kwargs):

	if instance.grade:
		semester = instance.student.semester
		semesters = Semester.objects.filter(year__gte=semester.year, grading_deadline__lte=datetime.now()).exclude(Q(year=semester.year, semester__lt=semester.semester) | Q(semester=3)).count()

		passed_terms = semesters
		instance.student.passed_terms = passed_terms
		print('passed terms:', passed_terms)
		instance.student.save()

@receiver(post_save, sender=Semester)
def warning_system(sender, instance, created, **kwargs):

	if instance.status == 2:
		students = Student.objects.filter(status=1)
		print(students)
		for s in students:
			if s.gpa < 2.0 and s.credits >= 30:
				s.warning += 1
				if s.warning >= 3:
					s.status = 3
				s.save()

@receiver(m2m_changed, sender=Segment.courses.through)
def segment_total_credits(sender, instance, **kwargs):
	if instance.segment_type == 1:
		c2 = instance.courses.aggregate(Sum('credits'))
		print(c2['credits__sum'])
		instance.credits = c2['credits__sum']
		instance.save()


@receiver(post_save, sender=Segment)
def program_total_credits(sender, instance, created, **kwargs):
	programs = instance.program_set.all()
	for program in programs:
		program.save()

@receiver(m2m_changed, sender=Program.segments.through)
def program_total_credits2(sender, instance, **kwargs):
	c = instance.segments.aggregate(Sum('credits'))
	instance.total_credits = c['credits__sum']
	instance.save()

@receiver(post_save, sender=Program)
def program_total_credits2_post(sender, instance, created, **kwargs):
	if created:
		instance.save()

@receiver(post_save, sender=Segment)
def segment_post_save(sender, instance, created, **kwargs):
	if created:
		instance.save()
