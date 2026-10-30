# Video Knowledge Extractor

将视频整理为有时间戳、可追溯的知识文档。当前仓库提供一个 **抖音单视频 / 本地视频 skill** 和媒体预处理脚本；跨平台入口、知识库检索和双链整合仍处于设计阶段，详见 [设计方案](DESIGN.md)。

## 当前能力

- 通过单个抖音分享链接或本地视频启动 agent 工作流；抖音下载使用单独安装的 DouK-Downloader。
- 本地提取音频、转写、固定间隔及画面变化抽帧，生成带时间戳的联系表；macOS 上可选 Vision OCR。
- 由 agent 结合转写和画面整理文档、核对重要事实并挑选少量配图。脚本负责预处理，并不独立生成完整知识文档。
- 支持选择素材保留方式，保护用户提供的原始本地文件。

## 使用

在支持 Claude Code 项目级 skills 的环境中打开本仓库，使用 `/douyin-knowledge-extractor` 并提供单条抖音链接或本地视频路径。流程和限制见 [SKILL.md](.claude/skills/douyin-knowledge-extractor/SKILL.md)，安装与具体命令见 [TOOLS.md](.claude/skills/douyin-knowledge-extractor/TOOLS.md)。

预处理需要 FFmpeg、ffprobe 和 Python；默认的 MLX Whisper 转写面向 Apple Silicon Mac，可选 OCR 需要 macOS 和 Swift。抖音链接下载另需安装 DouK-Downloader，平台访问与登录状态可能变化。模型初次使用可能下载权重；第三方工具及模型分别受其自身许可约束。

下载素材、转写和知识库内容可能包含个人信息。默认在本地处理，未经授权不上传；请勿将素材、凭据或私人输出提交至仓库。生成的处理清单可能包含本地媒体的绝对路径。

## 规划

[DESIGN.md](DESIGN.md) 介绍主 skill、平台获取、通用处理和知识库整合的边界、数据契约、隐私规则和实施路线。欢迎在此基础上讨论；该文档描述的是方案，并不表示规划功能已经实现。

## 许可证

本项目采用 [MIT License](LICENSE)。外部下载工具、FFmpeg、转写工具及模型权重分别适用其自身许可，本仓库不包含这些第三方工具或模型。
