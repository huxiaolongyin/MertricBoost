// import { omit } from 'naive-ui/es/_utils';

/**
 * Namespace Api
 *
 * All backend api type
 */
declare namespace Api {
  namespace Common {
    /** 分页的常用参数 */
    interface PaginatingCommonParams {
      /** page page number */
      page: number;
      /** page pageSize */
      pageSize: number;
      /** total count */
      total: number;

      userName: string;
    }

    /** 分页查询列表数据常用参数 */
    interface PaginatingQueryRecord<T = any> extends PaginatingCommonParams {
      records: T[];
    }

    /**
     * 启用状态
     *
     * -“0”：禁用 -“1”：启用
     */
    type EnableStatus = '1' | '0';

    /** common record */
    type CommonRecord<T = any> = {
      /** record id */
      id: number;
      /** record creator */
      createBy: string;
      /** record create time */
      createTime: string;
      /** record updater */
      updateBy: string;
      /** record update time */
      updateTime: string;
      /** record status */
      status: EnableStatus | null;
    } & T;

    // 定义单个表单字段的类型
    interface FormType<T> {
      key: keyof T;
      label: string;
      component: any;
      props?: any;
      placeholder?: string;
    }

    type TimeType = 'daily' | 'weekly' | 'monthly' | 'yearly' | 'cumulative';

    // 常用搜索参数
    type CommonSearchParams = Pick<Common.PaginatingCommonParams, 'page' | 'pageSize'>;
    // 常用检索参数
    type CommonIdParams = { id: number };
    // 常用删除参数
    type CommonDeleteParams = { id: number };

    // 常用批量删除参数
    type CommonBatchDeleteParams = { ids: string[] };
  }

  /**
   * 命名空间授权
   *
   * 后端 api 模块：“auth”
   */
  namespace Auth {
    interface LoginToken {
      token: string;
      refreshToken: string;
    }

    interface UserInfo {
      userId: string;
      userName: string;
      roles: string[];
      buttons: string[];
    }
  }

  /**
   * 命名空间路由
   *
   * 后端 api 模块：“路由”
   */
  namespace Route {
    type ElegantConstRoute = import('@elegant-router/types').ElegantConstRoute;

    interface MenuRoute extends ElegantConstRoute {
      id: string;
    }

    interface UserRoute {
      routes: MenuRoute[];
      home: import('@elegant-router/types').LastLevelRouteKey;
    }
  }
  /**
   * 命名空间系统管理
   *
   * 后端 API 模块：“Metric”
   */
  namespace Metric {
    type StatisticType = 'sum' | 'avg' | 'max' | 'min' | 'count' | 'default';

    type StatisticalPeriod = 'daily' | 'monthly' | 'yearly' | 'cumulative';

    type ChartType = 'bar' | 'line';

    // 指标数据
    interface MetricData {
      id: number; // 唯一标识符
      metricName: string; // 指标名称
      metricDesc: string; // 指标描述
      dataModelId: number; // 选用数据模型
      statisticalPeriod: StatisticalPeriod; // 统计周期
      statisticScope: number; // 统计范围
      chartType: ChartType | ''; // 图表类型
      sensitivity: string; // 敏感等级
      domains: string[]; // 领域
      domainIds: number[]; // 领域ID
      tags: string[]; // 标签
      tagIds: number[]; // 标签ID
      formatType: FormatType; // 格式化类型
      metricFormat: FormatType; // 指标格式
      dimCols: SelectOptions[]; // 维度列
      queryCount: number; // 查询热度
      updateBy: string; // 更新人
      createBy: string; // 创建人
      updateTime: string; // 更新时间
      createTime: string; // 创建时间
      data: MetricDataPoint[]; // 指标数据
      dimData: { key: string[] }[]; // 维度数据
    }

    type MetricDataPoint = {
      date: string;
      value: number;
      [dimension: string]: string | number; // 允许任何维度字段，如 vin
    };

    // 指标列表查询参数
    type MetricListSearchParams = CommonType.RecordNullable<
      Pick<MetricData, 'domainIds' | 'tagIds' | 'sensitivity'> & {
        nameOrDesc: string;
        order: string;
      }
    > &
      Api.Common.CommonSearchParams;

    // 指标详情查询参数
    type MetricDetailSearchParams = CommonType.RecordNullable<{
      id: number;
      statisticalPeriod: StatisticalPeriod | '';
      dateRange: [number, number];
      dimSelect: string; // 发送给接口的参数
      dimFilter: string[]; // 维度过滤参数
      sort: Sort;
    }>;

