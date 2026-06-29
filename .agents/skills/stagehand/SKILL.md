---
name: stagehand
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging stagehand. Use this skill whenever modifying stagehand configurations or adding related functionality.
---
# stagehand

## File Tree

```text
stagehand/
├── assets
├── modules
│   └── stagehand (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/stagehand`

```python
packages\cli\src\base.ts:
⋮
│export abstract class BrowseCommand extends Command {
│  public override async init(): Promise<void> {
│    await super.init();
│    // Seed the CLI version from oclif's Config (the single source of truth) so
│    // non-command contexts — remote session userMetadata and cloud API headers
│    // — can stamp the real version without any filesystem read. This runs in
│    // every process before run(), including the background `browse daemon` that
│    // creates Browserbase sessions, so cli_version never regresses to "unknown".
│    setCliVersion(this.config.version);
│  }
│
⋮

packages\cli\src\commands\cloud\fetch.ts:
⋮
│type FetchFormat = (typeof fetchFormats)[number];
│
⋮

packages\cli\src\commands\cloud\sessions\create.ts:
⋮
│interface SessionCreateFlagInputs {
│  proxies?: boolean;
│  "advanced-stealth"?: boolean;
│  verified?: boolean;
│  "solve-captchas"?: boolean;
│  "block-ads"?: boolean;
│  region?: string;
│  "keep-alive"?: boolean;
│  timeout?: number;
│  "context-id"?: string;
⋮

packages\cli\src\commands\cloud\sessions\list.ts:
⋮
│type SessionStatus = "RUNNING" | "ERROR" | "TIMED_OUT" | "COMPLETED";
│
⋮

packages\cli\src\lib\driver\command-cli.ts:
⋮
│export type DriverFlags = DriverModeFlags & {
│  session?: string;
⋮
│export async function runDriverCommandFromFlags(
│  command: DriverCommandName,
│  params: unknown,
│  flags: DriverFlags,
⋮

packages\cli\src\lib\driver\flags.ts:
⋮
│export function sessionName(value?: string): string {
│  return value ?? process.env.BROWSE_SESSION ?? "default";
⋮

packages\cli\src\lib\driver\types.ts:
│export type ConnectionTarget =
⋮

packages\cli\tests\helpers\fake-browserbase-server.ts:
⋮
│export interface CapturedRequest {
│  method: string;
│  path: string;
│  headers: IncomingMessage["headers"];
│  bodyBuffer: Buffer;
│  bodyText: string;
│  jsonBody?: unknown;
⋮

packages\cli\tests\helpers\run-cli.ts:
⋮
│export interface RunCliOptions {
│  cwd?: string;
│  env?: NodeJS.ProcessEnv;
⋮

packages\cli\tests\identity-attribution.test.ts:
⋮
│describe("BrowseCommand.init() — version seeding at lifecycle boundary", () => {
│  beforeEach(() => {
│    // Fresh module so getCliVersion starts unseeded ("unknown") before init.
│    vi.resetModules();
│  });
│
│  it("seeds getCliVersion() from this.config.version when init() runs", async () => {
│    const { Config } = await import("@oclif/core");
│    const { BrowseCommand } = await import("../src/base.js");
│    const { getCliVersion } = await import("../src/lib/identity.js");
│
│    // Load the package's real oclif Config (this is the same Config oclif
│    // hands every command; its .version comes from package.json => 0.9.0).
│    // fileURLToPath keeps this correct on Windows (no leading-slash artifact).
│    const config = await Config.load(
│      fileURLToPath(new URL("..", import.meta.url)),
⋮
│    class TestCommand extends BrowseCommand {
│      async run(): Promise<void> {}
⋮

packages\core\examples\2048.ts:
⋮
│async function example() {
│  console.log("🎮 Starting 2048 bot...");
│  const stagehand = new Stagehand({
│    env: "LOCAL",
│    verbose: 1,
│  });
│
│  console.log("🌟 Initializing Stagehand...");
│  await stagehand.init();
│  const page = stagehand.context.pages()[0];
⋮

packages\core\examples\actionable-observe-example.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│  });
│  await stagehand.init();
│  const page = stagehand.context.pages()[0];
│
│  await page.goto("https://www.apartments.com/san-francisco-ca/");
│
⋮

packages\core\examples\clipboard.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto("https://example.com");
│
│  await new Promise((resolve) => setTimeout(resolve, 3000));
│  await page.evaluate(() => {
│    document.body.innerHTML =
│      "<textarea autofocus style='width:400px;height:120px'></textarea>";
│    document.querySelector("textarea")?.focus();
│  });
│
⋮

packages\core\examples\cua-replay.ts:
⋮
│async function runDemo(runNumber: number) {
│  const startTime = Date.now();
│
│  v3Logger({
│    level: 1,
│    category: "demo",
│    message: `RUN ${runNumber}: ${runNumber === 1 ? "BUILDING CACHE" : "USING CACHE"}`,
│  });
│
│  const stagehand = new Stagehand({
⋮

packages\core\examples\custom-client-aisdk.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│    llmClient: new AISdkClient({
│      model: openai("gpt-4.1"),
│    }),
│  });
│
│  await stagehand.init();
⋮

packages\core\examples\custom-client-openai.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│    llmClient: new CustomOpenAIClient({
│      modelName: "gpt-4.1-mini",
│      client: new OpenAI({
│        apiKey: process.env.OPENAI_API_KEY,
│      }),
│    }),
⋮

packages\core\examples\deep-locator.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://browserbase.github.io/stagehand-eval-sites/sites/oopif-in-closed-shadow-dom/",
│  );
│
│  // crossing OOPIF & shadow root boundaries with deep locator
│  await page
│    .deepLocator(
│      "/html/body/shadow-host//section/iframe/html/body/main/section[1]/form/div/div[1]/input",
⋮

packages\core\examples\dropdown.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://browserbase.github.io/stagehand-eval-sites/sites/scroll-dropdown/",
│  );
│
│  const actResult = await stagehand.act(
│    "choose 'Peach' from the favorite colour dropdown",
│  );
│
⋮

packages\core\examples\example.ts:
⋮
│async function example(stagehand: Stagehand) {
│  /**
│   * Add your code here!
│   */
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://browserbase.github.io/stagehand-eval-sites/sites/iframe-hn/",
│  );
│
│  const { extraction } = await stagehand.extract(
⋮

packages\core\examples\form-filling-sensible.ts:
⋮
│async function formFillingSensible() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│  });
│  await stagehand.init();
│  const page = stagehand.context.pages()[0];
│
│  // Go to the website and wait for it to load
│  await page.goto("https://file.1040.com/estimate/", {
⋮

packages\core\examples\google-enter.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│  });
│  await stagehand.init();
│  const page = stagehand.context.pages()[0];
│  await page.goto("https://google.com");
│  await stagehand.act("type in 'Browserbase'");
│  await stagehand.act("press enter");
⋮

packages\core\examples\highlight.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://browserbase.github.io/stagehand-eval-sites/sites/closed-shadow-root-in-oopif/",
│  );
│
│  await page
│    .deepLocator(
│      "xpath=/html/body/main/section/iframe/html/body/shadow-demo//div/button",
│    )
⋮

packages\core\examples\instructions.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│    systemPrompt:
│      "if the users says `secret12345`, click on the 'getting started' tab. additionally, if the us
│  });
│  await stagehand.init();
│
│  const page = stagehand.context.pages()[0];
⋮

packages\core\examples\integrations\exa.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto("https://www.google.com");
│
│  const agent = stagehand.agent({
│    integrations: [
│      `https://mcp.exa.ai/mcp?exaApiKey=${process.env.EXA_API_KEY}`,
│    ],
│    // Optional: Add custom instructions
│    systemPrompt: `You are a helpful assistant that can use a browser as well as external tools suc
⋮

packages\core\examples\integrations\patchright.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const browser = await chromium.connectOverCDP({
│    wsEndpoint: stagehand.connectURL(),
│  });
│
│  const prContext = browser.contexts()[0];
│  const prPage = prContext.pages()[0];
│  await prPage.goto("https://github.com/microsoft/playwright/issues/30261");
│
│  await stagehand.act("scroll to the bottom of the page", { page: prPage });
│
⋮

packages\core\examples\integrations\playwright.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const browser = await chromium.connectOverCDP({
│    wsEndpoint: stagehand.connectURL(),
│  });
│  const pwContext = browser.contexts()[0];
│  const pwPage1 = pwContext.pages()[0];
│  await pwPage1.goto("https://docs.stagehand.dev/first-steps/introduction");
│
│  const pwPage2 = await pwContext.newPage();
│  await pwPage2.goto("https://docs.stagehand.dev/configuration/observability");
│
⋮

packages\core\examples\integrations\puppeteer.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const browser = await puppeteer.connect({
│    browserWSEndpoint: stagehand.connectURL(),
│    defaultViewport: null,
│  });
│  const ppPages = await browser.pages();
│  const ppPage = ppPages[0];
│
│  await ppPage.goto("https://www.browserbase.com/blog");
│
⋮

packages\core\examples\integrations\supabase.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto("https://www.opentable.com/");
│
│  const supabaseClient = await connectToMCPServer(
│    `https://server.smithery.ai/@supabase-community/supabase-mcp/mcp?api_key=${process.env.SMITHERY
│  );
│
│  const agent = stagehand.agent({
│    model: "openai/computer-use-preview",
⋮

packages\core\examples\parameterize-api-key.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "LOCAL",
│    verbose: 1,
│    model: {
│      modelName: "gpt-4.1-mini",
│      apiKey: process.env.USE_OPENAI_API_KEY,
│    },
│  });
│
⋮

