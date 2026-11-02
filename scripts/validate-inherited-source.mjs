// Preserved source integrity checks from inherited CI; no host installation or runtime support claim.
import { readdirSync, readFileSync, existsSync, statSync } from "node:fs";
import { join, basename } from "node:path";

const errors = [];
const fail = (msg) => errors.push(msg);

const pluginJson = JSON.parse(readFileSync("plugin.json", "utf8"));
const agyPluginJson = JSON.parse(readFileSync(".antigravity-plugin/plugin.json", "utf8"));

const allowedPluginKeys = new Set([
  "$schema",
  "name",
  "version",
  "description",
  "author",
  "homepage",
  "repository",
  "license",
  "keywords",
  "extensions",
]);
for (const key of Object.keys(pluginJson)) {
  if (!allowedPluginKeys.has(key)) {
    fail(`plugin.json contains unsupported key "${key}"`);
  }
}
if (pluginJson.$schema !== "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json") {
  fail(`plugin.json $schema must be https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`);
}
if (!/^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$/.test(pluginJson.name ?? "")) {
  fail(`plugin.json has invalid name "${pluginJson.name}"`);
}
for (const field of ["name", "version", "description"]) {
  if (!pluginJson[field] || typeof pluginJson[field] !== "string") {
    fail(`plugin.json missing string field "${field}"`);
  }
  if (pluginJson[field] !== agyPluginJson[field]) {
    fail(`Manifest mismatch for "${field}": plugin.json="${pluginJson[field]}" vs .antigravity-plugin/plugin.json="${agyPluginJson[field]}"`);
  }
}
if (!agyPluginJson.logo || !existsSync(agyPluginJson.logo)) {
  fail(`.antigravity-plugin/plugin.json logo "${agyPluginJson.logo}" does not exist`);
}

const parseFrontmatter = (filePath) => {
  const content = readFileSync(filePath, "utf8");
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) {
    fail(`${filePath}: missing YAML frontmatter`);
    return null;
  }
  return match[1];
};

const validateSkillDir = (skillsRoot) => {
  const dirs = readdirSync(skillsRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();
  for (const dir of dirs) {
    const skillFile = join(skillsRoot, dir, "SKILL.md");
    if (!existsSync(skillFile)) {
      fail(`${skillsRoot}/${dir}: missing SKILL.md`);
      continue;
    }
    const fm = parseFrontmatter(skillFile);
    if (!fm) continue;
    const nameMatch = fm.match(/^name:\s*(.+)$/m);
    const descMatch = fm.match(/^description:\s*(.+)$/m);
    const skillName = nameMatch?.[1]?.trim();
    if (skillName !== dir) {
      fail(`${skillFile}: frontmatter name "${skillName}" does not match directory "${dir}"`);
    }
    if (!descMatch?.[1]?.trim()) {
      fail(`${skillFile}: missing description in frontmatter`);
    }
    for (const badKey of ["paths", "icon", "color"]) {
      if (new RegExp(`^${badKey}:`, "m").test(fm)) {
        fail(`${skillFile}: unsupported top-level frontmatter key "${badKey}"`);
      }
    }
  }
  return dirs;
};

const expectedSkills = validateSkillDir("skills");
for (const autoEntry of readdirSync("automations", { withFileTypes: true })) {
  if (!autoEntry.isDirectory()) continue;
  const autoSkillsRoot = join("automations", autoEntry.name, "skills");
  if (existsSync(autoSkillsRoot) && statSync(autoSkillsRoot).isDirectory()) {
    validateSkillDir(autoSkillsRoot);
  }
}

const validAgentTools = new Set([
  "send_message",
  "read_file",
  "view_file",
  "grep_search",
  "find_by_name",
  "list_dir",
  "read_url_content",
  "search_web",
  "schedule",
  "generate_image",
  "edit_file",
  "multi_replace_file_content",
  "replace_file_content",
  "write_file",
  "write_to_file",
  "run_command",
  "manage_task",
  "notebook_edit",
  "define_subagent",
  "invoke_subagent",
  "manage_subagents",
]);

const expectedAgents = readdirSync("agents")
  .filter((f) => f.endsWith(".md"))
  .sort();
for (const agentFile of expectedAgents) {
  const fullPath = join("agents", agentFile);
  const fm = parseFrontmatter(fullPath);
  if (!fm) continue;
  const expectedName = basename(agentFile, ".md");
  const nameMatch = fm.match(/^name:\s*(.+)$/m);
  const descMatch = fm.match(/^description:\s*(.+)$/m);
  if (nameMatch?.[1]?.trim() !== expectedName) {
    fail(`${fullPath}: frontmatter name "${nameMatch?.[1]?.trim()}" does not match "${expectedName}"`);
  }
  if (!descMatch?.[1]?.trim()) {
    fail(`${fullPath}: missing description in frontmatter`);
  }
  for (const toolMatch of fm.matchAll(/^\s*-\s*([a-z0-9_]+)\s*$/gm)) {
    const toolName = toolMatch[1];
    if (!validAgentTools.has(toolName)) {
      fail(`${fullPath}: unregistered Antigravity subagent tool "${toolName}"`);
    }
  }
}

const toKebab = (s) =>
  s
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");

const potetoSkill = readFileSync("skills/poteto-mode/SKILL.md", "utf8");
const principlesSection = potetoSkill.split("## Principles")[1]?.split("## Autonomy")[0] ?? "";
const playbooksSection = potetoSkill.split("## Playbooks")[1] ?? "";

const indexedPrinciples = new Set();
for (const line of principlesSection.split(/\r?\n/)) {
  const m = line.match(/^- \*\*([^*]+?)\.?\*\*(?: \(\*\*(principle-[a-z0-9-]+)\*\*\))?/);
  if (m) {
    indexedPrinciples.add(m[2] ?? `principle-${toKebab(m[1])}`);
  }
}
const diskPrinciples = new Set(expectedSkills.filter((s) => s.startsWith("principle-")));
for (const p of indexedPrinciples) {
  if (!diskPrinciples.has(p)) fail(`skills/poteto-mode/SKILL.md references missing principle skill "${p}"`);
}
for (const p of diskPrinciples) {
  if (!indexedPrinciples.has(p)) fail(`skills/${p} is not indexed in skills/poteto-mode/SKILL.md`);
}

const indexedPlaybooks = new Set();
for (const line of playbooksSection.split(/\r?\n/)) {
  const m = line.match(/^- \*\*([^*]+?)\.\*\*(?:.*?File: `playbooks\/([^`]+)`)?/);
  if (m) {
    indexedPlaybooks.add(m[2] ?? `${toKebab(m[1])}.md`);
  }
}
const diskPlaybooks = new Set(readdirSync("skills/poteto-mode/playbooks").filter((f) => f.endsWith(".md")));
for (const pb of indexedPlaybooks) {
  if (!diskPlaybooks.has(pb)) fail(`skills/poteto-mode/SKILL.md references missing playbook "playbooks/${pb}"`);
}
for (const pb of diskPlaybooks) {
  if (!indexedPlaybooks.has(pb)) fail(`skills/poteto-mode/playbooks/${pb} is not indexed in skills/poteto-mode/SKILL.md`);
}

if (errors.length > 0) {
  for (const err of errors) console.error(`ERROR: ${err}`);
  process.exit(1);
}
console.log(`Validated ${expectedSkills.length} skills, ${expectedAgents.length} agents, and ${diskPlaybooks.size} playbooks.`);
