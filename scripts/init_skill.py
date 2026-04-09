#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--resources scripts,references,assets] [--examples]
"""

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Resources (optional)

### scripts/
### references/
### assets/
"""

def normalize_skill_name(skill_name):
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized

def title_case_skill_name(skill_name):
    return " ".join(word.capitalize() for word in skill_name.split("-"))

def init_skill(skill_name, path, resources, include_examples):
    skill_dir = Path(path).resolve() / skill_name
    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None
    skill_dir.mkdir(parents=True, exist_ok=False)
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)
    (skill_dir / "SKILL.md").write_text(skill_content)
    for resource in resources:
        (skill_dir / resource).mkdir(exist_ok=True)
    print(f"[OK] Skill '{skill_name}' initialized at {skill_dir}")
    return skill_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_name")
    parser.add_argument("--path", required=True)
    parser.add_argument("--resources", default="")
    args = parser.parse_args()
    resources = [r.strip() for r in args.resources.split(",") if r.strip()]
    init_skill(normalize_skill_name(args.skill_name), args.path, resources, False)
