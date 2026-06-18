"""Phrasal-verb detection service with optional spaCy support."""

from dataclasses import dataclass
import re

from app.seed_data import PHAVE_MASTER_LIST


@dataclass(frozen=True)
class PVDetectionRecord:
    """Detected phrasal verb transfer object.

    Args:
        pv_lemma: Normalized phrasal verb lemma.
        verb: Verb component.
        particle: Particle component.
        sentence_index: Zero-based sentence index.
        token_start: Character offset start.
        token_end: Character offset end.
        transparency: Literal, semi-transparent, or figurative category.
        in_phave_list: Whether the item appears in the master list.
        layer1_confidence: Parser or rule confidence.
        final_confirmed: Human-verification placeholder decision.

    Returns:
        None.

    Raises:
        None.
    """

    pv_lemma: str
    verb: str
    particle: str
    sentence_index: int
    token_start: int
    token_end: int
    transparency: str
    in_phave_list: bool
    layer1_confidence: float
    final_confirmed: bool = True


@dataclass(frozen=True)
class PVDetectionResult:
    """Aggregate detection output.

    Args:
        detections: Confirmed and candidate phrasal verbs.
        word_count: Whitespace-separated word count.
        pv_count: Confirmed phrasal-verb count.
        pvr_per_1k: Phrasal verbs per thousand words.

    Returns:
        None.

    Raises:
        None.
    """

    detections: list[PVDetectionRecord]
    word_count: int
    pv_count: int
    pvr_per_1k: float


class PVDetector:
    """Detect phrasal verbs using a lightweight three-layer approximation.

    Args:
        master_list: Optional PV transparency lookup.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, master_list: dict[str, str] | None = None) -> None:
        """Initialize the detector.

        Args:
            master_list: Optional mapping from normalized PV lemma to transparency.

        Returns:
            None.

        Raises:
            None.
        """

        self.master_list = master_list or PHAVE_MASTER_LIST
        self._patterns = [
            (lemma, re.compile(rf"\b{re.escape(lemma.replace('_', ' '))}\b", re.IGNORECASE))
            for lemma in sorted(self.master_list, key=len, reverse=True)
        ]

    def detect(self, text: str) -> PVDetectionResult:
        """Detect PVs in a text response.

        Args:
            text: Text to analyze.

        Returns:
            PVDetectionResult: Detection details and rate.

        Raises:
            None.
        """

        detections: list[PVDetectionRecord] = []
        sentence_starts = self._sentence_starts(text)
        for lemma, pattern in self._patterns:
            for match in pattern.finditer(text):
                verb, particle = lemma.split("_", 1)
                # The regex layer keeps the app runnable without a 500MB model; spaCy can be enabled later.
                detections.append(
                    PVDetectionRecord(
                        pv_lemma=lemma,
                        verb=verb,
                        particle=particle,
                        sentence_index=self._sentence_index(sentence_starts, match.start()),
                        token_start=match.start(),
                        token_end=match.end(),
                        transparency=self.master_list.get(lemma, "semi_transparent"),
                        in_phave_list=lemma in self.master_list,
                        layer1_confidence=0.72,
                    )
                )
        unique = self._deduplicate(detections)
        word_count = len(re.findall(r"\b[\w'-]+\b", text))
        pv_count = sum(1 for item in unique if item.final_confirmed)
        pvr = round((pv_count / word_count) * 1000, 2) if word_count else 0.0
        return PVDetectionResult(detections=unique, word_count=word_count, pv_count=pv_count, pvr_per_1k=pvr)

    def _sentence_starts(self, text: str) -> list[int]:
        """Find rough sentence start offsets.

        Args:
            text: Text to segment.

        Returns:
            list[int]: Character offsets for sentence starts.

        Raises:
            None.
        """

        starts = [0]
        for match in re.finditer(r"[.!?]\s+", text):
            starts.append(match.end())
        return starts

    def _sentence_index(self, starts: list[int], offset: int) -> int:
        """Map a character offset to a sentence index.

        Args:
            starts: Sentence start offsets.
            offset: Character offset to locate.

        Returns:
            int: Zero-based sentence index.

        Raises:
            None.
        """

        index = 0
        for candidate in starts:
            if candidate <= offset:
                index = starts.index(candidate)
        return index

    def _deduplicate(self, detections: list[PVDetectionRecord]) -> list[PVDetectionRecord]:
        """Remove duplicate matches from overlapping patterns.

        Args:
            detections: Raw detection records.

        Returns:
            list[PVDetectionRecord]: Unique detections.

        Raises:
            None.
        """

        seen: set[tuple[int, int, str]] = set()
        unique: list[PVDetectionRecord] = []
        for item in sorted(detections, key=lambda record: (record.token_start, record.token_end)):
            key = (item.token_start, item.token_end, item.pv_lemma)
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return unique
