import django_filters
from django_filters import CharFilter
from django.db.models import Q

from .models import *

class CourseFilter(django_filters.FilterSet):

	search_bar = django_filters.CharFilter(method='custom_filter',label="Search")

	# course_id = CharFilter(field_name="course_id", lookup_expr='icontains')
	# course_name = CharFilter(field_name="course_name", lookup_expr='icontains')

	class Meta:
		model = Course
		fields = ['course__department__college', 'course__department', 'search_bar']

	def custom_filter(self, queryset, name, value):
		return queryset.filter(
				Q(course_id__iendswith=value) | Q(course_name__icontains=value)
		)


class SectionFilter(django_filters.FilterSet):
	class Meta:
		model = Section
		fields = '__all__'
