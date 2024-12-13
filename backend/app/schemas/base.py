from typing import Any
from datetime import date, datetime
from fastapi.responses import JSONResponse


class Custom(JSONResponse):
    def __init__(
        self,
        code: str | int = "0000",
        status_code: int = 200,
        msg: str = "OK",
        data: Any = None,
        **kwargs,
    ):
        if data:
            data = self.process_dates(data)
        content = {"code": str(code), "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=status_code)

    def process_dates(self, obj):
        """
        处理 data 字典中任意嵌套层级的日期类型数据
        """
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self.process_dates(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.process_dates(item) for item in obj]
        return obj


class Success(Custom):
    pass


class Fail(Custom):
    def __init__(
        self,
        code: str | int = "4000",
        msg: str = "OK",
        data: Any = None,
        **kwargs,
    ):
        super().__init__(code=code, msg=msg, data=data, status_code=200, **kwargs)


class Error(Custom):
    def __init__(
        self,
        code: str | int = "4000",
        msg: str = "服务器内部错误",
        data: Any = None,
        **kwargs,
    ):
        super().__init__(code=code, msg=msg, data=data, status_code=400, **kwargs)


class SuccessExtra(Custom):
    def __init__(
        self,
        code: str | int = "0000",
        msg: str = "OK",
        data: Any = None,
        total: int = 0,
        current: int = 1,
        size: int = 20,
        **kwargs,
    ):
        # kwargs.update({"total": total, "current": current, "size": size})
        if isinstance(data, dict):
            data.update({"total": total, "current": current, "size": size})
        super().__init__(code=code, msg=msg, data=data, status_code=200, **kwargs)
