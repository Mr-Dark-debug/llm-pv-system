"""CSV and JSON export service."""

import csv
import io
import json

from sqlalchemy.orm import Session

from app.models import LLMResponse, Participant, SurveyResponse


class ExportService:
    """Export persisted research data.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the export service.

        Args:
            db: SQLAlchemy session.

        Returns:
            None.

        Raises:
            None.
        """

        self.db = db

    def participants_csv(self) -> str:
        """Export participant and survey scores as CSV.

        Args:
            None.

        Returns:
            str: CSV text.

        Raises:
            csv.Error: If CSV serialization fails.
        """

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["participant_code", "study", "condition", "age", "cefr", "lei", "pva"])
        rows = self.db.query(Participant, SurveyResponse).join(SurveyResponse, SurveyResponse.participant_id == Participant.id).all()
        for participant, survey in rows:
            writer.writerow([participant.participant_code, participant.study, participant.condition, participant.age, participant.cefr_self_rating, survey.lei, survey.pva])
        return output.getvalue()

    def benchmark_json(self) -> str:
        """Export LLM benchmark responses as JSON.

        Args:
            None.

        Returns:
            str: JSON text.

        Raises:
            TypeError: If JSON serialization fails.
        """

        rows = self.db.query(LLMResponse).all()
        payload = [
            {
                "id": row.id,
                "model_id": row.model.model_id,
                "prompt_id": row.prompt.prompt_id,
                "run_id": row.run_id,
                "status": row.status,
                "word_count": row.word_count,
                "pv_count": row.pv_count,
                "pvr_per_1k": row.pvr_per_1k,
                "output_text": row.output_text,
            }
            for row in rows
        ]
        return json.dumps(payload, default=str, indent=2)
