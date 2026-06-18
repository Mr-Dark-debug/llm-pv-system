"""PV Avoidance Score calculation service."""


class PVACalculator:
    """Compute composite phrasal-verb avoidance.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    def calculate(
        self,
        forced_choice_pv_chosen: list[bool],
        translation_pv_used: list[bool],
        acceptability_scores: list[int],
    ) -> float:
        """Calculate PVA as a 0-100 composite.

        Args:
            forced_choice_pv_chosen: Whether PV option was selected for D items.
            translation_pv_used: Whether a PV was produced for E items.
            acceptability_scores: Ratings for PV variants on a 1-5 scale.

        Returns:
            float: Composite avoidance score where higher means more avoidance.

        Raises:
            None.
        """

        forced_avoidance = self._avoidance_rate(forced_choice_pv_chosen)
        translation_avoidance = self._avoidance_rate(translation_pv_used)
        if acceptability_scores:
            acceptability_avoidance = sum((5 - min(max(score, 1), 5)) / 4 for score in acceptability_scores) / len(acceptability_scores)
        else:
            acceptability_avoidance = 0.0
        # Production tasks carry more weight than judgements because they directly measure avoidance behavior.
        return round(((0.4 * forced_avoidance) + (0.4 * translation_avoidance) + (0.2 * acceptability_avoidance)) * 100, 2)

    def _avoidance_rate(self, values: list[bool]) -> float:
        """Return share of items where a PV was not chosen/used.

        Args:
            values: Boolean item outcomes.

        Returns:
            float: Avoidance rate from 0 to 1.

        Raises:
            None.
        """

        if not values:
            return 0.0
        return sum(1 for value in values if not value) / len(values)