    type Sort = 'ASC' | 'DESC';

    // 获取到的指标列表
    type MetricList = Common.PaginatingQueryRecord<MetricData>;

    // 获取到的指标详情
    type MetricDetail = {
      records: MetricData;
    };

    // 指标新增、编辑表单字段
    interface MetricFormFields {
      modelForm: Api.Common.FormType<MetricUpdateParams>[];
      metricForm: Api.Common.FormType<MetricUpdateParams>[];
      sensitivityForm: Api.Common.FormType<MetricUpdateParams>[];
      staticForm: Api.Common.FormType<MetricUpdateParams>[];
      chartForm: Api.Common.FormType<MetricUpdateParams>[];
    }

    // 指标新增参数
    type MetricAddParams = CommonType.RecordNullable<
      Pick<
        MetricData,
        | 'metricName'
        | 'metricDesc'
        | 'dataModelId'
        | 'statisticalPeriod'
        | 'statisticScope'
        | 'chartType'
        | 'sensitivity'
        | 'domainIds'
        | 'tagIds'
        | 'metricFormat'
      >
    >;

    // 指标更新参数
    type MetricUpdateParams = CommonType.RecordNullable<Pick<MetricData, 'id'>> & MetricAddParams;

    // 下拉框选项
    type SelectOptions = {
      value: string;
      label: string;
      options: SelectOptions[];
    };

    type FormatType = 'percent' | 'flow' | 'number' | 'currency' | 'default';
  }

  /**
   * 命名空间系统管理
   *
   * 后端 API Decision
   */
  namespace Decision {
    type DecisionData = Common.CommonRecord<{
      id: number;
      decisionName: string;
      decisionDesc: string;
      createBy: string;
      createTime: string;
      updateTime: string;
    }>;

    type DecisionSearchParams = CommonType.RecordNullable<
      Pick<DecisionData, 'decisionName' | 'decisionDesc' | 'createBy'> & Api.Common.CommonSearchParams
    >;

    type DecisionList = Common.PaginatingQueryRecord<DecisionData>;

    type DecisionAddParams = CommonType.RecordNullable<
      Pick<DecisionData, 'decisionName' | 'decisionDesc' | 'createBy'>
    >;

    type DecisionUpdateParams = CommonType.RecordNullable<Pick<DecisionData, 'id'>> & DecisionAddParams;

    type DecisionDeleteParams = CommonType.RecordNullable<Pick<DecisionData, 'id'>>;

    type DecisionDetail = {
      records: [
        {
          id: number;
          decisionName: string;
          decisionDesc: string;
          createBy: string;
          createTime: string;
          updateTime: string;
        }
      ];
    };
  }

  /** 命名空间系统管理 数据资产管理 后端 API 模块：“Asset” */
  namespace Asset {
    // 标签管理
    type TagData = Common.CommonRecord<{
      id: number;
      tagName: string;
      tagType: string;
      tagDesc: string;
      createBy: string;
      createTime: string;
      updateTime: string;
    }>;

    type TagSearchParams = CommonType.RecordNullable<
      Pick<TagData, 'tagName' | 'tagType' | 'createBy'> & Api.Common.CommonSearchParams
    >;

    type TagList = Common.PaginatingQueryRecord<TagData>;

    type TagAddParams = CommonType.RecordNullable<Pick<TagData, 'tagName' | 'tagType' | 'tagDesc' | 'createBy'>>;

    type TagUpdateParams = CommonType.RecordNullable<Pick<TagData, 'id'>> & TagAddParams;

    type MetricTagAddParams = {
      metricId: number;
      tagId: number;
    };

    type MetricTagDeleteParams = {
      metricId: number;
      tagName: string;
    };
  }

  /**
   * 命名空间系统管理
   *
   * 后端 API 模块：“DataService”
   */
  namespace DataService {
    type Method = 'get' | 'post';

    type ServiceApi = Common.CommonRecord<{
      id: number;
      metricName: string;
      apiName: string;
      apiDesc: string;
      apiPath: string;
      apiMethod: Method;
      appName: string;
      appId: number;
      status: string;
      createBy: string;
      createTime: string;
      updateTime: string;
    }>;

    // api 搜索参数
    type ServiceApiSearchParams = CommonType.RecordNullable<
      Pick<ServiceApi, 'metricName' | 'apiName' | 'status' | 'apiMethod' | 'appName' | 'createBy'> &
        Api.Common.CommonSearchParams
    >;

