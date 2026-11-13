"""Convert a LeRobot ``lerobot-eval`` result file into evallog's trial table.

Usage:
    python scripts/pilot_to_csv.py OUTPUT_DIR TRIALS_CSV \
        --policy pi05_base --task libero_10 --machine hao-ws
"""

import argparse
import csv
import datetime as dt
import json
import sys
from importlib import metadata
from pathlib import Path

FIELDS = [
    "trial_id", "study_id", "source", "timestamp", "policy", "task",
    "success", "progress", "pair_id", "condition_id", "failure_mode",
    "evaluator", "seed", "machine", "software_version",
]


def find_eval_info(output_dir):
    matches = sorted(Path(output_dir).rglob("eval_info.json"))
    if not matches:
        sys.exit(f"No eval_info.json found under {output_dir}")
    return matches[-1]


def iter_episodes(info):
    if "per_episode" in info:
        for ep in info["per_episode"]:
            yield None, ep
        return
    for key in ("per_task",):
        for group in info.get(key, []) or []:
            name = (
                f"{group.get('task_group', '')}_{group.get('task_id', '')}".strip("_")
                or None
            )
            metrics = group.get("metrics", group)
            if metrics.get("per_episode"):
                for ep in metrics["per_episode"]:
                    yield name, ep
            else:
                for ix, success in enumerate(metrics.get("successes", []) or []):
                    yield name, {"episode_ix": ix, "success": success}
    if not any(k in info for k in ("per_episode", "per_task", "per_group")):
        sys.exit(f"Could not find per-episode results. Top-level keys: {list(info)}")


def lerobot_version():
    try:
        return f"lerobot=={metadata.version('lerobot')}"
    except metadata.PackageNotFoundError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("trials_csv")
    parser.add_argument("--policy", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--study-id", default="libero-pilot")
    parser.add_argument("--machine", required=True)
    args = parser.parse_args()

    info = json.loads(find_eval_info(args.output_dir).read_text())
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    version = lerobot_version()

    out = Path(args.trials_csv)
    new_file = not out.exists()
    rows = 0
    with out.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        for task_name, ep in iter_episodes(info):
            task = task_name or args.task
            ix = ep.get("episode_ix", rows)
            condition = f"init_{ix:02d}" if isinstance(ix, int) else f"init_{ix}"
            writer.writerow({
                "trial_id": f"{args.machine}-{args.policy}-{task}-{condition}",
                "study_id": args.study_id,
                "source": "sim",
                "timestamp": now,
                "policy": args.policy,
                "task": task,
                "success": int(bool(ep.get("success", False))),
                "progress": "",
                "pair_id": f"{task}-{condition}",
                "condition_id": condition,
                "failure_mode": "",
                "evaluator": "",
                "seed": ep.get("seed", ""),
                "machine": args.machine,
                "software_version": version,
            })
            rows += 1

    print(f"Wrote {rows} trials to {out}")


if __name__ == "__main__":
    main()
