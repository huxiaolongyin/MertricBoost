from metricboost.core.crud import CRUDBase
from metricboost.models.system import Log
from metricboost.schemas.logs import LogCreate, LogUpdate


class LogController(CRUDBase[Log, LogCreate, LogUpdate]):
    def __init__(self):
        super().__init__(model=Log)


log_controller = LogController()