    // api 添加参数
    type ServiceApiAddParams = CommonType.RecordNullable<
      Pick<ServiceApi, 'metricName' | 'apiName' | 'apiDesc' | 'apiPath' | 'apiMethod' | 'createBy' | 'appName'>
    > & {
      status: Api.Common.EnableStatus;
      params: ServiceApiParams[];
    };

    // api 更新参数
    type ServiceApiUpdateParams = CommonType.RecordNullable<Pick<ServiceApi, 'id'>> & ServiceApiAddParams;

    // api 列表
    type ServiceApiList = Common.PaginatingQueryRecord<ServiceApi>;

    // api 详情
    type ServiceApiDetail = {
      records: [
        {
          id: number;
          metricName: string;
          apiName: string;
          apiDesc: string;
          apiPath: string;
          apiMethod: Method;
          appId: number;
          status: string;
          createBy: string;
          createTime: string;
          updateTime: string;
          params: ServiceApiParams[];
        }
      ];
    };

    type ServiceApiParams = {
      id: number;
      paramName: string;
      paramLoc?: string;
      paramType: string;
      paramDesc: string;
      isRequired: number;
      default: string;
      example: string;
    };

    type ServiceApiParamsUpdateParams = CommonType.RecordNullable<ServiceApiParams>;

    // APP
    type ServiceApp = Common.CommonRecord<{
      id: number;
      appName: string;
      appDesc: string;
      status: Api.Common.EnableStatus;
      appKey: string;
      appSecret: string;
      createBy: string;
    }>;

    // app 搜索参数
    type ServiceAppSearchParams = CommonType.RecordNullable<
      Pick<ServiceApp, 'status' | 'appName' | 'createBy'> & Api.Common.CommonSearchParams
    >;

    // app 添加参数
    type ServiceAppAddParams = CommonType.RecordNullable<
      Pick<ServiceApp, 'appName' | 'appDesc' | 'appKey' | 'appSecret' | 'status' | 'createBy'>
    >;

    // app 更新参数
    type ServiceAppUpdateParams = CommonType.RecordNullable<Pick<ServiceApp, 'id'>> & ServiceAppAddParams;

    // app 列表
    type ServiceAppList = Common.PaginatingQueryRecord<ServiceApp>;

    type ServiceAppDetail = {
      records: [
        {
          id: number;
          appName: string;
          appDesc: string;
        }
      ];
    };
  }
  /**
   * 命名空间系统管理
   *
   * 后端 API 模块：“Collect”
   */
  namespace Collect {
    type Collect = Common.CommonRecord<{
      id: number;
      name: string;
      type: string;
      schedule: string;
      status: Api.Common.EnableStatus;
      originDatabaseId: number[];
      originDatabase: string[];
      originDatabaseType: string[];
      originTable: string;
      targetDatabaseId: number[];
      targetDatabase: string[];
      targetDatabaseType: string[];
      targetTable: string;
      createBy: string;
      createTime: string;
      updateTime: string;
    }>;

    type CollectSearchParams = CommonType.RecordNullable<
      Pick<Collect, 'name' | 'type' | 'status'> &
        Common.CommonSearchParams & {
          originDatabaseIds: (number | string)[];
          targetDatabaseIds: number[];
        }
    >;

    // 数据采集添加
    type CollectAddParams = CommonType.RecordNullable<
      Pick<
        Collect,
        | 'name'
        | 'type'
        | 'schedule'
        | 'status'
        | 'originDatabaseId'
        | 'originTable'
        | 'targetDatabaseId'
        | 'targetTable'
      >
    >;

    // 数据采集更新
    type CollectUpdateParams = CommonType.RecordNullable<Pick<Collect, 'id'>> & CollectAddParams;

    // 数据采集列表
    type CollectList = Common.PaginatingQueryRecord<Collect>;
  }
  /**
   * 命名空间系统管理
   *
   * 后端 API 模块：“systemManage”
   */
  namespace SystemManage {
    /** role */
    type Role = Common.CommonRecord<{
      /** role name */
      roleName: string;
      /** role code */
      roleCode: string;
      /** role description */
      roleDesc: string;
      /** role home */
      roleHome: string;
      /** 敏感等级 */
      sensitivity: string;
      /** 域分类 */
      domainIds: number[];
      /** role status */
      status: Api.Common.EnableStatus;
    }>;

