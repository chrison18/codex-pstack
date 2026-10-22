import { afterEach, expect, test } from "bun:test";
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { validateCodexInventory } from "./validate-codex-inventory";

const directories: string[] = [];
const repository = resolve(import.meta.dir, "..");
const catalogPath = "docs/migration/codex-skill-inventory.json";

function fixture(): string {
  const root = mkdtempSync(join(tmpdir(), "pstack-inventory-"));
  directories.push(root);
  const catalog = JSON.parse(readFileSync(join(repository, catalogPath), "utf8"));
  const evidence = [...new Set<string>(catalog.units.map((unit: { evidencePath: string | null }) => unit.evidencePath).filter(Boolean))];
  for (const path of [catalogPath, ...evidence, ...catalog.units.map((unit: { sourcePath: string }) => unit.sourcePath)]) {
    mkdirSync(dirname(join(root, path)), { recursive: true });
    cpSync(join(repository, path), join(root, path));
  }
  cpSync(join(repository, "plugins/pstack"), join(root, "plugins/pstack"), { recursive: true });
  return root;
}

function change(root: string, edit: (value: { units: { id: string; status: string }[] }) => void) {
  const file = join(root, catalogPath);
  const value = JSON.parse(readFileSync(file, "utf8"));
  edit(value);
  writeFileSync(file, JSON.stringify(value));
}

afterEach(() => {
  for (const directory of directories.splice(0)) rmSync(directory, { recursive: true, force: true });
});

test("accounts for all inherited skills, roles, playbooks and Benny skills", () => {
  expect(validateCodexInventory(fixture())).toEqual({ skill: 59, agent: 2, playbook: 23, "automation-skill": 3 });
});

test("rejects omission of an inherited source", () => {
  const root = fixture();
  change(root, (value) => { value.units.pop(); });
  expect(() => validateCodexInventory(root)).toThrow("missing inherited");
});

test("requires explicit accounting for newly added source skills", () => {
  const root = fixture();
  mkdirSync(join(root, "skills/new-skill"));
  writeFileSync(join(root, "skills/new-skill/SKILL.md"), "new source");
  expect(() => validateCodexInventory(root)).toThrow("missing inherited");
});

test("rejects source drift without a provenance update", () => {
  const root = fixture();
  writeFileSync(join(root, "skills/how/SKILL.md"), "changed source");
  expect(() => validateCodexInventory(root)).toThrow("Source changed");
});

test("does not accept supported claims without a packaged artifact", () => {
  const root = fixture();
  change(root, (value) => {
    const unit = value.units.find((unit: { id: string }) => unit.id === "skill:how");
    if (!unit) throw new Error("Fixture is missing how");
    unit.status = "adapted";
  });
  expect(() => validateCodexInventory(root)).toThrow("in-package target");
});

test("accepts a checkout reached through a root symlink", () => {
  const root = fixture();
  const parent = mkdtempSync(join(tmpdir(), "pstack-inventory-alias-"));
  directories.push(parent);
  const link = join(parent, "checkout");
  symlinkSync(root, link);
  expect(validateCodexInventory(link).skill).toBe(59);
});

test("rejects unaccounted distributed skills", () => {
  const root = fixture();
  mkdirSync(join(root, "plugins/pstack/skills/untracked"));
  writeFileSync(join(root, "plugins/pstack/skills/untracked/SKILL.md"), "untracked package");
  expect(() => validateCodexInventory(root)).toThrow("inventory targets disagree");
});

test("adaptation claims require an evidence reference", () => {
  const root = fixture();
  change(root, (value) => {
    const unit = value.units.find((unit) => unit.id === "agent:poteto-agent");
    if (!unit) throw new Error("Fixture is missing poteto-agent");
    Object.assign(unit, { evidencePath: null });
  });
  expect(() => validateCodexInventory(root)).toThrow("needs an evidence file");
});

test("package targets cannot escape the isolated distribution", () => {
  const root = fixture();
  change(root, (value) => {
    const unit = value.units.find((unit) => unit.id === "agent:poteto-agent");
    if (!unit) throw new Error("Fixture is missing poteto-agent");
    Object.assign(unit, { packagePath: "plugins/pstack/../../skills/how/SKILL.md" });
  });
  expect(() => validateCodexInventory(root)).toThrow("escapes root");
});
