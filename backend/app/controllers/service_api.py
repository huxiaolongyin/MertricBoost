
from fastapi import HTTPException
from pydantic import BaseModel
from app.core.crud import CRUDBase
from app.models.system import User
from typing import NewType, TypeVar
from tortoise.expressions import Q
from tortoise.models import Model
from app.models.service import ServiceApi, ServiceApiParam
from app.schemas.service_api import ServiceApiCreate, ServiceApiUpdate, ServiceApiParamCreate, ServiceApiParamUpdate

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class ServiceApiController(CRUDBase[ServiceApi, ServiceApiCreate, ServiceApiUpdate]):
    def __init__(self):
        super().__init__(model=ServiceApi)

    async def get_api_list(self, page: int = 1, page_size: int = 10, search: Q = Q(),):
        """
        获取API列表
        """
        query = self.model.filter(search)
        # 获取总数
        total = await query.count()
        # 分页查询，预加载关联数据
        result = await query\
            .prefetch_related('params', 'create_by', 'app')\
            .offset((page - 1) * page_size)\
            .limit(page_size)
        
        return Total(total), result
    
    async def get_api_detail(self, api_id:int)->ServiceApi:
        """
        通过API ID获取API的详情，包含参数和创建者信息
        """
        api = await ServiceApi.get(id=api_id).prefetch_related('params', 'create_by', 'app')
        
        if not api:
            raise HTTPException(status_code=404, detail="API not found")
            
        return api
    
    async def create(self, obj_in:ServiceApiCreate) ->ServiceApi:
        """
        创建API的数据，包括API基本信息和参数信息
        """
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        # 创建API
        api_data = obj_in.model_dump(exclude={"params"})
        api = await super().create(api_data)
        # 创建API参数
        for param in obj_in.params:
            param_data = param.model_dump()
            param_data['api_id'] = api.id
            await ServiceApiParamController().create(param_data)

        return api

    async def update(self, id, obj_in:ServiceApiUpdate) ->ServiceApi:
        """
        更新API的数据，包括API基本信息和参数信息
        """
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        # 更新API
        api_data = obj_in.model_dump(exclude={"params"})
        # 更新API基本信息
        await super().update(id, api_data)
        # 如果包含参数更新
        if obj_in.params:
            # 删除现有参数
            await ServiceApiParam.filter(api_id=id).delete()
            # 创建新参数
            for param in obj_in.params:
                param_data = param.model_dump()
                param_data['api_id'] = id
                await ServiceApiParamController().create(param_data)
        
        return await ServiceApi.get(id=id).prefetch_related('params')
    
    async def remove(self, id):
        """
        删除API及其相关参数
        """
        # 删除API
        await super().remove(id)
        # 删除API参数
        await ServiceApiParam.filter(api_id=id).delete()

class ServiceApiParamController(CRUDBase[ServiceApiParam, ServiceApiParamCreate, ServiceApiParamUpdate]):
    def __init__(self):
        super().__init__(model=ServiceApiParam)
    
    async def create(self, obj_in):
        return await super().create(obj_in)