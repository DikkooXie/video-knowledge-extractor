# 工具与操作参考

以下命令仅为单条视频示例，执行前使用独立输出目录，变量通过 shell 安全赋值，不拼接执行分享文本。工具和模型可能更新，先检查各工具 `--help`。示例适合 Apple Silicon Mac；模型名称由用户按质量和下载大小调整。

## 安装

- FFmpeg：`brew install ffmpeg`。本流程不使用 yt-dlp，无需为它安装或配置浏览器 Cookie。
- 转写：在独立 Python 虚拟环境中运行 `python -m pip install mlx-whisper`。慢网络下安装可能超过普通命令超时，应使用长超时或后台任务并检查最终退出状态，不要因长时间无输出重复安装。调用虚拟环境中的 `mlx_whisper`，或将该环境的 `bin` 加入 PATH。参考 [MLX Whisper](https://github.com/ml-explore/mlx-examples/blob/main/whisper/README.md)。首次使用模型会下载权重，不保证网络可达。
- 在项目根目录创建虚拟环境后，可使用 `.venv/bin/mlx_whisper`；不可用时检查安装输出，按实际兼容的 Python 版本创建环境。

## 获取视频

1. 将用户输入中提取的单个 URL 安全赋给 `url`，以 `--` 将 URL 与选项隔开。对于 `v.douyin.com` 短链，先按正常 HTTPS 重定向解析，确认目标为 `douyin.com` 的作品页面；不跟随到无关站点。保留原始链接和最终链接，不输出含凭据的 URL。
2. 使用 [DouK-Downloader](https://github.com/JoeanAmier/TikTokDownloader) 的交互式模式下载；其 README 描述 Python 3.12+、`pip install -r requirements.txt`、`python main.py`，选择“终端交互模式 → 批量下载链接作品 → 手动输入待采集的作品链接”。无 Cookie 时可能反复报“响应内容不是有效的 JSON 数据”，不必等待全部重试；经用户明确授权后，可从其已登录浏览器的对应域名读取 Cookie，先确认实际浏览器（例如 Edge），使用后清空本次写入的临时 Cookie 配置，不删除用户的其他配置。它不是已验证的非交互式接口，也可能失效。账号凭据应由用户自行提供，避免读取或记录；不得要求用户粘贴到对话，也不要把 Cookie 写入输出文件。将下载完成的视频放到输出目录。工具源码的许可和额外声明见其仓库；不要复制 GPL 代码到本项目。
3. DouK 不可用时，要求用户提供本地视频路径并继续；记录链接下载失败，不声称已读取视频，也不回退到 yt-dlp。

## 提取

### 首选：一次性预处理脚本

`scripts/prepare_media.py` 用一条命令完成探测、抽帧、带时间戳的 2×2 联系表和转写。设 `skill_dir` 是本技能目录的绝对路径，`whisper` 是已安装的 `mlx_whisper` 可执行文件的绝对路径，`media` 是本地视频路径，`out` 是尚不存在的输出目录：

```sh
python3 -I "$skill_dir/scripts/prepare_media.py" \
  "$media" "$out" --whisper "$whisper"
```

- 默认每 10 秒采样并补结尾；同时以 2 fps、320 像素宽扫描显著变化，添加变化时间点，最多增加 300 帧。`--scene-threshold` 调整检测阈值，`--max-change-frames` 调整上限，`--skip-change-detection` 关闭检测；`manifest.json` 记录检测数量及是否截断。变化检测无法保证捕获微小文字、渐变或短暂画面。
- `--ocr` 在 macOS 使用 Swift Vision 对采样帧做本地 OCR，生成 `ocr.json`，含文字、置信度和归一化坐标；状态记在 manifest 中。它只提供辅助线索，不自动去重或保证识别准确。结合画面及时间戳人工合并重复页，关键小字回原视频核对。首次调用 Swift 可能较慢。
- `--skip-transcription` 跳过音频转写；`--interval` 可选 5/10/15/20/30 秒。
- 输出：`probe.json`、`frames/`、`sheets/`（每张 2×2，标签显示整秒；精确秒数见 manifest）、可选 `ocr.json`、`audio.wav` 与 `audio.{srt,txt,json,tsv,vtt}`、`manifest.json`。帧文件名中的数字为毫秒。
- 脚本以 `-I` 运行，不加载工作目录下的模块；输出目录已存在时直接报错，不会覆盖既有结果。长任务放后台，用 `manifest.json` 判断完成情况。

### 回退：手工命令

脚本不可用或需要特殊采样时，可手工执行。设 `media` 是已确认的本地视频路径，当前目录为独立输出目录：

```sh
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of json -- "$media" > probe.json
ffmpeg -nostdin -i "$media" -vn -ac 1 -ar 16000 audio.wav
mlx_whisper audio.wav --model mlx-community/whisper-small-mlx \
  --language zh --initial-prompt '以下是简体中文口播，使用简体中文和常用标点。' \
  --output-dir . --output-format all
mkdir frames
for t in 0 10 20 30; do
  ffmpeg -nostdin -loglevel error -ss "$t" -i "$media" -frames:v 1 \
    -vf scale=1280:-2 -q:v 3 "frames/t$(printf '%03d' "$t").jpg"
done
```

上述仅为前 40 秒示例；按实际时长继续每 10 秒取帧，并单独补采接近结尾的一帧（`-ss` 小于总时长），确保覆盖开头、中间、结尾。用 `-ss <秒>` 定位、以实际秒数命名，避免把 `fps` 抽帧的序号误当时间。逐张查看即可；需要减少图片读取次数时，将四张连续帧按时间顺序拼成 2×2 联系表，并在文档中记录每格时间，不能只按文件序号推断。例如已有 `t000.jpg`、`t010.jpg`、`t020.jpg`、`t030.jpg` 时：

```sh
mkdir -p sheets
ffmpeg -nostdin -loglevel error \
  -i frames/t000.jpg -i frames/t010.jpg -i frames/t020.jpg -i frames/t030.jpg \
  -filter_complex '[0:v][1:v]hstack[top];[2:v][3:v]hstack[bottom];[top][bottom]vstack' \
  -frames:v 1 -q:v 3 sheets/sheet01-t000.jpg
```

需要读取界面小字、数字或提示词卡片时，回到原视频按准确秒数导出原分辨率帧，再裁剪对应区域放大查看；1280 px 缩略帧不足以确认小字。保留 `cards/` 等证据图。10 秒采样会漏掉短暂画面，不能声称已看到采样点之间的全部变化。

Whisper 的 small 模型可能出现较多同音字错误，还可能把开头较长一段合并为单个时间戳。烧录字幕可用来校正人名、术语和数字，但须注明依据，不能无依据地润色原话。音频缺失时跳过转写；对静态画面无法识别的信息明确标记未知。若环境没有图像查看能力，应保留关键帧并说明。

`mlx_whisper` 的参数和安装说明以所安装版本的 `mlx_whisper --help` 为准；模型权重和工具许可需分别检查。模型下载失败时，记录网络错误并检查网络配置；若已有兼容的本地 MLX Whisper 模型目录，可在确认命令行支持后以该目录替换 `--model` 的值。不要默认为本地工具已安装或已取得视频内容。

## 成本与空间控制

单条 7 分钟视频的实测（Opus 级别模型，含 1 小时缓存）约为 8–9 美元等值，其中缓存写入占大头，输出只占约 1 美元。省钱的关键不是少做事，而是**不要重复把同一批图片和长文放进上下文**。

- **一次性预处理**：用 `scripts/prepare_media.py` 一次生成全部素材，避免逐条命令、逐张图片来回试错。
- **低清通读**：按 60–90 秒分段，每段只读一张 2×2 联系表加对应转写，读完立刻写成带时间戳的简短笔记；之后只汇总笔记，不重新加载图片或完整逐字稿。
- **定向高清**：只有提示词卡片、界面小字、数字、术语和存疑片段才回原视频导出原分辨率局部裁剪。看清后把文字写进笔记，同一张图不重复读。
- **不逐句润色**：只对明显同音字、专有名词、数字和关键结论触发字幕/画面校对；普通口播按转写原文记录。
- **不扩大采样间隔**：省钱的手段是减少重复读取，不是降低采样密度导致漏掉关键卡片。

## 素材保留与清理

第 2 步已向用户确认保留方式。清理时遵守：

| 选择 | 保留 | 删除 |
| --- | --- | --- |
| 文档和关键配图（默认） | `document.md`、正文引用的 `images/` 配图 | 本次任务生成的视频副本、`audio.*`、`probe.json`、`ocr.json`、`frames/`、`sheets/`、`cards/`、`manifest.json`；用户要求纯文字时也不保留配图 |
| 保留文档和文字资料 | `document.md`、正文引用的 `images/` 配图、`evidence.md`、相关的 `prompts.md`、字幕/转写文本 | 视频副本、音频、`probe.json`、`frames/`、`sheets/`、`cards/`、其他任务临时文件 |
| 保留全部资料 | 全部 | 无 |

安全规则：

1. 只删除**本次任务明确创建**的文件，删除前先列出完整路径和大小，让用户能看见范围。
2. 永远不删除、不覆盖用户提供的原始本地视频；如果 `media` 在输出目录之外，一律不动。
3. 不递归删除共享目录或上级目录，不对 `douyin-output/` 整体执行清理；逐条列出路径删除。
4. 先验证 `document.md` 存在且非空、时间戳在时长内，每张正文配图存在、可打开且与时间点和说明相符，文档中没有指向将被删除文件的引用，再清理。文档必须自包含必要证据（关键画面文字、时间点、术语），不能写“见 frames/t0120.jpg”这类清理后失效的引用。保留正文引用的 `images/` 文件，不将其作为临时帧清理。
5. 转写或视觉步骤失败时，清理会让失败部分无法复核，先请用户确认再删。
6. 清理失败或部分失败要如实报告；回复中列出实际保留和删除的素材。
