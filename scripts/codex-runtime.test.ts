import { expect, test } from "bun:test";
import { resolve } from "node:path";

test("project role lifecycle and model resolution preserve user state", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_runtime.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
}, 30000);

test("acceptance snapshots detect links, directories, types and permission changes", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_acceptance_state.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
});

test("research capture separates requested models, resolved starts and final answers", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_research_capture.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
});
