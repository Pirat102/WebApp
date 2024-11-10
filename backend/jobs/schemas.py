from ninja import Schema, FilterSchema, Field
from typing import Optional, List
from django.db.models import Q
from datetime import datetime

class ErrorSchema(Schema):
    message: str
    
class UserRegistrationSchema(Schema):
    username: str
    password: str
    email: Optional[str] = None

class JobSchema(Schema):
    id: int
    title: str
    company: Optional[str]
    location: Optional[str]
    operating_mode: Optional[str]
    salary: Optional[str]
    skills: dict  
    url: str
    scraped_date: datetime
    summary: Optional[str]
    

class JobFilterSchema(FilterSchema):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    operating_mode: Optional[str] = None
    salary: Optional[str] = None
    skills: Optional[List[str]] = None

    def filter_queryset(self, queryset):
        # Standard filters based on schema fields
        if self.title:
            queryset = queryset.filter(title__icontains=self.title)
        if self.company:
            queryset = queryset.filter(company__icontains=self.company)
        if self.location:
            queryset = queryset.filter(location__icontains=self.location)
        if self.operating_mode:
            queryset = queryset.filter(operating_mode__icontains=self.operating_mode)
        if self.salary:
            queryset = queryset.filter(salary__icontains=self.salary)

        # Custom filter logic for skills (AND logic)
        if self.skills:
            skills_query = Q()
            for skill in self.skills:
                skills_query &= Q(skills__has_key=skill)
            queryset = queryset.filter(skills_query)
        
        return queryset