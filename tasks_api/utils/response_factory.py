from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

class ResponseFactory:
    @staticmethod
    def succes_response(status_code: int = status.HTTP_200_OK, message: str = None, data: any = None) -> JSONResponse:
        content = {
            "status": "success",
        }

        if message:
            content["message"] = message

        if data:
            content["data"] = data

        return JSONResponse(
            content=content,
            status_code=status_code
        )

    @staticmethod
    def error_response(status_code: int = status.HTTP_400_BAD_REQUEST, detail: str = "Bad request") -> HTTPException:
        return HTTPException(
            status_code=status_code,
            detail=detail
        )