from metricboost.core.crud import CRUDBase
from metricboost.models.system import Api
from metricboost.schemas.apis import ApiCreate, ApiUpdate


class ApiController(CRUDBase[Api, ApiCreate, ApiUpdate]):
    def __init__(self):
        super().__init__(model=Api)


api_controller = ApiController()
