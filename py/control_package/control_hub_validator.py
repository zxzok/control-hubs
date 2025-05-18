from __future__ import annotations

"""Utilities to validate control hubs using a local Ollama model."""

from typing import List
import os
import subprocess
from .node_classification import NodeClassification
from .utils import load_network


class ControlHubValidator:
    """Query an Ollama model to analyze control hub functions."""

    def __init__(self, input_file: str, model: str = "llama2", output_file: str = "./result/control_hub_validation.txt"):
        """Compute control hubs for ``input_file`` and validate via ``model``.

        Parameters
        ----------
        input_file : str
            Network file in ``.net`` format.
        model : str, optional
            Name of the local Ollama model to use.
        output_file : str, optional
            Destination path for the validation results.
        """
        self.input_file = input_file
        self.model = model
        self.output_file = output_file

        base = os.path.splitext(os.path.basename(input_file))[0]
        node_file = f"./result/{base}_nodeType.txt"
        self.classifier = NodeClassification(input_file, output_file=node_file)
        _, _, self.names = load_network(input_file)
        self.validate()

    def _query_model(self, prompt: str) -> str:
        """Return the model response for ``prompt`` or an error message."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                check=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception as exc:  # pragma: no cover - environment dependent
            return f"Failed to query model: {exc}"

    def validate(self) -> None:
        """Query the model about each control hub and write results."""
        results: List[str] = []
        for hub in sorted(self.classifier.Control_hub):
            name = self.names[hub] if hub < len(self.names) else str(hub)
            prompt = f"Explain the role of {name} in cancer."
            answer = self._query_model(prompt)
            results.append(f"{name}: {answer}\n")

        with open(self.output_file, "w") as f:
            f.writelines(results)

