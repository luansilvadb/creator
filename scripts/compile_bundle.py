#!/usr/bin/env python3
"""
System Instruction Omega Distiller.
Perfeição estética absoluta. Limpeza total de resíduos visuais e barras órfãs.
"""

import sys
import re
from pathlib import Path
from quick_validate import validate_skill

IGNORE_DIRS = {".git", ".gemini", ".agents", "__pycache__", "node_modules", "dist"}
IGNORE_FILES = {".gitignore", "package-lock.json", "LICENSE", "README.md", "AGENTS.md"}

COGNITIVE_MAP = {
    ".agile": "Núcleo de Inteligência",
    "planning": "Camada de Planejamento Estratégico",
    "sprints": "Ciclo de Execução Tática",
    "spec": "Especificações Técnicas Detalhadas",
    "history": "Arquivo de Memória Imutável",
    "assets": "Padrões de Representação",
    "core": "Núcleo de Inteligência",
    "runtime": "Ambiente de Operação",
    "releases": "Registros de Entrega",
    "archive": "Repositório de Longo Prazo",
    "scripts": "Capacidades Operacionais",
    "archive_manager": "Archive Manager",
    "mente-brilhante": "Mente Brilhante Ω",
    "adrs": "Registros de Decisões Arquiteturais",
    "current_sprint": "Ciclo de Sprint Ativo",
    "roadmap": "Diretriz de Roadmap",
    "backlog": "Backlog de Valor",
    "story_map": "Mapeamento de Jornada",
    "release_notes": "Notas de Entrega"
}

def strip_frontmatter(content):
    if content.startswith("---"):
        parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3: return parts[2].strip()
    return content.strip()

def semantic_cleanup(text, is_markdown=True):
    if not text: return ""
    if not is_markdown: return text.strip()

    def atomic_callback(match):
        label = match.group(1)
        if label: return f"**{label}**"
        full_match = match.group(0)
        atoms = [a for a in re.split(r'[/\\]', full_match) if a]
        distilled = []
        for atom in atoms:
            clean = re.sub(r"\.(py|md|js|ts|sh|txt|json|yaml)$", "", atom, flags=re.IGNORECASE).lower().strip(".")
            if clean in COGNITIVE_MAP:
                distilled.append(f"**{COGNITIVE_MAP[clean]}**")
            elif clean:
                distilled.append(f"**{clean.replace('_', ' ').replace('-', ' ').title()}**")
        return " ".join(distilled)

    tech_patterns = "|".join([re.escape(k) for k in sorted(COGNITIVE_MAP.keys(), key=len, reverse=True)])
    pattern = rf"\[(.*?)\]\([^)]+\)|(?<![\w/])(?:[\w.-]+/)*[\w.-]+\.(?:py|md|js|ts|sh|txt|json|yaml)\b|(?<![\w/])[\w.-]+\.(?:py|md|js|ts|sh|txt|json|yaml)\b|(?<![\w/])(?:[\w.-]+/)+|(?<![\w/])(?:{tech_patterns})\b"
    
    text = re.sub(pattern, atomic_callback, text, flags=re.IGNORECASE)

    # LIMPEZA OMEGA
    text = re.sub(r"\n## (Recursos|Resources|Files|Apoio|Folders|Instalação|Scripts|Referências|Assets).*?(?=\n## |$)", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\[TODO:.*?\]", "", text)
    text = re.sub(r'`\s*`', '', text) 
    text = text.replace("**/", "**").replace("/**", "**") # Limpeza de barras órfãs
    text = text.replace("- :", "-")
    text = text.replace(" / ", " ")
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

def distill_script(script_path):
    content = script_path.read_text(encoding="utf-8")
    name = script_path.stem.replace("_", " ").upper()
    doc = re.search(r'"""(.*?)"""', content, re.DOTALL)
    desc = doc.group(1).strip() if doc else "Protocolo operacional autônomo."
    actions = []
    if "shutil.copy" in content: actions.append("Preservar a imutabilidade via espelhamento de estado.")
    if "mkdir" in content: actions.append("Modularizar as camadas de persistência.")
    if "datetime" in content: actions.append("Garantir a auditoria temporal dos registros.")
    res = [f"### 🛠️ PROTOCOLO OPERACIONAL: {name}", f"**Essência**: {semantic_cleanup(desc)}"]
    if actions: res.append("**Lógica de Execução**:\n" + "\n".join([f"- {a}" for a in actions]))
    return "\n".join(res)

def distill_reference(md_path):
    content = strip_frontmatter(md_path.read_text(encoding="utf-8"))
    title = md_path.stem.replace("_", " ").upper()
    dense_lines = [l for l in content.split('\n') if l.strip().startswith(('#', '*', '-', '1.', '>')) or ':' in l]
    return f"### 📚 CÂNONE DE CONHECIMENTO: {title}\n" + semantic_cleanup("\n".join(dense_lines))

def distill_asset(md_path):
    content = strip_frontmatter(md_path.read_text(encoding="utf-8"))
    title = md_path.stem.replace("_TEMPLATE", "").replace("_", " ").upper()
    return f"### 📜 GRAMÁTICA DE SAÍDA: {title}\n**Objetivo**: Padronização de artefato de entrega.\n**Modelo Obrigatório**:\n```markdown\n{content}\n```"

def compile_omega_bundle(skill_path, output_file=None):
    skill_path = Path(skill_path).resolve()
    print(f"💎 Consolidando Perfeição Omega: {skill_path.name}")
    validate_skill(skill_path)
    bundle = []
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        bundle.append("# 🧠 MATRIZ DE IDENTIDADE")
        bundle.append(semantic_cleanup(strip_frontmatter(skill_md.read_text(encoding="utf-8"))))
        bundle.append("\n---\n")
    for folder, category, distiller in [
        ("assets", "🏛️ PADRÕES DE REPRESENTAÇÃO (GRAMÁTICAS)", distill_asset),
        ("references", "📚 CÂNONES DE CONHECIMENTO", distill_reference),
        ("scripts", "🛠️ COMPETÊNCIAS OPERACIONAIS (PROTOCOLOS)", distill_script)
    ]:
        dir_path = skill_path / folder
        if dir_path.exists():
            bundle.append(f"# {category}")
            for ext in ["md", "py", "js", "sh"]:
                for f in sorted(dir_path.glob(f"*.{ext}")):
                    print(f"  [{folder.upper()}] Purificando {f.name}")
                    bundle.append(distiller(f))
            bundle.append("\n---\n")
    output_file = Path(output_file) if output_file else Path("dist/system-instruction.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    content = re.sub(r"\n{3,}", "\n\n", "\n".join(bundle))
    content = re.sub(r'\n -', '\n  -', content)
    output_file.write_text(content, encoding="utf-8")
    print(f"\n[SUCCESS] Omega Intelligence Bundle Finalizado: {output_file}")
    from test_coverage import run_coverage_test
    run_coverage_test(skill_path, output_file)
    return output_file

if __name__ == "__main__":
    compile_omega_bundle(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
