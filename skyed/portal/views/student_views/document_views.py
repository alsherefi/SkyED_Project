from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
import datetime
import random
from datetime import datetime, timedelta
from ...filters import SectionFilter, CourseFilter
from django.urls import reverse
from ...utils import generate_qrcode, render_to_pdf
# from .student_homepage import get_registration_semester
# from .planner_view import get_current_semester

def document_redirect(doc):
    if doc.doc_type == 1:
        return redirect(reverse('portal:show_document', args=[doc.id]))
    elif doc.doc_type == 2:
        return redirect(reverse('portal:show_transcript', args=[doc.id]))

@login_required(login_url='/portal/login')
def create_document_view(request, doc_type):
    if doc_type not in [1, 2]:
        raise Http404("Document Type Doesn't exist")

    if request.method == 'POST' and doc_type in [1, 2]:
        try:
            print('Checking if document already exists')
            doc = Document.objects.get(login=request.user, semester__status=1, doc_type=doc_type)
            print('Document Already Exists')
            return document_redirect(doc)
        except Document.DoesNotExist:
            semester = get_object_or_404(Semester, status=1)
            try:
                print('There is no document exists')
                new_document = Document.objects.create(login=request.user, doc_type=doc_type, semester=semester)
                return document_redirect(new_document)
            except:
                print('error creating document')
                return redirect(reverse('portal:account_view'))
        except Document.MultipleObjectsReturned:
            print('Document MultipleObjectsReturned Exception')
            old_doc = Document.objects.filter(login=request.user, semester__status=1, doc_type=doc_type).first()
            return document_redirect(old_doc)

    print("Unkown Error Occured")
    return redirect(reverse('portal:account_view'))

# https://www.youtube.com/watch?v=5umK8mwmpWM
def show_document_view(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id, doc_type=1)

    title = "To Whom it may Concern Document"
    text = "This document is to certify that "+ doc.login.first_name + " " + doc.login.last_name + " is officially one of the students at SkyED. He/She is hard working student and this is shown based on the passion that the student has in studying. This document is official which was issued upon his/her request for whatever purpose it may serve. Finally, SkyED family wants to thank this successive person and wish for all students in SkyED the best in their educational and social life."

    qrcode = generate_qrcode(qrurl='https://skyed.site' + reverse('portal:show_document', args=[doc_id]))

    context = {
        'title': title,
        'text': text,
        'document': doc,
        'login': doc.login,
        'svg': qrcode,
    }

    return render(request, "portal/student/show_document.html", context)

    # pdf = render_to_pdf("portal/student/show_document.html", context)
    # return HttpResponse(pdf, content_type="application/pdf")



# https://www.youtube.com/watch?v=5umK8mwmpWM
def show_transcript_view(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id, doc_type=2)
    
    sections = doc.login.student.section_set.annotate(grade=F('studentsection__grade')).filter(semester__grading_deadline__lte=doc.document_date).order_by('semester__year', 'semester__semester')
    sections = sections.order_by('semester__year', 'semester__semester')

    organized_sections = []
    s = []
    if sections:
        x = sections[0].semester.semester
    for section in sections:
        if x != section.semester.semester:
            x = section.semester.semester
            organized_sections.append(s)
            s = []
        s.append(section)
    organized_sections.append(s)

    qrcode = generate_qrcode('https://skyed.site' + reverse('portal:show_transcript', args=[doc_id]))

    context = {
        'document': doc,
        'login': doc.login,
        'svg': qrcode,
        'semesters': organized_sections,
    }

    # return render(request, 'portal/student/trans.html', context)
    return render(request, 'portal/student/transcript.html', context)

    # pdf = render_to_pdf("portal/student/transcript.html", context)
    # return HttpResponse(pdf, content_type="application/pdf")
