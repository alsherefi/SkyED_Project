from django.urls import path
from . import views
from . import scrapingTool

app_name = 'portal'

general_patterns = [
    path('', views.home, name='home_redirect'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home, name='home'),

    # the first url
    # path('', views.name, name='') 

    ######################## Other ######################################
    # path('scrape/', scrapingTool.announcement_scrape, name='scrape'),
    # path('scrape_login/', scrapingTool.login_scrape, name='scrape')

]

student_patterns = [
    path('student/', views.home, name='student_home'),
    path('student/student_homepage/', views.student_homepage, name='student_homepage'),
    path('student/logout/', views.logout_view, name='logout_view'),
    path('student/announcement/', views.announcement_view, name='announcement_view'),
    path('student/grades/sem=<int:sem>/', views.grades_view, name='grades_view'),
    path('student/registration/', views.registration_view, name='registration_view'),
    path('student/schedule/', views.schedule_view, name='schedule_view'),
    path('student/account/', views.account_view, name='account_view'),
    path('student/planner/', views.planner_view, name='planner_view'),
    path('student/ajax_search_course', views.course_search, name='course_search'),
    path('student/testpage/', views.test_view, name='test_view'),
    path('student/student/soon/', views.soon_view, name='soon_view'),
    path('student/add_to_plan/', views.add_to_plan_view, name='add_to_plan_view'),
    path('student/remove_section/', views.remove_section_view, name='remove_section'),
    path('student/remove_from_planner/<str:course>/<str:semester>/<str:year>', views.remove_from_planner, name='remove_from_planner'),
    path('student/change_password/', views.change_password_view, name='change_password_view'),
    path('student/ajax-show_sections/', views.show_sections, name="show_sections"),
    path('student/ajax-add_section/', views.ajax_add_section, name="add_section"),
    path('student/create_document/doc_type=<int:doc_type>/', views.create_document_view, name='create_document'),
    path('student/show_document/id=<uuid:doc_id>/', views.show_document_view, name="show_document"),
    path('student/show_transcript/id=<uuid:doc_id>/', views.show_transcript_view, name="show_transcript"),
    path('student/my_schedule/sem=<int:sem>/', views.my_schedule_view, name='my_schedule'),
]

instructor_patterns = [
	path('instructor/', views.home, name='instructors_homepage_redirect'),
	path('instructor/homepage/', views.instructors_homepage_view, name='instructors_homepage'),
    path('instructor/make_announcement/', views.make_announcement_view, name='make_announcement'),
    path('instructor/show_sections/', views.list_sections_view, name='show_sections_list'),
    path('instructor/ajax_students_list/', views.list_students_view, name='ajax_students_list'),
    path('instructor/csv_students_list/id=<int:sid>', views.csv_students_list, name='csv_students_list'),
    path('instructor/send_announcement/', views.send_announcement_view, name='send_announcement'),
    path('instructor/account/', views.instructor_account_view, name='instructor_account'),
    path('instructor/grading/', views.grade_sections_view, name='grading'),
    path('instructor/schedule/', views.schedule_view, name='make_schedule'),
    path('instructor/csv_grades_list/id=<int:sid>', views.csv_grades_list, name='csv_grades_list'),
    path('instructor/ajax_grades_list/', views.list_students_grade_view, name='ajax_grades_list'),
    path('instructor/ajax_grading/', views.ajax_grade_students, name='ajax_grading'),
    path('instructor/change_password/', views.inst_change_password, name='inst_change_password'),

]

urlpatterns = general_patterns + student_patterns + instructor_patterns
