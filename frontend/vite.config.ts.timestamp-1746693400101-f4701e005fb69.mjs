// vite.config.ts
import process3 from "node:process";
import { URL, fileURLToPath } from "node:url";
import { defineConfig, loadEnv } from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser@5.36.0/node_modules/vite/dist/node/index.js";

// build/plugins/index.ts
import vue from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/@vitejs+plugin-vue@5.1.4_vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser@5.36.0__vue@3.5.11_typescript@5.6.3_/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import vueJsx from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/@vitejs+plugin-vue-jsx@4.0.1_vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser@5.36.0__vue@3.5.11_typescript@5.6.3_/node_modules/@vitejs/plugin-vue-jsx/dist/index.mjs";
import VueDevtools from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/vite-plugin-vue-devtools@7.4.6_rollup@4.24.0_vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser_zxgriitykwt7yeiuppc6jge464/node_modules/vite-plugin-vue-devtools/dist/vite.mjs";
import progress from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/vite-plugin-progress@0.0.7_vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser@5.36.0_/node_modules/vite-plugin-progress/dist/index.mjs";

// build/plugins/router.ts
import ElegantVueRouter from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/@elegant-router+vue@0.3.8/node_modules/@elegant-router/vue/dist/vite.mjs";
function setupElegantRouter() {
  return ElegantVueRouter({
    layouts: {
      base: "src/layouts/base-layout/index.vue",
      blank: "src/layouts/blank-layout/index.vue"
    },
    customRoutes: {
      names: [
        "exception_403",
        "exception_404",
        "exception_500",
        "document_project",
        "document_project-link",
        "document_vue",
        "document_vite",
        "document_unocss",
        "document_naive",
        "document_antd",
        "document_alova"
      ]
    },
    routePathTransformer(routeName, routePath) {
      const key = routeName;
      if (key === "login") {
        const modules = ["pwd-login", "code-login", "register", "reset-pwd", "bind-wechat"];
        const moduleReg = modules.join("|");
        return `/login/:module(${moduleReg})?`;
      }
      return routePath;
    },
    onRouteMetaGen(routeName) {
      const key = routeName;
      const constantRoutes = ["login", "403", "404", "500"];
      const meta = {
        title: key,
        i18nKey: `route.${key}`
      };
      if (constantRoutes.includes(key)) {
        meta.constant = true;
      }
      return meta;
    }
  });
}

// build/plugins/unocss.ts
import process from "node:process";
import path from "node:path";
import unocss from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/@unocss+vite@0.63.4_rollup@4.24.0_vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser@5.36.0_/node_modules/@unocss/vite/dist/index.mjs";
import presetIcons from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/@unocss+preset-icons@0.63.4/node_modules/@unocss/preset-icons/dist/index.mjs";
import { FileSystemIconLoader } from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/@iconify+utils@2.1.33/node_modules/@iconify/utils/lib/loader/node-loaders.mjs";
function setupUnocss(viteEnv) {
  const { VITE_ICON_PREFIX, VITE_ICON_LOCAL_PREFIX } = viteEnv;
  const localIconPath = path.join(process.cwd(), "src/assets/svg-icon");
  const collectionName = VITE_ICON_LOCAL_PREFIX.replace(`${VITE_ICON_PREFIX}-`, "");
  return unocss({
    presets: [
      presetIcons({
        prefix: `${VITE_ICON_PREFIX}-`,
        scale: 1,
        extraProperties: {
          display: "inline-block"
        },
        collections: {
          [collectionName]: FileSystemIconLoader(
            localIconPath,
            (svg) => svg.replace(/^<svg\s/, '<svg width="1em" height="1em" ')
          )
        },
        warn: true
      })
    ]
  });
}

// build/plugins/unplugin.ts
import process2 from "node:process";
import path2 from "node:path";
import Icons from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/unplugin-icons@0.19.3_@vue+compiler-sfc@3.5.11_webpack-sources@3.2.3/node_modules/unplugin-icons/dist/vite.js";
import IconsResolver from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/unplugin-icons@0.19.3_@vue+compiler-sfc@3.5.11_webpack-sources@3.2.3/node_modules/unplugin-icons/dist/resolver.js";
import Components from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/unplugin-vue-components@0.27.4_@babel+parser@7.25.7_rollup@4.24.0_vue@3.5.11_typescript@5.6.3__webpack-sources@3.2.3/node_modules/unplugin-vue-components/dist/vite.js";
import { AntDesignVueResolver, NaiveUiResolver } from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/unplugin-vue-components@0.27.4_@babel+parser@7.25.7_rollup@4.24.0_vue@3.5.11_typescript@5.6.3__webpack-sources@3.2.3/node_modules/unplugin-vue-components/dist/resolvers.js";
import { FileSystemIconLoader as FileSystemIconLoader2 } from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/unplugin-icons@0.19.3_@vue+compiler-sfc@3.5.11_webpack-sources@3.2.3/node_modules/unplugin-icons/dist/loaders.js";
import { createSvgIconsPlugin } from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/vite-plugin-svg-icons@2.0.1_vite@5.4.8_@types+node@22.7.5_sass@1.79.4_terser@5.36.0_/node_modules/vite-plugin-svg-icons/dist/index.mjs";
function setupUnplugin(viteEnv) {
  const { VITE_ICON_PREFIX, VITE_ICON_LOCAL_PREFIX } = viteEnv;
  const localIconPath = path2.join(process2.cwd(), "src/assets/svg-icon");
  const collectionName = VITE_ICON_LOCAL_PREFIX.replace(`${VITE_ICON_PREFIX}-`, "");
  const plugins = [
    Icons({
      compiler: "vue3",
      customCollections: {
        [collectionName]: FileSystemIconLoader2(
          localIconPath,
          (svg) => svg.replace(/^<svg\s/, '<svg width="1em" height="1em" ')
        )
      },
      scale: 1,
      defaultClass: "inline-block"
    }),
    Components({
      dts: "src/typings/components.d.ts",
      types: [{ from: "vue-router", names: ["RouterLink", "RouterView"] }],
      resolvers: [
        AntDesignVueResolver({
          importStyle: false
        }),
        NaiveUiResolver(),
        IconsResolver({ customCollections: [collectionName], componentPrefix: VITE_ICON_PREFIX })
      ]
    }),
    createSvgIconsPlugin({
      iconDirs: [localIconPath],
      symbolId: `${VITE_ICON_LOCAL_PREFIX}-[dir]-[name]`,
      inject: "body-last",
      customDomId: "__SVG_ICON_LOCAL__"
    })
  ];
  return plugins;
}

