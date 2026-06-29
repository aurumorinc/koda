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

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/CloakBrowser`

```python
bin\fetch-widevine.py:
⋮
│def _read_varint(b, i):
⋮
│def main(argv=None):
│    ap = argparse.ArgumentParser(description="Fetch the Widevine CDM for CloakBrowser (Linux).")
⋮
│    def log(msg):
⋮

cloakbrowser\__init__.py:
⋮
│def __getattr__(name):
⋮

cloakbrowser\browser.py:
⋮
│class ProxySettings(_ProxySettingsRequired, total=False):
⋮
│def launch(
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
│def launch_persistent_context(
│    user_data_dir: str | os.PathLike,
│    headless: bool = True,
│    proxy: str | ProxySettings | None = None,
│    args: list[str] | None = None,
│    stealth_args: bool = True,
│    user_agent: str | None = None,
│    viewport: dict | None = _VIEWPORT_UNSET,
│    locale: str | None = None,
│    timezone: str | None = None,
⋮
│def launch_context(
│    headless: bool = True,
│    proxy: str | ProxySettings | None = None,
│    args: list[str] | None = None,
│    stealth_args: bool = True,
│    user_agent: str | None = None,
│    viewport: dict | None = _VIEWPORT_UNSET,
│    locale: str | None = None,
│    timezone: str | None = None,
│    color_scheme: Literal["light", "dark", "no-preference"] | None = None,
⋮
│async def launch_context_async(
│    headless: bool = True,
│    proxy: str | ProxySettings | None = None,
│    args: list[str] | None = None,
│    stealth_args: bool = True,
│    user_agent: str | None = None,
│    viewport: dict | None = _VIEWPORT_UNSET,
│    locale: str | None = None,
│    timezone: str | None = None,
│    color_scheme: Literal["light", "dark", "no-preference"] | None = None,
⋮
│def maybe_resolve_geoip(
│    geoip: bool,
│    proxy: str | ProxySettings | None,
│    timezone: str | None,
│    locale: str | None,
⋮
│def build_args(
│    stealth_args: bool,
│    extra_args: list[str] | None,
│    timezone: str | None = None,
│    locale: str | None = None,
│    headless: bool = True,
│    extension_paths: list[str] | None = None,
⋮
│def _maybe_warn_windows_fonts(chrome_args: list[str]) -> None:
⋮

cloakbrowser\config.py:
⋮
│def get_default_stealth_args() -> list[str]:
⋮
│def normalize_requested_version(version: str | None = None) -> str | None:
⋮
│def get_chromium_version() -> str:
⋮
│def get_platform_tag() -> str:
⋮
│def get_cache_dir() -> Path:
⋮
│def get_binary_dir(version: str | None = None, pro: bool = False) -> Path:
⋮
│def get_binary_path(version: str | None = None, pro: bool = False) -> Path:
⋮
│def _version_tuple(v: str) -> tuple[int, ...]:
⋮
│def _version_newer(a: str, b: str) -> bool:
⋮
│def get_archive_ext() -> str:
⋮
│def get_archive_name(tag: str | None = None) -> str:
⋮
│def get_local_binary_override() -> str | None:
⋮

cloakbrowser\download.py:
⋮
│def ensure_binary(
│    license_key: str | None = None,
│    browser_version: str | None = None,
⋮

cloakbrowser\geoip.py:
⋮
│def resolve_proxy_geo_with_ip(
│    proxy_url: str,
⋮
│def resolve_proxy_exit_ip(proxy_url: str) -> str | None:
⋮

cloakbrowser\human\__init__.py:
⋮
│def patch_context(context: Any, cfg: HumanConfig) -> None:
⋮
│def patch_context_async(context: Any, cfg: HumanConfig) -> None:
⋮

cloakbrowser\human\actionability.py:
⋮
│class ActionabilityError(RuntimeError):
⋮
│class ElementNotAttachedError(ActionabilityError):
⋮
│class ElementNotVisibleError(ActionabilityError):
⋮
│class ElementNotStableError(ActionabilityError):
⋮
│class ElementNotEnabledError(ActionabilityError):
⋮
│class ElementNotEditableError(ActionabilityError):
⋮
│class ElementNotReceivingEventsError(ActionabilityError):
⋮

cloakbrowser\human\config.py:
⋮
│@dataclass
│class HumanConfig:
⋮
│def _careful_config() -> HumanConfig:
⋮
│def resolve_config(
│    preset: HumanPreset = "default",
│    overrides: HumanConfigOverrides | None = None,
⋮
│def rand_range(r: Range) -> float:
⋮
│def rand_int_range(r: Range) -> int:
⋮
│def sleep_ms(ms: float) -> None:
⋮
│async def async_sleep_ms(ms: float) -> None:
⋮

cloakbrowser\human\keyboard.py:
⋮
│class RawKeyboard(Protocol):
⋮

cloakbrowser\human\mouse.py:
⋮
│class RawMouse(Protocol):
⋮

cloakbrowser\license.py:
⋮
│@dataclass
│class LicenseInfo:
⋮

cloakbrowser\widevine.py:
⋮
│def resolve_widevine_cdm_dir(binary_path: str | os.PathLike) -> Path | None:
⋮
│def seed_widevine_hint(user_data_dir: str | os.PathLike, binary_path: str | os.PathLike) -> None:
⋮

dotnet\src\CloakBrowser\CloakLauncher.cs:
⋮
│public static class CloakLauncher
│{
⋮
│    public static List<string> BuildArgs(
│        bool stealthArgs,
│        List<string>? extraArgs,
│        string? timezone = null,
│        string? locale = null,
│        bool headless = true,
⋮

dotnet\src\CloakBrowser\CloakLog.cs:
⋮
│public static class CloakLog
│{
⋮
│    public static void Debug(string message) => Emit(CloakLogLevel.Debug, message);
│    public static void Info(string message) => Emit(CloakLogLevel.Info, message);
│    public static void Warning(string message) => Emit(CloakLogLevel.Warning, message);
│    public static void Error(string message) => Emit(CloakLogLevel.Error, message);
│
│    public static void Debug(string format, params object?[] args) => Emit(CloakLogLevel.Debug, Fmt
│    public static void Info(string format, params object?[] args) => Emit(CloakLogLevel.Info, Fmt(f
│    public static void Warning(string format, params object?[] args) => Emit(CloakLogLevel.Warning,
│
│    private static string Fmt(string format, object?[] args)
⋮
│    private static void Emit(CloakLogLevel level, string message)
⋮

dotnet\src\CloakBrowser\CloakVersion.cs:
⋮
│public static class CloakVersion
⋮

dotnet\src\CloakBrowser\Config.cs:
⋮
│public static class Config
│{
⋮
│    public static string GetChromiumVersion()
⋮
│    public static string? NormalizeRequestedVersion(string? version = null)
⋮
│    public static string GetPlatformTag()
⋮
│    private static PlatformNotSupportedException Unsupported(string system, Architecture arch) =>
│        new($"Unsupported platform: {system} {arch}. " +
⋮
│    public static string GetCacheDir()
⋮
│    public static string GetBinaryDir(string? version = null, bool pro = false)
⋮
│    public static string GetEffectiveVersion(bool pro = false)
⋮
│    public static int[] VersionTuple(string v) =>
⋮

dotnet\src\CloakBrowser\Diagnostics.cs:
⋮
│internal static class Diagnostics
│{
│    internal static Dictionary<string, object?> Collect(bool quick)
⋮

dotnet\src\CloakBrowser\Download.cs:
⋮
│public sealed class BinaryVerificationError : Exception
⋮

dotnet\src\CloakBrowser\Handles.cs:
⋮
│public sealed class CloakBrowserHandle : IAsyncDisposable
│{
⋮
│    public Task<IPage> NewPageAsync(BrowserNewPageOptions? options = null) =>
⋮
│public sealed class CloakContextHandle : IAsyncDisposable
│{
⋮
│    public Task<IPage> NewPageAsync() => Context.NewPageAsync();
│
⋮

dotnet\src\CloakBrowser\Human\Actionability.cs:
⋮
│public class ActionabilityError : Exception
⋮
│public sealed class ElementNotAttachedError : ActionabilityError
⋮
│public sealed class ElementNotVisibleError : ActionabilityError
⋮
│public sealed class ElementNotStableError : ActionabilityError
⋮
│public sealed class ElementNotEnabledError : ActionabilityError
⋮
│public sealed class ElementNotEditableError : ActionabilityError
⋮
│public sealed class ElementNotReceivingEventsError : ActionabilityError
⋮
│public static class Actionability
│{
⋮
│    internal static double RemainingMs(double deadline) => Math.Max(0, deadline - NowMs());
│
⋮

dotnet\src\CloakBrowser\Human\HumanConfig.cs:
⋮
│public sealed class HumanConfig
│{
⋮
│    public HumanConfig Clone() => (HumanConfig)MemberwiseClone();
⋮
│public static class HumanConfigExtensions
│{
⋮
│    public static HumanConfig With(this HumanConfig baseCfg, IReadOnlyDictionary<string, object>? o
⋮

dotnet\src\CloakBrowser\Human\HumanKeyboard.cs:
⋮
│public interface IRawKeyboard
│{
⋮
│    Task InsertTextAsync(string text);
⋮
│public interface IRawCdpSession
│{
│    Task SendAsync(string method, JsonObject? args = null);
⋮
│public interface IRawEvaluator
│{
│    Task EvaluateAsync(string expression, object? arg);
⋮
│public static class HumanKeyboard
│{
⋮
│    public static async Task HumanTypeAsync(
│        IRawEvaluator? evaluator,
│        IRawKeyboard raw,
│        string text,
│        HumanConfig cfg,
⋮

dotnet\src\CloakBrowser\Human\HumanMouse.cs:
⋮
│public interface IRawMouse
│{
│    Task MoveAsync(double x, double y);
⋮
│public static class HumanMouse
│{
⋮
│    public static async Task HumanMoveAsync(
│        IRawMouse raw,
│        double startX, double startY,
│        double endX, double endY,
⋮

dotnet\src\CloakBrowser\Human\HumanRandom.cs:
⋮
│public static class HumanRandom
│{
⋮
│    public static double NextDouble() => Rng.NextDouble();
│
⋮
│    public static double RandRange(Range r) => Rand(r.Min, r.Max);
│
⋮
│    public static int RandIntRange(Range r) => RandInt((int)r.Min, (int)r.Max);
│
⋮
│    public static Task SleepMsAsync(double ms)
⋮

dotnet\src\CloakBrowser\Human\HumanScroll.cs:
⋮
│public interface IRawScrollPage
⋮
│public static class HumanScroll
│{
⋮
│    public static async Task<ScrollResult> HumanScrollIntoViewAsync(
│        IRawScrollPage page,
│        IRawMouse raw,
│        Func<Task<BoundingBox?>> getBox,
│        double cursorX, double cursorY,
⋮

dotnet\src\CloakBrowser\Human\IsolatedWorld.cs:
⋮
│public sealed class IsolatedWorld
│{
⋮
│    public async Task<JsonElement?> EvaluateAsync(string expression)
⋮

dotnet\src\CloakBrowser\Human\PlaywrightAdapters.cs:
⋮
│internal sealed class PlaywrightRawMouse : IRawMouse
│{
⋮
│    public Task MoveAsync(double x, double y) => _mouse.MoveAsync((float)x, (float)y);
⋮
│internal sealed class PlaywrightRawKeyboard : IRawKeyboard
│{
⋮
│    public Task InsertTextAsync(string text) => _keyboard.InsertTextAsync(text);
⋮
│internal sealed class PlaywrightCdpSession : IRawCdpSession
│{
⋮
│    public async Task SendAsync(string method, JsonObject? args = null)
⋮
│internal sealed class PlaywrightEvaluator : IRawEvaluator
│{
⋮
│    public async Task EvaluateAsync(string expression, object? arg)
⋮

dotnet\src\CloakBrowser\LaunchOptions.cs:
⋮
│public class LaunchOptions
⋮
│public class LaunchContextOptions : LaunchOptions
⋮

dotnet\src\CloakBrowser\License.cs:
⋮
│public static class License
│{
⋮
│    public static string? ResolveLicenseKey(string? licenseKey = null)
⋮
│    public static LicenseInfo? ValidateLicense(string licenseKey)
⋮
│    public static string? GetProLatestVersion()
⋮

dotnet\src\CloakBrowser\ProxySettings.cs:
⋮
│public sealed class ProxySettings
⋮

dotnet\src\CloakBrowser\ViewportDefaults.cs:
⋮
│internal static class ViewportDefaults
│{
│    public static BrowserNewPageOptions ApplyHeadedNoViewport(BrowserNewPageOptions? options, bool 
⋮
│    public static BrowserNewContextOptions ApplyHeadedNoViewport(BrowserNewContextOptions? options,
⋮

dotnet\src\CloakBrowser\Widevine.cs:
⋮
│public static class Widevine
│{
⋮
│    public static void SeedWidevineHint(string? userDataDir, string binaryPath)
⋮

dotnet\src\CloakBrowser\Wrappers\HumanCursor.cs:
⋮
│internal sealed class HumanCursor
│{
⋮
│    public void Set(double x, double y) { X = x; Y = y; }
│
⋮
│    public async Task EnsureInitializedAsync(HumanConfig cfg)
⋮
│    public Task HumanTypeAsync(string text, HumanConfig cfg) =>
⋮

dotnet\src\CloakBrowser\Wrappers\HumanizedBrowser.cs:
⋮
│[GenerateInterfaceDelegation(typeof(IBrowser))]
│public sealed partial class HumanizedBrowser : IBrowser
│{
⋮
│    public async Task<IPage> NewPageAsync(BrowserNewPageOptions? options = null) =>
│        await Humanize.WrapPageAsync(
│            await _inner.NewPageAsync(ViewportDefaults.ApplyHeadedNoViewport(options, _headless)).C
⋮

dotnet\src\CloakBrowser\Wrappers\HumanizedBrowserContext.cs:
⋮
│[GenerateInterfaceDelegation(typeof(IBrowserContext))]
│public sealed partial class HumanizedBrowserContext : IBrowserContext
│{
⋮
│    public async Task<IPage> NewPageAsync() =>
⋮

dotnet\src\CloakBrowser\Wrappers\HumanizedFrame.cs:
⋮
│[GenerateInterfaceDelegation(typeof(IFrame))]
│public sealed partial class HumanizedFrame : IFrame
│{
⋮
│    public async Task<IReadOnlyList<string>> SelectOptionAsync(string selector, string values, Fram
⋮
│    public async Task<IReadOnlyList<string>> SelectOptionAsync(string selector, IElementHandle valu
⋮
│    public async Task<IReadOnlyList<string>> SelectOptionAsync(string selector, IEnumerable<string>
⋮
│    public async Task<IReadOnlyList<string>> SelectOptionAsync(string selector, SelectOptionValue v
⋮
│    public async Task<IReadOnlyList<string>> SelectOptionAsync(string selector, IEnumerable<IElemen
⋮
│    public async Task<IReadOnlyList<string>> SelectOptionAsync(string selector, IEnumerable<SelectO
⋮

dotnet\src\CloakBrowser\Wrappers\HumanizedKeyboard.cs:
⋮
│[GenerateInterfaceDelegation(typeof(IKeyboard))]
│public sealed partial class HumanizedKeyboard : IKeyboard
│{
⋮
│    public Task InsertTextAsync(string text) =>
│        // InsertText is an atomic IME-style insertion; humanize it as paced typing.
⋮

dotnet\src\CloakBrowser\Wrappers\HumanizedMouse.cs:
⋮
│[GenerateInterfaceDelegation(typeof(IMouse))]
│public sealed partial class HumanizedMouse : IMouse
│{
⋮
│    public async Task MoveAsync(float x, float y, MouseMoveOptions? options = null)
⋮

dotnet\tests\CloakBrowser.Tests\BezierMathTests.cs:
⋮
│public class BezierMathTests
│{
│    // Mirrors Python _FakeRawMouse - records every movement point.
│    private sealed class FakeRawMouse : IRawMouse
│    {
│        public List<(double X, double Y)> Moves { get; } = new();
│        public Task MoveAsync(double x, double y) { Moves.Add((x, y)); return Task.CompletedTask; }
⋮

dotnet\tests\CloakBrowser.Tests\EnvSerialCollection.cs:
⋮
│[CollectionDefinition("env-serial")]
│public sealed class EnvSerialCollection { }

dotnet\tests\CloakBrowser.Tests\Human\NonAsciiKeyboardTests.cs:
⋮
│public class NonAsciiKeyboardTests
│{
│    /// <summary>A fake raw keyboard that records the keys pressed and the text inserted.</summary>
│    private sealed class RecordingKeyboard : IRawKeyboard
│    {
⋮
│        public Task InsertTextAsync(string text) { Inserted.Add(text); return Task.CompletedTask; }
⋮

dotnet\tests\CloakBrowser.Tests\LicenseTests.cs:
⋮
│[Collection("env-serial")]
│public class LicenseTests : IDisposable
│{
⋮
│    private sealed class RecordingHandler : HttpMessageHandler
│    {
⋮
│        protected override Task<HttpResponseMessage> SendAsync(
⋮

dotnet\tests\CloakBrowser.Tests\ScrollFallbackTests.cs:
⋮
│public class ScrollFallbackTests
│{
│    private sealed class FakeRawMouse : IRawMouse
│    {
│        public Task MoveAsync(double x, double y) => Task.CompletedTask;
⋮
│    private sealed class NoViewportPage : IRawScrollPage
⋮

dotnet\tests\CloakBrowser.Tests\Wrappers\FakeProxy.cs:
⋮
│public sealed class CallRecord
⋮
│public class FakeProxy : DispatchProxy
│{
⋮
│    protected override object? Invoke(MethodInfo? targetMethod, object?[]? args)
⋮

examples\integrations\aws_lambda\lambda_handler.py:
⋮
│def _validate_url(url: str) -> None:
⋮

js\examples\stealth-test.ts:
⋮
│interface TestResult {
│  name: string;
│  status: "PASS" | "FAIL" | "ERROR";
│  verdict: string;
⋮
│async function testSannysoft() {
│  console.log("--- bot.sannysoft.com ---");
│  await page.goto("https://bot.sannysoft.com", {
│    waitUntil: "networkidle",
│    timeout: 30000,
│  });
│  await page.waitForTimeout(3000);
│
│  const result = await page.evaluate(() => {
│    const rows = document.querySelectorAll("table tr");
⋮
│async function testIncolumitas() {
│  console.log("--- bot.incolumitas.com ---");
│  await page.goto("https://bot.incolumitas.com", {
│    waitUntil: "networkidle",
│    timeout: 30000,
│  });
│  await page.waitForTimeout(12000); // needs time for all detection tests
│
│  const result = await page.evaluate(() => {
│    const text = document.body.innerText;
⋮
│async function testBrowserScan() {
│  console.log("--- BrowserScan ---");
│  await page.goto("https://www.browserscan.net/bot-detection", {
│    waitUntil: "networkidle",
│    timeout: 30000,
│  });
│  await page.waitForTimeout(5000);
│
│  const result = await page.evaluate(() => {
│    const text = document.body.innerText;
⋮
│async function testDeviceAndBrowserInfo() {
│  console.log("--- deviceandbrowserinfo.com ---");
│  await page.goto("https://deviceandbrowserinfo.com/are_you_a_bot", {
│    waitUntil: "domcontentloaded",
│    timeout: 30000,
│  });
│  await page.waitForTimeout(8000);
│
│  const result = await page.evaluate(() => {
│    const text = document.body.innerText;
⋮
│async function testFingerprintJS() {
│  console.log("--- FingerprintJS ---");
│  await page.goto("https://demo.fingerprint.com/web-scraping", {
│    waitUntil: "networkidle",
│    timeout: 30000,
│  });
│  await page.waitForTimeout(5000);
│
│  try {
│    await page.click("button:has-text('Search')", { timeout: 5000 });
⋮
│async function testRecaptcha() {
│  console.log("--- reCAPTCHA v3 (Google) ---");
│  await page.goto(
│    "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
│    { waitUntil: "networkidle", timeout: 30000 }
│  );
│  await page.waitForTimeout(8000);
│
│  const result = await page.evaluate(() => {
│    const text = document.body.innerText;
⋮

js\src\config.ts:
⋮
│export function getCacheDir(): string {
│  const custom = process.env.CLOAKBROWSER_CACHE_DIR;
│  if (custom) return custom;
│  return path.join(os.homedir(), ".cloakbrowser");
⋮

js\src\download.ts:
⋮
│export class BinaryVerificationError extends Error {
│  constructor(message: string) {
│    super(message);
│    this.name = "BinaryVerificationError";
│  }
⋮

js\src\fonts.ts:
⋮
│export function windowsFontsPresent(): boolean | null {
│  let listing: string;
│  try {
│    // maxBuffer 16 MB: a host with a large font set can produce an fc-list
│    // listing well over Node's 1 MB default, which would otherwise throw and
│    // skip the warning (Python/.NET have no such cap).
│    listing = execFileSync("fc-list", { encoding: "utf8", timeout: 5000, maxBuffer: 16 * 1024 * 102
│  } catch {
│    return null;
│  }
⋮

js\src\human-puppeteer\index.ts:
⋮
│class StealthEval {
│  private cdp: CDPSession | null = null;
│  private contextId: number | null = null;
│  private page: Page;
│
│  constructor(page: Page) {
│    this.page = page;
│  }
│
│  private async ensureCdp(): Promise<CDPSession> {
⋮
│  async evaluate(expression: string): Promise<any> {
│    if (this.contextId === null) {
│      await this.createWorld();
│    }
│
│    for (let attempt = 0; attempt < 2; attempt++) {
│      try {
│        const cdp = await this.ensureCdp();
│        const result = await cdp.send('Runtime.evaluate', {
│          expression,
⋮

js\src\human\actionability.ts:
⋮
│export class ActionabilityError extends Error {
│  selector: string;
│  check: string;
│
│  constructor(selector: string, check: string, message: string) {
│    super(`Element ${JSON.stringify(selector)} failed ${check} check: ${message}`);
│    this.name = 'ActionabilityError';
│    this.selector = selector;
│    this.check = check;
│  }
⋮
│export class ElementNotAttachedError extends ActionabilityError {
│  constructor(selector: string) {
│    super(selector, 'attached', 'element not found in DOM');
│    this.name = 'ElementNotAttachedError';
│  }
⋮
│export class ElementNotVisibleError extends ActionabilityError {
│  constructor(selector: string) {
│    super(selector, 'visible', 'element is not visible');
│    this.name = 'ElementNotVisibleError';
│  }
⋮
│export class ElementNotStableError extends ActionabilityError {
│  constructor(selector: string) {
│    super(selector, 'stable', 'element position is still changing');
│    this.name = 'ElementNotStableError';
│  }
⋮
│export class ElementNotEnabledError extends ActionabilityError {
│  constructor(selector: string) {
│    super(selector, 'enabled', 'element is disabled');
│    this.name = 'ElementNotEnabledError';
│  }
⋮
│export class ElementNotEditableError extends ActionabilityError {
│  constructor(selector: string) {
│    super(selector, 'editable', 'element is not editable');
│    this.name = 'ElementNotEditableError';
│  }
⋮
│export class ElementNotReceivingEventsError extends ActionabilityError {
│  coveringTag: string;
│  constructor(selector: string, coveringTag: string = 'unknown') {
│    super(selector, 'pointer_events', `element is covered by <${coveringTag}>`);
│    this.name = 'ElementNotReceivingEventsError';
│    this.coveringTag = coveringTag;
│  }
⋮

js\src\human\config.ts:
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
│export type HumanActionOptions = Partial<HumanConfig> & {
│  timeout?: number;
│  force?: boolean;
│  human_config?: Partial<HumanConfig>;
⋮
│export function sleep(ms: number): Promise<void> {
│  return new Promise(resolve => setTimeout(resolve, ms));
⋮

js\src\human\index.ts:
⋮
│class StealthEval {
│  private cdp: CDPSession | null = null;
│  private contextId: number | null = null;
│  private page: Page;
│
│  constructor(page: Page) {
│    this.page = page;
│  }
│
│  private async ensureCdp(): Promise<CDPSession> {
⋮
│  async evaluate(expression: string): Promise<any> {
│    if (this.contextId === null) {
│      await this.createWorld();
│    }
│
│    for (let attempt = 0; attempt < 2; attempt++) {
│      try {
│        const cdp = await this.ensureCdp();
│        const result = await cdp.send('Runtime.evaluate', {
│          expression,
⋮
│class CursorState {
│  x = 0;
│  y = 0;
│  initialized = false;
⋮

js\src\human\mouse.ts:
⋮
│export interface RawMouse {
│  move: (x: number, y: number) => Promise<void>;
│  down: (options?: any) => Promise<void>;
│  up: (options?: any) => Promise<void>;
│  wheel: (deltaX: number, deltaY: number) => Promise<void>;
⋮
│export interface RawKeyboard {
│  down: (key: string) => Promise<void>;
│  up: (key: string) => Promise<void>;
│  type: (text: string) => Promise<void>;
│  insertText: (text: string) => Promise<void>;
⋮

js\src\license.ts:
⋮
│export interface LicenseInfo {
│  valid: boolean;
│  plan: string;
│  expires: string | null;
⋮

js\src\playwright.ts:
⋮
│export async function launch(options: LaunchOptions = {}): Promise<Browser> {
│  const { chromium } = await import("playwright-core");
│  const browser = await chromium.launch(await buildLaunchOptions(options));
│  // Headed: a bare browser.newPage() would inherit Playwright's emulated 1280x720
│  // viewport -> outerWidth < innerWidth (impossible window = bot tell). Default
│  // newPage()/newContext() to viewport:null so the page tracks the real window.
│  // Headless keeps Playwright's default viewport (coherent there).
│  if (!effectiveHeadless(options)) {
│    applyDefaultNoViewport(browser);
│  }
⋮

js\src\proxy.ts:
⋮
│export interface ParsedProxy {
│  server: string;
│  username?: string;
│  password?: string;
⋮
│export type ProxyDict = { server: string; bypass?: string; username?: string; password?: string };
│
⋮
│export interface ProxyConfig {
│  /** Playwright proxy option (for HTTP proxies). */
│  proxyOption?: ParsedProxy;
│  /** Chrome CLI args (for SOCKS5 proxies, e.g. ["--proxy-server=socks5://..."]). */
│  proxyArgs: string[];
⋮

js\src\puppeteer.ts:
⋮
│export async function launch(options: LaunchOptions = {}): Promise<Browser> {
│  const puppeteer = await import("puppeteer-core");
│  const { binaryPath, args } = await resolveArgs(options);
│  const proxyAuth = resolveProxy(options, args);
│
│  const browser = await puppeteer.default.launch({
│    ...options.launchOptions,
│    executablePath: binaryPath,
│    headless: options.headless ?? true,
│    args,
⋮

js\src\types.ts:
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
│export interface LaunchContextOptions extends LaunchOptions {
│  /** Custom user agent string. */
│  userAgent?: string;
│  /** Viewport size. */
│  viewport?: { width: number; height: number } | null;
│  /** Browser locale, e.g. "en-US". */
│  locale?: string;
│  /** IANA timezone — alias for `timezone`. Either works. */
│  timezoneId?: string;
│  /** Color scheme preference — 'light', 'dark', or 'no-preference'. */
⋮

js\src\widevine.ts:
⋮
│function realPath(p: string): string {
│  try {
│    return fs.realpathSync(p);
│  } catch {
│    return path.resolve(p);
│  }
⋮
│function seedingDisabled(): boolean {
│  const val = (process.env.CLOAKBROWSER_WIDEVINE ?? "").trim().toLowerCase();
│  return val === "0" || val === "false" || val === "off" || val === "no";
⋮
│export function resolveWidevineCdmDir(binaryPath: string): string | null {
│  const custom = process.env.CLOAKBROWSER_WIDEVINE_CDM;
│  if (custom !== undefined) {
│    // Set exclusively (overrides auto-detection). An empty/whitespace value is
│    // invalid — return null rather than let path.join("", ...) match a stray
│    // manifest.json in the working directory.
│    if (custom.trim() === "") return null;
│    return isFile(path.join(custom, "manifest.json")) ? realPath(custom) : null;
│  }
│  for (const cdmDir of [
⋮
│export function seedWidevineHint(userDataDir: string, binaryPath: string): void {
│  if (process.platform !== "linux") return;
│  if (seedingDisabled()) return;
│  // Empty userDataDir = Playwright's ephemeral profile (its own temp dir);
│  // a persistent hint can't be placed there, and "" would pollute the CWD.
│  if (!userDataDir) return;
│
│  // Everything below is best-effort and must never break the browser launch,
│  // so the whole body (resolution + write) is guarded.
│  try {
⋮

tests\test_cloakserve.py:
⋮
│class TestExternalHost:
│    """Test public host selection for rewritten CDP WebSocket URLs."""
│
│    class _Request:
⋮
│class TestHandlerURLRewriting:
│    """Verify handlers rewrite CDP WebSocket URLs to the public cloakserve endpoint."""
│
│    class _Request:
│        def __init__(self, headers, query_string="fingerprint=seed1", port=9222, scheme="http"):
│            self.headers = headers
│            self.query_string = query_string
│            self.scheme = scheme
⋮
│        class _Pool:
│            async def get_or_launch(self, **_kwargs):
⋮
│    class _FakeResponse:
⋮
│    class _FakeSession:
│        def __init__(self, data):
⋮
│        def get(self, *_args, **_kwargs):
⋮
│    def _patch_session(self, monkeypatch, data):
⋮
│class TestWebSocketOriginGuard:
│    """Verify cloakserve rejects browser-origin CDP WebSocket hijacks."""
│
⋮
│    def test_ws_handler_rejects_untrusted_origin_before_launching_chrome(self):
│        class RejectingPool:
│            async def get_or_launch(self, **_kwargs):
⋮
│    def test_seed_ws_handler_rejects_untrusted_origin_before_launching_chrome(self):
│        class RejectingPool:
│            async def get_or_launch(self, **_kwargs):
⋮
│class TestHandlerURLRewriting:
│    """Verify handlers rewrite CDP WebSocket URLs to the public cloakserve endpoint."""
│
│    def _rewrite_version(self, orig_ws: str, host: str, seed: str | None, scheme: str = "ws") -> st
⋮
│    def _rewrite_list_entry(self, orig_ws: str, host: str, seed: str | None, scheme: str = "ws") ->
⋮
│class TestConnectionTracking:
│    """Test ChromePool.connect() / disconnect() without real Chrome."""
│
│    def _make_pool(self, idle_timeout: float = 0.0):
⋮
│    def _track_process(self, pool, seed="seed1"):
⋮
│    def _track_live_process(self, pool, seed="seed1"):
⋮
│    def test_idle_cleanup_disabled_by_default(self):
│        async def run():
│            pool = self._make_pool()
│            self._track_process(pool)
│
│            pool.connect("seed1")
│            pool.disconnect("seed1")
│
│            await asyncio.sleep(0)
⋮
│    def test_disconnect_to_zero_schedules_idle_cleanup(self):
│        async def run():
│            pool = self._make_pool(idle_timeout=0.01)
│            self._track_process(pool)
│            cleaned = []
│
│            async def fake_cleanup(seed):
│                cleaned.append(seed)
│                pool._processes.pop(seed, None)
│
│            pool._cleanup_process = fake_cleanup
⋮
│    def test_reconnect_cancels_pending_idle_cleanup(self):
│        async def run():
│            pool = self._make_pool(idle_timeout=0.03)
│            self._track_process(pool)
│            cleaned = []
│
│            async def fake_cleanup(seed):
│                cleaned.append(seed)
│                pool._processes.pop(seed, None)
│
│            pool._cleanup_process = fake_cleanup
⋮
│    def test_discovery_refreshes_pending_idle_cleanup(self):
│        async def run():
│            pool = self._make_pool(idle_timeout=1.0)
│            self._track_live_process(pool)
│
│            pool.connect("seed1")
│            pool.disconnect("seed1")
│            first_task = pool._idle_tasks["seed1"]
│
│            await pool.get_or_launch("seed1")
│            second_task = pool._idle_tasks["seed1"]
│
⋮
│class TestSafeRmtree:
│    """Verify _safe_rmtree refuses to delete outside data_dir."""
│
│    def _make_pool(self, data_dir: str):
⋮
```