"""Service for creating and validating shareable survey links."""

from secrets import token_urlsafe

from sqlalchemy.orm import Session

from app.models import SurveyLink


class SurveyLinkService:
    """Create and validate protected survey invitations.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the survey link service.

        Args:
            db: SQLAlchemy session.

        Returns:
            None.

        Raises:
            None.
        """

        self.db = db

    def create_link(self, study: str, label: str, condition: str | None = None) -> SurveyLink:
        """Create a new active survey link.

        Args:
            study: Study identifier.
            label: Human-readable link label.
            condition: Optional Study 1 condition.

        Returns:
            SurveyLink: Persisted survey link.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If persistence fails.
        """

        link = SurveyLink(token=self._unique_token(), study=study, condition=condition, label=label, is_active=True)
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link

    def get_active(self, token: str) -> SurveyLink | None:
        """Return an active link by token.

        Args:
            token: URL-safe survey token.

        Returns:
            SurveyLink | None: Active link when found.

        Raises:
            None.
        """

        return self.db.query(SurveyLink).filter(SurveyLink.token == token, SurveyLink.is_active.is_(True)).first()

    def list_links(self) -> list[SurveyLink]:
        """List all survey links newest first.

        Args:
            None.

        Returns:
            list[SurveyLink]: Persisted survey links.

        Raises:
            None.
        """

        return self.db.query(SurveyLink).order_by(SurveyLink.id.desc()).all()

    def mark_response(self, token: str | None) -> None:
        """Increment response count for a submitted token.

        Args:
            token: Optional URL-safe survey token.

        Returns:
            None.

        Raises:
            None.
        """

        if not token:
            return
        link = self.get_active(token)
        if link is not None:
            link.response_count += 1

    def _unique_token(self) -> str:
        """Generate a unique invitation token.

        Args:
            None.

        Returns:
            str: URL-safe token.

        Raises:
            None.
        """

        while True:
            token = token_urlsafe(18)
            if self.db.query(SurveyLink).filter(SurveyLink.token == token).first() is None:
                return token
