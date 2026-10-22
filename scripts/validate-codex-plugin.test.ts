import { afterEach, expect, test } from "bun:test";
import { cpSync, mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { validateCodexPlugin } from "./validate-codex-plugin";

const directories: string[] = [];
function fixture(): string {
  const root = mkdtempSync(join(tmpdir(), "pstack-package-test-"));
  directories.push(root);
  const source = resolve(import.meta.dir, "..");
  for (const path of ["plugins", ".agents", "LICENSE"]) cpSync(join(source, path), join(root, path), { recursive: true });
  return root;
}

afterEach(() => {
  for (const directory of directories.splice(0)) rmSync(directory, { recursive: true, force: true });
});

test("validates the distributable preview independently of inherited skills", () => {
  const root = fixture();
  mkdirSync(join(root, "skills/legacy"), { recursive: true });
  writeFileSync(join(root, "skills/legacy/SKILL.md"), "not part of the Codex package");
  expect(validateCodexPlugin(root)).toEqual(["poteto-mode"]);
});

test("rejects implicit invocation, including a truthy string instead of a boolean", () => {
  for (const value of ["true", '"false"']) {
    const root = fixture();
    writeFileSync(join(root, "plugins/pstack/skills/poteto-mode/agents/openai.yaml"), `policy:\n  allow_implicit_invocation: ${value}\n`);
    expect(() => validateCodexPlugin(root)).toThrow("explicit invocation");
  }
});

test("rejects publishing an unported skill", () => {
  const root = fixture();
  mkdirSync(join(root, "plugins/pstack/skills/unported"));
  expect(() => validateCodexPlugin(root)).toThrow("only poteto-mode");
});

test("rejects package references outside the installed package", () => {
  const root = fixture();
  const file = join(root, "plugins/pstack/skills/poteto-mode/SKILL.md");
  writeFileSync(file, readFileSync(file, "utf8") + "\n[legacy](../../../../LICENSE)\n");
  expect(() => validateCodexPlugin(root)).toThrow("escapes");
});

test("rejects symlinks that leak unported repository content", () => {
  const root = fixture();
  symlinkSync(join(root, "LICENSE"), join(root, "plugins/pstack/skills/poteto-mode/legacy.md"));
  expect(() => validateCodexPlugin(root)).toThrow("escapes");
});

test("rejects a marketplace that points at the inherited package", () => {
  const root = fixture();
  const file = join(root, ".agents/plugins/marketplace.json");
  const catalog = JSON.parse(readFileSync(file, "utf8"));
  catalog.plugins[0].source.path = "./";
  writeFileSync(file, JSON.stringify(catalog));
  expect(() => validateCodexPlugin(root)).toThrow("isolated Codex package");
});
