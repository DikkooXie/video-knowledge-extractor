# 抖音链接解析、登录与个人收藏采集调研

查询日期：2026-10-29（CST）。范围为抖音中国版，覆盖公开的一手仓库、源码、发布记录、GitHub API 与抖音开放平台资料。本文另补充与知识提取相关的转写、OCR 候选。GitHub 指标是查询时的快照，`pushed_at` 为仓库最后推送时间，不等同于默认分支最后提交时间；开放 issue 数包含 GitHub API 统计的开放 issue/PR。数量、接口与条款均可能变化。

## 结论与证据边界

1. **链接解析与收藏采集有候选实现，但未验证当前可用。** Mintnoii 的下载器 README 声称支持短链、浏览器扫码登录、当前登录账号的收藏夹和同步；dousub 声称提供扫码、视频下载及收藏列表，源码可见浏览器网络响应监听和滚动。DouK-Downloader 功能广、活跃度高，但其 5.6 发布记录明确禁用扫码登录，当前 README 还称不再维护加密参数算法。三者均非抖音官方能力。[Mintnoii README](https://github.com/Mintnoii/DouYin-Downloader/blob/master/README.md)、[dousub README](https://github.com/debiaoyu/dousub/blob/master/README.md)、[dousub 源码](https://github.com/debiaoyu/dousub/blob/master/dousub/core/browser.py)、[DouK README](https://github.com/JoeanAmier/TikTokDownloader/blob/master/README.md)、[5.6 发布记录](https://github.com/JoeanAmier/TikTokDownloader/releases/tag/5.6)。
2. **官方扫码授权不等于网站 Cookie，也不自动授予收藏权限。** 官方网站应用文档的搜索索引描述 OAuth 授权码流程；本次检索没有发现明确可读取个人收藏视频列表的官方接口。未找到不等于证明不存在；已找到的作者视频列表及视频数据能力不能替代个人收藏列表。[网站授权](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/sdk/web-app/web/permission)、[作者视频列表](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/server/reach-marketing/mount/self_mount/get-user-video-list)、[视频数据](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/server/basic-abilities/video-id-convert/user-recent-video-data/get-basic-data)。
3. **本次没有功能实测。** 没有登录账号、扫描二维码、访问私人收藏、运行下载器、抓取视频、验证解析/分页完整性或转写质量。所有功能判断是资料声明或静态源码观察；数值是只读查询所得，不能推断生产稳定性。

## 一手来源与访问局限

GitHub 仓库 README、源文件、发布记录和仓库元数据通过 GitHub 官方 API 读取；附链接指向仓库原文。公开页面直接抓取工具对 GitHub 和 `developer.open-douyin.com` 均报域名安全验证失败。官方能力部分因此仅依据指向抖音官方文档的搜索索引摘要，**未能直接检查完整正文、最新权限清单、配额、申请条件或错误码**；具体接口实际开放状态需在开放平台控制台及完整文档再次确认。未使用第三方文章作证据。也未登录开放平台，无法核验特定主体、应用或账号的资质。

## 开源候选对照

| 仓库 | 查询时许可证 | Stars / forks / 开放 issue | 最后推送 UTC；归档 | 对任务的关联 |
|---|---|---|---|---|
| [Mintnoii/DouYin-Downloader](https://github.com/Mintnoii/DouYin-Downloader) | GitHub API 识别 MIT；[LICENSE](https://github.com/Mintnoii/DouYin-Downloader/blob/master/LICENSE) | 3 / 0 / 0 | 2026-07-03 09:27:01；否 | README 声称短链、扫码或手机号、收藏夹列表和下载、定时同步 |
| [debiaoyu/dousub](https://github.com/debiaoyu/dousub) | README 写 MIT；API 返回 null，根目录未见独立 LICENSE，且 README 附非商业免责声明，**授权范围存在不确定性** | 0 / 0 / 0 | 2026-05-13 00:10:22；否 | README 声称扫码、分享链接下载、收藏列表、OCR 和 SDK |
| [JoeanAmier/TikTokDownloader / DouK-Downloader](https://github.com/JoeanAmier/TikTokDownloader) | GitHub API 识别 GPL-3.0；[许可证](https://github.com/JoeanAmier/TikTokDownloader/blob/master/LICENSE)；README 另附声明，复用前需一并审阅 | 17,190 / 2,854 / 48 | 2026-10-27 16:07:23；否 | README 声称链接批量下载、本人收藏及收藏夹、数据导出；历史扫码已禁用 |
| [jiji262/douyin-downloader](https://github.com/jiji262/douyin-downloader) | GitHub API 识别 MIT | 12,474 / 1,908 / 32 | 2026-10-14 11:30:46；否 | 相关原项目；README 中含其他平台功能，应针对具体版本逐项核验 |

另有 [tz-yang/douyin](https://github.com/tz-yang/douyin)，GitHub API 识别 MIT，3 stars、1 fork、0 个开放 issue，最后推送 2026-06-24 00:56:59 UTC，未归档。[README](https://github.com/tz-yang/douyin/blob/main/README.md) 声称支持短链、已登录账号的 `collect` / `collectmix`；收藏模式须单独使用且不支持增量截断，登录后保存 Cookie。其 README 与上述下载器内容相近，不能据此推断独立实现或可靠性；尚未深入核查源码或实测。[API](https://api.github.com/repos/tz-yang/douyin)

数据源：[Mintnoii API](https://api.github.com/repos/Mintnoii/DouYin-Downloader)、[dousub API](https://api.github.com/repos/debiaoyu/dousub)、[DouK API](https://api.github.com/repos/JoeanAmier/TikTokDownloader)、[jiji262 API](https://api.github.com/repos/jiji262/douyin-downloader)。星标只反映关注度，不证明质量或可用性。

### Mintnoii/DouYin-Downloader

- **声明：** 支持 `v.douyin.com` 等短链、视频和图文，Playwright 打开浏览器由用户扫码或手机号登录并保存 Cookie；`--list-collections`、`--collect` 和 `--sync` 面向收藏夹。README 声称可输出元数据和本地或远程转写。[README](https://github.com/Mintnoii/DouYin-Downloader/blob/85b4e77cfeb530b2994ae9332a91ad23061e759c/README.md)
- **明确限制：** 收藏及收藏合集仅针对 Cookie 当前登录账号；收藏模式须单独使用；README 说收藏不支持增量截断，浏览器翻页兜底仅对 `post` 完整验证。其 Cookie 过期时间及平台翻页行为是作者经验性声明，不能当作保证。
- **来源关系：** 该仓库 README 仍大量引用 jiji262 项目，GitHub API 的 `fork` 为 false；不能单凭 README 断言官方 fork 或现有同步关系。核查时默认分支提交为 `85b4e77cfeb530b2994ae9332a91ad23061e759c`。[API](https://api.github.com/repos/Mintnoii/DouYin-Downloader)、[提交](https://github.com/Mintnoii/DouYin-Downloader/commit/85b4e77cfeb530b2994ae9332a91ad23061e759c)。

### dousub

- **声明：** 提供 `login`、`download`、`favorites --json` 和 `get_favorites()`；下载通过 Playwright 打开页面获取视频地址，收藏示例包含标题和 URL。[README](https://github.com/debiaoyu/dousub/blob/6ad608f6ac29592d632ab092c9ba57975376cc80/README.md)
- **静态源码观察：** `qr_login_async` 获取网页二维码并等待登录 Cookie；`get_favorites_async` 监听含 `/aweme/v1/web/aweme/listcollection/` 的响应，并滚动直到连续多次无新增。这是网页行为实现，不是官方开放 API 承诺；停止滚动不能证明收藏无遗漏。[源码](https://github.com/debiaoyu/dousub/blob/6ad608f6ac29592d632ab092c9ba57975376cc80/dousub/core/browser.py)
- **许可与限制：** README 写 MIT，但仓库根目录没有独立 LICENSE，GitHub API 未识别许可证；README 同时声明不得用于商业用途。应请权利人澄清，不应把它直接视为已确认可商用 MIT 代码。[根目录](https://github.com/debiaoyu/dousub/tree/master)、[README](https://github.com/debiaoyu/dousub/blob/master/README.md)。零星标及有限历史不能说明可维护性。

### DouK-Downloader

- **声明：** 可采集链接、账号喜欢/收藏/收藏夹作品，保存 CSV、XLSX、SQLite；收藏模式仅支持当前 Cookie 账号，喜欢/收藏数据返回作品发布日期而非操作日期；大量结果需全量获取后过滤。当前 README 指出 Web UI 尚未更新。[README](https://github.com/JoeanAmier/TikTokDownloader/blob/473c90ff70c663cfb69310fff2b8d5192f200661/README.md)
- **扫码与平台变化：** 5.6 发布说明明确“禁用扫码登录功能”；当前源码中的扫码菜单项被注释，README 指导手动或剪贴板输入 Cookie。作者称加密参数算法不再维护，可能因平台变化失效。项目[发布记录](https://github.com/JoeanAmier/TikTokDownloader/releases)提及收藏下载，而[用户 issue #794](https://github.com/JoeanAmier/TikTokDownloader/issues/794)报告收藏获取失败：这是个别用户反馈，不证明所有环境均失效，但体现了需要按版本、账号和时间实测。[5.6](https://github.com/JoeanAmier/TikTokDownloader/releases/tag/5.6)、[源码](https://github.com/JoeanAmier/TikTokDownloader/blob/master/src/application/TikTokDownloader.py)、[README](https://github.com/JoeanAmier/TikTokDownloader/blob/master/README.md)。
- **许可：** API 和仓库 LICENSE 标识 GPL-3.0；README 另列免责声明及使用限制。分发、组合或商业用途前应核对具体 LICENSE 和声明，必要时咨询权利人；不要把 GPL 组件当作 MIT 代码直接复制。

## 官方能力与差异

| 场景 | 本次查到的一手官方资料 | 边界 |
|---|---|---|
| 网站扫码登录 | [网站应用授权](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/sdk/web-app/web/permission) 的搜索索引描述用户扫码确认、回调授权码，再换 token；[登录授权概述](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/sdk/mobile-app/permission/overall-permission)描述 OAuth 授权码 | 应用准入、回调、权限 scope 等以可访问的当前完整文档和控制台为准；本次没有实测 token 或扫码 |
| 作者作品列表 | [作者视频列表](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/server/reach-marketing/mount/self_mount/get-user-video-list)的搜索索引描述授权作者视频列表；另有[账号视频列表](https://open.douyin.com/platform/resource/docs/openapi/video-management/douyin/search-video/account-video-list)文档 | 前者面向特定小程序/挂载场景；这些资料均不能证明存在获取用户收藏视频列表的接口。账号视频列表正文及实际权限尚未直接核验 |
| 视频数据 | [近期视频基础数据](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/server/basic-abilities/video-id-convert/user-recent-video-data/get-basic-data) 索引描述小程序申请 `ma.item.data`、用户授权、近 30 天作品数据 | 面向指定授权及业务场景；不能据此推断通用链接解析、视频文件下载或收藏列表能力 |
| 收藏列表 | 用“收藏视频列表”“接口”等检索官方域名，未发现明确接口文档 | 这是本次检索结果，不是穷尽性证明；可能有未索引、需登录、特定合作方或后来变更的能力 |

开发者论坛中有用户讨论旧视频列表接口失效及替代权限，但讨论并非平台正式能力清单，不能用作当前可用性结论。[官方论坛讨论](https://developer.open-douyin.com/forum/question/post/6a9ab2de2c8e05501d04dc30)。应向平台核实当前应用类型、可申请 scope、数据对象、下载授权、配额和审核条件。

第三方浏览器方案依赖用户在抖音网页登录后的会话 Cookie，可能受网页结构、反自动化策略、会话过期和网络环境影响。OAuth token 是开放平台授予的受限凭证，不能假设它可替代网页 Cookie。会话文件应视为账号凭证，限制读取、避免写入日志、提供退出和删除机制；[Playwright 官方认证状态文档](https://playwright.dev/docs/auth)也提醒状态文件可能含敏感 Cookie 和请求头。

## 面向知识提取的补充候选

以下仅依据项目的一手仓库描述和 GitHub API 元数据，均未安装或运行，模型许可证及依赖许可证需要单独检查。

| 项目 | 仓库许可证 | Stars / forks / 开放 issue | 最后推送 UTC；归档 | 声明能力与注意点 |
|---|---|---|---|---|
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | MIT | 26,280 / 2,186 / 18 | 2026-10-25 07:17:13；否 | 基于 CTranslate2 的 Whisper 推理；速度、硬件及量化效果须按实际模型和机器评估 |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | Apache-2.0 | 91,921 / 11,584 / 262 | 2026-09-16 03:31:50；否 | 文字检测与识别；抽帧会遗漏快速切换文字，去重、排版和图文识别仍需设计 |
| [WhisperX](https://github.com/m-bain/whisperX) | BSD-2-Clause | 24,920 / 2,508 / 214 | 2026-10-22 14:53:44；否 | 声称语音识别、词级对齐及说话人分离；对齐模型和说话人分离模型可能有独立条款和访问条件 |

指标来源：[faster-whisper API](https://api.github.com/repos/SYSTRAN/faster-whisper)、[PaddleOCR API](https://api.github.com/repos/PaddlePaddle/PaddleOCR)、[WhisperX API](https://api.github.com/repos/m-bain/whisperX)。[MLX Whisper 示例](https://github.com/ml-explore/mlx-examples/blob/main/whisper/README.md)也可作为 Apple Silicon 候选，支持词级时间戳，Hugging Face 模型可自动下载；本机 `uname -m` 输出为 `arm64`；未核实处理器型号、性能或模型许可，也未调查该项目指标，不作为已验证方案。实施时应固定并记录工具版本和模型，勿假定默认模型一致。faster-whisper 的 CTranslate2 支持 arm64 CPU，而其上游 GPU 支持为 NVIDIA CUDA，不应据此承诺 Metal 加速；参见 [CTranslate2 硬件支持](https://opennmt.net/CTranslate2/hardware_support.html)。PaddleOCR 的 macOS 条件应按其[官方 FAQ](https://www.paddleocr.ai/main/en/FAQ.html)及所选版本核对，以上均未在本机实测。

转写无法保证方言、背景音乐、多说话人、专有名词的准确性；OCR 依赖画面清晰度、字幕停留时间及语言，口播和画面各自可能包含独有信息。时间戳应保留来源、起止时间和原始内容，模型总结附指向片段的证据，避免把生成内容当作原话；无音频、纯图文、失效链接和识别失败应有显式状态。

## 建议的验证与实施顺序

1. 先以用户主动提供的单条分享链接为输入，分别记录解析后的作品标识、规范链接、标题、可用媒体和失败原因；区分视频与图文。真实账号访问、下载或任何采集均须另行获得授权；本次没有执行。
2. 将官方 OAuth 与本地浏览器登录设计为不同适配器。优先核实开放平台是否允许所需对象和用途；网页会话方案需明确用户授权、平台规则、凭证保存及失效处理。
3. 若获授权验证本人收藏，准备已知数量且包含多个文件夹、视频、图文及失效项的测试集；对照网页计数检查分页、去重、遗漏、权限错误及恢复。采集结果标明获取时间、账号范围和不完整状态；不能把滚动停止当作全量证明。
4. 逐步建立 CLI：链接输入及元数据 → 经过授权的素材处理 → 转写/OCR 与时间戳 → 可追溯的结构化笔记 → 收藏批处理。各阶段输出明确成功、跳过、失败和来源；对已知样本人工对照关键词、关键时间点及漏项，报告质量而非仅报告执行成功。
5. 选型前复核仓库最新提交、许可证及依赖、平台条款、内容版权和个人数据处理范围；保留替换采集适配器的能力，避免依赖任何单一未公开网页接口。
