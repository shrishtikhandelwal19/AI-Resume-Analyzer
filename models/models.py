from datetime import datetime
from typing import Optional, Dict, Any, List

class User:
    """Model representing an authenticated application user."""
    def __init__(
        self,
        id: Optional[int],
        username: str,
        email: Optional[str],
        full_name: Optional[str],
        target_role: Optional[str],
        industry: Optional[str],
        theme_pref: str = "dark",
        created_at: Optional[str] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.target_role = target_role
        self.industry = industry
        self.theme_pref = theme_pref
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary representation."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "target_role": self.target_role,
            "industry": self.industry,
            "theme_pref": self.theme_pref,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Constructs User model from database dictionary representation."""
        return cls(
            id=data.get("id"),
            username=data.get("username", ""),
            email=data.get("email"),
            full_name=data.get("full_name"),
            target_role=data.get("target_role"),
            industry=data.get("industry"),
            theme_pref=data.get("theme_pref", "dark"),
            created_at=data.get("created_at")
        )


class ResumeAnalysis:
    """Model representing a parsed and analyzed resume against a Job Description."""
    def __init__(
        self,
        id: Optional[int],
        user_id: int,
        filename: str,
        resume_text: str,
        job_title: Optional[str],
        job_desc: Optional[str],
        analysis_results: Dict[str, Any],
        uploaded_at: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.filename = filename
        self.resume_text = resume_text
        self.job_title = job_title
        self.job_desc = job_desc
        self.analysis_results = analysis_results
        self.uploaded_at = uploaded_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "resume_text": self.resume_text,
            "job_title": self.job_title,
            "job_desc": self.job_desc,
            "analysis_results": self.analysis_results,
            "uploaded_at": self.uploaded_at
        }
