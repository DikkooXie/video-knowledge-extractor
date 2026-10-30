#!/usr/bin/env python3
"""Prepare one local video for evidence-based, low-context analysis."""

import argparse
import json
import math
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys


def run(command):
    subprocess.run(command, check=True)


def run_media_tool(executable, arguments):
    # Run from the script's trusted project, not from downloaded media/output.
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run([executable, *arguments], check=True,
                   cwd=Path(__file__).resolve().parents[3], env=env)


def timestamp_label(second, path):
    """Write a dependency-free PGM timestamp; FFmpeg need not have drawtext."""
    segments = (
        "abcdef", "bc", "abged", "abgcd", "fgbc",
        "afgcd", "afgecd", "abc", "abcdefg", "abfgcd",
    )
    positions = {
        "a": (2, 0, 4, 1), "b": (6, 1, 1, 5), "c": (6, 7, 1, 5),
        "d": (2, 12, 4, 1), "e": (0, 7, 1, 5), "f": (0, 1, 1, 5),
        "g": (2, 6, 4, 1),
    }
    width, height = 1280, 180
    pixels = bytearray(width * height)
    scale = 6

    def rectangle(x, y, w, h):
        for row in range(y, y + h):
            start = row * width + x
            pixels[start:start + w] = b"\xff" * w

    for index, char in enumerate(f"{int(second) // 60:02d}:{int(second) % 60:02d}"):
        x = 28 + index * 110
        if char == ":":
            rectangle(x + 24, 84, 16, 16)
            rectangle(x + 24, 124, 16, 16)
        else:
            for segment in segments[int(char)]:
                px, py, pw, ph = positions[segment]
                rectangle(x + px * scale, 30 + py * scale, pw * scale, ph * scale)
    path.write_bytes(f"P5\n{width} {height}\n255\n".encode() + pixels)


def frame_name(second):
    return f"t{round(second * 1000):09d}.jpg"


