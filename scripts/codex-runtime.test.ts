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

test("Swarm acceptance rejects wrong bases and proves live writer overlap with a shared clock", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_swarm_fixture.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
}, 30000);

test("Swarm fault instruments preserve retry limits, declared races and actual Git conflicts", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_swarm_recovery.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
}, 30000);

test("portable fixtures expose a real consumer regression, PTY flow and bounded property fault", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_portable_fixture.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
}, 30000);

test("design missing-output evidence rejects false completion and invented candidates", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_design.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
});

test("Architect capture removes temporary auth despite client close failure", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_architect_reframe.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
});

test("Architect friction fixture exposes two independent failures and a valid control", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_architect_scrap.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
});

test("Arena worktree cleanup preserves unknown writers and unexpected refs", () => {
  const result = Bun.spawnSync(["python3", "-B", resolve(import.meta.dir, "test_codex_arena_worktrees.py")], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  expect(new TextDecoder().decode(result.stderr)).toContain("OK");
  expect(result.exitCode).toBe(0);
});
