from collections import Counter
from datetime import datetime, timedelta, time
from django.shortcuts import get_object_or_404
from ninja import Query
from typing import Dict, Any
from jobs.models import Job, JobApplication, ApplicationNote
from jobs.schemas import *
from django.contrib.auth.models import User
from ninja_extra.permissions import AllowAny
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI, api_controller, route
from ninja_jwt.authentication import JWTAuth
from ninja_extra.pagination import paginate, PageNumberPaginationExtra, PaginatedResponseSchema
from jobs.utils.salary_standardizer import average_salary

api = NinjaExtraAPI()


@api_controller('/auth', tags=['Authentication'], permissions=[AllowAny])
class AuthController:

    @route.post('register', response={200: Dict, 400: Dict})
    def register(self, user_data: UserRegistrationSchema) -> Dict:
        if User.objects.filter(username=user_data.username).exists():
            return 400, {"success": False, "message": "Username already exists"}
        
        User.objects.create_user(
            username=user_data.username,
            password=user_data.password
        )
        return 200, {"success": True, "message": "Registration successful"}

@api_controller("/jobs")
class JobController:
    @route.get("", response=List[JobSchema])
    def get_jobs(self):
        return Job.objects.all().order_by("-scraped_date")
    
    @route.get("stats", response=Dict[str, Any])
    def stats(self, filters: JobFilterSchema = Query(...)):
        today = datetime.combine(datetime.now().date(), time.min)
        last_week = today - timedelta(days=7)
        last_two_weeks = today - timedelta(days=14)
        last_month = today - timedelta(days=30)
        jobs = Job.objects.all()
        
        
        jobs = filters.filter_queryset(jobs)
        
        
        skill_freq = {}
        exp_stats = Counter()
        source_stats = Counter()
        work_mode = Counter()
        salary_count = 0
        min_total = 0
        max_total = 0
        
        for job in jobs:
            # Process all stats in single loop
            exp_stats[job.experience] += 1
            source_stats[job.source] += 1
            work_mode[job.operating_mode] += 1
            
            for skill in job.skills.keys():
                skill_freq[skill] = skill_freq.get(skill, 0) + 1
            
            if job.salary:
                min_value, max_value = average_salary(job.salary)
                min_total += min_value
                max_total += max_value
                salary_count += 1
                
        if salary_count > 0:
            avg_min = min_total / salary_count
            avg_max = max_total / salary_count
            salary = f"{int(avg_min)} - {int(avg_max)} PLN"
        else:
            salary = ""
            
        
        def sort_dict(d):
            return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
        
    
        return {
            "top_skills": sort_dict(skill_freq),
            "exp_stats": sort_dict(exp_stats),
            "source_stats": sort_dict(source_stats), 
            "operating_mode_stats": sort_dict(work_mode),
            "salary_stats": salary,
            "trends": {
                "today": jobs.filter(scraped_date__gte=today).count(),
                "last_7_days": jobs.filter(scraped_date__gte=last_week).count(),
                "last_14_days": jobs.filter(scraped_date__gte=last_two_weeks).count(),
                "last_30_days": jobs.filter(scraped_date__gte=last_month).count(),
        },
        }
    
    @route.get("dates", response=List[date])
    def available_dates(self):
        dates = Job.objects.dates('scraped_date', 'day',"DESC").distinct()
        return dates
                

    @route.get("/filter", response=PaginatedResponseSchema[JobSchema])
    @paginate(PageNumberPaginationExtra, page_size=50)
    def list_jobs(self, filters: JobFilterSchema=Query(...)):
        jobs = Job.objects.all()
        jobs = filters.filter_queryset(jobs)
        
        return jobs.order_by("-scraped_date")
    

@api_controller("/applications", auth=JWTAuth())
class JobApplicationController:
    @route.post("", response={200: JobApplicationSchema, 400: Dict})
    def create_application(self, request, payload: CreateApplicationSchema):
        try:
            job = Job.objects.get(id=payload.job_id)
        except Exception as e:
            return 400, {"success": False, f"message {payload}": f"Job not found {payload.id}"}
        
        if JobApplication.objects.filter(user=request.user, job_id=payload.job_id):
            return 400, {"success": False, "message": "Already applied to this job"}
        
        application = JobApplication.objects.create(
            user = request.user,
            job_id=payload.job_id
        )
        return application
        
    @route.get("", response=List[JobApplicationSchema])
    def get_user_applications(self, request):
        return JobApplication.objects.filter(user=request.user)
        
    @route.post("{application_id}/notes", response=ApplicationNoteSchema)
    def add_note(self, request, application_id: int, note_data: ApplicationNoteSchema):
        application = get_object_or_404(JobApplication, id=application_id, user=request.user)
        note = ApplicationNote.objects.create(
            application=application,
            content=note_data.content
        )
        return note
    
    @route.patch("{application_id}", response=JobApplicationSchema)
    def update_application_status(self, request, application_id: int, status_data: UpdateStatusSchema):
        application = get_object_or_404(JobApplication, id=application_id, user=request.user)
        application.status = status_data.status
        application.save()
        return application
    
    @route.delete("{application_id}", response={200: Dict, 404: Dict})
    def delete_application(self, request, application_id: int):
        application = get_object_or_404(JobApplication, id=application_id, user=request.user)
        application.delete()
        return 200, {"success": True, "message": "Application deleted"}
    
    @route.delete("{application_id}/notes/{note_id}", response={200: Dict, 404: Dict})
    def delete_note(self, request, note_id: int, application_id):
        application = get_object_or_404(JobApplication, id=application_id, user=request.user)
        note = get_object_or_404(ApplicationNote, application=application, id=note_id)
        note.delete()
        return 200, {"success": True, "message": "Note deleted"}
        
        
    

    
    
api.register_controllers(NinjaJWTDefaultController, AuthController, JobController, JobApplicationController)
