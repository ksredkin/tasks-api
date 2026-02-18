from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

class ResponseFactory:
    """Фабрика для создания ответов API"""
    @staticmethod
    def success_response(status_code: int = status.HTTP_200_OK, message: str = None, data: any = None) -> JSONResponse:
        """Создает успешный JSON-ответ"""
        content = {"status": "success"}

        if message:
            content["message"] = message

        if data:
            content["data"] = data

        return JSONResponse(content=content, status_code=status_code)

    @staticmethod
    def error_response(status_code: int = status.HTTP_400_BAD_REQUEST, detail: str = "Bad request") -> HTTPException:
        """Создает исключение для ошибок API"""
        return HTTPException(status_code=status_code, detail=detail)