import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import date, datetime

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_resume_api_models():
    """Test that resume API models work correctly"""
    try:
        from backend.api.models.resumes.models import (
            ResumeCreate,
            ResumeUpdate,
            ResumeResponse,
            ResumeListResponse
        )
        from backend.data.resume_models import (
            ContactInfo,
            WorkExperience,
            Education,
            Skill,
            Project,
            Certification,
            ResumeStatus,
            ResumeType
        )
        
        # Test creating a ResumeCreate model
        user_id = uuid.uuid4()
        contact_info = ContactInfo(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="+1-555-123-4567",
            location="San Francisco, CA",
            linkedin_url="https://linkedin.com/in/johndoe",
            github_url="https://github.com/johndoe"
        )
        
        work_experience = [
            WorkExperience(
                company="Tech Corp",
                position="Senior Software Engineer",
                location="San Francisco, CA",
                start_date=date(2020, 1, 1),
                end_date=date(2023, 12, 31),
                is_current=False,
                description="Led development of cloud-based applications",
                achievements=["Increased system performance by 40%", "Mentored junior developers"],
                skills_used=["Python", "AWS", "Docker"]
            )
        ]
        
        education = [
            Education(
                institution="University of California",
                degree="Bachelor of Science",
                field_of_study="Computer Science",
                start_date=date(2016, 9, 1),
                end_date=date(2020, 5, 15),
                gpa=3.8
            )
        ]
        
        skills = [
            Skill(
                name="Python",
                level="advanced",
                category="Programming Languages",
                years_experience=5
            ),
            Skill(
                name="JavaScript",
                level="intermediate",
                category="Programming Languages",
                years_experience=3
            )
        ]
        
        projects = [
            Project(
                name="E-commerce Platform",
                description="Built a scalable e-commerce platform",
                start_date=date(2022, 3, 1),
                end_date=date(2022, 9, 30),
                technologies=["React", "Node.js", "MongoDB"],
                achievements=["Reduced load time by 50%", "Implemented secure payment processing"]
            )
        ]
        
        certifications = [
            Certification(
                name="AWS Certified Solutions Architect",
                issuer="Amazon Web Services",
                issue_date=date(2021, 6, 15),
                credential_id="AWS123456"
            )
        ]
        
        create_data = {
            "user_id": user_id,
            "title": "Senior Software Engineer Resume",
            "resume_type": ResumeType.BASE,
            "status": ResumeStatus.DRAFT,
            "contact_info": contact_info,
            "summary": "Experienced software engineer with 5+ years of expertise in building scalable applications",
            "work_experience": work_experience,
            "education": education,
            "skills": skills,
            "projects": projects,
            "certifications": certifications
        }
        
        resume_create = ResumeCreate(**create_data)
        assert resume_create.user_id == user_id
        assert resume_create.title == "Senior Software Engineer Resume"
        assert resume_create.resume_type == ResumeType.BASE
        assert resume_create.status == ResumeStatus.DRAFT
        assert resume_create.contact_info.full_name == "John Doe"
        assert len(resume_create.work_experience) == 1
        assert len(resume_create.education) == 1
        assert len(resume_create.skills) == 2
        assert len(resume_create.projects) == 1
        assert len(resume_create.certifications) == 1
        
        # Test creating a ResumeUpdate model
        update_data = {
            "title": "Updated Senior Software Engineer Resume",
            "status": ResumeStatus.ACTIVE
        }
        
        resume_update = ResumeUpdate(**update_data)
        assert resume_update.title == "Updated Senior Software Engineer Resume"
        assert resume_update.status == ResumeStatus.ACTIVE
        
        # Test creating a ResumeResponse model
        resume_id = uuid.uuid4()
        created_at = datetime(2023, 1, 15, 10, 30, 0)
        updated_at = datetime(2023, 1, 20, 14, 45, 0)
        
        response_data = {
            "id": resume_id,
            "user_id": user_id,
            "title": "Senior Software Engineer Resume",
            "resume_type": ResumeType.BASE,
            "status": ResumeStatus.ACTIVE,
            "contact_info": contact_info,
            "summary": "Experienced software engineer with 5+ years of expertise in building scalable applications",
            "work_experience": work_experience,
            "education": education,
            "skills": skills,
            "projects": projects,
            "certifications": certifications,
            "version": 2,
            "created_at": created_at,
            "updated_at": updated_at,
            "last_generated_at": datetime(2023, 1, 20, 15, 0, 0)
        }
        
        resume_response = ResumeResponse(**response_data)
        assert resume_response.id == resume_id
        assert resume_response.user_id == user_id
        assert resume_response.title == "Senior Software Engineer Resume"
        assert resume_response.status == ResumeStatus.ACTIVE
        assert resume_response.version == 2
        assert resume_response.created_at == created_at
        assert resume_response.updated_at == updated_at
        
        # Test creating a ResumeListResponse model
        list_response_data = {
            "resumes": [resume_response],
            "total": 1,
            "page": 1,
            "page_size": 10
        }
        
        resume_list_response = ResumeListResponse(**list_response_data)
        assert len(resume_list_response.resumes) == 1
        assert resume_list_response.total == 1
        assert resume_list_response.page == 1
        assert resume_list_response.page_size == 10
        
        print("All resume API models work correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test resume API models: {e}")


def test_resume_api_endpoints_exist():
    """Test that resume API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the resume endpoints exist
        # GET /resumes/ (list resumes)
        response = client.get("/resumes/")
        assert response.status_code in [200, 403, 401]  # Should exist (403/401 if auth required)
        
        # GET /resumes/{resume_id} (get specific resume)
        response = client.get(f"/resumes/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist (404 if resume not found)
        
        # POST /resumes/ (create resume)
        response = client.post("/resumes/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # PUT /resumes/{resume_id} (update resume)
        response = client.put(f"/resumes/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /resumes/{resume_id} (delete resume)
        response = client.delete(f"/resumes/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All resume API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify resume API endpoints: {e}")


def test_resume_api_documentation():
    """Test that resume API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes resume endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that resume endpoints are documented
        assert "/resumes/" in paths
        assert "/resumes/{resume_id}" in paths
        
        # Check that the methods are documented
        resumes_path = paths["/resumes/"]
        resume_id_path = paths["/resumes/{resume_id}"]
        
        assert "get" in resumes_path
        assert "post" in resumes_path
        assert "get" in resume_id_path
        assert "put" in resume_id_path
        assert "delete" in resume_id_path
        
        print("Resume API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify resume API documentation: {e}")