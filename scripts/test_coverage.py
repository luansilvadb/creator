#!/usr/bin/env python3
"""
Instruction Coverage Tester - Premium Edition.
Valida a integridade da System Instruction com suporte a purificação terminológica.
"""

import sys
import os
import re
from pathlib import Path

def normalize_concept(name):
    # 1. Remover extensão
    name = re.sub(r"\.(py|md|js|ts|sh|txt|json|yaml)$", "", name, flags=re.IGNORECASE)
    # 2. Remover sufixos de sistema como _TEMPLATE ou template
    name = re.sub(r"(_TEMPLATE|template|_template|TEMPLATE)$", "", name, flags=re.IGNORECASE)
    # 3. Normalizar espaçamento e capitalização
    return name.replace("_", " ").replace("-", " ").strip().title()

def run_coverage_test(skill_path, bundle_path):
    skill_path = Path(skill_path).resolve()
    bundle_path = Path(bundle_path).resolve()

    if not bundle_path.exists():
        print(f"[ERROR] Bundle não encontrado: {bundle_path}")
        sys.exit(1)

    bundle_text = bundle_path.read_text(encoding="utf-8").lower()
    targets = []
    
    # 1. Validar Identidade pelo Título Real no SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.*)", content, re.MULTILINE)
        if match:
            real_title = match.group(1).strip().lower()
            targets.append(("SKILL.md", real_title))
        else:
            targets.append(("SKILL.md", skill_path.name.lower()))

    # 2. Varredura de Protocolos e Capacidades
    ignore = {".git", ".gemini", ".agents", "__pycache__", "node_modules", "dist", "temp_skills"}
    
    for root, dirs, files in os.walk(skill_path):
        dirs[:] = [d for d in dirs if d not in ignore]
        rel_root = Path(root).relative_to(skill_path)
        if rel_root.name in ignore: continue

        for f in files:
            if f in ["SKILL.md", ".gitignore", "AGENTS.md"] or f.startswith(".") or "license" in f.lower():
                continue
            
            if f.endswith((".md", ".py", ".js", ".sh", ".ts")):
                concept = normalize_concept(f)
                targets.append((f"{rel_root}/{f}", concept.lower()))

    print(f"🛡️  Auditando Cobertura Premium: {bundle_path.name}")
    print(f"📂  Skill Fonte: {skill_path.name}")
    print("-" * 65)
    
    total = len(targets)
    found_count = 0
    missing = []

    for original, concept in targets:
        # Busca flexível: o conceito purificado deve estar no texto
        if concept in bundle_text:
            found_count += 1
            status = "✅ OK"
        else:
            missing.append((original, concept))
            status = "❌ MISSING"
        
        print(f"{status:10} | {original:38} -> '{concept}'")

    print("-" * 65)
    coverage = (found_count / total) * 100 if total > 0 else 100
    print(f"📊 REPORT: {coverage:.1f}% COVERAGE")
    print(f"🔍 {found_count} de {total} conceitos purificados integrados.")

    if missing:
        print("\n⚠️  ALERTA DE COVERAGE:")
        for orig, concept in missing:
            print(f"   - {orig} (Esperado conceito: '{concept}')")
        sys.exit(1)
    else:
        print("\n✨ FINALIZADO: System Instruction Purificada com 100% de Cobertura!")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/test_coverage.py <skill_folder> <bundle_file>")
        sys.exit(1)
    run_coverage_test(skill_path, bundle_path)
