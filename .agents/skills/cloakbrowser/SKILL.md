---
name: cloakbrowser
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging cloakbrowser. Use this skill whenever modifying cloakbrowser configurations or adding related functionality.
---
# cloakbrowser

## File Tree

```text
cloakbrowser/
├── assets
├── modules
│   └── CloakBrowser (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

### AST Map: `modules/CloakBrowser`

```python
cloakbrowser/_version.py:
│__version__ = "0.3.32"

cloakbrowser/browser.py:
⋮
│async def launch_async(  # noqa: C901
│    headless: bool = True,
│    proxy: str | ProxySettings | None = None,
│    args: list[str] | None = None,
│    stealth_args: bool = True,
│    timezone: str | None = None,
│    locale: str | None = None,
│    geoip: bool = False,
│    humanize: bool = False,
│    human_preset: HumanPreset = "default",
⋮

cloakbrowser/config.py:
⋮
│def get_chromium_version() -> str:
⋮
│def get_platform_tag() -> str:
⋮
│def get_cache_dir() -> Path:
⋮
│def get_binary_dir(version: str | None = None) -> Path:
⋮
│def get_binary_path(version: str | None = None) -> Path:
⋮
│def get_archive_ext() -> str:
⋮
│def get_archive_name(tag: str | None = None) -> str:
⋮
│def get_local_binary_override() -> str | None:
⋮

cloakbrowser/human/config.py:
⋮
│HumanPreset = Literal["default", "careful"]
│
⋮
│@dataclass
│class HumanConfig:
⋮
│def rand_range(r: Range) -> float:
⋮

cloakbrowser/widevine.py:
⋮
│def resolve_widevine_cdm_dir(binary_path: str | os.PathLike) -> Path | None:
⋮

js/src/human/config.ts:
⋮
│export interface HumanConfig {
│  // Keyboard
│  typing_delay: number;
│  typing_delay_spread: number;
│  typing_pause_chance: number;
│  typing_pause_range: [number, number];
│  shift_down_delay: [number, number];
│  shift_up_delay: [number, number];
│  key_hold: [number, number];
│  field_switch_delay: [number, number];
⋮
│export type HumanPreset = 'default' | 'careful';
│
⋮
│export function sleep(ms: number): Promise<void> {
│  return new Promise(resolve => setTimeout(resolve, ms));
⋮

js/src/types.ts:
⋮
│export interface LaunchOptions {
│  /** Run in headless mode (default: true). */
│  headless?: boolean;
│  /**
│   * Proxy server — URL string or Playwright proxy object.
│   * String: 'http://user:pass@proxy:8080' (credentials auto-extracted).
│   * Object: { server: "http://proxy:8080", bypass: ".google.com", ... }
│   *   — passed directly to Playwright.
│   */
│  proxy?: string | { server: string; bypass?: string; username?: string; password?: string };
⋮

js/src/widevine.ts:
⋮
│export function resolveWidevineCdmDir(binaryPath: string): string | null {
│  const custom = process.env.CLOAKBROWSER_WIDEVINE_CDM;
│  // `!== undefined` (not truthiness): a present-but-empty env var is "set" and
│  // used exclusively — it resolves to an invalid path and skips seeding.
│  const cdmDir = custom !== undefined ? custom : path.join(path.dirname(binaryPath), "WidevineCdm")
│  return isFile(path.join(cdmDir, "manifest.json")) ? realPath(cdmDir) : null;
⋮

tests/test_cloakserve.py:
⋮
│parse_connection_params = _mod.parse_connection_params
│parse_cli_args = _mod.parse_cli_args
⋮
│class TestHandlerURLRewriting:
│    """Verify handlers rewrite CDP WebSocket URLs to the public cloakserve endpoint."""
│
⋮
│    class _FakeSession:
│        def __init__(self, data):
⋮
│        def get(self, *_args, **_kwargs):
⋮
```
