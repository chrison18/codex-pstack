"""Exercise local Codex packaging and context injection without calling a model."""

import argparse
import http.server
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading


def run_smoke(repository, executable):
    with tempfile.TemporaryDirectory(prefix="pstack-codex-smoke-") as scratch:
        root = Path(scratch).resolve()
        home, workspace = root / "codex-home", root / "workspace"
        home.mkdir()
        workspace.mkdir()
        environment = {**os.environ, "CODEX_HOME": str(home)}

        def cli(*arguments):
            result = subprocess.run(
                [executable, "--no-daemon", *arguments], cwd=workspace,
                env=environment, capture_output=True, text=True, timeout=45,
                stdin=subprocess.DEVNULL,
            )
            if result.returncode:
                raise RuntimeError(f"Codex {arguments[:2]} failed: {result.stderr[-1500:]}")
            return result.stdout

        version = cli("--version").strip()
        cli("plugin", "marketplace", "add", str(repository), "--json")
        installed = json.loads(cli("plugin", "add", "pstack@codex-pstack", "--json"))
        installed_path = Path(installed["installedPath"])
        actual = sorted(p.relative_to(installed_path).as_posix() for p in installed_path.rglob("SKILL.md"))
        assert actual == ["skills/poteto-mode/SKILL.md", "skills/setup-pstack/SKILL.md"], actual
        assert json.loads(cli("plugin", "list", "--json"))["installed"][0]["enabled"]

        captured = queue.Queue()

        class Capture(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if "input" in payload:
                    captured.put(payload)
                self.send_response(500)
                self.end_headers()

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Capture)
        threading.Thread(target=server.serve_forever, daemon=True).start()

        def body_loaded(prompt):
            arguments = [
                executable, "--no-daemon", "exec", "--ephemeral", "--skip-git-repo-check",
                "-s", "read-only", "-C", str(workspace), "--json",
                "-c", 'model_provider="pstack_probe"',
                "-c", 'model="gpt-6.1-sol"',
                "-c", 'model_providers.pstack_probe.name="Local context capture"',
                "-c", f'model_providers.pstack_probe.base_url="http://127.0.0.1:{server.server_port}/v1"',
                "-c", 'model_providers.pstack_probe.wire_api="responses"',
                "-c", 'model_providers.pstack_probe.requires_openai_auth=false',
                prompt,
            ]
            with (root / "cli.log").open("w") as output:
                process = subprocess.Popen(
                    arguments, cwd=workspace, env=environment, stdin=subprocess.DEVNULL,
                    stdout=output, stderr=output,
                )
                try:
                    request = captured.get(timeout=30)
                    assert request["model"] == "gpt-6.1-sol"
                    content = json.dumps(request["input"])
                    return "The primary chat owns the playbook" in content
                except queue.Empty as error:
                    raise RuntimeError("Codex did not reach the local context capture") from error
                finally:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=5)

        try:
            assert not body_loaded("Investigate the failing tests."), "Implicit activation"
            assert body_loaded("$pstack:poteto-mode Check availability."), "Qualified invocation missing"
            assert not body_loaded("$poteto-mode Check availability."), "Recheck short-name behavior in this client"
            subprocess.run(
                [sys.executable, str(repository / "scripts/link-codex-entry.py"), str(workspace)],
                check=True, capture_output=True, text=True,
            )
            alias = workspace / ".agents/skills/poteto-mode"
            assert not body_loaded("Implement a feature and fix a bug."), "Alias activated implicitly"
            assert body_loaded("$poteto-mode Check availability."), "Short invocation missing with alias"
            alias.unlink()
            cli("plugin", "remove", "pstack@codex-pstack", "--json")
            assert not installed_path.exists(), "Plugin cache survived removal"
            assert not json.loads(cli("plugin", "list", "--json"))["installed"]
            assert not body_loaded("$poteto-mode Check availability."), "Removed alias still loads"
            cli("plugin", "marketplace", "remove", "codex-pstack")
        finally:
            server.shutdown()
            server.server_close()

        print(json.dumps({
            "client": version,
            "install": "PASS", "packageInventory": "PASS",
            "qualifiedInvocation": "PASS", "implicitExclusion": "PASS",
            "shortInvocationWithProjectAlias": "PASS", "removal": "PASS",
            "scope": "CLI host context injection; no model response or desktop UI tested",
        }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex", help="Codex CLI executable")
    arguments = parser.parse_args()
    run_smoke(Path(__file__).resolve().parent.parent, arguments.codex)
