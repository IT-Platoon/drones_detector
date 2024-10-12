from fastapi import Request, encoders, exceptions, responses, status


async def validation_exception_handler(
    _: Request,
    exc: exceptions.RequestValidationError,
):
    """
    Custom validation exception handler.
    """
    modified_details = []
    for error in exc.errors():
        modified_details.append(
            {
                "field": error["loc"][-1],
                "message": error["msg"],
            }
        )
    return responses.JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=encoders.jsonable_encoder({"detail": modified_details}),
    )

