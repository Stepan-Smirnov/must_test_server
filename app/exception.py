from fastapi import HTTPException, status


class CustomExceptions(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ServerError(CustomExceptions):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error."


class BadDatetime(CustomExceptions):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "An incorrect date is specified"
