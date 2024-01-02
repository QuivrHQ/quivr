from fastapi import HTTPException
from modules.brain.dto.inputs import CreateBrainProperties


def validate_api_brain(brain: CreateBrainProperties):
    if brain.brain_definition is None:
        raise HTTPException(status_code=404, detail="Brain definition not found")

    if brain.brain_definition.url is None:
        raise HTTPException(status_code=404, detail="Brain url not found")

    if brain.brain_definition.method is None:
        raise HTTPException(status_code=404, detail="Brain method not found")
