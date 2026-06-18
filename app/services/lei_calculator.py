"""LLM Exposure Index scoring service."""


class LEICalculator:
    """Compute benchmark-weighted LLM exposure.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    def calculate(
        self,
        frequencies: dict[str, int],
        tool_model_ids: dict[str, list[str]],
        model_pvrs: dict[str, float],
        duration_of_use_months: int,
        daily_minutes_llm: int,
    ) -> float:
        """Calculate the LLM Exposure Index.

        Args:
            frequencies: Tool frequency scores on a 1-5 scale.
            tool_model_ids: Models associated with each tool.
            model_pvrs: Benchmark PVR values by model id.
            duration_of_use_months: Ordinal duration score from 1 to 5.
            daily_minutes_llm: Daily usage minutes from 0 to 120.

        Returns:
            float: Rounded LEI score.

        Raises:
            None.
        """

        weighted = 0.0
        for tool, frequency in frequencies.items():
            models = tool_model_ids.get(tool, [])
            if not models:
                continue
            mean_pvr = sum(model_pvrs.get(model_id, 0.0) for model_id in models) / len(models)
            weighted += max(frequency - 1, 0) * mean_pvr
        minutes_factor = min(max(daily_minutes_llm, 0), 120) / 120
        duration_factor = min(max(duration_of_use_months, 1), 5) / 5
        # Minutes dominate intensity; duration contributes conservatively to avoid inflating long-but-rare use.
        return round(weighted * ((0.5 * minutes_factor) + (0.125 * duration_factor)), 2)
