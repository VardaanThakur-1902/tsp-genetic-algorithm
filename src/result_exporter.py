
import json
from pathlib import Path


def save_result(
    output_path: str,
    algorithm: str,
    route: list[int],
    route_labels: list[str],
    distance: float,
    runtime_seconds: float,
    configuration: dict,
) -> None:
    """Save the solver's result and configuration as JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    result = {
        "algorithm": algorithm,
        "route_indices": route,
        "route_labels": route_labels,
        "distance": distance,
        "runtime_seconds": runtime_seconds,
        "configuration": configuration,
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print(f"Result saved to: {path}")