    /** 角色添加参数 */
    type RoleAddParams = Pick<
      Role,
      'roleName' | 'roleCode' | 'roleDesc' | 'roleHome' | 'status' | 'sensitivity' | 'domainIds'
    >;

    /** role update params */
    type RoleUpdateParams = CommonType.RecordNullable<Pick<Role, 'id'>> & RoleAddParams;

    /** 角色搜索参数 */
    type RoleSearchParams = CommonType.RecordNullable<
      Pick<Role, 'roleName' | 'roleCode' | 'status'> & Common.CommonSearchParams
    >;

    /** role list */
    type RoleList = Common.PaginatingQueryRecord<Role>;

    /** role authorized */
    type RoleAuthorized = Role & { menuIds: number[]; apiIds: number[]; buttonIds: number[] };

    /** get role authorized params */
    type RoleAuthorizedParams = Pick<RoleAuthorized, 'id'>;

    /** role authorized list */
    type RoleAuthorizedList = CommonType.RecordNullable<RoleAuthorized>;

    /** all role */
    type AllRole = Pick<Role, 'id' | 'roleName' | 'roleCode'>;

    /**
     * api method
     *
     * - "1": "GET"
     * - "2": "POST"
     * - "3": "PUT"
     * - "4": "PATCH"
     * - "5": "DELETE"
     */
    type methods = 'get' | 'post' | 'put' | 'patch' | 'delete';

    /** api */
    type Api = Common.CommonRecord<{
      /** api path */
      path: string;
      /** api method */
      method: methods;
      /** api summary */
      summary: string;
      /** api tags name */
      tags: string;
    }>;

    /** api add params */
    type ApiAddParams = Pick<Api, 'path' | 'method' | 'summary' | 'tags' | 'status'>;

    /** api update params */
    type ApiUpdateParams = CommonType.RecordNullable<Pick<Api, 'id'>> & ApiAddParams;

    /** api search params */
    type ApiSearchParams = CommonType.RecordNullable<
      Pick<Api, 'path' | 'method' | 'summary' | 'tags' | 'status'> & Common.CommonSearchParams
    >;

    /** api list */
    type ApiList = Common.PaginatingQueryRecord<Api>;

    /**
     * log type
     *
     * - "1": "ApiLog"
     * - "2": "UserLog"
     * - "3": "AdminLog"
     * - "4": "SystemLog"
     */
    type logTypes = '1' | '2' | '3' | '4';

    /**
     * api method
     *
     * - "1": "GET"
     * - "2": "POST"
     * - "3": "PUT"
     * - "4": "PATCH"
     * - "5": "DELETE"
     */
    type logDetailTypes =
      | '1101'
      | '1102'
      | '1201'
      | '1202'
      | '1203'
      | '1211'
      | '1212'
      | '1213'
      | '1301'
      | '1302'
      | '1303'
      | '1311'
      | '1312'
      | '1313'
      | '1314'
      | '1315'
      | '1401'
      | '1402'
      | '1403'
      | '1404'
      | '1411'
      | '1412'
      | '1413'
      | '1414'
      | '1415'
      | '1501'
      | '1502'
      | '1503'
      | '1504'
      | '1505'
      | '1506'
      | '1507'
      | '1511'
      | '1512'
      | '1513'
      | '1514'
      | '1515'
      | '1601'
      | '1611'
      | '1612'
      | '1613'
      | '1614'
      | '1615';

    /** log */
    type Log = Common.CommonRecord<{
      /** log type */
      logType: logTypes;
      /** log user */
      logUser: string;
      /** log detail */
      logDetailType: logDetailTypes | null;
      /** request url */
      requestUrl: string;
      /** create time */
      createTime: string;
      /** create time */
      responseCode: string;
    }>;

    /** log add params */
    type LogAddParams = Pick<
      Log,
      'logType' | 'logUser' | 'logDetailType' | 'requestUrl' | 'createTime' | 'responseCode'
    >;

    /** log update params */
    type LogUpdateParams = CommonType.RecordNullable<Pick<Log, 'id'>> & LogAddParams;

    /** log search params */
    type LogSearchParams = CommonType.RecordNullable<
      Pick<Log, 'logType' | 'logUser' | 'logDetailType' | 'requestUrl' | 'createTime' | 'responseCode'> &
        Common.CommonSearchParams & { timeRange: string }
    >;

    /** log list */
    type LogList = Common.PaginatingQueryRecord<Log>;

