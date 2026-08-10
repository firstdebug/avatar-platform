# avatar-platform - Codex plugin

This is the self-contained Codex package published by the avatar-platform
repository. It includes the runtime resources required by its Skills.

## Contents

- `.codex-plugin/plugin.json` - Codex plugin manifest.
- `skills/` - avatar-platform skills and references.
- `.codex/agents/` - converted Codex agent definitions.
- `tools/` - Xfyun platform Python tools for login, credentials, templates,
  live projects, model management, and knowledge bases.
- `config/` - tool registry, platform registry, and error-code mappings.
- `docs/` and `rules/` - source documentation and domain conventions.

## Codex Usage

The entry skill is `avatar-workflow-entry`. For virtual-human or digital-human
tasks, start from that skill so it can route to the correct expert skill.

When a skill asks to run `python tools/...`, run it from the plugin root:

```powershell
Set-Location <plugin-root>
python tools\xfyun_query_services.py
```

Install the GitHub marketplace and plugin with:

```powershell
codex plugin marketplace add firstdebug/avatar-platform --ref main
codex plugin add avatar-platform@avatar-platform-codex
```

## Runtime Dependencies

The Python tools require Python 3.8+ and the packages in `tools/requirements.txt`.
The browser-login flow also needs Playwright Chromium:

```powershell
pip install -r tools\requirements.txt
playwright install chromium
```

Network and browser operations are intentionally not run during plugin packaging.
