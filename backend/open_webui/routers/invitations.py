import datetime
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging
from uuid import UUID

from pydantic import BaseModel

from open_webui.env import SRC_LOG_LEVELS
from open_webui.constants import ERROR_MESSAGES
from open_webui.models.invitation import (
    InvitationModel,
    InvitationForm,
    Invitations
)

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from fastapi.responses import FileResponse, StreamingResponse


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

class EmailRequest(BaseModel):
    email: str
    subject: str
    message: str
    user: str
    password: str

class InvitationRequest(BaseModel):
    token: UUID

def send_email(to_email: str, subject: str, message: str, user: str, password: str):
    try:
        # Configuración del servidor SMTP
        smtp_server = "mail.sintergica.ai"
        smtp_port = 465
        smtp_user = user
        smtp_password = password

        # Construcción del mensaje
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Envío del correo
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=60) as server:  # Usar SMTP_SSL y timeout
            # server.starttls()  <-- ¡ELIMINA ESTA LÍNEA!
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit() #Buena práctica
            print(f"Exito al enviar email: {smtp_user} {smtp_password} {to_email} {subject} {message}")  # Imprime el error completo, no solo la traceback
    except Exception as e:
        print(f"Error al enviar email: {e}")  # Imprime el error completo, no solo la traceback
        # traceback.print_tb(e.__traceback__) # Esto ya lo hace la linea de arriba, no lo necesitas


@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    send_email(email_request.email, email_request.subject, email_request.message, email_request.user,
               email_request.password)
    return {"message": "Email enviado exitosamente"}


@router.post("/send")
async def send_invitation(email_request: EmailRequest):
    invitation_search = Invitations.insert_new_invitation(
        InvitationForm(
            **{
                "token": uuid.uuid4(),
                "is_active": True,
                "email": email_request.email,
                "expire_date": datetime.datetime.now() + datetime.timedelta(days=7),
            }
        )
    )

    email_request.message = email_request.message + "\n" + str(invitation_search.token)

    send_email(email_request.email, email_request.subject, email_request.message, email_request.user,
               email_request.password)
    #return {"message": "Invitación enviada exitosamente"}

    if invitation_search:
        return {"message": "Invitación enviada exitosamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT("Error sending invitation"),
        )


@router.post("/resend")
async def resend_invitation(email_request: EmailRequest):
    invitation_search = Invitations.get_invitation_by_email(email_request.email)

    if invitation_search is None:
        return {"message": "Invitación inexistente"}
        #return await send_invitation(email_request)

    if invitation_search.expire_date >= datetime.datetime.now():
        invitation_search.is_active = True
    else:
        invitation_search.is_active = False
        invitation_search.expire_date = datetime.datetime.now() + datetime.timedelta(days=7)

    email_request.message = email_request.message + "\n" + invitation_search.token
    send_email(email_request.email, email_request.subject, email_request.message, email_request.user, email_request.password)

    return {"message": "Invitación enviada exitosamente"}


@router.post("/validate")
async def validate_invitation(invitation_string: InvitationRequest):
    invitation_search = Invitations.get_invitation_by_id(invitation_string.token)

    if invitation_search is None:
        return {"message": "Invitación inexistente"}

    if invitation_search.expire_date < datetime.datetime.now():
        invitation_search.is_active = False
        invitation = InvitationModel(
            **{
                **invitation_search.model_dump()
            }
        )
        Invitations.update_invitation_status_by_id(invitation)
        return {"message": "Invitación invalida"}

    return {"message": "Invitación valida"}

@router.post("/consume")
async def consume_invitation(invitation_string: InvitationRequest):
    return {"message": "Invitación valida"}