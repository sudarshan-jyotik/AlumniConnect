"""Referral Request repository."""
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.models.referral_request import ReferralRequest, RequestStatus
from app.repositories.base import BaseRepository

class ReferralRequestRepository(BaseRepository[ReferralRequest]):
    def __init__(self, db: Session):
        super().__init__(ReferralRequest, db)

    def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[ReferralRequest]:
        """Get requests by student."""
        return self.db.query(ReferralRequest).filter(
            ReferralRequest.student_id == student_id
        ).options(
            joinedload(ReferralRequest.student),
            joinedload(ReferralRequest.company)
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: RequestStatus, skip: int = 0, limit: int = 100) -> List[ReferralRequest]:
        """Get requests by status."""
        status_val = status.value if hasattr(status, 'value') else str(status)
        return self.db.query(ReferralRequest).filter(
            ReferralRequest.status.in_([status, status_val])
        ).options(
            joinedload(ReferralRequest.student),
            joinedload(ReferralRequest.company)
        ).offset(skip).limit(limit).all()

    def get_approved(self, skip: int = 0, limit: int = 100) -> List[ReferralRequest]:
        """Get approved & fulfilled requests (visible to alumni)."""
        return self.db.query(ReferralRequest).filter(
            ReferralRequest.status.in_([
                RequestStatus.APPROVED,
                RequestStatus.APPROVED.value,
                RequestStatus.FULFILLED,
                RequestStatus.FULFILLED.value,
            ])
        ).options(
            joinedload(ReferralRequest.student),
            joinedload(ReferralRequest.company)
        ).offset(skip).limit(limit).all()

    def get_all_with_details(self, skip: int = 0, limit: int = 100) -> List[ReferralRequest]:
        """Get all requests with student and company loaded."""
        return self.db.query(ReferralRequest).options(
            joinedload(ReferralRequest.student),
            joinedload(ReferralRequest.company)
        ).offset(skip).limit(limit).all()

    def get_with_details(self, request_id: int) -> Optional[ReferralRequest]:
        """Get request with all relationships loaded."""
        return self.db.query(ReferralRequest).filter(
            ReferralRequest.id == request_id
        ).options(
            joinedload(ReferralRequest.student),
            joinedload(ReferralRequest.company)
        ).first()
