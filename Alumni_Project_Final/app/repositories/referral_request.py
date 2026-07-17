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
        ).options(joinedload(ReferralRequest.company)).offset(skip).limit(limit).all()

    def get_by_status(self, status: RequestStatus, skip: int = 0, limit: int = 100) -> List[ReferralRequest]:
        """Get requests by status."""
        return self.db.query(ReferralRequest).filter(
            ReferralRequest.status == status
        ).options(
            joinedload(ReferralRequest.student),
            joinedload(ReferralRequest.company)
        ).offset(skip).limit(limit).all()

    def get_approved(self, skip: int = 0, limit: int = 100) -> List[ReferralRequest]:
        """Get approved requests (visible to alumni)."""
        return self.db.query(ReferralRequest).filter(
            ReferralRequest.status == RequestStatus.APPROVED
        ).options(
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