// build/plugins/html.ts
function setupHtmlPlugin(buildTime) {
  const plugin = {
    name: "html-plugin",
    apply: "build",
    transformIndexHtml(html) {
      return html.replace("<head>", `<head>
    <meta name="buildTime" content="${buildTime}">`);
    }
  };
  return plugin;
}

// build/plugins/index.ts
function setupVitePlugins(viteEnv, buildTime) {
  const plugins = [
    vue(),
    vueJsx(),
    VueDevtools(),
    setupElegantRouter(),
    setupUnocss(viteEnv),
    ...setupUnplugin(viteEnv),
    progress(),
    setupHtmlPlugin(buildTime)
  ];
  return plugins;
}

// src/utils/service.ts
import json5 from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/json5@2.2.3/node_modules/json5/lib/index.js";
function createServiceConfig(env) {
  const { VITE_SERVICE_BASE_URL, VITE_OTHER_SERVICE_BASE_URL } = env;
  let other = {};
  try {
    other = json5.parse(VITE_OTHER_SERVICE_BASE_URL);
  } catch {
    console.error("VITE_OTHER_SERVICE_BASE_URL is not a valid json5 string");
  }
  const httpConfig = {
    baseURL: VITE_SERVICE_BASE_URL,
    other
  };
  const otherHttpKeys = Object.keys(httpConfig.other);
  const otherConfig = otherHttpKeys.map((key) => {
    return {
      key,
      baseURL: httpConfig.other[key],
      proxyPattern: createProxyPattern(key)
    };
  });
  const config = {
    baseURL: httpConfig.baseURL,
    proxyPattern: createProxyPattern(),
    other: otherConfig
  };
  return config;
}
function createProxyPattern(key) {
  if (!key) {
    return "/proxy-default";
  }
  return `/proxy-${key}`;
}

// build/config/proxy.ts
function createViteProxy(env, enable) {
  const isEnableHttpProxy = enable && env.VITE_HTTP_PROXY === "Y";
  if (!isEnableHttpProxy) return void 0;
  const { baseURL, proxyPattern, other } = createServiceConfig(env);
  const proxy = createProxyItem({ baseURL, proxyPattern });
  other.forEach((item) => {
    Object.assign(proxy, createProxyItem(item));
  });
  return proxy;
}
function createProxyItem(item) {
  const proxy = {};
  proxy[item.proxyPattern] = {
    target: item.baseURL,
    changeOrigin: true,
    rewrite: (path3) => path3.replace(new RegExp(`^${item.proxyPattern}`), "")
  };
  return proxy;
}

// build/config/time.ts
import dayjs from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/dayjs@1.11.13/node_modules/dayjs/dayjs.min.js";
import utc from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/dayjs@1.11.13/node_modules/dayjs/plugin/utc.js";
import timezone from "file:///C:/Users/Administrator/code/MetricBoost/frontend/node_modules/.pnpm/dayjs@1.11.13/node_modules/dayjs/plugin/timezone.js";
function getBuildTime() {
  dayjs.extend(utc);
  dayjs.extend(timezone);
  const buildTime = dayjs.tz(Date.now(), "Asia/Shanghai").format("YYYY-MM-DD HH:mm:ss");
  return buildTime;
}

