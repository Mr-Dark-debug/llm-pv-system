"""JSON survey API routes."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.survey import SurveyLinkCreate, SurveyLinkRead, SurveySubmit, SurveySubmitResponse
from app.services.survey_link_service import SurveyLinkService
from app.services.survey_service import SurveyService

router = APIRouter(prefix="/api/survey", tags=["survey"])


@router.post("/submit", response_model=SurveySubmitResponse)
async def submit_survey(payload: SurveySubmit, db: Session = Depends(get_db)) -> SurveySubmitResponse:
    """Submit participant survey data.

    Args:
        payload: Survey request body.
        db: Database session dependency.

    Returns:
        SurveySubmitResponse: Participant code and computed scores.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If persistence fails.
    """

    try:
        participant, survey = SurveyService(db).submit_response(
            study=payload.study,
            demographics=payload.demographics,
            usage=payload.usage,
            tasks=payload.tasks,
            qualitative=payload.qualitative,
            condition=payload.condition,
            survey_link_token=payload.survey_link_token,
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return SurveySubmitResponse(participant_code=participant.participant_code, lei=survey.lei, pva=survey.pva)


@router.post("/links", response_model=SurveyLinkRead)
async def create_survey_link(payload: SurveyLinkCreate, request: Request, db: Session = Depends(get_db)) -> SurveyLinkRead:
    """Create a protected survey share link.

    Args:
        payload: Link creation request body.
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        SurveyLinkRead: Created link details.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If persistence fails.
    """

    link = SurveyLinkService(db).create_link(study=payload.study, label=payload.label, condition=payload.condition)
    return SurveyLinkRead(
        token=link.token,
        study=link.study,
        label=link.label,
        condition=link.condition,
        is_active=link.is_active,
        response_count=link.response_count,
        url=str(request.url_for("survey_link_page", token=link.token)),
    )


@router.get("/links", response_model=list[SurveyLinkRead])
async def list_survey_links(request: Request, db: Session = Depends(get_db)) -> list[SurveyLinkRead]:
    """List protected survey share links.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        list[SurveyLinkRead]: Existing link details.

    Raises:
        None.
    """

    links = SurveyLinkService(db).list_links()
    return [
        SurveyLinkRead(
            token=link.token,
            study=link.study,
            label=link.label,
            condition=link.condition,
            is_active=link.is_active,
            response_count=link.response_count,
            url=str(request.url_for("survey_link_page", token=link.token)),
        )
        for link in links
    ]
