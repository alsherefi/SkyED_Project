# from django.http import HttpRequest
# from .models import *
# import datetime
# from django.shortcuts import render
# import string
# import random
# import names
# from django.contrib.auth.models import Group

# # # https://geekflare.com/password-generator-python-code/

# # ## characters to generate password from
# characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

# departments = ('9988', '1370', '1360', '1350', '1030', '1030', '1011', '0940', '0900', '0830', '0820', '0490', '0480', '0430', '0420', '0418', '0410', '0380', '0360', '0330', '0320', '0310', '0200')

# def generate_random_password():
# 	## length of password from the user
# 	length = 10

# 	## shuffling the characters
# 	random.shuffle(characters)
	
# 	## picking random characters from the list
# 	password = []
# 	for i in range(length):
# 		password.append(random.choice(characters))

# 	## shuffling the resultant password
# 	random.shuffle(password)

# 	## converting the list to string
# 	## printing the list
# 	return "".join(password)

# # def announcement_scrape(request):
# # 	for j in range(2):
# # 		for k in range(2, 10):
# # 			college_number = str(j) + str(k)
# # 			if college_number == '17':
# # 				continue
# # 			for i in range(20):
# # 				college = College.objects.get(id=college_number)
# # 				details = f"This is announcement text {i} for the College: {college.college_name}" 
# # 				c = Announcement(college_id=college_number, title='Announcement Test Number c' + str(i), info=details, adate=datetime.date(2021, i % 12 + 1, i + 1))
# # 				c.save()

# # 		for k in range(10):
# # 			for i in range(20):
# # 				department = Department.objects.get(id=departments[k])
# # 				details = f"This is announcement text {i} for the {department.name} department" 
# # 				c = DeptAnnouncement(department=department, title='Announcement Test Number d' + str(i), info=details, adate=datetime.date(2021, i % 12 + 1, i + 1))
# # 				c.save()

# 	# return render(request, 'portal/test.html')


# def login_scrape(request):

# 	k = 0
# 	w = 0
# 	for j in range(10): 
# 		for i in range(1, 31):
# 			fname = None
# 			if i % 2 == 0:
# 				fname = names.get_first_name(gender='male')
# 				gender = 'M'
# 			else:
# 				fname = names.get_first_name(gender='female')
# 				gender = 'F'
			
# 			digits = random.randint(0, 12)
# 			rgid = f'2{22 - (digits//2)}111' + str((100 + k))
# 			k += 1

# 			mname = (
# 				random.choice(string.ascii_uppercase) + 
# 				' ' +
# 				random.choice(string.ascii_uppercase) +
# 				' ' +
# 				random.choice(string.ascii_uppercase)
# 			)
# 			lname = names.get_last_name()
# 			l = Login.objects.create_user(email=fname + '.' + rgid + "@student.com", first_name=fname, middle_name=mname, last_name=lname, password=generate_random_password())

# 			l.groups.add(Group.objects.get(name='student'))
			
# 			s = Student(login = l, sex = gender, passed_terms=digits, registration_id=rgid, year=2022-(digits//2), status='enrolled')
# 			s.save()

# 		for i in range(1, 11):
# 			fname = None
# 			if i % 2 == 0:
# 				fname = names.get_first_name(gender='male')
# 				gender = 'M'
# 			else:
# 				fname = names.get_first_name(gender='female')
# 				gender = 'F'
			
# 			mname = (
# 				random.choice(string.ascii_uppercase) + 
# 				' ' +
# 				random.choice(string.ascii_uppercase) +
# 				' ' +
# 				random.choice(string.ascii_uppercase)
# 			)

# 			lname = names.get_last_name()

# 			digits = random.randint(0, 12)
# 			rgid = f'2{16 - (digits//2)}319' + str((100 + w))
# 			w += 1

# 			l = Login.objects.create_user(email=fname + '.' + rgid + "@instructor.com", first_name=fname, middle_name=mname, last_name=lname, password=generate_random_password())

# 			l.groups.add(Group.objects.get(name='instructor'))

# 			dept = random.choice(departments)
			
# 			inst = Instructor(login=l, dept_id=dept,registration_id=rgid)
# 			inst.save()

# 	return render(request, 'portal/test.html')