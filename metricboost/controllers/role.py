from metricboost.core.crud import CRUDBase
from metricboost.logger import get_logger
from metricboost.models.asset import Domain
from metricboost.models.system import Api, Button, Role
from metricboost.schemas.roles import RoleCreate, RoleUpdate

logger = get_logger(__name__)


class RoleController(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(model=Role)

    async def is_exist(self, role_name: str) -> bool:
        return await self.model.filter(role_name=role_name).exists()

    async def get_by_name(self, role_name: str) -> Role | None:
        return await self.model.filter(role_name=role_name).first()

    async def get_by_code(self, role_code: str) -> Role | None:
        return await self.model.filter(role_code=role_code).first()

    async def get_all(self) -> list[Role]:
        return await self.model.all()

    @staticmethod
    async def update_buttons_by_code(
        role: Role, buttons_codes: list[str] | None = None
    ) -> bool:
        if not buttons_codes:
            return False

        await role.buttons.clear()
        for button_code in buttons_codes:
            button_obj = await Button.get(button_code=button_code)
            await role.buttons.add(button_obj)
        return True

    @staticmethod
    async def update_apis_by_code(
        role: Role, apis_codes: list[str] | None = None
    ) -> bool:
        if not apis_codes:
            return False

        await role.apis.clear()
        for api_code in apis_codes:
            api_obj = await Api.get(api_code=api_code)
            await role.apis.add(api_obj)
        return True

    @staticmethod
    async def update_domain_by_ids(
        id: int, domain_ids: list[str] | None = None
    ) -> bool:
        try:
            role = await Role.get(id=id)
            if not domain_ids:
                return False
            await role.domains.clear()
            for domain_id in domain_ids:
                domain_obj = await Domain.get(id=domain_id)
                await role.domains.add(domain_obj)
            return True
        except Exception as e:
            logger.error(f"更新角色{id}的域失败")
            raise e


role_controller = RoleController()
