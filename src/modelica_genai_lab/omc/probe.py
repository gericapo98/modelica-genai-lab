from __future__ import annotations
from dataclasses import dataclass
import os
import platform
import shutil
import subprocess
from typing import Optional, Sequence

@dataclass
class OmcProbeResult:
    found: bool
    exe: Optional[str]
    version: Optional[str]
    how: str
    notes: str

def _try_cmd(cmd: Sequence[str]) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=5)
        return True, out.strip()
    except Exception as e:
        return False, str(e)

def _detect_executable() -> tuple[Optional[str], str]:
    omc_env = os.environ.get("OMC") or os.environ.get("OMC_PATH")
    if omc_env and shutil.which(omc_env):
        return shutil.which(omc_env), "env(OMC/OMC_PATH)"
    omc_path = shutil.which("omc")
    if omc_path:
        return omc_path, "PATH"
    return None, "not found"

def _read_version(omc_exe: str) -> Optional[str]:
    for args in (["--version"], ["+version"]):
        ok, out = _try_cmd([omc_exe, *args])
        if ok:
            return out.splitlines()[0]
    ok, out = _try_cmd([omc_exe])
    if ok:

        for line in out.splitlines():
            if "OpenModelica" in line or "Version" in line:
                return line.strip()
    return None

def _install_hint() -> str:
    sys = platform.system().lower()
    if "darwin" in sys or "mac" in sys:
        return (
            "macOS: install via Homebrew:\n"
            "  brew update && brew install openmodelica\n\n"
            "If already installed but not found, ensure your PATH includes Homebrew bin, e.g.:\n"
            "  echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> ~/.zprofile && source ~/.zprofile\n"
            "and that 'omc' is on PATH: which omc\n"
        )
    if "linux" in sys:
        return (
            "Linux:\n"
            "  Ubuntu/Debian:  sudo apt-get install openmodelica\n"
            "  Arch:           sudo pacman -S openmodelica\n"
            "Ensure 'omc' is on PATH (echo $PATH; which omc). If installed in a nonstandard path,\n"
            "set OMC or OMC_PATH to the absolute path of the 'omc' binary.\n"
        )
    return (
        "Install OpenModelica from https://openmodelica.org/download/ and ensure 'omc' is on PATH.\n"
        "You can also set OMC or OMC_PATH to the absolute path of the 'omc' binary."
    )

def probe_omc() -> OmcProbeResult:
    exe, how = _detect_executable()
    if not exe:
        return OmcProbeResult(
            found=False,
            exe=None,
            version=None,
            how=how,
            notes=_install_hint(),
        )
    ver = _read_version(exe)
    notes = ""
    # Helpful env info
    mode = []
    for k in ("OMC", "OMC_PATH", "MODELICAPATH"):
        v = os.environ.get(k)
        if v:
            mode.append(f"{k}={v}")
    if mode:
        notes = "env: " + ", ".join(mode)
    return OmcProbeResult(found=True, exe=exe, version=ver, how=how, notes=notes)
