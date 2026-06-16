from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence


ROOT = Path(__file__).resolve().parent


def _find_node_exe() -> Optional[Path]:
    """Locate node.exe from PATH or well-known install locations."""
    # 1. Check if node/nodejs is already on PATH
    for cmd in ("node", "nodejs", "node.exe"):
        found = shutil.which(cmd)
        if found:
            return Path(found)

    # 2. Search well-known locations (WorkBuddy managed runtime first)
    candidates = [
        Path.home() / ".workbuddy" / "binaries" / "node" / "versions",
        Path(os.environ.get("APPDATA", "")) / ".." / ".workbuddy" / "binaries" / "node" / "versions",
        Path("C:/Program Files/nodejs"),
        Path("C:/Program Files (x86)/nodejs"),
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "nodejs",
    ]
    for base in candidates:
        try:
            base = base.resolve()
        except Exception:
            pass
        if not base.is_dir():
            continue
        # Versions sub-directory (e.g. 22.12.0/)
        for child in sorted(base.iterdir(), reverse=True):
            exe = child / "node.exe"
            if exe.is_file():
                return exe
        # Direct directory
        exe = base / "node.exe"
        if exe.is_file():
            return exe
    return None


def _patch_execjs_node_runtime() -> None:
    """Patch execjs to use the absolute path of node.exe.

    execjs on Windows looks for 'nodejs' in PATH which is often missing.
    We locate node.exe and override the runtime command to use the full path
    so execjs works regardless of PATH configuration.
    """
    node_exe = _find_node_exe()
    if not node_exe:
        print("[startup] WARNING: node.exe not found; execjs JS runtime may fail.")
        return

    node_exe_str = str(node_exe)
    node_dir_str = str(node_exe.parent)

    # Always inject the node directory into PATH (needed for subprocess calls within execjs)
    current_path = os.environ.get("PATH", "")
    if node_dir_str.lower() not in current_path.lower():
        os.environ["PATH"] = node_dir_str + os.pathsep + current_path
        print(f"[startup] Added Node.js dir to PATH: {node_dir_str}")

    try:
        import execjs._runtimes as runtimes

        for _name, rt in runtimes._runtimes:
            if _name == "Node" and hasattr(rt, "_command"):
                rt._command = [node_exe_str]
                rt._binary_cache = [node_exe_str]
                rt._available = True
                break
        print(f"[startup] execjs Node runtime patched to: {node_exe_str}")
    except Exception as exc:
        print(f"[startup] execjs patch skipped ({exc}), relying on PATH.")


# Patch execjs immediately so it can find Node.js regardless of PATH
_patch_execjs_node_runtime()


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the Spider_XHS product platform.")
    parser.add_argument("--host", default="127.0.0.1", help="Backend host.")
    parser.add_argument("--port", type=int, default=8000, help="Backend port.")
    parser.add_argument("--reload", action="store_true", help="Enable Uvicorn reload.")
    parser.add_argument("--with-frontend", action="store_true", help="Also start the frontend Vite dev server.")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Frontend dev server port.")
    return parser.parse_args(argv)


def resolve_npm_executable() -> str:
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        raise FileNotFoundError("npm was not found on PATH; install Node.js or start the frontend manually.")
    return npm


def build_frontend_command(port: int, npm_executable: Optional[str] = None) -> list[str]:
    npm = npm_executable or resolve_npm_executable()
    return [npm, "run", "dev", "--", "--host", "127.0.0.1", "--port", str(port)]


def start_frontend(port: int) -> Optional[subprocess.Popen]:
    frontend_dir = ROOT / "frontend"
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("frontend/package.json not found; skipping frontend startup.")
        return None

    command = build_frontend_command(port)
    print(f"Starting frontend at http://127.0.0.1:{port}")
    return subprocess.Popen(command, cwd=str(frontend_dir))


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    # Resolve host/port: CLI args take precedence, then YAML/env config defaults
    host = args.host
    port = args.port
    try:
        from backend.app.core.config import get_settings
        settings = get_settings()
        # Use config values only when CLI args are at their defaults
        if host == "127.0.0.1" and settings.server_host:
            host = settings.server_host
        if port == 8000 and settings.server_port:
            port = settings.server_port
    except Exception:
        pass

    frontend_process = start_frontend(args.frontend_port) if args.with_frontend else None

    print(f"Starting backend at http://{host}:{port}")
    try:
        import uvicorn

        uvicorn.run("backend.app.main:app", host=host, port=port, reload=args.reload)
    finally:
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
