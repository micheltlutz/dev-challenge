"""The scorecard: results expressed as acceptance criteria, not stack traces.

A challenger should be able to read the output and know which line of the
specification they have not satisfied yet. Everything here exists to make that
true.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from specs_index import criteria_by_id, load_challenges

STATUS_ICON = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP", "missing": "----"}


@dataclass
class Result:
    ac_id: str
    status: str
    detail: str = ""


@dataclass
class Scorecard:
    base_url: str
    challenge: str | None = None
    results: dict[str, Result] = field(default_factory=dict)
    filtered_out: int = 0

    def record(self, ac_id: str, status: str, detail: str = "") -> None:
        # A criterion covered by several tests is only green if all of them are.
        existing = self.results.get(ac_id)
        if existing and existing.status == "failed":
            return
        if existing and existing.status == "skipped" and status == "passed":
            return
        self.results[ac_id] = Result(ac_id, status, detail)

    def note_filtered(self, count: int) -> None:
        self.filtered_out = count

    def _rows(self) -> list[tuple[str, Result, str]]:
        """(challenge_id, result, criterion title) ordered by the spec's order."""
        catalogue = criteria_by_id()
        challenges = load_challenges()

        wanted = (
            [self.challenge]
            if self.challenge and self.challenge in challenges
            else sorted({catalogue[a].challenge for a in self.results if a in catalogue})
        )

        rows = []
        for challenge_id in wanted:
            for criterion in challenges[challenge_id].criteria:
                result = self.results.get(criterion.id) or Result(
                    criterion.id, "missing", "no harness test covers this criterion"
                )
                rows.append((challenge_id, result, criterion.title))
        return rows

    @property
    def counts(self) -> dict[str, int]:
        tally = {"passed": 0, "failed": 0, "skipped": 0, "missing": 0}
        for _challenge, result, _title in self._rows():
            tally[result.status] = tally.get(result.status, 0) + 1
        return tally

    def print_to(self, reporter) -> None:
        rows = self._rows()
        if not rows:
            return

        write = reporter.write_line
        write("")
        write("=" * 72)
        write("  ACCEPTANCE CRITERIA")
        write(f"  target: {self.base_url}")
        if self.challenge:
            write(f"  challenge: {self.challenge}")
        write("=" * 72)

        current = None
        for challenge_id, result, title in rows:
            if challenge_id != current:
                current = challenge_id
                write("")
                write(f"  {load_challenges()[challenge_id].title}  ({challenge_id})")
                write("  " + "-" * 68)
            write(f"  {STATUS_ICON[result.status]}  {result.ac_id}  {title}")
            if result.detail and result.status != "passed":
                write(f"        └─ {result.detail[:120]}")

        tally = self.counts
        total = sum(tally.values())
        write("")
        write("  " + "-" * 68)
        write(
            f"  {tally['passed']}/{total} criteria passed"
            f"   ({tally['failed']} failed, {tally['skipped']} skipped,"
            f" {tally['missing']} uncovered)"
        )
        if tally["skipped"]:
            write("  Skipped criteria could not be checked -- see the reasons above.")
        write("=" * 72)
        write("")

    def to_json(self) -> str:
        rows = self._rows()
        return json.dumps(
            {
                "base_url": self.base_url,
                "challenge": self.challenge,
                "summary": self.counts,
                "criteria": [
                    {
                        "challenge": challenge_id,
                        "id": result.ac_id,
                        "title": title,
                        "status": result.status,
                        "detail": result.detail,
                    }
                    for challenge_id, result, title in rows
                ],
            },
            indent=2,
        )

    def to_markdown(self) -> str:
        rows = self._rows()
        tally = self.counts
        total = sum(tally.values())

        lines = [
            "# Acceptance scorecard",
            "",
            f"- **Target:** `{self.base_url}`",
            f"- **Challenge:** `{self.challenge or 'all'}`",
            f"- **Result:** {tally['passed']}/{total} criteria passed",
            "",
        ]

        current = None
        for challenge_id, result, title in rows:
            if challenge_id != current:
                current = challenge_id
                lines += [
                    "",
                    f"## {load_challenges()[challenge_id].title} (`{challenge_id}`)",
                    "",
                    "| | Criterion | Notes |",
                    "|---|---|---|",
                ]
            icon = {"passed": "✅", "failed": "❌", "skipped": "⏭️", "missing": "⚪"}[
                result.status
            ]
            note = result.detail.replace("|", "\\|")[:160] if result.status != "passed" else ""
            lines.append(f"| {icon} | **{result.ac_id}** {title} | {note} |")

        return "\n".join(lines) + "\n"
