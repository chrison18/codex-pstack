import { readdirSync, readFileSync, realpathSync, statSync } from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";

type RecordValue = Record<string, unknown>;

function record(value: unknown, label: string): RecordValue {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
  return value as RecordValue;
}

function inside(root: string, path: string): string {
  const actual = realpathSync(path);
  const diff = relative(realpathSync(root), actual);
  if (diff === ".." || diff.startsWith("../") || isAbsolute(diff)) {
    throw new Error(`Path escapes its package: ${path}`);
  }
  return actual;
}

function readJson(path: string): RecordValue {
  return record(JSON.parse(readFileSync(path, "utf8")), path);
}

export function validateCodexPlugin(repository: string): string[] {
  const catalog = readJson(join(repository, ".agents/plugins/marketplace.json"));
  if (catalog.name !== "codex-pstack" || !Array.isArray(catalog.plugins) || catalog.plugins.length !== 1) {
    throw new Error("Marketplace must contain only the pstack preview");
  }
  const entry = record(catalog.plugins[0], "plugin entry");
  const source = record(entry.source, "plugin source");
  const policy = record(entry.policy, "installation policy");
  if (entry.name !== "pstack" || source.source !== "local" || source.path !== "./plugins/pstack") {
    throw new Error("Marketplace must target the isolated Codex package");
  }
  if (policy.installation !== "AVAILABLE" || policy.authentication !== "ON_INSTALL") {
    throw new Error("Preview must be available for explicit installation");
  }
  const root = inside(repository, join(repository, source.path));
  const manifest = readJson(join(root, "plugin.json"));
  if (manifest.$schema !== "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json" || manifest.name !== entry.name) {
    throw new Error("Invalid portable plugin identity");
  }
  if (typeof manifest.version !== "string" || !/^\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?$/.test(manifest.version)) {
    throw new Error("Plugin version must be a release or prerelease version");
  }
  if (typeof manifest.description !== "string" || !manifest.description.trim() || !record(manifest.author, "author").name) {
    throw new Error("Plugin requires a description and attribution");
  }
  const extension = record(record(manifest.extensions, "extensions")["com.openai"], "OpenAI extension");
  if (!record(extension.interface, "plugin interface").displayName) throw new Error("Plugin needs a display name");
  if (manifest.license !== "MIT" || readFileSync(join(root, "LICENSE"), "utf8") !== readFileSync(join(repository, "LICENSE"), "utf8")) {
    throw new Error("Packaged upstream license must be preserved");
  }
  const allowed = new Set(["plugin.json", "LICENSE", "skills"]);
  for (const name of readdirSync(root)) {
    if (!allowed.has(name)) throw new Error(`Unexpected preview component: ${name}`);
  }
  const skillRoot = join(root, "skills");
  const names = readdirSync(skillRoot).sort();
  if (names.join(",") !== "poteto-mode,setup-pstack") throw new Error("Core candidate must expose only poteto-mode and setup-pstack");
  const skill = inside(root, join(skillRoot, names[0]));
  const roles = join(skill, "resources/agents");
  const roleNames = readdirSync(roles).sort();
  if (roleNames.join(",") !== "comment-sicko.toml,poteto-agent.toml") {
    throw new Error("Core candidate must package exactly the two migrated roles");
  }
  for (const name of roleNames) {
    const role = record(Bun.TOML.parse(readFileSync(inside(root, join(roles, name)), "utf8")), "agent definition");
    if (role.name !== name.replace(/\.toml$/, "") || typeof role.description !== "string" || !role.description.trim() || typeof role.developer_instructions !== "string" || !role.developer_instructions.trim()) {
      throw new Error("Agent identity and instructions are required");
    }
    if (Object.keys(role).some((key) => !["name", "description", "developer_instructions"].includes(key))) {
      throw new Error("Role templates must inherit native settings; resolve model choices at spawn time");
    }
  }
  for (const name of names) {
    const current = inside(root, join(skillRoot, name));
  const text = readFileSync(join(current, "SKILL.md"), "utf8");
  const frontmatter = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!frontmatter) throw new Error("Skill must have YAML frontmatter");
  const metadata = record(Bun.YAML.parse(frontmatter[1]), "skill frontmatter");
  if (metadata.name !== name || typeof metadata.description !== "string" || !metadata.description.trim()) {
    throw new Error("Skill name and description must match discovery requirements");
  }
  const config = record(Bun.YAML.parse(readFileSync(join(current, "agents/openai.yaml"), "utf8")), "skill config");
  if (record(config.policy, "invocation policy").allow_implicit_invocation !== false) {
    throw new Error("Every pstack entry must require explicit invocation");
  }
  }
  function inspect(directory: string) {
    for (const name of readdirSync(directory)) {
      const path = inside(root, join(directory, name));
      if (statSync(path).isDirectory()) {
        inspect(path);
      } else if (name.endsWith(".md")) {
        for (const match of readFileSync(path, "utf8").matchAll(/\]\(([^)]+)\)/g)) {
          if (match[1].includes("://") || match[1].startsWith("#")) continue;
          inside(root, resolve(dirname(path), match[1].split("#")[0]));
        }
      }
    }
  }
  inspect(skillRoot);
  return names;
}

if (import.meta.main) {
  try {
    const names = validateCodexPlugin(resolve(import.meta.dir, ".."));
    console.log(`Validated Codex candidate: ${names.length} explicit skills (${names.join(", ")}).`);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
