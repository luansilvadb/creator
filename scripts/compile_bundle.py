#!/usr/bin/env python3
"""
System Instruction Pure Compiler - Zero Synthetic Garbage Edition.
Compila a skill em sua forma mais pura, removendo cabeçalhos inventados pelo 
compilador e focando exclusivamente no conteúdo original processado.
"""

import sys
import re
from pathlib import Path
from quick_validate import validate_skill

# Filtros Globais
IGNORE_DIRS = {".git", ".gemini", ".agents", "__pycache__", "node_modules", "dist"}
IGNORE_FILES = {".gitignore", "package-lock.json", "LICENSE", "README.md", "AGENTS.md"}
TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml"}
LOGIC_EXTS = {".py", ".sh", ".js", ".ts"}

def strip_frontmatter(content):
    if content.startswith("---"):
        parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3: return parts[2].strip()
    return content.strip()

def semantic_cleanup(text, is_markdown=True):
    if not text: return ""
    if not is_markdown: return text.strip()

    # 1. Remover seções exclusivas para criadores
    text = re.sub(r"\n## (Recursos|Resources|Files|Apoio|Folders|Instalação|Scripts|Referências|Assets).*?(?=\n## |$)", "", text, flags=re.DOTALL | re.IGNORECASE)
    
    # 2. Abstrair links de arquivos e caminhos técnicos
    def abstract_path(match):
        if match.group(1): return f"**{match.group(1)}**"
        full_match = match.group(0)
        filename = full_match.split('/')[-1]
        name_only = re.sub(r"\.(py|md|js|ts|sh|txt|json|yaml)$", "", filename, flags=re.IGNORECASE)
        return name_only.replace("_", " ").replace("-", " ").title()

    pattern = r"\[(.*?)\]\([^)]+\)|(?<![/\w])(?:[\w.-]+/)*[\w.-]+\.(?:py|md|js|ts|sh|txt|json|yaml)\b"
    text = re.sub(pattern, abstract_path, text)
    
    # 3. Limpeza final
    text = re.sub(r"\.(py|md|js|ts|sh|txt|json|yaml)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[TODO:.*?\]", "", text)
    
    return text.strip()

def compile_pure_bundle(skill_path, output_file=None):
    skill_path = Path(skill_path).resolve()
    if not skill_path.exists() or not skill_path.is_dir():
        return None

    print(f"💎 Compilando Pure Skill: {skill_path.name}")
    validate_skill(skill_path)

    bundle_content = []
    
    # --- 1. ARQUIVOS DA RAIZ (SKILL.md assume o topo) ---
    # Priorizar o SKILL.md para ser o primeiro
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        print("  [ROOT] Integrando Identidade (SKILL.md)")
        content = strip_frontmatter(skill_md.read_text(encoding="utf-8"))
        bundle_content.append(semantic_cleanup(content))
        bundle_content.append("\n---\n")

    # Outros arquivos na raiz
    for file in sorted(skill_path.iterdir()):
        if file.is_file() and file.name != "SKILL.md" and file.suffix in TEXT_EXTS and file.name not in IGNORE_FILES:
            print(f"  [ROOT] Integrando: {file.name}")
            content = strip_frontmatter(file.read_text(encoding="utf-8"))
            bundle_content.append(f"# {file.stem.upper().replace('_', ' ')}")
            if file.suffix in [".json", ".yaml", ".yml"]:
                bundle_content.append(f"```json\n{content.strip()}\n```")
            else:
                bundle_content.append(semantic_cleanup(content, is_markdown=(file.suffix == ".md")))
            bundle_content.append("\n")

    # --- 2. VARREDURA DINÂMICA DE MÓDULOS ---
    for item in sorted(skill_path.iterdir()):
        if item.is_dir() and item.name not in IGNORE_DIRS:
            section_title = item.name.replace("_", " ").replace("-", " ").upper()
            print(f"📂  Processando Módulo: {section_title}")
            
            # Protocolos (.md, .txt)
            md_files = sorted(list(item.rglob("*.md"))) + sorted(list(item.rglob("*.txt")))
            if md_files:
                for md_file in md_files:
                    title = md_file.stem.replace("_", " ").replace("-", " ").upper()
                    print(f"    - Protocolo: {title}")
                    content = strip_frontmatter(md_file.read_text(encoding="utf-8"))
                    bundle_content.append(f"# {title}")
                    bundle_content.append(semantic_cleanup(content, is_markdown=(md_file.suffix == ".md")))
                    bundle_content.append("\n")

            # Dados (.json, .yaml)
            data_files = sorted(list(item.rglob("*.json"))) + sorted(list(item.rglob("*.yaml"))) + sorted(list(item.rglob("*.yml")))
            if data_files:
                for data_file in data_files:
                    title = data_file.name.upper()
                    print(f"    - Dados: {title}")
                    content = data_file.read_text(encoding="utf-8")
                    bundle_content.append(f"## DATA: {title}")
                    bundle_content.append(f"```json\n{content.strip()}\n```")
                    bundle_content.append("\n")

            # Scripts (Capacidades)
            script_files = []
            for ext in ["py", "sh", "js", "ts"]:
                script_files.extend(list(item.rglob(f"*.{ext}")))
            
            if script_files:
                bundle_content.append(f"# {section_title} CAPABILITIES")
                for script in sorted(script_files):
                    try:
                        print(f"    - Capacidade: {script.name}")
                        script_text = script.read_text(encoding="utf-8")
                        doc_match = re.search(r'"""(.*?)"""', script_text, re.DOTALL)
                        purpose = semantic_cleanup(doc_match.group(1).strip()) if doc_match else "Protocolo operacional."
                        action_name = script.stem.replace("_", " ").replace("-", " ").upper()
                        bundle_content.append(f"- **{action_name}**: {purpose}")
                        usage = re.search(r"(Usage|Uso|Ex):.*?(?=\n|$)", script_text, re.IGNORECASE)
                        if usage:
                            bundle_content.append(f"  *Interface*: `{semantic_cleanup(usage.group(0).strip())}`")
                    except: pass
                bundle_content.append("\n")

    # --- 3. FINALIZAÇÃO ---
    output_file = Path(output_file) if output_file else Path("dist/system-instruction.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        raw_bundle = "\n".join(bundle_content)
        raw_bundle = re.sub(r"\n{3,}", "\n\n", raw_bundle)
        output_file.write_text(raw_bundle, encoding="utf-8")
        print(f"\n[SUCCESS] Pure System Instruction compilada em: {output_file}")
        
        from test_coverage import run_coverage_test
        run_coverage_test(skill_path, output_file)
        return output_file
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

if __name__ == "__main__":
    compile_pure_bundle(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