    /**
     * user gender
     *
     * - "1": "male"
     * - "2": "female"
     * - "3": "unknow"
     */
    type UserGender = '1' | '2' | '3';

    /** user */
    type User = Common.CommonRecord<{
      /** user name */
      userName: string;
      /** password */
      password: string;
      /** user gender */
      userGender: UserGender | null;
      /** user nick name */
      nickName: string;
      /** user phone */
      userPhone: string;
      /** user email */
      userEmail: string;
      /** user role code collection */
      userRoles: string[];
    }>;

    /** user add params */
    type UserAddParams = Pick<
      User,
      'userName' | 'password' | 'userGender' | 'nickName' | 'userPhone' | 'userEmail' | 'userRoles' | 'status'
    >;

    /** user update params */
    type UserUpdateParams = CommonType.RecordNullable<Pick<User, 'id'>> & UserAddParams;

    /** user search params */
    type UserSearchParams = CommonType.RecordNullable<
      Pick<User, 'userName' | 'password' | 'userGender' | 'nickName' | 'userPhone' | 'userEmail' | 'status'> &
        Common.CommonSearchParams
    >;

    /** user list */
    type UserList = Common.PaginatingQueryRecord<User>;

    /**
     * menu type
     *
     * - "1": directory
     * - "2": menu
     */
    type MenuType = '1' | '2';

    type MenuButton = {
      /**
       * button code
       *
       * it can be used to control the button permission
       */
      buttonCode: string;
      /** button description */
      buttonDesc: string;
    };

    /**
     * icon type
     *
     * - "1": iconify icon
     * - "2": local icon
     */
    type IconType = '1' | '2';

    type MenuPropsOfRoute = Pick<
      import('vue-router').RouteMeta,
      | 'i18nKey'
      | 'keepAlive'
      | 'constant'
      | 'order'
      | 'href'
      | 'hideInMenu'
      | 'activeMenu'
      | 'multiTab'
      | 'fixedIndexInTab'
      | 'query'
    >;

    type Menu = Common.CommonRecord<{
      /** parent menu id */
      parentId: number;
      /** menu type */
      menuType: MenuType;
      /** menu name */
      menuName: string;
      /** route name */
      routeName: string;
      /** route path */
      routePath: string;
      /** component */
      component?: string;
      /** iconify icon name or local icon name */
      icon: string;
      /** icon type */
      iconType: IconType;
      /** buttons */
      buttons?: MenuButton[] | null;
      /** children menu */
      children?: Menu[] | null;
    }> &
      MenuPropsOfRoute;

    /** menu add params */
    // type MenuAddParams = Pick<
    //   Menu,
    //   | 'parentId'
    //   | 'menuType'
    //   | 'menuName'
    //   | 'routeName'
    //   | 'routePath'
    //   | 'component'
    //   | 'icon'
    //   | 'iconType'
    //   | 'buttons'
    //   | 'children'
    // >;
    type MenuAddParams = Pick<
      Menu,
      | 'menuType'
      | 'menuName'
      | 'routeName'
      | 'routePath'
      | 'component'
      | 'order'
      | 'i18nKey'
      | 'icon'
      | 'iconType'
      | 'status'
      | 'parentId'
      | 'keepAlive'
      | 'constant'
      | 'href'
      | 'hideInMenu'
      | 'activeMenu'
      | 'multiTab'
      | 'fixedIndexInTab'
    > & {
      query: NonNullable<Menu['query']>;
      buttons: NonNullable<Menu['buttons']>;
      layout: string;
      page: string;
      pathParam: string;
    };

    /** menu update params */
    type MenuUpdateParams = CommonType.RecordNullable<Pick<Menu, 'id'>> & MenuAddParams;

    /** menu list */
    type MenuList = Common.PaginatingQueryRecord<Menu>;

    type MenuTree = {
      id: number;
      label: string;
      pId: number;
      children?: MenuTree[];
    };

    type ButtonTree = {
      id: number;
      label: string;
      pId: number;
      children?: ButtonTree[];
    };

    /** 数据库 */
    type Database = Common.CommonRecord<{
      name: string /** 数据库名称 */;
      type: string /** 数据库类型 */;
      host: string /** 数据库地址 */;
      port: number /** 数据库端口 */;
      username: string /** 数据库用户名 */;
      password: string /** 数据库密码 */;
      database: string /** 数据库 */;
      description: string /** 数据库描述 */;
    }>;

    type DatabaseList = Common.PaginatingQueryRecord<Database>;

