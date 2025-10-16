from __future__ import annotations
import argparse
import sys
from . import __version__
from .hello import say_hello


def _cmd_version(_: argparse.Namespace) -> int:
    print(f"modelica-genai-lab {__version__}")
    return 0


def _cmd_env(_: argparse.Namespace) -> int:
    print(f"python: {sys.version.split()[0]}")
    print("package import: OK")
    return 0


def _cmd_hello(args: argparse.Namespace) -> int:
    msg = say_hello()
    if args.name:
        msg = f"{msg} Hi, {args.name}!"
    print(msg)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="modelica-genai",
        description="Modelica GenAI Lab CLI (minimal)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ver = sub.add_parser("version", help="Show tool version")
    p_ver.set_defaults(func=_cmd_version)

    p_env = sub.add_parser("env", help="Environment sanity check")
    p_env.set_defaults(func=_cmd_env)

    p_hello = sub.add_parser("hello", help="Say hello")
    p_hello.add_argument("--name", help="Optional name")
    p_hello.set_defaults(func=_cmd_hello)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

applypatch << 'PATCH'
*** Begin Patch
*** Update File: src/modelica_genai_lab/cli.py
@@
 from .hello import say_hello
+from .omc import probe_omc
 
@@
     p_hello.set_defaults(func=_cmd_hello)
 
+    # --- omc group ---
+    p_omc = sub.add_parser("omc", help="OpenModelica utilities")
+    sub_omc = p_omc.add_subparsers(dest="omc_cmd", required=True)
+
+    def _cmd_omc_probe(_: argparse.Namespace) -> int:
+        res = probe_omc()
+        if res.found:
+            print("omc:        FOUND")
+            print(f"where:      {res.exe}  (via {res.how})")
+            print(f"version:    {res.version or 'unknown'}")
+            if res.notes:
+                print(res.notes)
+            return 0
+        else:
+            print("omc:        NOT FOUND")
+            print(f"how:        {res.how}")
+            print()
+            print(res.notes)
+            return 1
+
+    p_omc_probe = sub_omc.add_parser("probe", help="Detect omc and print version")
+    p_omc_probe.set_defaults(func=_cmd_omc_probe)
+
*** End Patch
PATCH



