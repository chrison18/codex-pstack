import { afterEach, expect, test } from "bun:test";
import { lstatSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, readlinkSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const roots: string[] = [];
const helper = join(import.meta.dir, "link-codex-entry.py");
function project() {
  const root = mkdtempSync(join(tmpdir(), "pstack-link-test-"));
  roots.push(root);
  return root;
}
function run(root: string) {
  return Bun.spawnSync(["python3", helper, root]);
}
afterEach(() => {
  for (const root of roots.splice(0)) rmSync(root, { recursive: true, force: true });
});

test("creates a project skill link to the maintained preview", () => {
  const root = project();
  expect(run(root).exitCode).toBe(0);
  const path = join(root, ".agents/skills/poteto-mode");
  expect(lstatSync(path).isSymbolicLink()).toBe(true);
  expect(readlinkSync(path)).toBe(resolve(import.meta.dir, "../plugins/pstack/skills/poteto-mode"));
});

test("does not nest a link inside an existing skill directory", () => {
  const root = project();
  const path = join(root, ".agents/skills/poteto-mode");
  mkdirSync(path, { recursive: true });
  writeFileSync(join(path, "SKILL.md"), "existing skill\n");
  expect(run(root).exitCode).toBe(1);
  expect(readdirSync(path)).toEqual(["SKILL.md"]);
  expect(readFileSync(join(path, "SKILL.md"), "utf8")).toBe("existing skill\n");
});

test("preserves a dangling skill symlink", () => {
  const root = project();
  const parent = join(root, ".agents/skills");
  mkdirSync(parent, { recursive: true });
  const path = join(parent, "poteto-mode");
  symlinkSync("missing-skill", path);
  expect(run(root).exitCode).toBe(1);
  expect(readlinkSync(path)).toBe("missing-skill");
});

test("preserves an existing file and an already installed link", () => {
  const root = project();
  const parent = join(root, ".agents/skills");
  mkdirSync(parent, { recursive: true });
  const path = join(parent, "poteto-mode");
  writeFileSync(path, "existing file\n");
  expect(run(root).exitCode).toBe(1);
  expect(readFileSync(path, "utf8")).toBe("existing file\n");
  rmSync(path);
  expect(run(root).exitCode).toBe(0);
  const target = readlinkSync(path);
  expect(run(root).exitCode).toBe(1);
  expect(readlinkSync(path)).toBe(target);
});
