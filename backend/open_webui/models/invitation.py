import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from open_webui.internal.db import Base, JSONField, get_db
from open_webui.env import SRC_LOG_LEVELS
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text, JSON, DateTime, Boolean

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Invitation DB Schema
####################


class Invitation(Base):
    __tablename__ = "invitation"
    token = Column(String, primary_key=True)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    expire_date = Column(DateTime)


class InvitationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: UUID
    email: str
    is_active: bool
    expire_date: datetime


class InvitationForm(BaseModel):
    token: UUID
    email: str
    is_active: bool
    expire_date: datetime


class InvitationTable:
    def insert_new_invitation(self, new_invitation: InvitationForm) -> Optional[InvitationModel]:
        with get_db() as db:
            invitation = InvitationModel(
                **{
                    **new_invitation.model_dump(),
                }
            )

            try:
                result = Invitation(**invitation.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return InvitationModel.model_validate(result)
                else:
                    return None
            except Exception as e:
                print(f"Error creating tool: {e}")
                return None

    def get_invitation_by_id(self, token: UUID) -> Optional[InvitationModel]:
        with get_db() as db:
            try:
                invitation = db.get(Invitation, token)
                return InvitationModel.model_validate(invitation)
            except Exception:
                return None

    def get_invitation_by_email(self, email: str) -> Optional[InvitationModel]:
        with get_db() as db:
            try:
                invitation = db.get(Invitation, email)
                return InvitationModel.model_validate(invitation)
            except Exception:
                return None

    def get_invitations(self) -> list[InvitationModel]:
        with get_db() as db:
            return [InvitationModel.model_validate(invitation) for invitation in db.query(Invitation).all()]

    def get_invitations_by_ids(self, tokens: list[UUID]) -> list[InvitationModel]:
        with get_db() as db:
            return [
                InvitationModel.model_validate(invitation)
                for invitation in db.query(Invitation)
                .filter(Invitation.id.in_(tokens))
                .order_by(Invitation.updated_at.desc())
                .all()
            ]

    def get_invitation_by_user_id(self, email: str) -> list[InvitationModel]:
        with get_db() as db:
            return [
                InvitationModel.model_validate(invitation)
                for invitation in db.query(Invitation).filter_by(email=email).all()
            ]

    def update_invitation_expiration_by_id(self, token: UUID) -> Optional[InvitationModel]:
        with get_db() as db:
            try:
                invitation = db.query(Invitation).filter_by(token=token).first()
                invitation.expire_date = datetime.now() + timedelta(days=7)
                db.commit()

                return InvitationModel.model_validate(invitation)
            except Exception:
                return None

    def update_invitation_status_by_id(self, token: str) -> Optional[InvitationModel]:
        with get_db() as db:
            try:
                invitation = db.query(Invitation).filter_by(token=token).first()
                invitation.is_active = False
                db.commit()

                return InvitationModel.model_validate(invitation)
            except Exception:
                return None

    def delete_file_by_id(self, token: UUID) -> bool:
        with get_db() as db:
            try:
                db.query(Invitation).filter_by(token=token).delete()
                db.commit()

                return True
            except Exception:
                return False

    def delete_all_files(self) -> bool:
        with get_db() as db:
            try:
                db.query(Invitation).delete()
                db.commit()

                return True
            except Exception:
                return False


Invitations = InvitationTable()