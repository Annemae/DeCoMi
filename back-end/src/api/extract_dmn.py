"""extract_dmn.py file.

Defines a REST API endpoint for extracting a DMN model from source code.
"""
from flask import request
from flask_restful import Resource
from core.prototype_steps.extract_decision_logic_level import extract_decision_logic_level
from core.prototype_steps.extract_decision_requirement_level import \
    extract_decision_requirement_level
from core.prototype_steps.create_dmn_xml import create_dmn_xml
from core.prototype_steps.extract_decisions import extract_decisions
from typing import Dict, Any


class ExtractDMN(Resource):
    """Flask-RESTful Resource handling POST requests to extract a DMN model."""

    def post(self: "ExtractDMN") -> Dict[str, Any]:
        """Collect provided source code and returns extracted DMN model."""
        uploaded_file = request.files.get('file')

        # Name of the file where results are saved.
        # Used for testing purposes, e.g., Case1 or Case2.
        name = "prototype"

        if uploaded_file:
            source_code = uploaded_file.read().decode('utf-8')

            # Extract decisions (i.e., functions) per DMN model using GPT-4.1 Temp 0.6.
            grouped_decisions = extract_decisions(source_code, name)

            if len(grouped_decisions) != 0:
                dmn_models = []

                for group_of_decisions in grouped_decisions:
                    combined_decisions = "\n".join(group_of_decisions)

                    # Extract decision requirement level (i.e., DRD)
                    # using Gemini 2.5 Pro Temp 0.
                    decision_requirement_level = \
                        extract_decision_requirement_level(combined_decisions, name)

                    # Extract decision logic level (i.e., individual decision
                    # tables) using Gemini 2.5 Pro Temp 0.
                    decision_logic_level = ""
                    decision_number = 1
                    for decision in group_of_decisions:
                        decision_logic_level += \
                            extract_decision_logic_level(decision, name + decision_number)
                        decision_number += 1

                    # Create a complete DMN model using Gemini 2.5 Pro Temp 0.
                    dmn_model = \
                        create_dmn_xml(
                            decision_requirement_level + decision_logic_level,
                            name)

                    dmn_models.append(dmn_model)

                return {"models": dmn_models}
