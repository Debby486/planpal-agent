import json
import os
from datetime import timedelta

from django.utils import timezone
from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

PLANPAL_CATEGORIES = [
    "Deep Work",
    "Errands",
    "Fitness",
    "Admin",
    "Family",
    "Learning",
    "Rest",
    "Other",
]

CATEGORY_COLORS = {
    "Deep Work": "#6366F1",
    "Errands": "#10B981",
    "Fitness": "#F43F5E",
    "Admin": "#F59E0B",
    "Family": "#8B5CF6",
    "Learning": "#06B6D4",
    "Rest": "#64748B",
    "Other": "#94A3B8",
}


def llm_plan(prompt: str) -> dict:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI()

    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)

    system = (
        f"You are PlanPal, an everyday planning agent.\n"
        f"Today is {today.isoformat()}.\n"
        f"When the user says 'tomorrow', use date {tomorrow.isoformat()}.\n\n"
        "Return ONLY valid JSON (no markdown, no backticks).\n"
        "JSON shape:\n"
        "{\n"
        '  "date": "YYYY-MM-DD",\n'
        '  "tasks": [\n'
        "    {\n"
        '      "title": "string",\n'
        f'      "category": "one of: {", ".join(PLANPAL_CATEGORIES)}",\n'
        '      "due_at": "ISO8601 datetime",\n'
        '      "remind_minutes_before": number\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Rules:\n"
        "- If remind_minutes_before is missing, default to 30.\n"
        "- Do not add extra keys.\n"
    )

    resp = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    raw = resp.output_text.strip()
    plan = json.loads(raw)

    for t in plan.get("tasks", []):
        category = (t.get("category") or "Other").strip()
        if category not in PLANPAL_CATEGORIES:
            category = "Other"

        t["category"] = category
        t["color"] = CATEGORY_COLORS.get(category, CATEGORY_COLORS["Other"])

        if "remind_minutes_before" not in t:
            t["remind_minutes_before"] = 30

    return plan


def plan_from_prompt(prompt: str) -> dict:
    return llm_plan(prompt)
