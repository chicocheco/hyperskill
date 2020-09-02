from django.shortcuts import redirect, render
from django.views import View
from resume.models import Resume


class ResumesView(View):

    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()
        return render(request, 'resumes.html', {'resumes': resumes})


class NewResumeView(View):

    def post(self, request, *args, **kwargs):
        desc = request.POST.get('description')
        Resume.objects.create(author=request.user, description=desc)
        return redirect('/resumes/')
