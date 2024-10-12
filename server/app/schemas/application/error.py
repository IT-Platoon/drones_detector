from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: dict = Field(..., example=[
        {
            'field': 'quantity', 
            'message': 'value is not a valid integer',
        }
    ])