    /** 数据库搜索参数 */
    type DatabaseSearchParams = CommonType.RecordNullable<
      Pick<Database, 'name' | 'type' | 'createBy' | 'status'> & Common.CommonSearchParams
    >;

    /** 数据库添加参数 */
    type DatabaseAddParams = CommonType.RecordNullable<Omit<Database, 'id' | 'createTime' | 'updateTime' | 'updateBy'>>;

    /** 数据库更新参数 */
    type DatabaseUpdateParams = CommonType.RecordNullable<Pick<Database, 'id'>> & DatabaseAddParams;

    /** 数据库连接测试参数 */
    type DatabaseTestParams = CommonType.RecordNullable<Pick<Database, 'id'>> & DatabaseAddParams;

    // 数据域和主题域
    type Domain = Common.CommonRecord<{
      domainName: string /** 数据域名称 */;
      domainDesc: string /** 数据域描述 */;
      domainType: string /** 数据域类型 */;
    }>;

    type DomainList = Common.PaginatingQueryRecord<Domain>;

    // 搜索参数
    type DomainSearchParams = CommonType.RecordNullable<
      Pick<Domain, 'domainName' | 'createBy'> & Common.CommonSearchParams
    >;

    // 添加参数
    type DomainAddParams = CommonType.RecordNullable<
      Pick<Domain, 'domainName' | 'domainDesc' | 'domainType' | 'createBy'>
    >;

    // 数据域更新参数
    type DomainUpdateParams = CommonType.RecordNullable<Pick<Domain, 'id'>> & DomainAddParams;

    // 获取主题模型树
    type DomainTree = {
      id: number;
      label: string;
      children?: DomainTree[];
    };

    // 主题模型
    type DataModel = Common.CommonRecord<{
      name: string; // 模型名称
      description: string; // 模型描述
      databaseId: number; // 数据库ID
      tableName: string; // 表名
      dataDomains: number[]; // 数据域ID
      topicDomains: number[]; // 主题域ID
      columnsConf: TableColumns[];
    }>;

    type DataModelList = Common.PaginatingQueryRecord<DataModel>;

    type DomainSearchList = {
      domainIds: number[];
    };
    /** 主题模型搜索参数 */
    type DataModelSearchParams = CommonType.RecordNullable<
      Pick<DataModel, 'name' | 'createBy' | 'status'> & Common.CommonSearchParams & DomainSearchList
    >;

    // 主题模型添加参数，将 fieldConf 改为string类型，好对应接口发送
    type DataModelAddParams = CommonType.RecordNullable<
      Omit<DataModel, 'columnsConf'> & {
        columnsConf: string;
      }
    >;

    /** 主题模型更新参数 */
    type DataModelUpdateParams = CommonType.RecordNullable<Pick<DataModel, 'id'>> & DataModelAddParams;

    // 数据预览参数
    type DataPreviewSearchParams = CommonType.RecordNullable<
      {
        databaseId: number;
        tableName: string;
      } & Common.CommonSearchParams
    >;

    type DataPreview = Common.CommonRecord<{
      id: number;
      [key: string]: any; // 允许任意其他字段
    }>;

    type DataPreviewList = Common.PaginatingQueryRecord<DataPreview>;

    type Table = Common.CommonRecord<{
      tableName: string;
      tableComment: string;
    }>;

    type TableList = Common.PaginatingQueryRecord<Table>;

    type TableSearchParams = { databaseId: number };

    // 定义数据模型的创建、修改的表单类型
    interface DataModelForm {
      currentStep: number;
      stepOne: Pick<CommonType.RecordNullable<DataModel>, 'databaseId' | 'tableName'>;
      stepTwo: Pick<CommonType.RecordNullable<DataModel>, 'columnsConf'>;
      stepThree: Pick<
        CommonType.RecordNullable<DataModel>,
        'name' | 'description' | 'dataDomains' | 'topicDomains' | 'status'
      >;
    }

    // 定义获取数据字段信息的类型
    interface TableColumnsSearchParams {
      databaseId: number;
      tableName: string;
      editMode: editMode;
    }

    type editMode = 'add' | 'edit';

    interface TableColumns {
      columnName: string;
      columnType: string;
      columnComment: string;
      staticType: string | null;
      aggMethod: string | null;
      format: string | null;
      extraCaculate: string | null;
    }

    type TableColumnsList = Common.PaginatingQueryRecord<TableColumns>;
  }
}
