# ProxyRules · 多客户端代理规则与配置生成

[![Generate Config Files](https://github.com/luluape/ProxyRules/actions/workflows/auto_generate.yml/badge.svg)](https://github.com/luluape/ProxyRules/actions/workflows/auto_generate.yml)
[![Validate rules and generator](https://github.com/luluape/ProxyRules/actions/workflows/pr_validate.yml/badge.svg)](https://github.com/luluape/ProxyRules/actions/workflows/pr_validate.yml)

本仓库由 [luluape](https://github.com/luluape) 维护，基于原项目 **Higanoneko/ProxyRules** 延续开发，整合多方公开规则源，提供 Mihomo、Stash、Loon、Surge、Egern 的配置生成、统一分流策略和自动校验。**不提供代理节点或付费订阅**。

> **Egern 目前为 Beta**：公开配置是无节点的模板，必须在本地填入自己的 Egern 原生 HTTPS 订阅地址；不要把个人订阅、节点或密钥提交到公开仓库。[兼容性与测试范围](docs/EGERN_COMPATIBILITY.md)。

## 配置导航

| 客户端 | 推荐配置（直接获取原始文件） | 其他选项及说明 |
|---|---|---|
| **Mihomo / Clash Meta** | [IPv6 + DNS 基础版](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-1_full-0.yaml) | [无 IPv6](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-0_dns-1_full-0.yaml) · [全部版本](#mihomo-clash-meta) |
| **Stash** | [完整配置（IPv6）](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_config_full.yaml) | [无 IPv6](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_config_full_no_ipv6.yaml) · [覆写及一键导入](#stash) |
| **Loon** | [IPv6 配置](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Loon/Loon_config.lcf) | [无 IPv6](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Loon/Loon_config_no_ipv6.lcf) · [一键导入](#loon) |
| **Surge** | [IPv6 配置](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Surge/Surge_config.conf) | [无 IPv6](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Surge/Surge_config_no_ipv6.conf) · [一键导入](#surge) |
| **Egern（Beta）** | [IPv6 公开模板](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Egern/Egern_config.yaml) | [无 IPv6 模板](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Egern/Egern_config_no_ipv6.yaml) · [使用与兼容性说明](docs/EGERN_COMPATIBILITY.md) |

**其他入口：** [Mihomo4Root](#mihomo-clash-meta) · [EasyTier / WireGuard](Wireguard_Easytier/README.md) · [生成器使用文档](README_Dev.md) · [规则一致性说明](docs/PHASE2_CONSISTENCY.md) · [GitHub Actions](https://github.com/luluape/ProxyRules/actions)。

**版本命名：** `ipv6-1/0` 表示启用/禁用 IPv6；`dns-1/0` 表示配置/不配置 DNS；`full-1/0` 表示完整/基础配置。不同客户端需要使用各自原生格式，不能互换导入。

## 当前支持情况

| 工具 | 状态 | 说明 |
|------|------|------|
| [Mihomo](#mihomo-clash-meta) | ✅ 已支持 | `.yaml` 覆写文件 和 `.js` 覆写脚本 |
| [Stash](#stash) | ✅ 已支持 | `.yaml` 覆写文件 和 `.stoverride` 覆写文件 |
| [Loon](#loon) | ✅ 已支持 | `.lcf` 配置文件 |
| [Surge](#surge) | ✅ 已支持 | `.conf` 配置文件 |
| [Egern](#egern-beta) | 🧪 Beta | 29 个策略组、30 组规则；公开无凭据模板 |
| QuantumultX | ❌ 未支持 | 目前未纳入本项目生成器 |


## 快速开始

### Egern (Beta)

Egern 与其他四个客户端共用策略与规则定义，当前公开模板包含 **29 个策略组、30 条远程规则引用**，有 IPv6 和无 IPv6 两种版本。

- [Egern IPv6 模板（YAML）](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Egern/Egern_config.yaml)
- [Egern 无 IPv6 模板（YAML）](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Egern/Egern_config_no_ipv6.yaml)
- [兼容性报告与尚待验证项目](docs/EGERN_COMPATIBILITY.md)

1. 下载所需 YAML 模板到本地。
2. 将模板中的 `https://example.invalid/REPLACE_WITH_YOUR_EGERN_SUBSCRIPTION` **仅在本地**替换为自己的 Egern 原生 HTTPS 订阅地址。
3. 在 Egern 中导入本地 YAML，检查节点、策略组及规则更新。

**注意：** 模板不包含节点，未替换占位符前不能正常代理；Beta 已通过初步实机导入和节点选择测试，不代表全部分流、广告拦截和网络切换场景已通过验证。切勿公开个人订阅 URL。


### Mihomo (Clash Meta)

**覆写文件 (.yaml) ⭐ 优先使用**
  - [mihomo_config_ipv6-1_dns-1_full-0.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-1_full-0.yaml) - 启用 IPv6，启用 DNS，基础配置 ⭐ 推荐
  - [mihomo_config_ipv6-0_dns-1_full-0.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-0_dns-1_full-0.yaml) - 禁用 IPv6，启用 DNS，基础配置
  - [mihomo_config_ipv6-0_dns-1_full-1.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-0_dns-1_full-1.yaml) - 禁用 IPv6，启用 DNS，完整配置
  - [mihomo_config_ipv6-1_dns-1_full-1.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-1_full-1.yaml) - 启用 IPv6，启用 DNS，完整配置
  - [mihomo_config_ipv6-1_dns-0_full-0.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-0_full-0.yaml) - 启用 IPv6，不配置 DNS 或域名嗅探，基础配置
  - [mihomo_config_ipv6-1_dns-0_full-1.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-0_full-1.yaml) - 启用 IPv6，不配置 DNS 或域名嗅探，完整配置
  - [mihomo_config_ipv6-0_dns-0_full-0.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-0_dns-0_full-0.yaml) - 禁用 IPv6，不配置 DNS 或域名嗅探，基础配置
  - [mihomo_config_ipv6-0_dns-0_full-1.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-0_dns-0_full-1.yaml) - 禁用 IPv6，不配置 DNS 或域名嗅探，完整配置

**覆写脚本 (.js)**
  - [mihomo_convert_ipv6-1_dns-1_full-0.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-1_dns-1_full-0.js) - 启用 IPv6，启用 DNS，基础配置 ⭐ 推荐
  - [mihomo_convert_ipv6-0_dns-1_full-0.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-0_dns-1_full-0.js) - 禁用 IPv6，启用 DNS，基础配置
  - [mihomo_convert_ipv6-0_dns-1_full-1.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-0_dns-1_full-1.js) - 禁用 IPv6，启用 DNS，完整配置
  - [mihomo_convert_ipv6-1_dns-1_full-1.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-1_dns-1_full-1.js) - 启用 IPv6，启用 DNS，完整配置
  - [mihomo_convert_ipv6-1_dns-0_full-0.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-1_dns-0_full-0.js) - 启用 IPv6，不配置 DNS 或域名嗅探，基础配置
  - [mihomo_convert_ipv6-1_dns-0_full-1.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-1_dns-0_full-1.js) - 启用 IPv6，不配置 DNS 或域名嗅探，完整配置
  - [mihomo_convert_ipv6-0_dns-0_full-0.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-0_dns-0_full-0.js) - 禁用 IPv6，不配置 DNS 或域名嗅探，基础配置
  - [mihomo_convert_ipv6-0_dns-0_full-1.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_ipv6-0_dns-0_full-1.js) - 禁用 IPv6，不配置 DNS 或域名嗅探，完整配置

**Mihomo4Root 配置 (.yaml)**

用于 [Box4Root](https://github.com/boxproxy/box) 、 [Surfing](https://github.com/GitMetaio/Surfing) 等运行在 Root Shell 环境中的工具。
  - [Mihomo4Root_mihomo_config.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo4Root/Mihomo4Root_mihomo_config.yaml) - 启用 IPv6，禁用 TUN。 ⭐ 推荐（需要更改 Mihomo4Root 的运行模式为 Enhanced 等非 TUN 模式）
  - [Mihomo4Root_mihomo_config_no_ipv6.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo4Root/Mihomo4Root_mihomo_config_no_ipv6.yaml) - 禁用 IPv6，禁用 TUN。（需要更改 Mihomo4Root 的运行模式为 Enhanced 等非 TUN 模式）
  - [Mihomo4Root_mihomo_config_tun.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo4Root/Mihomo4Root_mihomo_config_tun.yaml) - 启用 IPv6，启用 TUN。
  - [Mihomo4Root_mihomo_config_tun_no_ipv6.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo4Root/Mihomo4Root_mihomo_config_tun_no_ipv6.yaml) - 禁用 IPv6，启用 TUN。


**Sparkle/Clash Party 使用方法**

推荐使用 [Sparkle](https://github.com/xishang0128/sparkle)

1. 打开覆写
2. 在上方地址栏中粘贴上方覆写脚本的链接
3. 点击「导入」按钮，（可选）将导入后的文件更改名称为你认为合适的名称，并且开启全局
4. 为对应的配置文件添加该覆写（如果已开启全局则不需要）

**Sparkle/Clash Party 特别设置**

需要注意，Sparkle/Clash Party 在默认设置下还会接管 DNS 和 SNI（域名嗅探），需要手动在设置中关闭「控制 DNS 设置」和「控制域名嗅探」两个选项。

**SubStore 使用方法**

  -  [mihomo_convert_args.js](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_args.js) - SubStore 可导入参数脚本

可传入参数，传入多个参数时，用`&`分隔：
* `ipv6`：是否启用 IPv6，取值 `0`（禁用）或 `1`（启用），默认值 `1`
* `full`：是否使用完整配置，取值 `0`（基础配置）或 `1`（完整配置），默认值 `0`
* `dns`：是否配置 DNS 和域名嗅探，取值 `0`（不配置）或 `1`（配置），默认值 `1`

用例：
```
https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_convert_args.js#ipv6=1&full=0&dns=0
```

**ShellCrash 使用方法**

使用 `curl` 下载配置文件到本地：

```bash
curl -o /path/to/config/mihomo_config.yaml https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-1_full-0.yaml
```

使用 `wget` 下载配置文件到本地：

```bash
wget -O /path/to/config/mihomo_config.yaml https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Mihomo/mihomo_config_ipv6-1_dns-1_full-0.yaml
```
> 以上 Sample 均使用启用 IPv6 的基础配置文件作为示例，请根据需要替换为其他版本的配置文件链接。


在 [ShellCrash](https://github.com/juewuy/ShellCrash) 的 配置文件管理中选择 `本地生成配置文件(基于内核providers,推荐！)`

先选择 `选择规则模版` 修改为下载的配置文件路径，再选择 `生成配置文件` 即可生成最终配置文件。

### Stash

**覆写文件 (.stoverride) ⭐ 优先使用**
- 点击以下链接直接导入到 Stash（推荐）：
  - [一键导入 Stash_override_ipv6-1_dns-1.stoverride](https://intradeus.github.io/http-protocol-redirector?r=stash://install-override?url=https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_override_ipv6-1_dns-1.stoverride) - 启用 IPv6，启用 DNS ⭐ 推荐
  - [一键导入 Stash_override_ipv6-0_dns-1.stoverride](https://intradeus.github.io/http-protocol-redirector?r=stash://install-override?url=https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_override_ipv6-0_dns-1.stoverride) - 禁用 IPv6，启用 DNS
  - [一键导入 Stash_override_ipv6-1_dns-0.stoverride](https://intradeus.github.io/http-protocol-redirector?r=stash://install-override?url=https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_override_ipv6-1_dns-0.stoverride) - 启用 IPv6，不配置 DNS
  - [一键导入 Stash_override_ipv6-0_dns-0.stoverride](https://intradeus.github.io/http-protocol-redirector?r=stash://install-override?url=https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_override_ipv6-0_dns-0.stoverride) - 禁用 IPv6，不配置 DNS

**配置文件 (.yaml)**
  - [Stash_config_full.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_config_full.yaml) - 启用 IPv6 版本 ⭐ 推荐
  - [Stash_config_full_no_ipv6.yaml](https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Stash/Stash_config_full_no_ipv6.yaml) - 禁用 IPv6 版本


### Surge

**配置文件 (.conf)**
  - [一键导入 Surge_config.conf](https://intradeus.github.io/http-protocol-redirector?r=surge:///install-config?url=https%3A%2F%2Fraw.githubusercontent.com%2Fluluape%2FProxyRules%2Fmain%2FConfig%2FSurge%2FSurge_config.conf) - 启用 IPv6 版本 ⭐ 推荐
  - [一键导入 Surge_config_no_ipv6.conf](https://intradeus.github.io/http-protocol-redirector?r=surge:///install-config?url=https%3A%2F%2Fraw.githubusercontent.com%2Fluluape%2FProxyRules%2Fmain%2FConfig%2FSurge%2FSurge_config_no_ipv6.conf) - 禁用 IPv6 版本

### Loon

**配置文件 (.lcf)**
- 点击以下链接直接导入到 Loon（推荐）：
  - [一键导入 Loon_config.lcf](https://intradeus.github.io/http-protocol-redirector?r=loon://import?sub=https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Loon/Loon_config.lcf) - 启用 IPv6 版本 ⭐ 推荐
  - [一键导入 Loon_config_no_ipv6.lcf](https://intradeus.github.io/http-protocol-redirector?r=loon://import?sub=https://raw.githubusercontent.com/luluape/ProxyRules/main/Config/Loon/Loon_config_no_ipv6.lcf) - 禁用 IPv6 版本

**使用方法：**
1. 下载配置文件到本地
2. 在 Loon 中导入下载的配置文件
3. 选择下载的 `.lcf` 文件，并在 Loon 中按其支持的方式添加节点或订阅。



## WireGuard / EasyTier 扩展

本仓库还提供 EasyTier 相关的 WireGuard 配置扩展，
用于 Mihomo 和 Surge。该功能独立于五客户端主配置。

| 客户端 | 扩展配置 | 说明 |
|---|---|---|
| Mihomo | [EasyTier 转换脚本](Wireguard_Easytier/Mihomo/mihomo_convert_args.js) | 在订阅转换结果中添加 EasyTier 节点和相关路由 |
| Surge | [Easytier.sgmodule](Wireguard_Easytier/Surge/Easytier.sgmodule) | Surge 独立模块，添加 EasyTier WireGuard 节点与路由 |

详细参数配置及使用方法请参阅
[EasyTier 使用说明](Wireguard_Easytier/README.md)。

**注意：** 使用前需要根据实际组网环境填写 WireGuard 参数。
不要直接修改自动生成的文件。

## 分流策略

本仓库包含以下分流策略组：

### 规则列表

| 策略组 | 包含的规则 |
|--------|-----------|
| AI | AI |
| Telegram | Telegram |
| YouTube | YouTube, YouTubeMusic |
| Netflix | Netflix |
| TikTok | TikTok |
| Spotify | Spotify |
| Steam | Steam |
| Game | Game, Playhorny, Nikke |
| E-Hentai | E-Hentai |
| PornSite | PornSite, Furrybar |
| US Media | Stream\_US |
| Taiwan Media | Stream\_TW |
| Japan Media | Stream\_JP |
| Global Media | Stream\_Global |
| Apple | Apple |
| Microsoft | Microsoft |
| Google | Google |
| Google FCM | GoogleFCM |
| Sogou Privacy | SogouPrivacy |
| ADBlock | ADBlock |
| 直接连接 | LocalNetwork, LocalNetworkIP |

### 节点组

| 名称 | 说明 |
|------|------|
| 香港节点 | HongKong |
| 台湾节点 | Taiwan |
| 新加坡节点 | Singapore |
| 美国节点 | Unite State |
| 日本节点 | Japan |
| 其他节点 | 其他地区节点 |

## 自定义规则

规则定义完全由 `Base/Rules/RemoteRules.yaml` 驱动，**无需修改 Go 代码**。

文件分为两个区域：

- **`BaseRules`**：基础规则集，每条包含完整的 `policyname`（策略组归属）、`tagname`（展示名）
- **`CustomRules`**：自定义规则，通过 `parenttag` 归入已有策略组（如 Playhorny 的 `parenttag: "Game"` 使其归入 Game）

### 新增一条规则

在 `CustomRules` 下添加：

```yaml
CustomRules:
  MyRule:
    name: "MyRule"
    category: "Higanoneko"              # 规则源分类，对应 RemoteRulesLinkBase.yaml
    behavior: "classical"             # domain / classical / ip
    remotefile: "./MyRule/MyRule.list" # 远程规则文件路径
    parenttag: "Game"                # 归入 Game 策略组
```

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | 是 | 规则显示名称 |
| `category` | 是 | 规则源分类，对应 `RemoteRulesLinkBase.yaml` 中的 Categories |
| `behavior` | 是 | `domain` / `classical` / `ip` |
| `remotefile` | 是 | 远程规则文件路径，拼接基础 URL 形成完整下载链接 |
| `policyname` | BaseRules 必需 | 归属的策略组名称 |
| `tagname` | 可选 | 展示标签名，默认使用 `name` |
| `parenttag` | 可选 | 父规则 RuleID，子规则继承父规则的 `policyname` |
| `surgeoption` | 可选 | Surge 专用参数（如 `extended-matching`） |

> 规则顺序与 YAML 书写顺序一致，BaseRules 在前、CustomRules 在后。

## 开发

生成器源码、`go.mod` 和内部包都位于 `program/`。

本地重新生成配置时，请在 `program/` 目录执行：

```bash
cd program
go run ./cmd/proxyrules --tool all
```

### 自动更新与发布保护

- [`Generate Config Files`](.github/workflows/auto_generate.yml)：每日定时及符合路径条件的推送触发；同步上游规则、生成配置，并在校验通过后提交更新。也支持手动运行。
- [`Validate rules and generator`](.github/workflows/pr_validate.yml)：在适用的 PR 中执行生成器及规则校验，防止有问题的变更直接进入主分支。
- [第一阶段发布保护](docs/RELEASE_GUARD.md)：检查关键产物、Egern 规则数量异常及公开订阅占位符。
- [第二阶段五客户端一致性校验](docs/PHASE2_CONSISTENCY.md)：检查策略组覆盖、规则绑定和分流顺序。

自动生成成功只说明流水线和静态校验通过，不代表任一客户端实机上的全部连接、DNS、广告拦截行为均已验证。

## 感谢

### 项目来源

本仓库基于 **Higanoneko/ProxyRules** 的原有项目结构与思路继续维护、修复和扩展。感谢原作者 Higanoneko 的工作；现有新功能和发布产物由 `luluape/ProxyRules` 独立维护。原仓库链接仅作为历史来源说明，不用作当前配置下载地址。


本仓库集成了以下优秀的规则源项目，感谢所有开发者的贡献：

### 规则源项目

- **[SukkaW/Surge](https://github.com/SukkaW/Surge)** - 提供 Telegram、流媒体、搜狗输入法等规则
- **[Cats-Team/AdRules](https://github.com/Cats-Team/AdRules)** - 提供广告拦截规则
- **[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)** - 提供 YouTube、Netflix、TikTok、Spotify、Steam、游戏、Apple、Microsoft、Google 等服务规则
- **[dler-io/Rules](https://github.com/dler-io/Rules)** - 提供 AI 服务规则

### 工具与资源

- **[MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)** - 提供 GeoIP 和 IPASN 数据库

---

**注意**：使用本仓库的配置文件前，请确保你已经配置好代理节点。配置文件中的策略组需要你手动指定对应的代理节点。
