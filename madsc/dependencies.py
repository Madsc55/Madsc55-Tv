"""Five-system dependency contract, without starting jobs or mutating production."""
from __future__ import annotations

OWNERS = {
    "k1": ("k2", "k3", "k4", "k5"),
    "k2": ("k3", "k4", "k5"),
    "k3": ("k4", "k5"),
    "k4": ("k5",),
    "k5": (),
}
TASKS = {
    "candidate_discovery": ("k2", "k3", "k4", "k5"),
    "channel_assessment": ("k1", "k2", "k3", "k4", "k5"),
    "ibo_device_decision": ("k1", "k3", "k4", "k5"),
    "backup_restore": ("k1", "k4", "k5"),
    "epg_pages": ("k1", "k3", "k4", "k5"),
    "schedule_collision": ("k1", "k2", "k3", "k4", "k5"),
}

def plan_task(task: str) -> dict:
    if task not in TASKS:
        raise ValueError("Unknown task; review notes and assign owners first")
    return {"task": task, "involved_categories": list(TASKS[task]),
            "execution_mode": "one_coordinated_batch",
            "independent_extra_triggers": 0,
            "schedule_activation_allowed": False,
            "legacy_workflows_disabled": False,
            "production_writes": False}

def validate_batch(tasks: list[str]) -> dict:
    if not isinstance(tasks, list) or len(set(tasks)) != len(tasks):
        raise ValueError("Duplicate or invalid task batch")
    plans = [plan_task(t) for t in tasks]
    return {"tasks": plans, "five_categories": list(OWNERS),
            "independent_extra_triggers": 0,
            "ready_for_production": False}
