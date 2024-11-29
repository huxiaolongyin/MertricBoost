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
      /** current page number */
      current: number;
      /** page size */
      size: number;
      /** total count */
      total: number;
    }

    /** 分页查询列表数据常用参数 */
    interface PaginatingQueryRecord<T = any> extends PaginatingCommonParams {
      records: T[];
    }

    /**
     * 启用状态
     *
     * -“1”：启用
     * -“2”：禁用
     */
    type EnableStatus = '1' | '2';

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
      key: keyof T
      label: string
      component: any
      props?: any
      placeholder?: string
    }

    type TimeType = 'day' | 'week' | 'month' | 'year';
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

    type StatisticalPeriod = 'day' | 'month' | 'quarter' | 'year';

    type ChartType = 'bar' | 'line';

    interface MetricData {
      id: number;                // 唯一标识符
      dataModel: number;         // 选用数据模型
      businessScope: string;     // 业务口径
      chineseName: string;       // 中文名
      englishName: string;       // 英文名
      alias: string;             // 别名
      sensitivity: string;       // 敏感度
      statisticType: StatisticType;    // 统计类型
      statisticalPeriod: StatisticalPeriod;  // 统计周期
      chartType: ChartType;       // 图表类型
      topicDomain: string;        // 主题域
      chartDisplayDate: number;   // 图表显示日期
      formatType: FormatType;         // 格式化类型
      dimensions: SelectOptions[]  // 接收到的维度
      tags: string[];
      publishStatus: Api.Common.EnableStatus | '';      // 发布状态
      displayStatus: Api.Common.EnableStatus | '';      // 显示状态
      favoritePerson: string;     // 收藏人
      createBy: string;          // 创建人
      updateTime: string;        // 更新时间
      data: Array<{
        date: string;            // 数据日期，假设使用字符串表示日期
        value: number;           // 数据值
        [key: string]: any;
      }>;
    }

    interface MetricFormFields {
      modelForm: Api.Common.FormType<MetricUpdateParams>[]
      metricForm: Api.Common.FormType<MetricUpdateParams>[]
      sensitivityForm: Api.Common.FormType<MetricUpdateParams>[]
      staticForm: Api.Common.FormType<MetricUpdateParams>[]
      chartForm: Api.Common.FormType<MetricUpdateParams>[]
      publishForm: Api.Common.FormType<MetricUpdateParams>[]
    }


    type MetricSearchParams = CommonType.RecordNullable<Pick<MetricData, "id" | 'chineseName' | "statisticalPeriod" | "sensitivity" | "favoritePerson" | "topicDomain" | "publishStatus" | "createBy" | 'displayStatus'>
      & Api.SystemManage.CommonSearchParams & {
        dateRange: [number, number]
        dimensionDrillDown: string // 发送给接口的参数
        dimensionFilter: string
        comparisonOperators: string
        conditions: string[]
        sort: Sort
      }>;

    type Sort = 'asc' | 'desc'

    type MetricList = Common.PaginatingQueryRecord<MetricData>;

    type MetricAddParams = CommonType.RecordNullable<Pick<MetricData, "dataModel" | "businessScope" | "chineseName" | "englishName" | "alias" | "sensitivity" | "statisticalPeriod" | "chartType" | "chartDisplayDate" | "publishStatus" | 'createBy'>>;

    type MetricUpdateParams = CommonType.RecordNullable<Pick<MetricData, 'id'>> & MetricAddParams;

    type SelectOptions = {
      value: string;
      label: string;
      options: SelectOptions[]
    }

    type FormatType = 'percent' | 'flow' | 'number' | 'percent' | 'currency' | 'default';
  }

  /**
 * 命名空间系统管理
 *
 * 后端 API 模块：“Tag”
 */
  namespace Tag {
    type TagData = Common.CommonRecord<{
      id: number;
      tagName: string;
      tagType: string;
      tagDesc: string;
      createBy: string;
      createTime: string;
      updateTime: string;
    }>

    type TagSearchParams = CommonType.RecordNullable<Pick<TagData, "tagName" | "tagType" | "createBy"> & Api.SystemManage.CommonSearchParams>;

    type TagList = Common.PaginatingQueryRecord<TagData>;

    type TagAddParams = CommonType.RecordNullable<Pick<TagData, "tagName" | "tagType" | "tagDesc" | "createBy">>;

    type TagUpdateParams = CommonType.RecordNullable<Pick<TagData, "id">> & TagAddParams;

    type MetricTagAddParams = {
      metricId: number;
      tagId: string;
      createBy: string;
    }

    type MetricTagDeleteParams = {
      metricId: number;
      tag: string;
    }
  }
  /**
   * 命名空间系统管理
   *
   * 后端 API 模块：“systemManage”
   */
  namespace SystemManage {
    type CommonSearchParams = Pick<Common.PaginatingCommonParams, 'current' | 'size'>;

    /** common delete params */
    type CommonDeleteParams = { id: number };

    /** common batch delete params */
    type CommonBatchDeleteParams = { ids: string[] };

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
    }>;

    /** 角色添加参数 */
    type RoleAddParams = Pick<Role, 'roleName' | 'roleCode' | 'roleDesc' | 'roleHome' | 'status'>;

    /** role update params */
    type RoleUpdateParams = CommonType.RecordNullable<Pick<Role, 'id'>> & RoleAddParams;

    /** 角色搜索参数 */
    type RoleSearchParams = CommonType.RecordNullable<
      Pick<Role, 'roleName' | 'roleCode' | 'status'> & CommonSearchParams
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
      Pick<Api, 'path' | 'method' | 'summary' | 'tags' | 'status'> & CommonSearchParams
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
      Pick<
        Log,
        'logType' | 'logUser' | 'logDetailType' | 'requestUrl' | 'createTime' | 'responseCode'
      > &
      CommonSearchParams & { timeRange: string }
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
      Pick<
        User,
        'userName' | 'password' | 'userGender' | 'nickName' | 'userPhone' | 'userEmail' | 'status'
      > &
      CommonSearchParams
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
      databaseName: string; /** 数据库名称 */
      databaseType: string; /** 数据库类型 */
      databaseHost: string; /** 数据库地址 */
      databasePort: number; /** 数据库端口 */
      databaseUser: string; /** 数据库用户名 */
      password: string; /** 数据库密码 */
      databaseDatabase: string; /** 数据库 */
      databaseDesc: string; /** 数据库描述 */
    }>;

    type DatabaseList = Common.PaginatingQueryRecord<Database>;

    /** 数据库搜索参数 */
    type DatabaseSearchParams = CommonType.RecordNullable<
      Pick<Database, 'databaseName' | 'databaseType' | 'createBy' | 'status'> & CommonSearchParams
    >;

    /** 数据库添加参数 */
    type DatabaseAddParams = CommonType.RecordNullable<Omit<Database, 'id' | 'createTime' | 'updateTime' | 'updateBy'>>;

    /** 数据库更新参数 */
    type DatabaseUpdateParams = CommonType.RecordNullable<Pick<Database, 'id'>> & DatabaseAddParams;

    /** 数据库连接测试参数 */
    type DatabaseTestParams = CommonType.RecordNullable<Pick<Database, 'id'>> & DatabaseAddParams;


    // 数据域和主题域
    type Domain = Common.CommonRecord<{
      domainName: string; /** 数据域名称 */
      domainDesc: string; /** 数据域描述 */
    }>;

    type DomainList = Common.PaginatingQueryRecord<Domain>;

    // 搜索参数
    type DomainSearchParams = CommonType.RecordNullable<Pick<Domain, 'domainName' | 'createBy'> & CommonSearchParams>;

    // 添加参数 
    type DomainAddParams = CommonType.RecordNullable<Pick<Domain, 'domainName' | 'domainDesc' | 'createBy'>>;

    // 数据域更新参数
    type DomainUpdateParams = CommonType.RecordNullable<Pick<Domain, 'id'>> & DomainAddParams;

    // 主题模型
    type DataModel = Common.CommonRecord<{
      dataModelName: string; // 模型名称
      dataModelDesc: string; // 模型描述
      database: number; // 数据库ID
      tableName: string;  // 表名
      dataDomain: number; // 数据域ID
      topicDomain: number; // 主题域ID
      fieldConf: TableColumns[]
    }>

    type DataModelList = Common.PaginatingQueryRecord<DataModel>;

    type DomainSearchList = {
      dataDomainList: number[],
      topicDomainList: number[]
    }
    /** 主题模型搜索参数 */
    type DataModelSearchParams = CommonType.RecordNullable<Pick<DataModel, 'dataModelName' | 'createBy' | 'status'> & CommonSearchParams & DomainSearchList>;

    // 主题模型添加参数，将 fieldConf 改为string类型，好对应接口发送
    type DataModelAddParams = CommonType.RecordNullable<Omit<DataModel, 'fieldConf'> & {
      fieldConf: string
    }>;

    /** 主题模型更新参数 */
    type DataModelUpdateParams = CommonType.RecordNullable<Pick<DataModel, 'id'>> & DataModelAddParams;

    // 数据预览参数
    type DataPreviewSearchParams = CommonType.RecordNullable<{
      databaseId: number;
      tableName: string;
      addOrEdit: AddOrEdit
    } & CommonSearchParams>;


    type DataPreview = Common.CommonRecord<{
      id: number;
      [key: string]: any; // 允许任意其他字段
    }>

    type DataPreviewList = Common.PaginatingQueryRecord<DataPreview>;

    type Table = Common.CommonRecord<{
      tableName: string;
      tableComment: string;
    }>

    type TableList = Common.PaginatingQueryRecord<Table>;

    type TableSearchParams = { database: number }

    // 定义数据模型的创建、修改的表单类型
    interface DataModelForm {
      currentStep: number;
      stepOne: Pick<CommonType.RecordNullable<DataModel>, 'database' | 'tableName'>
      stepTwo: Pick<CommonType.RecordNullable<DataModel>, 'fieldConf'>
      stepThree: Pick<CommonType.RecordNullable<DataModel>, 'dataModelName' | 'dataModelDesc' | 'dataDomain' | 'topicDomain' | 'status'>
    }

    // 定义获取数据字段信息的类型
    interface TableColumnsSearchParams {
      database: number;
      tableName: string;
      addOrEdit: AddOrEdit
    }

    type AddOrEdit = 'add' | 'edit'

    interface TableColumns {
      columnName: string;
      columnType: string;
      columnComment: string;
      semanticType: string | null;
      format: string | null;
      staticType: string | null;
      extendedComputation: string | null;
    }

    type TableColumnsList = Common.PaginatingQueryRecord<TableColumns>;


  }
}
