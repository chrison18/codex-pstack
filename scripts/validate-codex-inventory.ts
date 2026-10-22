import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, realpathSync, statSync } from "node:fs";
import { isAbsolute, join, relative, resolve, sep } from "node:path";

type ObjectValue = Record<string, unknown>;
const baselineCounts = { skill: 59, agent: 2, playbook: 23, "automation-skill": 3 };
type Kind = keyof typeof baselineCounts;

function object(value: unknown, label: string): ObjectValue {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label} must be an object`);
  return value as ObjectValue;
}

function contained(root: string, path: string): string {
  const actual = realpathSync(path);
  const offset = relative(realpathSync(root), actual);
  if (offset === ".." || offset.startsWith(`..${sep}`) || isAbsolute(offset)) throw new Error(`Path escapes root: ${path}`);
  return actual;
}

function discoverSources(repository: string): Map<string, { kind: Kind; id: string }> {
  const result = new Map<string, { kind: Kind; id: string }>();
  const locations: [Kind, string, boolean][] = [
    ["skill", "skills", true],
    ["agent", "agents", false],
    ["playbook", "skills/poteto-mode/playbooks", false],
    ["automation-skill", "automations/benny/skills", true],
  ];
  for (const [kind, directory, skill] of locations) {
    for (const name of readdirSync(join(repository, directory))) {
      const source = `${directory}/${name}${skill ? "/SKILL.md" : ""}`;
      if (skill ? !existsSync(join(repository, source)) : !name.endsWith(".md")) continue;
      const id = `${kind}:${skill ? name : name.slice(0, -3)}`;
      result.set(source, { kind, id });
    }
  }
  return result;
}

export function validateCodexInventory(repository: string): Record<Kind, number> {
  repository = realpathSync(repository);
  const catalog = object(JSON.parse(readFileSync(join(repository, "docs/migration/codex-skill-inventory.json"), "utf8")), "inventory");
  if (catalog.schemaVersion !== 1 || catalog.sourceBaseline !== "a06537a883278a63132e2518971166002f3de5de") {
    throw new Error("Inventory must identify the inherited migration baseline");
  }
  if (typeof catalog.phase3Base !== "string" || !/^[a-f0-9]{40}$/.test(catalog.phase3Base)) {
    throw new Error("Inventory needs an exact phase 3 base commit");
  }
  const counts = object(catalog.counts, "counts");
  if (Object.keys(counts).length !== Object.keys(baselineCounts).length) throw new Error("Unexpected inventory count categories");
  if (!Array.isArray(catalog.units)) throw new Error("Inventory units must be an array");
  const sources = discoverSources(repository);
  const seen = new Set<string>();
  const actualCounts = { skill: 0, agent: 0, playbook: 0, "automation-skill": 0 };
  const packagedSkills = new Set<string>();
  const packageRoot = contained(repository, join(repository, "plugins/pstack"));
  for (const raw of catalog.units) {
    const unit = object(raw, "inventory unit");
    if (typeof unit.sourcePath !== "string" || seen.has(unit.sourcePath)) throw new Error("Duplicate or invalid inventory source");
    const source = sources.get(unit.sourcePath);
    if (!source || unit.kind !== source.kind || unit.id !== source.id) throw new Error(`Unknown source identity: ${unit.sourcePath}`);
    seen.add(unit.sourcePath);
    actualCounts[source.kind] += 1;
    const file = contained(repository, join(repository, unit.sourcePath));
    const digest = createHash("sha256").update(readFileSync(file)).digest("hex");
    if (unit.sourceSha256 !== digest) throw new Error(`Source changed; reconcile provenance: ${unit.sourcePath}`);
    if (!Number.isInteger(unit.ownerPhase) || Number(unit.ownerPhase) < 2 || Number(unit.ownerPhase) > 5) {
      throw new Error(`Invalid owner phase: ${unit.sourcePath}`);
    }
    if (typeof unit.note !== "string" || !unit.note.trim()) throw new Error(`Missing adaptation note: ${unit.sourcePath}`);
    if (typeof unit.status !== "string" || !["adapted", "partial", "pending", "deferred"].includes(unit.status)) throw new Error(`Invalid adaptation status: ${unit.sourcePath}`);
    if (unit.status === "deferred" && Number(unit.ownerPhase) < 4) throw new Error(`Deferred runtime must name phase 4 or 5: ${unit.sourcePath}`);
    if (unit.status === "adapted" || unit.status === "partial") {
      if (typeof unit.packagePath !== "string" || !unit.packagePath.startsWith("plugins/pstack/")) {
        throw new Error(`Adapted or partial unit needs an in-package target: ${unit.sourcePath}`);
      }
      const target = contained(packageRoot, join(repository, unit.packagePath));
      if (!statSync(target).isFile()) throw new Error(`Package target must be a file: ${unit.packagePath}`);
      if (typeof unit.evidencePath !== "string" || !statSync(contained(repository, join(repository, unit.evidencePath))).isFile()) {
        throw new Error(`Adaptation claim needs an evidence file: ${unit.sourcePath}`);
      }
      if ((source.kind === "skill" || source.kind === "automation-skill") && unit.packagePath.endsWith("/SKILL.md")) {
        packagedSkills.add(unit.packagePath);
      }
    } else if (unit.packagePath !== null || unit.evidencePath !== null) {
      throw new Error(`Pending/deferred unit cannot claim a package target or passed evidence: ${unit.sourcePath}`);
    }
  }
  if (seen.size !== sources.size) throw new Error("Inventory is missing inherited source units");
  for (const kind of Object.keys(baselineCounts) as Kind[]) {
    if (actualCounts[kind] !== baselineCounts[kind] || counts[kind] !== baselineCounts[kind]) {
      throw new Error(`Inherited ${kind} inventory changed; reconcile the baseline explicitly`);
    }
  }
  const visited = new Set<string>();
  const distributed = new Set<string>();
  function inspect(directory: string) {
    const actual = contained(packageRoot, directory);
    if (visited.has(actual)) throw new Error(`Repeated package directory: ${directory}`);
    visited.add(actual);
    for (const name of readdirSync(directory)) {
      const path = join(directory, name);
      const target = contained(packageRoot, path);
      if (statSync(target).isDirectory()) inspect(path);
      else if (name === "SKILL.md") distributed.add(relative(repository, path).split("\\").join("/"));
    }
  }
  inspect(join(packageRoot, "skills"));
  if (distributed.size !== packagedSkills.size || [...distributed].some((path) => !packagedSkills.has(path))) {
    throw new Error("Distributed skills and inventory targets disagree");
  }
  return actualCounts;
}

if (import.meta.main) {
  try {
    const counts = validateCodexInventory(resolve(import.meta.dir, ".."));
    console.log(`Validated inherited source inventory: ${JSON.stringify(counts)}`);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