// vite.config.ts
var __vite_injected_original_import_meta_url = "file:///C:/Users/Administrator/code/MetricBoost/frontend/vite.config.ts";
var vite_config_default = defineConfig((configEnv) => {
  const viteEnv = loadEnv(configEnv.mode, process3.cwd());
  const buildTime = getBuildTime();
  const enableProxy = configEnv.command === "serve" && !configEnv.isPreview;
  return {
    base: viteEnv.VITE_BASE_URL,
    resolve: {
      alias: {
        "~": fileURLToPath(new URL("./", __vite_injected_original_import_meta_url)),
        "@": fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url))
      }
    },
    css: {
      preprocessorOptions: {
        scss: {
          api: "modern-compiler",
          additionalData: `@use "@/styles/scss/global.scss" as *;`
        }
      }
    },
    plugins: setupVitePlugins(viteEnv, buildTime),
    define: {
      BUILD_TIME: JSON.stringify(buildTime)
    },
    server: {
      host: "0.0.0.0",
      port: 9527,
      open: true,
      proxy: createViteProxy(viteEnv, enableProxy),
      fs: {
        cachedChecks: false
      }
    },
    preview: {
      port: 9725
    },
    build: {
      reportCompressedSize: false,
      sourcemap: viteEnv.VITE_SOURCE_MAP === "Y",
      commonjsOptions: {
        ignoreTryCatch: false
      }
    }
  };
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiLCAiYnVpbGQvcGx1Z2lucy9pbmRleC50cyIsICJidWlsZC9wbHVnaW5zL3JvdXRlci50cyIsICJidWlsZC9wbHVnaW5zL3Vub2Nzcy50cyIsICJidWlsZC9wbHVnaW5zL3VucGx1Z2luLnRzIiwgImJ1aWxkL3BsdWdpbnMvaHRtbC50cyIsICJzcmMvdXRpbHMvc2VydmljZS50cyIsICJidWlsZC9jb25maWcvcHJveHkudHMiLCAiYnVpbGQvY29uZmlnL3RpbWUudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBZG1pbmlzdHJhdG9yXFxcXGNvZGVcXFxcTWV0cmljQm9vc3RcXFxcZnJvbnRlbmRcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXEFkbWluaXN0cmF0b3JcXFxcY29kZVxcXFxNZXRyaWNCb29zdFxcXFxmcm9udGVuZFxcXFx2aXRlLmNvbmZpZy50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vQzovVXNlcnMvQWRtaW5pc3RyYXRvci9jb2RlL01ldHJpY0Jvb3N0L2Zyb250ZW5kL3ZpdGUuY29uZmlnLnRzXCI7aW1wb3J0IHByb2Nlc3MgZnJvbSAnbm9kZTpwcm9jZXNzJztcbmltcG9ydCB7IFVSTCwgZmlsZVVSTFRvUGF0aCB9IGZyb20gJ25vZGU6dXJsJztcbmltcG9ydCB7IGRlZmluZUNvbmZpZywgbG9hZEVudiB9IGZyb20gJ3ZpdGUnO1xuaW1wb3J0IHsgc2V0dXBWaXRlUGx1Z2lucyB9IGZyb20gJy4vYnVpbGQvcGx1Z2lucyc7XG5pbXBvcnQgeyBjcmVhdGVWaXRlUHJveHksIGdldEJ1aWxkVGltZSB9IGZyb20gJy4vYnVpbGQvY29uZmlnJztcblxuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKGNvbmZpZ0VudiA9PiB7XG4gIGNvbnN0IHZpdGVFbnYgPSBsb2FkRW52KGNvbmZpZ0Vudi5tb2RlLCBwcm9jZXNzLmN3ZCgpKSBhcyB1bmtub3duIGFzIEVudi5JbXBvcnRNZXRhO1xuXG4gIGNvbnN0IGJ1aWxkVGltZSA9IGdldEJ1aWxkVGltZSgpO1xuXG4gIGNvbnN0IGVuYWJsZVByb3h5ID0gY29uZmlnRW52LmNvbW1hbmQgPT09ICdzZXJ2ZScgJiYgIWNvbmZpZ0Vudi5pc1ByZXZpZXc7XG5cbiAgcmV0dXJuIHtcbiAgICBiYXNlOiB2aXRlRW52LlZJVEVfQkFTRV9VUkwsXG4gICAgcmVzb2x2ZToge1xuICAgICAgYWxpYXM6IHtcbiAgICAgICAgJ34nOiBmaWxlVVJMVG9QYXRoKG5ldyBVUkwoJy4vJywgaW1wb3J0Lm1ldGEudXJsKSksXG4gICAgICAgICdAJzogZmlsZVVSTFRvUGF0aChuZXcgVVJMKCcuL3NyYycsIGltcG9ydC5tZXRhLnVybCkpXG4gICAgICB9XG4gICAgfSxcbiAgICBjc3M6IHtcbiAgICAgIHByZXByb2Nlc3Nvck9wdGlvbnM6IHtcbiAgICAgICAgc2Nzczoge1xuICAgICAgICAgIGFwaTogJ21vZGVybi1jb21waWxlcicsXG4gICAgICAgICAgYWRkaXRpb25hbERhdGE6IGBAdXNlIFwiQC9zdHlsZXMvc2Nzcy9nbG9iYWwuc2Nzc1wiIGFzICo7YFxuICAgICAgICB9XG4gICAgICB9XG4gICAgfSxcbiAgICBwbHVnaW5zOiBzZXR1cFZpdGVQbHVnaW5zKHZpdGVFbnYsIGJ1aWxkVGltZSksXG4gICAgZGVmaW5lOiB7XG4gICAgICBCVUlMRF9USU1FOiBKU09OLnN0cmluZ2lmeShidWlsZFRpbWUpXG4gICAgfSxcbiAgICBzZXJ2ZXI6IHtcbiAgICAgIGhvc3Q6ICcwLjAuMC4wJyxcbiAgICAgIHBvcnQ6IDk1MjcsXG4gICAgICBvcGVuOiB0cnVlLFxuICAgICAgcHJveHk6IGNyZWF0ZVZpdGVQcm94eSh2aXRlRW52LCBlbmFibGVQcm94eSksXG4gICAgICBmczoge1xuICAgICAgICBjYWNoZWRDaGVja3M6IGZhbHNlXG4gICAgICB9XG4gICAgfSxcbiAgICBwcmV2aWV3OiB7XG4gICAgICBwb3J0OiA5NzI1XG4gICAgfSxcbiAgICBidWlsZDoge1xuICAgICAgcmVwb3J0Q29tcHJlc3NlZFNpemU6IGZhbHNlLFxuICAgICAgc291cmNlbWFwOiB2aXRlRW52LlZJVEVfU09VUkNFX01BUCA9PT0gJ1knLFxuICAgICAgY29tbW9uanNPcHRpb25zOiB7XG4gICAgICAgIGlnbm9yZVRyeUNhdGNoOiBmYWxzZVxuICAgICAgfVxuICAgIH1cbiAgfTtcbn0pO1xuIiwgImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBZG1pbmlzdHJhdG9yXFxcXGNvZGVcXFxcTWV0cmljQm9vc3RcXFxcZnJvbnRlbmRcXFxcYnVpbGRcXFxccGx1Z2luc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcQWRtaW5pc3RyYXRvclxcXFxjb2RlXFxcXE1ldHJpY0Jvb3N0XFxcXGZyb250ZW5kXFxcXGJ1aWxkXFxcXHBsdWdpbnNcXFxcaW5kZXgudHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL0M6L1VzZXJzL0FkbWluaXN0cmF0b3IvY29kZS9NZXRyaWNCb29zdC9mcm9udGVuZC9idWlsZC9wbHVnaW5zL2luZGV4LnRzXCI7aW1wb3J0IHR5cGUgeyBQbHVnaW5PcHRpb24gfSBmcm9tICd2aXRlJztcbmltcG9ydCB2dWUgZnJvbSAnQHZpdGVqcy9wbHVnaW4tdnVlJztcbmltcG9ydCB2dWVKc3ggZnJvbSAnQHZpdGVqcy9wbHVnaW4tdnVlLWpzeCc7XG5pbXBvcnQgVnVlRGV2dG9vbHMgZnJvbSAndml0ZS1wbHVnaW4tdnVlLWRldnRvb2xzJztcbmltcG9ydCBwcm9ncmVzcyBmcm9tICd2aXRlLXBsdWdpbi1wcm9ncmVzcyc7XG5pbXBvcnQgeyBzZXR1cEVsZWdhbnRSb3V0ZXIgfSBmcm9tICcuL3JvdXRlcic7XG5pbXBvcnQgeyBzZXR1cFVub2NzcyB9IGZyb20gJy4vdW5vY3NzJztcbmltcG9ydCB7IHNldHVwVW5wbHVnaW4gfSBmcm9tICcuL3VucGx1Z2luJztcbmltcG9ydCB7IHNldHVwSHRtbFBsdWdpbiB9IGZyb20gJy4vaHRtbCc7XG5cbmV4cG9ydCBmdW5jdGlvbiBzZXR1cFZpdGVQbHVnaW5zKHZpdGVFbnY6IEVudi5JbXBvcnRNZXRhLCBidWlsZFRpbWU6IHN0cmluZykge1xuICBjb25zdCBwbHVnaW5zOiBQbHVnaW5PcHRpb24gPSBbXG4gICAgdnVlKCksXG4gICAgdnVlSnN4KCksXG4gICAgVnVlRGV2dG9vbHMoKSxcbiAgICBzZXR1cEVsZWdhbnRSb3V0ZXIoKSxcbiAgICBzZXR1cFVub2Nzcyh2aXRlRW52KSxcbiAgICAuLi5zZXR1cFVucGx1Z2luKHZpdGVFbnYpLFxuICAgIHByb2dyZXNzKCksXG4gICAgc2V0dXBIdG1sUGx1Z2luKGJ1aWxkVGltZSlcbiAgXTtcblxuICByZXR1cm4gcGx1Z2lucztcbn1cbiIsICJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcQWRtaW5pc3RyYXRvclxcXFxjb2RlXFxcXE1ldHJpY0Jvb3N0XFxcXGZyb250ZW5kXFxcXGJ1aWxkXFxcXHBsdWdpbnNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXEFkbWluaXN0cmF0b3JcXFxcY29kZVxcXFxNZXRyaWNCb29zdFxcXFxmcm9udGVuZFxcXFxidWlsZFxcXFxwbHVnaW5zXFxcXHJvdXRlci50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vQzovVXNlcnMvQWRtaW5pc3RyYXRvci9jb2RlL01ldHJpY0Jvb3N0L2Zyb250ZW5kL2J1aWxkL3BsdWdpbnMvcm91dGVyLnRzXCI7aW1wb3J0IHR5cGUgeyBSb3V0ZU1ldGEgfSBmcm9tICd2dWUtcm91dGVyJztcbmltcG9ydCBFbGVnYW50VnVlUm91dGVyIGZyb20gJ0BlbGVnYW50LXJvdXRlci92dWUvdml0ZSc7XG5pbXBvcnQgdHlwZSB7IFJvdXRlS2V5IH0gZnJvbSAnQGVsZWdhbnQtcm91dGVyL3R5cGVzJztcblxuZXhwb3J0IGZ1bmN0aW9uIHNldHVwRWxlZ2FudFJvdXRlcigpIHtcbiAgcmV0dXJuIEVsZWdhbnRWdWVSb3V0ZXIoe1xuICAgIGxheW91dHM6IHtcbiAgICAgIGJhc2U6ICdzcmMvbGF5b3V0cy9iYXNlLWxheW91dC9pbmRleC52dWUnLFxuICAgICAgYmxhbms6ICdzcmMvbGF5b3V0cy9ibGFuay1sYXlvdXQvaW5kZXgudnVlJ1xuICAgIH0sXG4gICAgY3VzdG9tUm91dGVzOiB7XG4gICAgICBuYW1lczogW1xuICAgICAgICAnZXhjZXB0aW9uXzQwMycsXG4gICAgICAgICdleGNlcHRpb25fNDA0JyxcbiAgICAgICAgJ2V4Y2VwdGlvbl81MDAnLFxuICAgICAgICAnZG9jdW1lbnRfcHJvamVjdCcsXG4gICAgICAgICdkb2N1bWVudF9wcm9qZWN0LWxpbmsnLFxuICAgICAgICAnZG9jdW1lbnRfdnVlJyxcbiAgICAgICAgJ2RvY3VtZW50X3ZpdGUnLFxuICAgICAgICAnZG9jdW1lbnRfdW5vY3NzJyxcbiAgICAgICAgJ2RvY3VtZW50X25haXZlJyxcbiAgICAgICAgJ2RvY3VtZW50X2FudGQnLFxuICAgICAgICAnZG9jdW1lbnRfYWxvdmEnXG4gICAgICBdXG4gICAgfSxcbiAgICByb3V0ZVBhdGhUcmFuc2Zvcm1lcihyb3V0ZU5hbWUsIHJvdXRlUGF0aCkge1xuICAgICAgY29uc3Qga2V5ID0gcm91dGVOYW1lIGFzIFJvdXRlS2V5O1xuXG4gICAgICBpZiAoa2V5ID09PSAnbG9naW4nKSB7XG4gICAgICAgIGNvbnN0IG1vZHVsZXM6IFVuaW9uS2V5LkxvZ2luTW9kdWxlW10gPSBbJ3B3ZC1sb2dpbicsICdjb2RlLWxvZ2luJywgJ3JlZ2lzdGVyJywgJ3Jlc2V0LXB3ZCcsICdiaW5kLXdlY2hhdCddO1xuXG4gICAgICAgIGNvbnN0IG1vZHVsZVJlZyA9IG1vZHVsZXMuam9pbignfCcpO1xuXG4gICAgICAgIHJldHVybiBgL2xvZ2luLzptb2R1bGUoJHttb2R1bGVSZWd9KT9gO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gcm91dGVQYXRoO1xuICAgIH0sXG4gICAgb25Sb3V0ZU1ldGFHZW4ocm91dGVOYW1lKSB7XG4gICAgICBjb25zdCBrZXkgPSByb3V0ZU5hbWUgYXMgUm91dGVLZXk7XG5cbiAgICAgIGNvbnN0IGNvbnN0YW50Um91dGVzOiBSb3V0ZUtleVtdID0gWydsb2dpbicsICc0MDMnLCAnNDA0JywgJzUwMCddO1xuXG4gICAgICBjb25zdCBtZXRhOiBQYXJ0aWFsPFJvdXRlTWV0YT4gPSB7XG4gICAgICAgIHRpdGxlOiBrZXksXG4gICAgICAgIGkxOG5LZXk6IGByb3V0ZS4ke2tleX1gIGFzIEFwcC5JMThuLkkxOG5LZXlcbiAgICAgIH07XG5cbiAgICAgIGlmIChjb25zdGFudFJvdXRlcy5pbmNsdWRlcyhrZXkpKSB7XG4gICAgICAgIG1ldGEuY29uc3RhbnQgPSB0cnVlO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gbWV0YTtcbiAgICB9XG4gIH0pO1xufVxuIiwgImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBZG1pbmlzdHJhdG9yXFxcXGNvZGVcXFxcTWV0cmljQm9vc3RcXFxcZnJvbnRlbmRcXFxcYnVpbGRcXFxccGx1Z2luc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcQWRtaW5pc3RyYXRvclxcXFxjb2RlXFxcXE1ldHJpY0Jvb3N0XFxcXGZyb250ZW5kXFxcXGJ1aWxkXFxcXHBsdWdpbnNcXFxcdW5vY3NzLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BZG1pbmlzdHJhdG9yL2NvZGUvTWV0cmljQm9vc3QvZnJvbnRlbmQvYnVpbGQvcGx1Z2lucy91bm9jc3MudHNcIjtpbXBvcnQgcHJvY2VzcyBmcm9tICdub2RlOnByb2Nlc3MnO1xuaW1wb3J0IHBhdGggZnJvbSAnbm9kZTpwYXRoJztcbmltcG9ydCB1bm9jc3MgZnJvbSAnQHVub2Nzcy92aXRlJztcbmltcG9ydCBwcmVzZXRJY29ucyBmcm9tICdAdW5vY3NzL3ByZXNldC1pY29ucyc7XG5pbXBvcnQgeyBGaWxlU3lzdGVtSWNvbkxvYWRlciB9IGZyb20gJ0BpY29uaWZ5L3V0aWxzL2xpYi9sb2FkZXIvbm9kZS1sb2FkZXJzJztcblxuZXhwb3J0IGZ1bmN0aW9uIHNldHVwVW5vY3NzKHZpdGVFbnY6IEVudi5JbXBvcnRNZXRhKSB7XG4gIGNvbnN0IHsgVklURV9JQ09OX1BSRUZJWCwgVklURV9JQ09OX0xPQ0FMX1BSRUZJWCB9ID0gdml0ZUVudjtcblxuICBjb25zdCBsb2NhbEljb25QYXRoID0gcGF0aC5qb2luKHByb2Nlc3MuY3dkKCksICdzcmMvYXNzZXRzL3N2Zy1pY29uJyk7XG5cbiAgLyoqIFRoZSBuYW1lIG9mIHRoZSBsb2NhbCBpY29uIGNvbGxlY3Rpb24gKi9cbiAgY29uc3QgY29sbGVjdGlvbk5hbWUgPSBWSVRFX0lDT05fTE9DQUxfUFJFRklYLnJlcGxhY2UoYCR7VklURV9JQ09OX1BSRUZJWH0tYCwgJycpO1xuXG4gIHJldHVybiB1bm9jc3Moe1xuICAgIHByZXNldHM6IFtcbiAgICAgIHByZXNldEljb25zKHtcbiAgICAgICAgcHJlZml4OiBgJHtWSVRFX0lDT05fUFJFRklYfS1gLFxuICAgICAgICBzY2FsZTogMSxcbiAgICAgICAgZXh0cmFQcm9wZXJ0aWVzOiB7XG4gICAgICAgICAgZGlzcGxheTogJ2lubGluZS1ibG9jaydcbiAgICAgICAgfSxcbiAgICAgICAgY29sbGVjdGlvbnM6IHtcbiAgICAgICAgICBbY29sbGVjdGlvbk5hbWVdOiBGaWxlU3lzdGVtSWNvbkxvYWRlcihsb2NhbEljb25QYXRoLCBzdmcgPT5cbiAgICAgICAgICAgIHN2Zy5yZXBsYWNlKC9ePHN2Z1xccy8sICc8c3ZnIHdpZHRoPVwiMWVtXCIgaGVpZ2h0PVwiMWVtXCIgJylcbiAgICAgICAgICApXG4gICAgICAgIH0sXG4gICAgICAgIHdhcm46IHRydWVcbiAgICAgIH0pXG4gICAgXVxuICB9KTtcbn1cbiIsICJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcQWRtaW5pc3RyYXRvclxcXFxjb2RlXFxcXE1ldHJpY0Jvb3N0XFxcXGZyb250ZW5kXFxcXGJ1aWxkXFxcXHBsdWdpbnNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXEFkbWluaXN0cmF0b3JcXFxcY29kZVxcXFxNZXRyaWNCb29zdFxcXFxmcm9udGVuZFxcXFxidWlsZFxcXFxwbHVnaW5zXFxcXHVucGx1Z2luLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BZG1pbmlzdHJhdG9yL2NvZGUvTWV0cmljQm9vc3QvZnJvbnRlbmQvYnVpbGQvcGx1Z2lucy91bnBsdWdpbi50c1wiO2ltcG9ydCBwcm9jZXNzIGZyb20gJ25vZGU6cHJvY2Vzcyc7XG5pbXBvcnQgcGF0aCBmcm9tICdub2RlOnBhdGgnO1xuaW1wb3J0IHR5cGUgeyBQbHVnaW5PcHRpb24gfSBmcm9tICd2aXRlJztcbmltcG9ydCBJY29ucyBmcm9tICd1bnBsdWdpbi1pY29ucy92aXRlJztcbmltcG9ydCBJY29uc1Jlc29sdmVyIGZyb20gJ3VucGx1Z2luLWljb25zL3Jlc29sdmVyJztcbmltcG9ydCBDb21wb25lbnRzIGZyb20gJ3VucGx1Z2luLXZ1ZS1jb21wb25lbnRzL3ZpdGUnO1xuaW1wb3J0IHsgQW50RGVzaWduVnVlUmVzb2x2ZXIsIE5haXZlVWlSZXNvbHZlciB9IGZyb20gJ3VucGx1Z2luLXZ1ZS1jb21wb25lbnRzL3Jlc29sdmVycyc7XG5pbXBvcnQgeyBGaWxlU3lzdGVtSWNvbkxvYWRlciB9IGZyb20gJ3VucGx1Z2luLWljb25zL2xvYWRlcnMnO1xuaW1wb3J0IHsgY3JlYXRlU3ZnSWNvbnNQbHVnaW4gfSBmcm9tICd2aXRlLXBsdWdpbi1zdmctaWNvbnMnO1xuXG5leHBvcnQgZnVuY3Rpb24gc2V0dXBVbnBsdWdpbih2aXRlRW52OiBFbnYuSW1wb3J0TWV0YSkge1xuICBjb25zdCB7IFZJVEVfSUNPTl9QUkVGSVgsIFZJVEVfSUNPTl9MT0NBTF9QUkVGSVggfSA9IHZpdGVFbnY7XG5cbiAgY29uc3QgbG9jYWxJY29uUGF0aCA9IHBhdGguam9pbihwcm9jZXNzLmN3ZCgpLCAnc3JjL2Fzc2V0cy9zdmctaWNvbicpO1xuXG4gIC8qKiBUaGUgbmFtZSBvZiB0aGUgbG9jYWwgaWNvbiBjb2xsZWN0aW9uICovXG4gIGNvbnN0IGNvbGxlY3Rpb25OYW1lID0gVklURV9JQ09OX0xPQ0FMX1BSRUZJWC5yZXBsYWNlKGAke1ZJVEVfSUNPTl9QUkVGSVh9LWAsICcnKTtcblxuICBjb25zdCBwbHVnaW5zOiBQbHVnaW5PcHRpb25bXSA9IFtcbiAgICBJY29ucyh7XG4gICAgICBjb21waWxlcjogJ3Z1ZTMnLFxuICAgICAgY3VzdG9tQ29sbGVjdGlvbnM6IHtcbiAgICAgICAgW2NvbGxlY3Rpb25OYW1lXTogRmlsZVN5c3RlbUljb25Mb2FkZXIobG9jYWxJY29uUGF0aCwgc3ZnID0+XG4gICAgICAgICAgc3ZnLnJlcGxhY2UoL148c3ZnXFxzLywgJzxzdmcgd2lkdGg9XCIxZW1cIiBoZWlnaHQ9XCIxZW1cIiAnKVxuICAgICAgICApXG4gICAgICB9LFxuICAgICAgc2NhbGU6IDEsXG4gICAgICBkZWZhdWx0Q2xhc3M6ICdpbmxpbmUtYmxvY2snXG4gICAgfSksXG4gICAgQ29tcG9uZW50cyh7XG4gICAgICBkdHM6ICdzcmMvdHlwaW5ncy9jb21wb25lbnRzLmQudHMnLFxuICAgICAgdHlwZXM6IFt7IGZyb206ICd2dWUtcm91dGVyJywgbmFtZXM6IFsnUm91dGVyTGluaycsICdSb3V0ZXJWaWV3J10gfV0sXG4gICAgICByZXNvbHZlcnM6IFtcbiAgICAgICAgQW50RGVzaWduVnVlUmVzb2x2ZXIoe1xuICAgICAgICAgIGltcG9ydFN0eWxlOiBmYWxzZVxuICAgICAgICB9KSxcbiAgICAgICAgTmFpdmVVaVJlc29sdmVyKCksXG4gICAgICAgIEljb25zUmVzb2x2ZXIoeyBjdXN0b21Db2xsZWN0aW9uczogW2NvbGxlY3Rpb25OYW1lXSwgY29tcG9uZW50UHJlZml4OiBWSVRFX0lDT05fUFJFRklYIH0pXG4gICAgICBdXG4gICAgfSksXG4gICAgY3JlYXRlU3ZnSWNvbnNQbHVnaW4oe1xuICAgICAgaWNvbkRpcnM6IFtsb2NhbEljb25QYXRoXSxcbiAgICAgIHN5bWJvbElkOiBgJHtWSVRFX0lDT05fTE9DQUxfUFJFRklYfS1bZGlyXS1bbmFtZV1gLFxuICAgICAgaW5qZWN0OiAnYm9keS1sYXN0JyxcbiAgICAgIGN1c3RvbURvbUlkOiAnX19TVkdfSUNPTl9MT0NBTF9fJ1xuICAgIH0pXG4gIF07XG5cbiAgcmV0dXJuIHBsdWdpbnM7XG59XG4iLCAiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXEFkbWluaXN0cmF0b3JcXFxcY29kZVxcXFxNZXRyaWNCb29zdFxcXFxmcm9udGVuZFxcXFxidWlsZFxcXFxwbHVnaW5zXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBZG1pbmlzdHJhdG9yXFxcXGNvZGVcXFxcTWV0cmljQm9vc3RcXFxcZnJvbnRlbmRcXFxcYnVpbGRcXFxccGx1Z2luc1xcXFxodG1sLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BZG1pbmlzdHJhdG9yL2NvZGUvTWV0cmljQm9vc3QvZnJvbnRlbmQvYnVpbGQvcGx1Z2lucy9odG1sLnRzXCI7aW1wb3J0IHR5cGUgeyBQbHVnaW4gfSBmcm9tICd2aXRlJztcblxuZXhwb3J0IGZ1bmN0aW9uIHNldHVwSHRtbFBsdWdpbihidWlsZFRpbWU6IHN0cmluZykge1xuICBjb25zdCBwbHVnaW46IFBsdWdpbiA9IHtcbiAgICBuYW1lOiAnaHRtbC1wbHVnaW4nLFxuICAgIGFwcGx5OiAnYnVpbGQnLFxuICAgIHRyYW5zZm9ybUluZGV4SHRtbChodG1sKSB7XG4gICAgICByZXR1cm4gaHRtbC5yZXBsYWNlKCc8aGVhZD4nLCBgPGhlYWQ+XFxuICAgIDxtZXRhIG5hbWU9XCJidWlsZFRpbWVcIiBjb250ZW50PVwiJHtidWlsZFRpbWV9XCI+YCk7XG4gICAgfVxuICB9O1xuXG4gIHJldHVybiBwbHVnaW47XG59XG4iLCAiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXEFkbWluaXN0cmF0b3JcXFxcY29kZVxcXFxNZXRyaWNCb29zdFxcXFxmcm9udGVuZFxcXFxzcmNcXFxcdXRpbHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkM6XFxcXFVzZXJzXFxcXEFkbWluaXN0cmF0b3JcXFxcY29kZVxcXFxNZXRyaWNCb29zdFxcXFxmcm9udGVuZFxcXFxzcmNcXFxcdXRpbHNcXFxcc2VydmljZS50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vQzovVXNlcnMvQWRtaW5pc3RyYXRvci9jb2RlL01ldHJpY0Jvb3N0L2Zyb250ZW5kL3NyYy91dGlscy9zZXJ2aWNlLnRzXCI7aW1wb3J0IGpzb241IGZyb20gJ2pzb241JztcblxuLyoqXG4gKiBDcmVhdGUgc2VydmljZSBjb25maWcgYnkgcGFnZSBlbnZcbiAqXG4gKiBAcGFyYW0gZW52IFRoZSBwYWdlIGVudlxuICovXG5leHBvcnQgZnVuY3Rpb24gY3JlYXRlU2VydmljZUNvbmZpZyhlbnY6IEVudi5JbXBvcnRNZXRhKSB7XG4gIGNvbnN0IHsgVklURV9TRVJWSUNFX0JBU0VfVVJMLCBWSVRFX09USEVSX1NFUlZJQ0VfQkFTRV9VUkwgfSA9IGVudjtcblxuICBsZXQgb3RoZXIgPSB7fSBhcyBSZWNvcmQ8QXBwLlNlcnZpY2UuT3RoZXJCYXNlVVJMS2V5LCBzdHJpbmc+O1xuICB0cnkge1xuICAgIG90aGVyID0ganNvbjUucGFyc2UoVklURV9PVEhFUl9TRVJWSUNFX0JBU0VfVVJMKTtcbiAgfSBjYXRjaCB7XG4gICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICBjb25zb2xlLmVycm9yKCdWSVRFX09USEVSX1NFUlZJQ0VfQkFTRV9VUkwgaXMgbm90IGEgdmFsaWQganNvbjUgc3RyaW5nJyk7XG4gIH1cblxuICBjb25zdCBodHRwQ29uZmlnOiBBcHAuU2VydmljZS5TaW1wbGVTZXJ2aWNlQ29uZmlnID0ge1xuICAgIGJhc2VVUkw6IFZJVEVfU0VSVklDRV9CQVNFX1VSTCxcbiAgICBvdGhlclxuICB9O1xuXG4gIGNvbnN0IG90aGVySHR0cEtleXMgPSBPYmplY3Qua2V5cyhodHRwQ29uZmlnLm90aGVyKSBhcyBBcHAuU2VydmljZS5PdGhlckJhc2VVUkxLZXlbXTtcblxuICBjb25zdCBvdGhlckNvbmZpZzogQXBwLlNlcnZpY2UuT3RoZXJTZXJ2aWNlQ29uZmlnSXRlbVtdID0gb3RoZXJIdHRwS2V5cy5tYXAoa2V5ID0+IHtcbiAgICByZXR1cm4ge1xuICAgICAga2V5LFxuICAgICAgYmFzZVVSTDogaHR0cENvbmZpZy5vdGhlcltrZXldLFxuICAgICAgcHJveHlQYXR0ZXJuOiBjcmVhdGVQcm94eVBhdHRlcm4oa2V5KVxuICAgIH07XG4gIH0pO1xuXG4gIGNvbnN0IGNvbmZpZzogQXBwLlNlcnZpY2UuU2VydmljZUNvbmZpZyA9IHtcbiAgICBiYXNlVVJMOiBodHRwQ29uZmlnLmJhc2VVUkwsXG4gICAgcHJveHlQYXR0ZXJuOiBjcmVhdGVQcm94eVBhdHRlcm4oKSxcbiAgICBvdGhlcjogb3RoZXJDb25maWdcbiAgfTtcblxuICByZXR1cm4gY29uZmlnO1xufVxuXG4vKipcbiAqIGdldCBiYWNrZW5kIHNlcnZpY2UgYmFzZSB1cmxcbiAqXG4gKiBAcGFyYW0gZW52IC0gdGhlIHBhZ2UgZW52XG4gKiBAcGFyYW0gaXNQcm94eSAtIGlmIHVzZSBwcm94eVxuICovXG5leHBvcnQgZnVuY3Rpb24gZ2V0U2VydmljZUJhc2VVUkwoZW52OiBFbnYuSW1wb3J0TWV0YSwgaXNQcm94eTogYm9vbGVhbikge1xuICBjb25zdCB7IGJhc2VVUkwsIG90aGVyIH0gPSBjcmVhdGVTZXJ2aWNlQ29uZmlnKGVudik7XG5cbiAgY29uc3Qgb3RoZXJCYXNlVVJMID0ge30gYXMgUmVjb3JkPEFwcC5TZXJ2aWNlLk90aGVyQmFzZVVSTEtleSwgc3RyaW5nPjtcblxuICBvdGhlci5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgIG90aGVyQmFzZVVSTFtpdGVtLmtleV0gPSBpc1Byb3h5ID8gaXRlbS5wcm94eVBhdHRlcm4gOiBpdGVtLmJhc2VVUkw7XG4gIH0pO1xuXG4gIHJldHVybiB7XG4gICAgYmFzZVVSTDogaXNQcm94eSA/IGNyZWF0ZVByb3h5UGF0dGVybigpIDogYmFzZVVSTCxcbiAgICBvdGhlckJhc2VVUkxcbiAgfTtcbn1cblxuLyoqXG4gKiBHZXQgcHJveHkgcGF0dGVybiBvZiBiYWNrZW5kIHNlcnZpY2UgYmFzZSB1cmxcbiAqXG4gKiBAcGFyYW0ga2V5IElmIG5vdCBzZXQsIHdpbGwgdXNlIHRoZSBkZWZhdWx0IGtleVxuICovXG5mdW5jdGlvbiBjcmVhdGVQcm94eVBhdHRlcm4oa2V5PzogQXBwLlNlcnZpY2UuT3RoZXJCYXNlVVJMS2V5KSB7XG4gIGlmICgha2V5KSB7XG4gICAgcmV0dXJuICcvcHJveHktZGVmYXVsdCc7XG4gIH1cblxuICByZXR1cm4gYC9wcm94eS0ke2tleX1gO1xufVxuIiwgImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBZG1pbmlzdHJhdG9yXFxcXGNvZGVcXFxcTWV0cmljQm9vc3RcXFxcZnJvbnRlbmRcXFxcYnVpbGRcXFxcY29uZmlnXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBZG1pbmlzdHJhdG9yXFxcXGNvZGVcXFxcTWV0cmljQm9vc3RcXFxcZnJvbnRlbmRcXFxcYnVpbGRcXFxcY29uZmlnXFxcXHByb3h5LnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BZG1pbmlzdHJhdG9yL2NvZGUvTWV0cmljQm9vc3QvZnJvbnRlbmQvYnVpbGQvY29uZmlnL3Byb3h5LnRzXCI7aW1wb3J0IHR5cGUgeyBQcm94eU9wdGlvbnMgfSBmcm9tICd2aXRlJztcbmltcG9ydCB7IGNyZWF0ZVNlcnZpY2VDb25maWcgfSBmcm9tICcuLi8uLi9zcmMvdXRpbHMvc2VydmljZSc7XG5cbi8qKlxuICogU2V0IGh0dHAgcHJveHlcbiAqXG4gKiBAcGFyYW0gZW52IC0gVGhlIHBhZ2UgZW52XG4gKiBAcGFyYW0gZW5hYmxlIC0gSWYgZW5hYmxlIGh0dHAgcHJveHlcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVZpdGVQcm94eShlbnY6IEVudi5JbXBvcnRNZXRhLCBlbmFibGU6IGJvb2xlYW4pIHtcbiAgY29uc3QgaXNFbmFibGVIdHRwUHJveHkgPSBlbmFibGUgJiYgZW52LlZJVEVfSFRUUF9QUk9YWSA9PT0gJ1knO1xuXG4gIGlmICghaXNFbmFibGVIdHRwUHJveHkpIHJldHVybiB1bmRlZmluZWQ7XG5cbiAgY29uc3QgeyBiYXNlVVJMLCBwcm94eVBhdHRlcm4sIG90aGVyIH0gPSBjcmVhdGVTZXJ2aWNlQ29uZmlnKGVudik7XG5cbiAgY29uc3QgcHJveHk6IFJlY29yZDxzdHJpbmcsIFByb3h5T3B0aW9ucz4gPSBjcmVhdGVQcm94eUl0ZW0oeyBiYXNlVVJMLCBwcm94eVBhdHRlcm4gfSk7XG5cbiAgb3RoZXIuZm9yRWFjaChpdGVtID0+IHtcbiAgICBPYmplY3QuYXNzaWduKHByb3h5LCBjcmVhdGVQcm94eUl0ZW0oaXRlbSkpO1xuICB9KTtcblxuICByZXR1cm4gcHJveHk7XG59XG5cbmZ1bmN0aW9uIGNyZWF0ZVByb3h5SXRlbShpdGVtOiBBcHAuU2VydmljZS5TZXJ2aWNlQ29uZmlnSXRlbSkge1xuICBjb25zdCBwcm94eTogUmVjb3JkPHN0cmluZywgUHJveHlPcHRpb25zPiA9IHt9O1xuXG4gIHByb3h5W2l0ZW0ucHJveHlQYXR0ZXJuXSA9IHtcbiAgICB0YXJnZXQ6IGl0ZW0uYmFzZVVSTCxcbiAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgcmV3cml0ZTogcGF0aCA9PiBwYXRoLnJlcGxhY2UobmV3IFJlZ0V4cChgXiR7aXRlbS5wcm94eVBhdHRlcm59YCksICcnKVxuICB9O1xuXG4gIHJldHVybiBwcm94eTtcbn1cbiIsICJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcQWRtaW5pc3RyYXRvclxcXFxjb2RlXFxcXE1ldHJpY0Jvb3N0XFxcXGZyb250ZW5kXFxcXGJ1aWxkXFxcXGNvbmZpZ1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcQWRtaW5pc3RyYXRvclxcXFxjb2RlXFxcXE1ldHJpY0Jvb3N0XFxcXGZyb250ZW5kXFxcXGJ1aWxkXFxcXGNvbmZpZ1xcXFx0aW1lLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BZG1pbmlzdHJhdG9yL2NvZGUvTWV0cmljQm9vc3QvZnJvbnRlbmQvYnVpbGQvY29uZmlnL3RpbWUudHNcIjtpbXBvcnQgZGF5anMgZnJvbSAnZGF5anMnO1xuaW1wb3J0IHV0YyBmcm9tICdkYXlqcy9wbHVnaW4vdXRjJztcbmltcG9ydCB0aW1lem9uZSBmcm9tICdkYXlqcy9wbHVnaW4vdGltZXpvbmUnO1xuXG5leHBvcnQgZnVuY3Rpb24gZ2V0QnVpbGRUaW1lKCkge1xuICBkYXlqcy5leHRlbmQodXRjKTtcbiAgZGF5anMuZXh0ZW5kKHRpbWV6b25lKTtcblxuICBjb25zdCBidWlsZFRpbWUgPSBkYXlqcy50eihEYXRlLm5vdygpLCAnQXNpYS9TaGFuZ2hhaScpLmZvcm1hdCgnWVlZWS1NTS1ERCBISDptbTpzcycpO1xuXG4gIHJldHVybiBidWlsZFRpbWU7XG59XG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQThVLE9BQU9BLGNBQWE7QUFDbFcsU0FBUyxLQUFLLHFCQUFxQjtBQUNuQyxTQUFTLGNBQWMsZUFBZTs7O0FDRHRDLE9BQU8sU0FBUztBQUNoQixPQUFPLFlBQVk7QUFDbkIsT0FBTyxpQkFBaUI7QUFDeEIsT0FBTyxjQUFjOzs7QUNIckIsT0FBTyxzQkFBc0I7QUFHdEIsU0FBUyxxQkFBcUI7QUFDbkMsU0FBTyxpQkFBaUI7QUFBQSxJQUN0QixTQUFTO0FBQUEsTUFDUCxNQUFNO0FBQUEsTUFDTixPQUFPO0FBQUEsSUFDVDtBQUFBLElBQ0EsY0FBYztBQUFBLE1BQ1osT0FBTztBQUFBLFFBQ0w7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsTUFDRjtBQUFBLElBQ0Y7QUFBQSxJQUNBLHFCQUFxQixXQUFXLFdBQVc7QUFDekMsWUFBTSxNQUFNO0FBRVosVUFBSSxRQUFRLFNBQVM7QUFDbkIsY0FBTSxVQUFrQyxDQUFDLGFBQWEsY0FBYyxZ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LFFBQU0sWUFBWSxhQUFhO0FBRS9CLFFBQU0sY0FBYyxVQUFVLFlBQVksV0FBVyxDQUFDLFVBQVU7QUFFaEUsU0FBTztBQUFBLElBQ0wsTUFBTSxRQUFRO0FBQUEsSUFDZCxTQUFTO0FBQUEsTUFDUCxPQUFPO0FBQUEsUUFDTCxLQUFLLGNBQWMsSUFBSSxJQUFJLE1BQU0sd0NBQWUsQ0FBQztBQUFBLFFBQ2pELEtBQUssY0FBYyxJQUFJLElBQUksU0FBUyx3Q0FBZSxDQUFDO0FBQUEsTUFDdEQ7QUFBQSxJQUNGO0FBQUEsSUFDQSxLQUFLO0FBQUEsTUFDSCxxQkFBcUI7QUFBQSxRQUNuQixNQUFNO0FBQUEsVUFDSixLQUFLO0FBQUEsVUFDTCxnQkFBZ0I7QUFBQSxRQUNsQjtBQUFBLE1BQ0Y7QUFBQSxJQUNGO0FBQUEsSUFDQSxTQUFTLGlCQUFpQixTQUFTLFNBQVM7QUFBQSxJQUM1QyxRQUFRO0FBQUEsTUFDTixZQUFZLEtBQUssVUFBVSxTQUFTO0FBQUEsSUFDdEM7QUFBQSxJQUNBLFFBQVE7QUFBQSxNQUNOLE1BQU07QUFBQSxNQUNOLE1BQU07QUFBQSxNQUNOLE1BQU07QUFBQSxNQUNOLE9BQU8sZ0JBQWdCLFNBQVMsV0FBVztBQUFBLE1BQzNDLElBQUk7QUFBQSxRQUNGLGNBQWM7QUFBQSxNQUNoQjtBQUFBLElBQ0Y7QUFBQSxJQUNBLFNBQVM7QUFBQSxNQUNQLE1BQU07QUFBQSxJQUNSO0FBQUEsSUFDQSxPQUFPO0FBQUEsTUFDTCxzQkFBc0I7QUFBQSxNQUN0QixXQUFXLFFBQVEsb0JBQW9CO0FBQUEsTUFDdkMsaUJBQWlCO0FBQUEsUUFDZixnQkFBZ0I7QUFBQSxNQUNsQjtBQUFBLElBQ0Y7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFsicHJvY2VzcyIsICJwcm9jZXNzIiwgInBhdGgiLCAiRmlsZVN5c3RlbUljb25Mb2FkZXIiLCAicGF0aCIsICJwcm9jZXNzIiwgIkZpbGVTeXN0ZW1JY29uTG9hZGVyIiwgInBhdGgiLCAicHJvY2VzcyJdCn0K
