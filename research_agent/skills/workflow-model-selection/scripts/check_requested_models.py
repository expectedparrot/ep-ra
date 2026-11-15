#!/usr/bin/env python3
"""Check a saved model selection against explicit researcher constraints."""

import argparse
import json
from pathlib import Path


def check_models(models, services=(), required_models=(), required_pairs=()):
    selected = [
        {"model": model.model, "service": model._inference_service_}
        for model in models
    ]
    errors = []
    if not selected:
        errors.append("No explicit models selected; an implicit default cannot satisfy the plan")
    allowed = set(services)
    for model in selected:
        if allowed and model["service"] not in allowed:
            errors.append(f"Model {model['model']!r} uses disallowed service {model['service']!r}")
    for missing in sorted(set(required_models) - {m["model"] for m in selected}):
        errors.append(f"Required model missing: {missing}")
    selected_pairs = {(m["service"], m["model"]) for m in selected}
    for service, name in sorted({tuple(pair) for pair in required_pairs} - selected_pairs):
        errors.append(f"Required model/provider pair missing: {name!r} on service {service!r}")
    return {"ok": not errors, "selected_models": selected, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--service", action="append", default=[], help="Allowed service (repeatable)")
    parser.add_argument("--require-model", action="append", default=[],
                        help="Required model identifier on any allowed service (repeatable)")
    parser.add_argument("--require-pair", action="append", nargs=2, default=[],
                        metavar=("SERVICE", "MODEL"),
                        help="Required model on its exact requested service (repeatable)")
    args = parser.parse_args()
    if not args.service and not args.require_model and not args.require_pair:
        parser.error("Provide at least one requested service, model, or service/model pair")
    from edsl import Jobs, ModelList
    from edsl.cli_shared import load_any_object

    if not args.artifact.is_file():
        parser.error("Expected an existing local artifact")
    artifact = load_any_object(str(args.artifact.resolve()))
    if isinstance(artifact, Jobs):
        models = artifact.models
    elif isinstance(artifact, ModelList):
        models = artifact
    else:
        parser.error("Expected a saved ModelList or Jobs artifact")
    result = check_models(models, args.service, args.require_model, args.require_pair)
    print(json.dumps(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
