"""HTML page routes rendered with Jinja2."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database import get_db
from app.models import LLMModel, Participant, Prompt
from app.services.analysis_service import AnalysisService
from app.services.survey_link_service import SurveyLinkService

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render dashboard status cards and charts.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered dashboard.

    Raises:
        None.
    """

    summary = AnalysisService(db).summary()
    return templates.TemplateResponse(request, "dashboard.html", {"summary": summary})


@router.get("/benchmark", response_class=HTMLResponse)
async def benchmark_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render benchmark control page.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered benchmark page.

    Raises:
        None.
    """

    models = db.query(LLMModel).order_by(LLMModel.provider, LLMModel.display_name).all()
    return templates.TemplateResponse(request, "benchmark.html", {"models": models})


@router.get("/benchmark/{model_id}", response_class=HTMLResponse)
async def benchmark_detail_page(model_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render per-model benchmark details.

    Args:
        model_id: Model primary key.
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered detail page.

    Raises:
        None.
    """

    model = db.get(LLMModel, model_id)
    return templates.TemplateResponse(request, "benchmark_detail.html", {"model": model})


@router.get("/survey/{study}", response_class=HTMLResponse)
async def survey_page(study: str, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render participant survey.

    Args:
        study: Study identifier.
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered survey page.

    Raises:
        None.
    """

    models = db.query(LLMModel).order_by(LLMModel.display_name).all()
    return templates.TemplateResponse(request, "survey.html", {"study": study, "models": models, "survey_link": None})


@router.get("/s/{token}", response_class=HTMLResponse, name="survey_link_page")
async def survey_link_page(token: str, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render participant survey from a protected share token.

    Args:
        token: URL-safe survey link token.
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered survey page.

    Raises:
        HTTPException: If the token is invalid or inactive.
    """

    link = SurveyLinkService(db).get_active(token)
    if link is None:
        raise HTTPException(status_code=404, detail="Survey link not found.")
    models = db.query(LLMModel).order_by(LLMModel.display_name).all()
    return templates.TemplateResponse(request, "survey.html", {"study": link.study, "models": models, "survey_link": link})


@router.get("/survey-links", response_class=HTMLResponse)
async def survey_links_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render survey link management page.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered survey link page.

    Raises:
        None.
    """

    links = SurveyLinkService(db).list_links()
    return templates.TemplateResponse(request, "survey_links.html", {"links": links})


@router.get("/survey-thanks", response_class=HTMLResponse)
async def survey_thanks(request: Request) -> HTMLResponse:
    """Render survey debrief page.

    Args:
        request: FastAPI request.

    Returns:
        HTMLResponse: Rendered thank-you page.

    Raises:
        None.
    """

    return templates.TemplateResponse(request, "survey_thanks.html")


@router.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render analysis charts page.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered analysis page.

    Raises:
        None.
    """

    summary = AnalysisService(db).summary()
    return templates.TemplateResponse(request, "analysis.html", {"summary": summary})


@router.get("/participants", response_class=HTMLResponse)
async def participants_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render admin participant table.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered participant table.

    Raises:
        None.
    """

    participants = db.query(Participant).order_by(Participant.id.desc()).all()
    return templates.TemplateResponse(request, "participants.html", {"participants": participants})


@router.get("/prompts", response_class=HTMLResponse)
async def prompts_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render prompt manager table.

    Args:
        request: FastAPI request.
        db: Database session dependency.

    Returns:
        HTMLResponse: Rendered prompts table.

    Raises:
        None.
    """

    prompts = db.query(Prompt).order_by(Prompt.prompt_id).all()
    return templates.TemplateResponse(request, "prompts.html", {"prompts": prompts})


@router.get("/export", response_class=HTMLResponse)
async def export_page(request: Request) -> HTMLResponse:
    """Render export links.

    Args:
        request: FastAPI request.

    Returns:
        HTMLResponse: Rendered export page.

    Raises:
        None.
    """

    return templates.TemplateResponse(request, "export.html")
