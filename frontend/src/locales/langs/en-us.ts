const local: App.I18n.Schema = {
  system: {
    title: 'MetricBoost',
    updateTitle: 'System Version Update Notification',
    updateContent: 'A new version of the system has been detected. Do you want to refresh the page immediately?',
    updateConfirm: 'Refresh immediately',
    updateCancel: 'Later'
  },
  common: {
    action: 'Action',
    add: 'Add',
    addSuccess: 'Add Success',
    backToHome: 'Back to home',
    batchDelete: 'Batch Delete',
    test: 'Test Link',
    testSuccess: 'Test Link Success',
    cancel: 'Cancel',
    close: 'Close',
    check: 'Check',
    createBy: 'Creator',
    createTime: 'Create Time',
    expandColumn: 'Expand Column',
    columnSetting: 'Column Setting',
    config: 'Config',
    confirm: 'Confirm',
    delete: 'Delete',
    deleteSuccess: 'Delete Success',
    confirmDelete: 'Are you sure you want to delete?',
    edit: 'Edit',
    view: 'View',
    warning: 'Warning',
    error: 'Error',
    index: 'Index',
    keywordSearch: 'Please enter keyword',
    logout: 'Logout',
    logoutConfirm: 'Are you sure you want to log out?',
    lookForward: 'Coming soon',
    modify: 'Modify',
    modifySuccess: 'Modify Success',
    noData: 'No Data',
    operate: 'Operate',
    pleaseCheckValue: 'Please check whether the value is valid',
    refresh: 'Refresh',
    refreshAPI: 'Refresh API',
    reset: 'Reset',
    search: 'Search',
    switch: 'Switch',
    tip: 'Tip',
    trigger: 'Trigger',
    update: 'Update',
    updateSuccess: 'Update Success',
    userCenter: 'User Center',
    yesOrNo: {
      yes: 'Yes',
      no: 'No'
    }
  },
  request: {
    logout: 'Logout user after request failed',
    logoutMsg: 'User status is invalid, please log in again',
    logoutWithModal: 'Pop up modal after request failed and then log out user',
    logoutWithModalMsg: 'User status is invalid, please log in again',
    refreshToken: 'The requested token has expired, refresh the token',
    tokenExpired: 'The requested token has expired'
  },
  theme: {
    themeSchema: {
      title: 'Theme Schema',
      light: 'Light',
      dark: 'Dark',
      auto: 'Follow System'
    },
    grayscale: 'Grayscale',
    colourWeakness: 'Colour Weakness',
    layoutMode: {
      title: 'Layout Mode',
      vertical: 'Vertical Menu Mode',
      horizontal: 'Horizontal Menu Mode',
      'vertical-mix': 'Vertical Mix Menu Mode',
      'horizontal-mix': 'Horizontal Mix menu Mode',
      reverseHorizontalMix: 'Reverse first level menus and child level menus position'
    },
    recommendColor: 'Apply Recommended Color Algorithm',
    recommendColorDesc: 'The recommended color algorithm refers to',
    themeColor: {
      title: 'Theme Color',
      primary: 'Primary',
      info: 'Info',
      success: 'Success',
      warning: 'Warning',
      error: 'Error',
      followPrimary: 'Follow Primary'
    },
    scrollMode: {
      title: 'Scroll Mode',
      wrapper: 'Wrapper',
      content: 'Content'
    },
    page: {
      animate: 'Page Animate',
      mode: {
        title: 'Page Animate Mode',
        fade: 'Fade',
        'fade-slide': 'Slide',
        'fade-bottom': 'Fade Zoom',
        'fade-scale': 'Fade Scale',
        'zoom-fade': 'Zoom Fade',
        'zoom-out': 'Zoom Out',
        none: 'None'
      }
    },
    fixedHeaderAndTab: 'Fixed Header And Tab',
    header: {
      height: 'Header Height',
      breadcrumb: {
        visible: 'Breadcrumb Visible',
        showIcon: 'Breadcrumb Icon Visible'
      }
    },
    tab: {
      visible: 'Tab Visible',
      cache: 'Tag Bar Info Cache',
      height: 'Tab Height',
      mode: {
        title: 'Tab Mode',
        chrome: 'Chrome',
        button: 'Button'
      }
    },
    sider: {
      inverted: 'Dark Sider',
      width: 'Sider Width',
      collapsedWidth: 'Sider Collapsed Width',
      mixWidth: 'Mix Sider Width',
      mixCollapsedWidth: 'Mix Sider Collapse Width',
      mixChildMenuWidth: 'Mix Child Menu Width'
    },
    footer: {
      visible: 'Footer Visible',
      fixed: 'Fixed Footer',
      height: 'Footer Height',
      right: 'Right Footer'
    },
    watermark: {
      visible: 'Watermark Full Screen Visible',
      text: 'Watermark Text'
    },
    themeDrawerTitle: 'Theme Configuration',
    pageFunTitle: 'Page Function',
    configOperation: {
      copyConfig: 'Copy Config',
      copySuccessMsg: 'Copy Success, Please replace the variable "themeSettings" in "src/theme/settings.ts"',
      resetConfig: 'Reset Config',
      resetSuccessMsg: 'Reset Success'
    }
  },
  route: {
    login: 'Login',
    403: 'No Permission',
    404: 'Page Not Found',
    500: 'Server Error',
    'iframe-page': 'Iframe',
    home: 'Home',
    metric: 'Metric',
    'metric-exploration': 'MetricExploration',
    dashboard: 'Dashboard',
    decision: 'Decision',
    report: 'Report',
    collect: 'Collect',
    document: 'Document',
    document_project: 'Project Document',
    'document_project-link': 'Project Document(External Link)',
    document_vue: 'Vue Document',
    document_vite: 'Vite Document',
    document_unocss: 'UnoCSS Document',
    document_naive: 'Naive UI Document',
    document_antd: 'Ant Design Vue Document',
    document_alova: 'Alova Document',
    'user-center': 'User Center',
    about: 'About',
    function: 'System Function',
    alova: 'Alova Example',
    alova_request: 'Alova Request',
    alova_user: 'User List',
    alova_scenes: 'Scenario Request',
    function_tab: 'Tab',
    'function_multi-tab': 'Multi Tab',
    'function_hide-child': 'Hide Child',
    'function_hide-child_one': 'Hide Child',
    'function_hide-child_two': 'Two',
    'function_hide-child_three': 'Three',
    function_request: 'Request',
    'function_toggle-auth': 'Toggle Auth',
    'function_super-page': 'Super Admin Visible',
    asset: 'Asset',
    asset_database: 'Database',
    asset_model: 'Data Model',
    asset_tag: 'Tag',
    service: 'Data Service',
    service_overview: 'Overview',
    'service_api-manange': 'API Manage',
    service_application: 'Application',
    manage: 'System',
    manage_log: 'Log Manage',
    manage_user: 'User Manage',
    manage_api: 'Api Manage',
    'manage_user-detail': 'User Detail',
    manage_role: 'Role Manage',
    manage_menu: 'Menu Manage',
    'manage_notification-settings': 'Notificat Settings',
    'manage_notification-tpls': 'Notificat Template',
    exception: 'Exception',
    exception_403: '403',
    exception_404: '404',
    exception_500: '500',
    plugin: 'Plugin',
    plugin_copy: 'Copy',
    plugin_charts: 'Charts',
    plugin_charts_echarts: 'ECharts',
    plugin_charts_antv: 'AntV',
    plugin_editor: 'Editor',
    plugin_editor_quill: 'Quill',
    plugin_editor_markdown: 'Markdown',
    plugin_icon: 'Icon',
    plugin_map: 'Map',
    plugin_print: 'Print',
    plugin_swiper: 'Swiper',
    plugin_video: 'Video',
    plugin_barcode: 'Barcode',
    plugin_pinyin: 'pinyin',
    plugin_excel: 'Excel',
    plugin_pdf: 'PDF preview',
    plugin_gantt: 'Gantt Chart',
    plugin_typeit: 'Typeit'
  },
  page: {
    login: {
      common: {
        loginOrRegister: 'Login / Register',
        userNamePlaceholder: 'Please enter user name',
        phonePlaceholder: 'Please enter phone number',
        codePlaceholder: 'Please enter verification code',
        passwordPlaceholder: 'Please enter password',
        confirmPasswordPlaceholder: 'Please enter password again',
        codeLogin: 'Verification code login',
        confirm: 'Confirm',
        back: 'Back',
        validateSuccess: 'Verification passed',
        loginSuccess: 'Login successfully',
        welcomeBack: 'Welcome back, {userName} !'
      },
      pwdLogin: {
        title: 'Password Login',
        rememberMe: 'Remember me',
        forgetPassword: 'Forget password?',
        register: 'Register',
        otherAccountLogin: 'Other Account Login',
        otherLoginMode: 'Other Login Mode',
        superAdmin: 'Super Admin',
        admin: 'Admin',
        user: 'User'
      },
      codeLogin: {
        title: 'Verification Code Login',
        getCode: 'Get verification code',
        reGetCode: 'Reacquire after {time}s',
        sendCodeSuccess: 'Verification code sent successfully',
        imageCodePlaceholder: 'Please enter image verification code'
      },
      register: {
        title: 'Register',
        agreement: 'I have read and agree to',
        protocol: '《User Agreement》',
        policy: '《Privacy Policy》'
      },
      resetPwd: {
        title: 'Reset Password'
      },
      bindWeChat: {
        title: 'Bind WeChat'
      }
    },
    about: {
      title: 'About',
      introduction: `SoybeanAdmin is an elegant and powerful admin template, based on the latest front-end technology stack, including Vue3, Vite5, TypeScript, Pinia and UnoCSS. It has built-in rich theme configuration and components, strict code specifications, and an automated file routing system. In addition, it also uses the online mock data solution based on ApiFox. SoybeanAdmin provides you with a one-stop admin solution, no additional configuration, and out of the box. It is also a best practice for learning cutting-edge technologies quickly.`,
      projectInfo: {
        title: 'Project Info',
        version: 'Version',
        latestBuildTime: 'Latest Build Time',
        githubLink: 'Github Link',
        previewLink: 'Preview Link'
      },
      prdDep: 'Production Dependency',
      devDep: 'Development Dependency'
    },
    home: {
      branchDesc:
        'For the convenience of everyone in developing and updating the merge, we have streamlined the code of the main branch, only retaining the homepage menu, and the rest of the content has been moved to the example branch for maintenance. The preview address displays the content of the example branch.',
      greeting: 'Good morning, {userName}, today is another day full of vitality!',
      weatherDesc: 'Today is cloudy to clear, 20℃ - 25℃!',
      projectCount: 'Project Count',
      todo: 'Todo',
      message: 'Message',
      downloadCount: 'Download Count',
      registerCount: 'Register Count',
      schedule: 'Work and rest Schedule',
      study: 'Study',
      work: 'Work',
      rest: 'Rest',
      entertainment: 'Entertainment',
      visitCount: 'Visit Count',
      turnover: 'Turnover',
      dealCount: 'Deal Count',
      projectNews: {
        title: 'Project News',
        moreNews: 'More News',
        desc1: 'Soybean created the open source project soybean-admin on May 28, 2021!',
        desc2: 'Yanbowe submitted a bug to soybean-admin, the multi-tab bar will not adapt.',
        desc3: 'Soybean is ready to do sufficient preparation for the release of soybean-admin!',
        desc4: 'Soybean is busy writing project documentation for soybean-admin!',
        desc5: 'Soybean just wrote some of the workbench pages casually, and it was enough to see!'
      },
      creativity: 'Creativity'
    },
    function: {
      tab: {
        tabOperate: {
          title: 'Tab Operation',
          addTab: 'Add Tab',
          addTabDesc: 'To about page',
          closeTab: 'Close Tab',
          closeCurrentTab: 'Close Current Tab',
          closeAboutTab: 'Close "About" Tab',
          addMultiTab: 'Add Multi Tab',
          addMultiTabDesc1: 'To MultiTab page',
          addMultiTabDesc2: 'To MultiTab page(with query params)'
        },
        tabTitle: {
          title: 'Tab Title',
          changeTitle: 'Change Title',
          change: 'Change',
          resetTitle: 'Reset Title',
          reset: 'Reset'
        }
      },
      multiTab: {
        routeParam: 'Route Param',
        backTab: 'Back function_tab'
      },
      toggleAuth: {
        toggleAccount: 'Toggle Account',
        authHook: 'Auth Hook Function `hasAuth`',
        superAdminVisible: 'Super Admin Visible',
        adminVisible: 'Admin Visible',
        adminOrUserVisible: 'Admin and User Visible'
      },
      request: {
        repeatedErrorOccurOnce: 'Repeated Request Error Occurs Once',
        repeatedError: 'Repeated Request Error',
        repeatedErrorMsg1: 'Custom Request Error 1',
        repeatedErrorMsg2: 'Custom Request Error 2'
      }
    },
    alova: {
      scenes: {
        captchaSend: 'Captcha Send',
        autoRequest: 'Auto Request',
        visibilityRequestTips: 'Automatically request when switching browser window',
        pollingRequestTips: 'It will request every 3 seconds',
        networkRequestTips: 'Automatically request after network reconnecting',
        refreshTime: 'Refresh Time',
        startRequest: 'Start Request',
        stopRequest: 'Stop Request',
        requestCrossComponent: 'Request Cross Component',
        triggerAllRequest: 'Manually Trigger All Automated Requests'
      }
    },
    metric: {
      metricPlaceholder: 'Metric Name or Description Search',
      domain: 'Domain',
      tag: 'Tag',
      sensitivity: 'Sensitivity',
      order: 'Order',
      formTile: {
        modelForm: 'Model Config',
        metricForm: 'Metric Config',
        sensitivityForm: 'Sensitivity Config',
        staticForm: 'Staticical Config',
        chartForm: 'Chart Config'
      }
    },
    dataAsset: {
      database: {
        title: 'Database List',
        name: 'Name',
        type: 'Type',
        host: 'Host',
        port: 'Port',
        database: 'Database',
        username: 'Username',
        password: 'Password',
        createBy: 'Creator',
        status: 'Status',
        description: 'Description',
        addDatabase: 'Add Database',
        editDatabase: 'Edit Database',
        form: {
          name: 'Please enter name',
          type: 'Please select type',
          host: 'Please enter host',
          port: 'Please enter port',
          database: 'Please enter database',
          status: 'Please select status',
          username: 'Please enter username',
          password: 'Please enter password',
          description: 'Please enter description',
          createBy: 'Please select creator'
        }
      },
      dataModel: {
        title: 'Data Model List',
        name: 'Model Name',
        description: 'Model Description',
        dataDomain: 'Data Domain',
        topicDomain: 'Topic Domain',
        status: 'Status',
        filter: 'Data Domain/Topic Domain',
        dataPreview: 'Data Preview',
        addDataModel: 'Add Data Model',
        editDataModel: 'Edit Data Model',
        databaseSelect: 'Database',
        tableName: 'TableName',
        form: {
          name: 'Please enter model name',
          description: 'Please enter model description',
          dataDomain: 'Please select data domain',
          topicDomain: 'Please select topic domain',
          status: 'Please select status',
          databaseSelect: 'Please select database',
          tableName: 'Please enter table name',
          createBy: 'Please select creator'
        }
      },
      tag: {
        title: 'Tag Manger',
        tagName: 'Name',
        tagType: 'Type',
        tagDesc: 'Description',
        form: {
          tagName: 'Please Input Tag Name',
          tagType: 'Please Select Tag Type',
          tagDesc: 'Please Input Tag Description'
        }
      }
    },
    collect: {
      title: 'Data Collection',
      name: 'Name',
      type: 'Type',
      schedule: 'Schedule',
      status: 'Status',
      originDatabase: 'Source Database',
      originTable: 'Source Table',
      targetDatabase: 'Target Database',
      targetTable: 'Target Table',
      formTile: {
        baseInfo: 'Base Info',
        collectForm: 'Collect Config',
        status: 'Status'
      },
      form: {
        name: 'Please enter the name',
        type: 'Please select the type',
        schedule: 'Please select the cron',
        status: 'Please select the status',
        originDatabase: 'Please select the source database',
        originTable: 'Please select the source table',
        targetDatabase: 'Please select the target database',
        targetTable: 'Please select the target table'
      }
    },
    manage: {
      common: {
        status: {
          enable: 'Enable',
          disable: 'Disable'
        }
      },
      role: {
        title: 'Role List',
        roleName: 'Role Name',
        roleCode: 'Role Code',
        domains: 'Domains',
        sensitivity: 'Sensitivity',
        roleStatus: 'Role Status',
        roleDesc: 'Role Description',
        menuAuth: 'Menu Auth',
        buttonAuth: 'Button Auth',
        apiAuth: 'API Auth',
        domainAuth: 'Domain Auth',
        sensitiveAuth: 'Sensitivity Auth',
        form: {
          roleName: 'Please enter role name',
          roleCode: 'Please enter role code',
          domains: 'Please select domains',
          sensitivity: 'Please select sensitivity',
          roleStatus: 'Please select role status',
          roleDesc: 'Please enter role description'
        },
        addRole: 'Add Role',
        editRole: 'Edit Role'
      },

      log: {
        title: 'Log List',
        logType: 'Log type',
        logUser: 'Log user',
        logDetailType: 'Log deatil',
        requestUrl: 'Request url',
        createTime: 'Create time',
        responseCode: 'Response code',
        form: {
          logType: 'Please select Log type',
          logUser: 'Please enter Log user',
          logDetailType: 'Please select Log deatil',
          requestUrl: 'Please enter Request url',
          createTime: 'Please select Create time',
          responseCode: 'Please enter Response code'
        },
        viewLog: 'View Log',
        logDetailTypes: {
          SystemStart: 'System start',
          SystemStop: 'System stop',
          UserLoginSuccess: 'User login success',
          UserAuthRefreshTokenSuccess: 'User authentication refresh token success',
          UserLoginGetUserInfo: 'User login get user info',
          UserLoginUserNameVaild: 'User login username valid',
          UserLoginErrorPassword: 'User login error password',
          UserLoginForbid: 'User login forbidden',
          ApiGetList: 'API get list',
          ApiGetTree: 'API get tree',
          ApiRefresh: 'API refresh',
          ApiGetOne: 'API get one',
          ApiCreateOne: 'API create one',
          ApiUpdateOne: 'API update one',
          ApiDeleteOne: 'API delete one',
          ApiBatchDelete: 'API batch delete',
          MenuGetList: 'Menu get list',
          MenuGetTree: 'Menu get tree',
          MenuGetPages: 'Menu get pages',
          MenuGetButtonsTree: 'Menu get buttons tree',
          MenuGetOne: 'Menu get one',
          MenuCreateOne: 'Menu create one',
          MenuUpdateOne: 'Menu update one',
          MenuDeleteOne: 'Menu delete one',
          MenuBatchDeleteOne: 'Menu batch delete',
          RoleGetList: 'Role get list',
          RoleGetMenus: 'Role get menus',
          RoleUpdateMenus: 'Role update menus',
          RoleGetButtons: 'Role get buttons',
          RoleUpdateButtons: 'Role update buttons',
          RoleGetApis: 'Role get APIs',
          RoleUpdateApis: 'Role update APIs',
          RoleGetOne: 'Role get one',
          RoleCreateOne: 'Role create one',
          RoleUpdateOne: 'Role update one',
          RoleDeleteOne: 'Role delete one',
          RoleBatchDeleteOne: 'Role batch delete',
          UserGetList: 'User get list',
          UserGetOne: 'User get one',
          UserCreateOne: 'User create one',
          UserUpdateOne: 'User update one',
          UserDeleteOne: 'User delete one',
          UserBatchDeleteOne: 'User batch delete'
        },
        logTypes: {
          ApiLog: 'Api log',
          UserLog: 'User log',
          AdminLog: 'Admin log',
          SystemLog: 'System log'
        }
      },
      api: {
        title: 'API List',
        path: 'Path',
        method: 'Method',
        summary: 'Summary',
        tags: 'Tags',
        status: 'Status',
        form: {
          path: 'Please enter path',
          method: 'Please select method',
          summary: 'Please enter summary',
          tags: 'Please enter tags',
          status: 'Please select user status'
        },
        addApi: 'Add API',
        editApi: 'Edit API',
        methods: {
          GET: 'GET',
          POST: 'POST',
          PUT: 'PUT',
          PATCH: 'PATCH',
          DELETE: 'DELETE'
        }
      },
      user: {
        title: 'User List',
        userName: 'User Name',
        password: 'Password',
        userGender: 'Gender',
        nickName: 'Nick Name',
        userPhone: 'Phone Number',
        userEmail: 'Email',
        userStatus: 'User Status',
        userRole: 'User Role',
        form: {
          userName: 'Please enter user name',
          password: 'Please enter password',
          userGender: 'Please select gender',
          nickName: 'Please enter nick name',
          userPhone: 'Please enter phone number',
          userEmail: 'Please enter email',
          userStatus: 'Please select user status',
          userRole: 'Please select user role'
        },
        addUser: 'Add User',
        editUser: 'Edit User',
        gender: {
          male: 'Male',
          female: 'Female',
          unknow: 'Unknow'
        }
      },
      menu: {
        home: 'Home',
        title: 'Menu List',
        id: 'ID',
        parentId: 'Parent ID',
        menuType: 'Menu Type',
        menuName: 'Menu Name',
        routeName: 'Route Name',
        routePath: 'Route Path',
        pathParam: 'Path Param',
        layout: 'Layout Component',
        page: 'Page Component',
        i18nKey: 'I18n Key',
        icon: 'Icon',
        localIcon: 'Local Icon',
        iconTypeTitle: 'Icon Type',
        order: 'Order',
        constant: 'Constant',
        keepAlive: 'Keep Alive',
        href: 'Href',
        hideInMenu: 'Hide In Menu',
        activeMenu: 'Active Menu',
        multiTab: 'Multi Tab',
        fixedIndexInTab: 'Fixed Index In Tab',
        query: 'Query Params',
        button: 'Button',
        buttonCode: 'Button Code',
        buttonDesc: 'Button Desc',
        menuStatus: 'Menu Status',
        form: {
          home: 'Please select home',
          menuType: 'Please select menu type',
          menuName: 'Please enter menu name',
          routeName: 'Please enter route name',
          routePath: 'Please enter route path',
          pathParam: 'Please enter path param',
          page: 'Please select page component',
          layout: 'Please select layout component',
          i18nKey: 'Please enter i18n key',
          icon: 'Please enter iconify name',
          localIcon: 'Please enter local icon name',
          order: 'Please enter order',
          keepAlive: 'Please select whether to cache route',
          href: 'Please enter href',
          hideInMenu: 'Please select whether to hide menu',
          activeMenu: 'Please select route name of the highlighted menu',
          multiTab: 'Please select whether to support multiple tabs',
          fixedInTab: 'Please select whether to fix in the tab',
          fixedIndexInTab: 'Please enter the index fixed in the tab',
          queryKey: 'Please enter route parameter Key',
          queryValue: 'Please enter route parameter Value',
          button: 'Please select whether it is a button',
          buttonCode: 'Please enter button code',
          buttonDesc: 'Please enter button description',
          menuStatus: 'Please select menu status'
        },
        addMenu: 'Add Menu',
        editMenu: 'Edit Menu',
        addChildMenu: 'Add Child Menu',
        type: {
          directory: 'Directory',
          menu: 'Menu'
        },
        iconType: {
          iconify: 'Iconify Icon',
          local: 'Local Icon'
        }
      }
    }
  },
  form: {
    required: 'Cannot be empty',
    userName: {
      required: 'Please enter user name',
      invalid: 'User name format is incorrect'
    },
    phone: {
      required: 'Please enter phone number',
      invalid: 'Phone number format is incorrect'
    },
    pwd: {
      required: 'Please enter password',
      invalid: '6-18 characters, including letters, numbers, and underscores'
    },
    confirmPwd: {
      required: 'Please enter password again',
      invalid: 'The two passwords are inconsistent'
    },
    code: {
      required: 'Please enter verification code',
      invalid: 'Verification code format is incorrect'
    },
    email: {
      required: 'Please enter email',
      invalid: 'Email format is incorrect'
    }
  },
  dropdown: {
    closeCurrent: 'Close Current',
    closeOther: 'Close Other',
    closeLeft: 'Close Left',
    closeRight: 'Close Right',
    closeAll: 'Close All'
  },
  icon: {
    themeConfig: 'Theme Configuration',
    themeSchema: 'Theme Schema',
    lang: 'Switch Language',
    fullscreen: 'Fullscreen',
    fullscreenExit: 'Exit Fullscreen',
    reload: 'Reload Page',
    collapse: 'Collapse Menu',
    expand: 'Expand Menu',
    pin: 'Pin',
    unpin: 'Unpin'
  },
  datatable: {
    itemCount: 'Total {total} items'
  }
};

export default local;
