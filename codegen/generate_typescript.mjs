#!/usr/bin/env node
/**
 * Generate TypeScript interfaces from JSON Schema contracts.
 *
 * Reads all .json files from contracts/schemas/ and produces a single
 * generated/typescript/src/models.ts file with all interfaces, plus an
 * index.ts barrel export.
 */

import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join, basename, resolve } from "node:path";
import { compileFromFile } from "json-schema-to-typescript";

const ROOT = resolve(import.meta.dirname, "..");
const SCHEMAS_DIR = join(ROOT, "contracts", "schemas");
const OUT_DIR = join(ROOT, "generated", "typescript", "src");

/** Convert schema filename to PascalCase (e.g. "tool-request.json" → "ToolRequest"). */
function filenameToPascal(filename) {
  return filename
    .replace(/\.json$/, "")
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join("");
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true });

  const files = (await readdir(SCHEMAS_DIR))
    .filter((f) => f.endsWith(".json"))
    .sort();

  console.log(`Found ${files.length} schema files`);

  const chunks = [];
  const exportNames = [];
  const seenInterfaces = new Set();

  for (const file of files) {
    const schemaPath = join(SCHEMAS_DIR, file);
    const name = filenameToPascal(file);

    try {
      const ts = await compileFromFile(schemaPath, {
        cwd: SCHEMAS_DIR,
        bannerComment: "",
        additionalProperties: false,
        declareExternallyReferenced: true,
        format: false,
        style: {
          singleQuote: true,
          trailingComma: "all",
          printWidth: 100,
        },
      });

      // Deduplicate: split output into individual interface blocks and only
      // keep those we haven't already emitted.
      const blocks = ts.split(/(?=^export )/m);
      const uniqueBlocks = [];
      for (const block of blocks) {
        const match = block.match(/^export interface (\w+)/);
        if (match) {
          if (seenInterfaces.has(match[1])) continue;
          seenInterfaces.add(match[1]);
        }
        // Skip empty blocks
        if (block.trim()) uniqueBlocks.push(block);
      }

      if (uniqueBlocks.length > 0) {
        chunks.push(`// --- ${file} ---\n${uniqueBlocks.join("")}`);
      }
      exportNames.push(name);
      console.log(`  ✓ ${file} → ${name}`);
    } catch (err) {
      console.error(`  ✗ ${file}: ${err.message}`);
      process.exit(1);
    }
  }

  // Write combined models file
  const header = [
    "// Auto-generated TypeScript interfaces from JSON Schema contracts.",
    "// DO NOT EDIT — run `make codegen-ts` to regenerate.",
    "",
    "/* eslint-disable */",
    "",
  ].join("\n");

  const modelsContent = header + chunks.join("\n\n") + "\n";
  await writeFile(join(OUT_DIR, "models.ts"), modelsContent, "utf-8");

  // Write barrel index
  const indexContent = [
    "// Auto-generated TypeScript interfaces from JSON Schema contracts.",
    "// DO NOT EDIT — run `make codegen-ts` to regenerate.",
    "",
    "export * from './models.js';",
    "",
  ].join("\n");
  await writeFile(join(OUT_DIR, "index.ts"), indexContent, "utf-8");

  console.log(`\nGenerated ${files.length} interfaces → ${OUT_DIR}/models.ts`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