packages\core\examples\record-video.ts:
⋮
│async function recordPlaywrightVideo(stagehand: Stagehand): Promise<void> {
│  const browser = await chromium.connectOverCDP({
│    wsEndpoint: stagehand.connectURL(),
│  });
│
│  const videoDir = path.resolve(process.cwd(), "artifacts", "stagehand-videos");
│  await mkdir(videoDir, { recursive: true });
│
│  const context = await browser.newContext({
│    recordVideo: {
⋮

packages\core\examples\return-xpath.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://browserbase.github.io/stagehand-eval-sites/sites/oopif-in-closed-shadow-dom/",
│  );
│
│  const xpath = await page.click(286, 628, { returnXpath: true });
│
│  // use the xpath that was returned from out coord click
│  await page.deepLocator(xpath).fill("hellooooooooo");
⋮

packages\core\examples\shadow-root.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://browserbase.github.io/stagehand-eval-sites/sites/shadow-dom-closed/",
│  );
│
│  // clicking in closed mode shadow root with an xpath
│  await page.locator("/html/body/shadow-demo//div/button").click();
│
│  await new Promise((resolve) => setTimeout(resolve, 3000));
│
⋮

packages\core\examples\targeted-extract.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://ambarc.github.io/web-element-test/stagehand-breaking-test.html",
│  );
│
│  await page
│    .deepLocator("/html/body/div[2]/div[3]/iframe/html/body/p")
│    .highlight({
│      durationMs: 5000,
⋮

packages\core\examples\v3-example.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto("https://www.apartments.com/san-francisco-ca/2-bedrooms/", {
│    waitUntil: "load",
│  });
│  const apartment_listings = await stagehand.extract(
│    "Extract all the apartment listings with their prices and their addresses.",
│    z.object({
│      listings: z.array(
│        z.object({
⋮

packages\core\examples\webmcp.ts:
⋮
│async function example(stagehand: Stagehand) {
│  const page = stagehand.context.pages()[0];
│  await page.goto(
│    "https://googlechromelabs.github.io/webmcp-tools/demos/react-flightsearch/",
│    { waitUntil: "load" },
│  );
│
│  const tools = await page.listWebMCPTools();
│  console.log(`Found ${tools.length} WebMCP tools:`);
│  for (const tool of tools) {
⋮

packages\core\examples\wordle.ts:
⋮
│async function example() {
│  const stagehand = new Stagehand({
│    env: "BROWSERBASE",
│    verbose: 1,
│  });
│  await stagehand.init();
│  const page = stagehand.context.pages()[0];
│  await page.goto("https://www.nytimes.com/games/wordle/index.html");
│  await stagehand.act("click 'Continue'");
│  await stagehand.act("click 'Play'");
⋮

packages\core\lib\v3\types\public\context.ts:
⋮
│export interface ClearCookieOptions {
│  name?: string | RegExp;
│  domain?: string | RegExp;
│  path?: string | RegExp;
⋮

packages\core\lib\v3\understudy\context.ts:
⋮
│export class V3Context {
│  private constructor(
│    readonly conn: CdpConnection,
│    private readonly env: "LOCAL" | "BROWSERBASE" = "LOCAL",
│    private readonly apiClient: StagehandAPIClient | null = null,
│    private readonly localBrowserLaunchOptions: LocalBrowserLaunchOptions | null = null,
│  ) {}
│
│  private readonly _piercerInstalled = new Set<string>();
│  // Timestamp for most recent popup/open signal
⋮

packages\core\scripts\gen-version.ts:
⋮
│type PackageJson = { version: string };
│
⋮

packages\core\tests\cache-variables.test.ts:
⋮
│function createFakeStorage<T>(entry: T): CacheStorage {
│  return {
│    enabled: true,
│    readJson: vi.fn().mockResolvedValue({ value: entry }),
│    writeJson: vi.fn().mockResolvedValue({}),
│    directory: "/tmp/cache",
│  } as unknown as CacheStorage;
⋮

packages\core\tests\integration\keyboard.spec.ts:
⋮
│function dataUrl(html: string): string {
│  return "data:text/html;charset=utf-8," + encodeURIComponent(html);
⋮

packages\core\tests\integration\observe-element-id-format.spec.ts:
⋮
│type MainFrameCase = {
│  name: string;
│  instruction: string;
│  targetText: string;
│  marker: string;
│  html: string;
⋮

packages\core\tests\integration\shadow-iframe-oopif.spec.ts:
⋮
│type Framework = "v3" | "puppeteer" | "playwright" | "patchright";
│
⋮

packages\core\tests\integration\shadow-iframe-spif.spec.ts:
⋮
│type Framework = "v3" | "puppeteer" | "playwright" | "patchright";
│
⋮

packages\core\tests\integration\v3.config.ts:
⋮
│export function getV3TestConfig(overrides: Partial<V3Options> = {}): V3Options {
│  return getV3DynamicTestConfig(overrides);
⋮

packages\core\tests\integration\v3.dynamic.config.ts:
⋮
│export function getV3DynamicTestConfig(
│  overrides: Partial<V3Options> = {},
⋮

packages\core\tests\unit\agent-temperature.test.ts:
⋮
│type AgentLlmOptions = {
│  onStepFinish?: (step: unknown) => Promise<void> | void;
│  onFinish?: (event: unknown) => void;
│  providerOptions?: Record<string, unknown>;
│  temperature?: number;
⋮

packages\core\tests\unit\aisdk-clients.test.ts:
⋮
│function createModel(modelId: string) {
│  return {
│    modelId,
│    specificationVersion: "v2",
│  } as unknown as LanguageModelV2;
⋮

packages\core\tests\unit\api-optional-model-api-key.test.ts:
⋮
│describe("StagehandAPIClient - optional modelApiKey", () => {
│  const logger = vi.fn();
│
│  // We mock fetch to avoid real network calls; we just need to verify
│  // that init() doesn't throw when modelApiKey is omitted and that
│  // the header is conditionally included.
│  let originalFetch: typeof globalThis.fetch;
│
│  function createSessionStartResponse(sessionId: string) {
│    return new Response(
│      JSON.stringify({
│        success: true,
│        data: { sessionId, available: true },
│      }),
│      {
│        status: 200,
│        headers: { "Content-Type": "application/json" },
│      },
⋮

packages\core\tests\unit\cache-llm-resolution.test.ts:
⋮
│function createFakeStorage<T>(entry: T): CacheStorage {
│  return {
│    enabled: true,
│    readJson: vi.fn().mockResolvedValue({ value: entry }),
│    writeJson: vi.fn().mockResolvedValue({}),
│    directory: "/tmp/cache",
│  } as unknown as CacheStorage;
⋮

packages\core\tests\unit\google-cua-click-conversion.test.ts:
⋮
│function createGoogleClient(): GoogleCUAClient {
│  return new GoogleCUAClient(
│    "google",
│    "google/gemini-3.5-flash",
│    "test instructions",
│    { apiKey: "test" },
│  );
⋮

packages\core\tests\unit\helpers\mockCDPSession.ts:
⋮
│type Handler = (params?: Record<string, unknown>) => Promise<unknown> | unknown;
│type EventHandler = (params?: Record<string, unknown>) => void;
│
│export class MockCDPSession implements CDPSessionLike {
│  public readonly id: string;
│  public readonly calls: Array<{
│    method: string;
│    params?: Record<string, unknown>;
│  }> = [];
│  private readonly listeners = new Map<string, Set<EventHandler>>();
│
│  constructor(
│    private readonly handlers: Record<string, Handler> = {},
│    sessionId = "mock-session",
⋮
│  async send<R = unknown>(
│    method: string,
│    params: Record<string, unknown> = {},
⋮
│  emit(event: string, params: Record<string, unknown> = {}): void {
│    for (const handler of this.listeners.get(event) ?? []) {
│      handler(params);
│    }
⋮
│  listenerCount(event: string): number {
│    return this.listeners.get(event)?.size ?? 0;
⋮
│  callsFor(method: string): Array<{ params?: Record<string, unknown> }> {
│    return this.calls
│      .filter((call) => call.method === method)
│      .map(({ params }) => ({ params }));
⋮

packages\core\tests\unit\microsoft-cua-client.test.ts:
⋮
│function createClient() {
│  const client = new MicrosoftCUAClient("microsoft", "fara-7b", undefined, {
│    apiKey: "test-key",
│    baseURL: "https://example.com",
│  });
│  client.setScreenshotProvider(async () => "mock-base64-screenshot");
│  return client;
⋮

packages\core\tests\unit\public-api\export-surface.test.ts:
⋮
│type PublicAPI = {
│  [K in keyof typeof publicApiShape]: StagehandExports[K];
⋮

packages\core\tests\unit\public-api\public-error-types.test.ts:
⋮
│describe("Stagehand public error types", () => {
│  describe("errors", () => {
│    it.each(errorTypes)("%s extends Error", (errorTypeName) => {
│      const ErrorClass = Stagehand[errorTypeName];
│      type ErrorClassType = typeof ErrorClass;
│      expectTypeOf<InstanceType<ErrorClassType>>().toExtend<Error>();
│      void ErrorClass; // Mark as used to satisfy ESLint
│    });
│  });
⋮

packages\core\tests\unit\safety-confirmation.test.ts:
⋮
│type LoggerMock = (message: LogLine) => void;
│
⋮

packages\core\tests\unit\understudy-command-exception.test.ts:
⋮
│describe("UnderstudyCommandException", () => {
│  it("extends StagehandError", () => {
│    const err = new UnderstudyCommandException("test");
│    expect(err).toBeInstanceOf(StagehandError);
│    expect(err).toBeInstanceOf(Error);
│  });
│
│  it("has the correct name", () => {
│    const err = new UnderstudyCommandException("test");
│    expect(err.name).toBe("UnderstudyCommandException");
⋮
│  it("preserves the original stack via cause for debugging", () => {
│    function deepFunction() {
│      throw new Error("deep error");
│    }
│
│    let original: Error;
│    try {
│      deepFunction();
│    } catch (e) {
│      original = e as Error;
⋮

packages\core\tests\unit\verifier-evidence.test.ts:
⋮
│function makeTrajectory(
│  steps: TrajectoryStep[],
│  extra: Partial<Trajectory> = {},
⋮

packages\core\tests\unit\xpath-resolver.test.ts:
⋮
│type DomGlobals = {
│  window: Window & typeof globalThis;
│  document: Document;
│  Node: typeof Node;
│  NodeFilter: typeof NodeFilter;
│  Element: typeof Element;
│  HTMLElement: typeof HTMLElement;
│  Document: typeof Document;
│  DocumentFragment: typeof DocumentFragment;
│  ShadowRoot: typeof ShadowRoot;
⋮

packages\docs\language-selector.js:
⋮
│(function() {
│  // ============================================
│  // CONFIGURATION
│  // ============================================
│
│  const DROPDOWN_LANGUAGES = ['TypeScript', 'Python', 'Java', 'Go', 'Ruby'];
│
│  const LANGUAGE_MAP = {
│    'TypeScript': 'Javascript',
│    'Python': 'Python',
⋮
│  function init() {
│    setupMenuClickHandler();
│    setupDropdownMenuObserver();
│    setupPageChangeObserver();
│    setupCodeBlockObserver();
│
│    restoreLanguageSelection();
│    updateVersionSwitcherVisibility();
│    updateSDKReferenceVisibility();
⋮

packages\evals\cli-legacy.ts:
⋮
│interface Config {
│  defaults: {
│    env: string;
│    trials: number;
│    concurrency: number;
│    provider: string | null;
│    model: string | null;
│    api: boolean;
│  };
│  benchmarks: Record<
⋮

packages\evals\core\contracts\representation.ts:
│export interface RepresentationOpts {
⋮
│export interface PageRepresentation {
│  kind: "accessibility_tree" | "snapshot_refs" | "dom_text" | "custom";
│  content: string;
│  metadata?: {
│    bytes?: number;
│    tokenEstimate?: number;
│    refCount?: number;
│    nodeCount?: number;
│  };
│  raw?: unknown;
⋮

packages\evals\core\contracts\results.ts:
│export type EnvironmentName = "local" | "browserbase";
│
│export type BrowserOwnership = "runner" | "tool";
│
│export type ConnectionMode =
│  | "launch"
│  | "attach_ws"
│  | "attach_http"
⋮
│export interface Artifact {
│  name: string;
│  type: "text" | "json" | "image" | "binary";
│  path?: string;
│  data?: Buffer | string;
│  mimeType?: string;
⋮

packages\evals\core\contracts\targets.ts:
│export type TargetKind =
⋮
│export type FocusedTarget = { kind: "focused" };
│
│export type ActionTarget =
│  | { kind: "selector"; value: string }
│  | { kind: "coords"; x: number; y: number }
│  | { kind: "snapshot_ref"; value: string }
│  | { kind: "role_name"; role: string; name?: string }
⋮
│export type WaitSpec =
│  | {
│      kind: "selector";
│      selector: string;
│      timeoutMs?: number;
│      state?: "attached" | "detached" | "visible" | "hidden";
│    }
│  | {
│      kind: "timeout";
│      timeoutMs: number;
⋮

packages\evals\core\contracts\tool.ts:
⋮
│export type ToolSurface =
│  | "understudy_code"
│  | "playwright_code"
│  | "cdp_code"
│  | "playwright_mcp"
│  | "chrome_devtools_mcp"
⋮
│export type StartupProfile =
│  | "runner_provided_local_cdp"
│  | "runner_provided_browserbase_cdp"
│  | "tool_launch_local"
│  | "tool_attach_local_cdp"
│  | "tool_create_browserbase"
⋮
│export interface CoreSession {
│  listPages(): Promise<CorePageHandle[]>;
│  activePage(): Promise<CorePageHandle>;
│  newPage(url?: string): Promise<CorePageHandle>;
│  selectPage(pageId: string): Promise<void>;
│  closePage(pageId: string): Promise<void>;
│  close(): Promise<void>;
│  getArtifacts(): Promise<Artifact[]>;
│  getRawMetrics(): Promise<Record<string, unknown>>;
⋮
│export interface ToolStartInput {
│  logger: EvalLogger;
│  startupProfile: StartupProfile;
│  environment: "LOCAL" | "BROWSERBASE";
│  providedEndpoint?: {
│    kind: "ws" | "http";
│    url: string;
│    headers?: Record<string, string>;
│  };
│  browserbase?: {
⋮

packages\evals\env.ts:
⋮
│export function getEnv(): "BROWSERBASE" | "LOCAL" {
│  return process.env.EVAL_ENV?.toLowerCase() === "browserbase"
│    ? "BROWSERBASE"
│    : "LOCAL";
⋮

packages\evals\errors.ts:
│export class EvalsError extends Error {
⋮

packages\evals\framework\adHocRubric.ts:
⋮
│export function adHocRubric(...criteria: string[]): Rubric {
│  if (criteria.length === 0) {
│    throw new Error("adHocRubric requires at least one criterion");
│  }
│  return {
│    items: criteria.map((c) => ({
│      criterion: c,
│      description: c,
│      maxPoints: 1,
│    })),
⋮

packages\evals\framework\harnesses\persistTrajectory.ts:
⋮
│export interface PersistAdapterTrajectoryOptions {
│  trajectory: Trajectory;
│  taskSpec: TaskSpec;
│  /** EvaluationResult from V3Evaluator.verify(). Written to scores/result.json. */
│  evaluationResult?: EvaluationResult;
│  /**
│   * Output directory root. Final layout lives at `<outputRoot>/<runId>/<task.id>/`.
│   * Defaults to `<cwd>/.trajectories`.
│   */
│  outputRoot?: string;
⋮

packages\evals\framework\rubricCache.ts:
⋮
│export interface RubricCacheOptions {
│  /**
│   * Root directory for cached rubrics. Defaults to
│   * `<packages/evals>/.rubric-cache`.
│   */
│  cacheRoot?: string;
│  /**
│   * Dataset name, used as a subdirectory under cacheRoot to keep different
│   * datasets' rubrics separate (e.g., "onlineMind2Web").
│   */
⋮
│interface CacheEntry {
│  taskId: string;
│  instructionHash: string;
│  generatedAt: string;
│  rubric: Rubric;
⋮
│export class RubricCache {
│  private readonly cacheDir: string;
│
│  constructor(opts: RubricCacheOptions) {
│    const root =
│      opts.cacheRoot ??
│      path.join(process.cwd(), "packages/evals/.rubric-cache");
│    this.cacheDir = path.join(root, opts.dataset);
│  }
│
⋮
│  async write(taskSpec: TaskSpec, rubric: Rubric): Promise<void> {
│    await fs.mkdir(this.cacheDir, { recursive: true });
│    const entry: CacheEntry = {
│      taskId: taskSpec.id,
│      instructionHash: hashInstruction(taskSpec.instruction),
│      generatedAt: new Date().toISOString(),
│      rubric,
│    };
│    await fs.writeFile(
│      this.entryPath(taskSpec.id),
⋮

packages\evals\framework\trajectoryRecorder.ts:
⋮
│export interface TrajectoryRecorderOptions {
│  taskSpec: TaskSpec;
│  /**
│   * Root directory under which trajectory dirs are written. Each task run
│   * gets a subdirectory named by runId/task.id.
│   * Defaults to `<cwd>/.trajectories`.
│   */
│  outputRoot?: string;
│  /** Run identifier (e.g., ISO timestamp + env). Defaults to a fresh timestamp. */
│  runId?: string;
⋮
│export interface TrajectoryFinishOptions {
│  status: TrajectoryStatus;
│  finalAnswer?: string;
│  usage?: Partial<TrajectoryUsage>;
⋮

packages\evals\framework\types.ts:
⋮
│export interface TaskRegistry {
│  /** All discovered tasks. */
│  tasks: DiscoveredTask[];
│  /** Lookup by name. */
│  byName: Map<string, DiscoveredTask>;
│  /** Lookup by tier. */
│  byTier: Map<Tier, DiscoveredTask[]>;
│  /** Lookup by category. */
│  byCategory: Map<string, DiscoveredTask[]>;
⋮

packages\evals\logger.ts:
⋮
│export class EvalLogger {
│  private logs: LogLineEval[] = [];
│  private echo: boolean;
│  stagehand?: V3;
│
│  constructor(echo = true) {
│    this.logs = [];
│    this.echo = echo;
│  }
│
⋮
│  init(stagehand?: V3) {
│    this.stagehand = stagehand;
⋮

packages\evals\runtimePaths.ts:
⋮
│type CallSiteWithScriptName = NodeJS.CallSite & {
│  getScriptNameOrSourceURL?: () => string | null;
⋮

packages\evals\scripts\backfill-webtailbench-rubrics.ts:
⋮
│interface RawRubric {
│  items: Array<Record<string, unknown>>;
⋮

packages\evals\scripts\test-evals.ts:
⋮
│type Runtime = "source" | "dist-esm";
│
⋮

packages\evals\tasks\bench\agent\onlineMind2Web.ts:
⋮
│function formatProcessScore(score: number | undefined): string {
│  return typeof score === "number" ? score.toFixed(2) : "n/a";
⋮

packages\evals\tasks\bench\agent\webtailbench.ts:
⋮
│function formatProcessScore(score: number | undefined): string {
│  return typeof score === "number" ? score.toFixed(2) : "n/a";
⋮

packages\evals\tasks\bench\agent\webvoyager.ts:
⋮
│function formatProcessScore(score: number | undefined): string {
│  return typeof score === "number" ? score.toFixed(2) : "n/a";
⋮

packages\evals\tasks\bench\experimental\extract_press_releases.ts:
⋮
│export default defineBenchTask(
│  { name: "extract_press_releases" },
│  async ({ debugUrl, sessionUrl, v3, logger }) => {
│    const schema = z.object({
│      items: z.array(
│        z.object({
│          title: z.string().describe("The title of the press release"),
│          publish_date: z
│            .string()
│            .describe("The date the press release was published"),
│        }),
│      ),
⋮
│    type PressRelease = z.infer<typeof schema>["items"][number];
│
⋮

packages\evals\tests\framework\claudeCodeAdapterImages.test.ts:
⋮
│function imageBlock(data: string) {
│  return {
│    type: "image",
│    source: { type: "base64", media_type: "image/png", data },
│  };
⋮

packages\evals\tests\framework\persistTrajectory.test.ts:
⋮
│function makeTrajectory(task: TaskSpec): Trajectory {
│  return {
│    task,
│    status: "complete",
│    finalAnswer: "Final answer text.",
│    usage: { input_tokens: 100, output_tokens: 50 },
│    steps: [
│      {
│        actionName: "goto",
│        actionArgs: { url: "https://example.com" },
⋮

packages\evals\tests\tui\doctor.test.ts:
⋮
│type DoctorJsonReport = {
│  verdict: string;
│  reasons: string[];
│  [key: string]: unknown;
⋮

packages\evals\tests\tui\experiments.test.ts:
⋮
│function makeChildProcess(args: string[]): EventEmitter & {
│  stdout: EventEmitter;
│  stderr: EventEmitter;
⋮

packages\evals\tui\commandTree.ts:
⋮
│export type CommandNode = {
│  /** Canonical lowercase name. */
│  name: string;
│  aliases?: readonly string[];
│  summary: string;
│  /** If present, executable as a leaf with the given args. */
│  handler?: CommandHandler;
│  /** If present, descendable as a namespace. */
│  children?: readonly CommandNode[];
│  /** Per-node help printer. Receives the absolute path that was resolved. */
⋮

packages\evals\tui\commands\config.ts:
⋮
│type Defaults = {
│  env?: string | null;
│  trials?: number | null;
│  concurrency?: number | null;
│  provider?: string | null;
│  model?: string | null;
│  api?: boolean | null;
│  verbose?: boolean | null;
│  agentModes?: AgentToolMode[] | null;
⋮
│export type CoreConfigSection = {
│  tool?: string;
│  startup?: string;
⋮
│export type WelcomeMeta = {
│  /** ISO 8601 timestamp when the first-run welcome was completed. */
│  firstRunCompletedAt?: string;
│  /** Schema version for the welcome marker (currently 1). */
│  version?: number;
⋮
│export type ConfigFile = {
│  defaults: Defaults;
│  benchmarks?: Record<string, unknown>;
│  core?: CoreConfigSection;
│  _meta?: WelcomeMeta;
⋮

packages\evals\tui\format.ts:
⋮
│export type TaskStatus = "pending" | "running" | "passed" | "failed" | "error";
│
⋮

packages\evals\tui\preview.ts:
⋮
│interface PreviewPayload {
│  target: string | null;
│  normalizedTarget: string | null;
│  tasks: string[];
│  skippedTasks: string[];
│  envOverrides: Record<string, string>;
│  runOptions: Record<string, unknown>;
│  matrix: MatrixRow[];
│  error?: string;
⋮

packages\evals\tui\tokenize.ts:
⋮
│export function tokenize(input: string): string[] {
│  const tokens: string[] = [];
│  let current = "";
│  let inQuote: string | null = null;
│
│  for (const ch of input) {
│    if (inQuote) {
│      if (ch === inQuote) {
│        inQuote = null;
│      } else {
⋮

packages\evals\types\evals.ts:
⋮
│export interface EvalInput {
│  name: string;
│  modelName: AvailableModel;
│  agentMode?: AgentToolMode;
│  isCUA?: boolean;
│  // Optional per-test parameters, used by data-driven tasks
│  params?: Record<string, unknown>;
⋮
│export type LogLineEval = LogLine & {
│  parsedAuxiliary?: string | object;
⋮

packages\evals\utils\imageResize.ts:
⋮
│export async function imageResize(
│  img: Buffer,
│  scaleFactor: number,
⋮

packages\server-v3\scripts\runtimePaths.ts:
⋮
│type CallSiteWithScriptName = NodeJS.CallSite & {
│  getScriptNameOrSourceURL?: () => string | null;
⋮

packages\server-v3\src\server.ts:
⋮
│const app = fastify({
│  disableRequestLogging: true,
│
│  genReqId: () => {
│    return randomUUID();
│  },
│
│  logger: {
│    formatters: {
│      level(label: string) {
│        return { level: label };
│      },
│    },
│
│    level: process.env.NODE_ENV === "production" ? "info" : "trace",
│
│    ...(usePrettyLogs && {
⋮

packages\server-v3\src\types\error.ts:
⋮
│export class AttemptedCloseOnNonActiveSessionError extends AppError {
│  constructor() {
│    super(
│      "Attempted to close session that is not currently active",
│      StatusCodes.CONFLICT,
│    );
│  }
⋮

packages\server-v3\src\types\fastify.d.ts:
⋮
│declare module "fastify" {
│  interface FastifyRequest {
│    metrics: {
│      startTime: number;
│    };
│  }
⋮

packages\server-v3\src\types\rrweb.ts:
│export interface Node {
⋮

packages\server-v3\tests\integration\utils.ts:
⋮
│export interface SSEEvent {
│  event?: string;
│  data?: string;
│  parsed?: unknown;
⋮
```