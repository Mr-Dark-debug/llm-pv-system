"""Core regression tests for the LEI/PVA benchmark application."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, init_db
from app.main import create_app
from app.models import LLMModel, Prompt
from app.services.lei_calculator import LEICalculator
from app.services.pv_detector import PVDetector
from app.services.pva_calculator import PVACalculator
from app.services.survey_service import SurveyService


def make_session():
    """Create an isolated in-memory database session.

    Args:
        None.

    Returns:
        sqlalchemy.orm.Session: A fresh SQLAlchemy session.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If table creation fails.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)()


def test_init_db_seeds_required_prompt_and_model_counts():
    """Verify startup data supports the benchmark scope.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If seed counts do not meet the protocol.
    """
    db = make_session()

    init_db(db)

    assert db.query(Prompt).count() == 90
    assert db.query(LLMModel).count() >= 16


def test_pv_detector_counts_known_phrasal_verbs_and_rates():
    """Detect phrasal verbs with transparent metadata.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If known PVs or rates are missed.
    """
    detector = PVDetector()

    result = detector.detect("Students look up words and give up less often when examples stand out.")

    lemmas = {item.pv_lemma for item in result.detections}
    assert {"look_up", "give_up", "stand_out"}.issubset(lemmas)
    assert result.pv_count == 3
    assert result.pvr_per_1k > 0


def test_lei_calculator_weights_frequency_by_model_pvr():
    """Compute exposure from frequency and benchmark-derived PVR.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If the weighted LEI formula changes unexpectedly.
    """
    score = LEICalculator().calculate(
        frequencies={"chatgpt": 5, "claude": 3, "gemini": 1},
        tool_model_ids={"chatgpt": ["gpt-4o"], "claude": ["claude-3-5-sonnet"], "gemini": ["gemini-1.5-pro"]},
        model_pvrs={"gpt-4o": 20.0, "claude-3-5-sonnet": 10.0, "gemini-1.5-pro": 5.0},
        duration_of_use_months=4,
        daily_minutes_llm=60,
    )

    assert score == 35.0


def test_pva_calculator_combines_avoidance_tasks():
    """Compute higher PVA when participants avoid PV choices.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If the composite PVA formula changes unexpectedly.
    """
    score = PVACalculator().calculate(
        forced_choice_pv_chosen=[True, False, False, False],
        translation_pv_used=[False, False, True],
        acceptability_scores=[1, 2, 5],
    )

    assert round(score, 2) == 68.33


def test_survey_service_creates_participant_and_scores_submission():
    """Persist one survey submission with computed LEI and PVA.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If the participant or computed scores are missing.
    """
    db = make_session()
    init_db(db)
    service = SurveyService(db)

    participant, survey = service.submit_response(
        study="study2",
        demographics={
            "age": 24,
            "gender": "self-described",
            "l1_language": "Hindi",
            "l1_family": "indo_aryan",
            "country": "IN",
            "education": "masters",
            "years_english": 12,
            "cefr_self_rating": "C1",
        },
        usage={
            "chatgpt_frequency": 5,
            "chatgpt_models": ["gpt-4o"],
            "claude_frequency": 2,
            "claude_models": ["claude-3-5-sonnet"],
            "daily_minutes_llm": 45,
            "duration_of_use_months": 4,
            "noticing_c7": 4,
            "noticing_c8": True,
            "noticing_c10": 5,
        },
        tasks={
            "forced_choice": [{"item_id": "D1", "pv_chosen": False}],
            "translation": [{"item_id": "E1", "translated_text": "continue", "pv_used": False, "meaning_correct": True, "score": 1}],
            "acceptability": [{"item_id": "F1", "rating": 2, "pv_variant": True}],
        },
        qualitative={"qualitative_g1": "I use chatbots for examples.", "qualitative_g2": "PVs feel informal."},
    )

    assert participant.participant_code.startswith("P")
    assert survey.lei is not None
    assert survey.pva is not None


def test_app_dashboard_renders_after_startup_seed():
    """Confirm the app boots and renders HTML without API keys.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If the dashboard fails to render.
    """
    app = create_app(database_url="sqlite://")

    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "LLMs as Linguistic Input" in response.text


def test_survey_share_link_flow_accepts_valid_token_and_rejects_bad_token():
    """Create a protected survey link and submit through it.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If protected link behavior regresses.
    """
    app = create_app(database_url="sqlite://")

    with TestClient(app) as client:
        created = client.post(
            "/api/survey/links",
            json={"study": "study2", "label": "Pilot Study 2", "condition": None},
        )
        assert created.status_code == 200
        token = created.json()["token"]

        page = client.get(f"/s/{token}")
        assert page.status_code == 200
        assert f'data-link-token="{token}"' in page.text

        bad = client.get("/s/not-a-real-token")
        assert bad.status_code == 404

        submitted = client.post(
            "/api/survey/submit",
            json={
                "study": "study2",
                "survey_link_token": token,
                "demographics": {
                    "age": 24,
                    "gender": "self-described",
                    "l1_language": "Hindi",
                    "l1_family": "other",
                    "country": "IN",
                    "education": "masters",
                    "years_english": 12,
                    "cefr_self_rating": "C1",
                },
                "usage": {
                    "chatgpt_frequency": 5,
                    "chatgpt_models": ["gpt-4o"],
                    "daily_minutes_llm": 30,
                    "duration_of_use_months": 3,
                },
                "tasks": {
                    "forced_choice": [{"item_id": "D1", "pv_chosen": False}],
                    "translation": [{"item_id": "E1", "translated_text": "continue", "pv_used": False}],
                    "acceptability": [{"item_id": "F1", "rating": 3, "pv_variant": True}],
                },
                "qualitative": {"qualitative_g1": "Useful.", "qualitative_g2": "Natural examples help."},
            },
        )
        assert submitted.status_code == 200
        assert submitted.json()["participant_code"].startswith("P")