def detect_changes(media, threshold):
    result = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", str(media),
         "-vf", f"fps=2,scale=320:-2,scdet=threshold={threshold},metadata=mode=print:key=lavfi.scd.time:file=-",
         "-an", "-f", "null", "-"], check=True, capture_output=True, text=True,
    )
    return [float(value) for value in re.findall(r"lavfi\.scd\.time=([0-9.]+)", result.stdout)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--whisper", default="mlx_whisper")
    parser.add_argument("--model", default="mlx-community/whisper-small-mlx")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--interval", type=int, default=10, choices=(5, 10, 15, 20, 30))
    parser.add_argument("--skip-transcription", action="store_true")
    parser.add_argument("--scene-threshold", type=float, default=10.0)
    parser.add_argument("--skip-change-detection", action="store_true")
    parser.add_argument("--max-change-frames", type=int, default=300)
    parser.add_argument("--ocr", action="store_true", help="Run local macOS Vision OCR on sampled frames")
    args = parser.parse_args()

    media = args.media.expanduser().resolve(strict=True)
    if not media.is_file():
        parser.error("media must be a file")
    output = args.output.expanduser().resolve()
    if output.exists():
        parser.error("output directory must not already exist")
    if media == output or output in media.parents:
        parser.error("output must not contain the source media")
    for executable in ("ffmpeg", "ffprobe"):
        if not shutil.which(executable):
            parser.error(f"missing executable: {executable}")
    if not args.skip_transcription and not shutil.which(args.whisper):
        parser.error(f"missing executable: {args.whisper}")

    output.mkdir(parents=True)
    frames = output / "frames"
    sheets = output / "sheets"
    frames.mkdir()
    sheets.mkdir()

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height,r_frame_rate",
         "-of", "json", "--", str(media)],
        check=True, capture_output=True, text=True,
    )
    (output / "probe.json").write_text(probe.stdout)
    metadata = json.loads(probe.stdout)
    duration = float(metadata["format"]["duration"])
    has_audio = any(s.get("codec_type") == "audio" for s in metadata.get("streams", []))

    if args.max_change_frames < 0 or not 0 <= args.scene_threshold <= 100:
        parser.error("invalid change detection threshold or frame limit")
    times = list(range(0, math.floor(duration), args.interval))
    last = max(0, math.floor(duration) - 1)
    if last not in times:
        times.append(last)
    changes = [] if args.skip_change_detection else detect_changes(media, args.scene_threshold)
    eligible = [t for t in changes if 0 <= t < duration and all(abs(t - x) >= 0.5 for x in times)]
    truncated = len(eligible) > args.max_change_frames
    if truncated and args.max_change_frames:
        selected = [eligible[i * len(eligible) // args.max_change_frames]
                    for i in range(args.max_change_frames)]
    else:
        selected = eligible[:args.max_change_frames]
    times = sorted(set(times + selected))
    for second in times:
        run([
            "ffmpeg", "-nostdin", "-loglevel", "error", "-ss", str(second),
            "-i", str(media), "-frames:v", "1", "-vf", "scale=1280:-2",
            "-q:v", "3", str(frames / frame_name(second)),
        ])

    layouts = {
        1: "0_0", 2: "0_0|w0_0",
        3: "0_0|w0_0|0_h0", 4: "0_0|w0_0|0_h0|w0_h0",
    }
    manifest = []
    for start in range(0, len(times), 4):
        group = times[start:start + 4]
        commands = []
        filters = []
        cells = []
        for index, second in enumerate(group):
            label_path = output / f".label-{round(second * 1000):09d}.pgm"
            timestamp_label(second, label_path)
            commands.extend(["-i", str(frames / frame_name(second))])
            commands.extend(["-i", str(label_path)])
            label = f"l{index}"
            cell = f"c{index}"
            filters.extend([
                f"[{index * 2 + 1}:v]format=rgb24[{label}]",
                f"[{index * 2}:v][{label}]vstack[{cell}]",
            ])
            cells.append(f"[{cell}]")
        if len(group) == 1:
            filters.append(f"{cells[0]}null[out]")
        else:
            filters.append(
                "".join(cells) +
                f"xstack=inputs={len(group)}:layout={layouts[len(group)]}[out]"
            )
        name = f"sheet{start // 4 + 1:03d}-t{round(group[0] * 1000):09d}.jpg"
        run([
            "ffmpeg", "-nostdin", "-loglevel", "error", *commands,
            "-filter_complex", ";".join(filters), "-map", "[out]",
            "-frames:v", "1", "-q:v", "3", str(sheets / name),
        ])
        manifest.append({"sheet": f"sheets/{name}", "seconds": group})
        for second in group:
            (output / f".label-{round(second * 1000):09d}.pgm").unlink()

    if has_audio and not args.skip_transcription:
        run([
            "ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(media),
            "-vn", "-ac", "1", "-ar", "16000", str(output / "audio.wav"),
        ])
        run_media_tool(args.whisper, [
            str(output / "audio.wav"), "--model", args.model,
            "--language", args.language,
            "--initial-prompt", "以下是简体中文口播，使用简体中文和常用标点。",
            "--output-dir", str(output), "--output-format", "all",
        ])

    ocr_status = "not requested"
    if args.ocr:
        if sys.platform != "darwin" or not shutil.which("swift"):
            ocr_status = "unavailable: macOS Swift required"
        else:
            result = subprocess.run(
                ["swift", str(Path(__file__).with_name("ocr.swift")),
                 *(str(frames / frame_name(t)) for t in times)],
                capture_output=True, text=True,
                cwd=Path(__file__).resolve().parents[3],
            )
            if result.returncode:
                ocr_status = "failed: " + result.stderr[-1000:]
            else:
                ocr_data = json.loads(result.stdout)
                (output / "ocr.json").write_text(json.dumps(ocr_data, ensure_ascii=False, indent=2) + "\n")
                ocr_status = "partial failure" if any("error" in item for item in ocr_data) else "complete"

    (output / "manifest.json").write_text(json.dumps({
        "source": str(media), "duration_seconds": duration,
        "interval_seconds": args.interval, "has_audio": has_audio,
        "transcribed": has_audio and not args.skip_transcription,
        "change_detection": {"enabled": not args.skip_change_detection,
                             "fps": 2, "threshold": args.scene_threshold,
                             "detected": len(changes), "selected": min(len(eligible), args.max_change_frames),
                             "truncated": truncated},
        "ocr_status": ocr_status,
        "contact_sheets": manifest,
        "review": "Read 60-90 seconds at a time. Use original-resolution crops only for small text, numbers, terms and uncertain evidence.",
    }, ensure_ascii=False, indent=2) + "\n")
    print(f"Prepared {len(times)} frames and {len(manifest)} contact sheets in {output}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(f"Command failed with exit code {error.returncode}: {error.cmd}")
