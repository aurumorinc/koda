---
name: stagehand
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging stagehand. Use this skill whenever modifying stagehand configurations or adding related functionality.
---
# stagehand

## File Tree

```text
stagehand/
├── modules
│   └── stagehand (See AST Map below)
└── SKILL.md
```

### AST Map: `modules/stagehand`

```python
packages/cli/src/base.ts:
⋮
│export abstract class BrowseCommand extends Command {
│  protected override async catch(
│    err: Error & { exitCode?: number },
│  ): Promise<unknown> {
│    if (err instanceof CommandFailure) {
│      recordCommandError("runtime", "COMMAND_FAILURE", err.telemetry);
│      process.stderr.write(`${err.message}\n`);
│      this.exit(err.exitCode);
│    }
│
⋮

packages/cli/src/commands/cloud/fetch.ts:
⋮
│type FetchFormat = (typeof fetchFormats)[number];
│
⋮

packages/cli/src/commands/cloud/sessions/create.ts:
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

packages/cli/src/commands/cloud/sessions/downloads/get.ts:
⋮
│export default class SessionsDownloadsGet extends BrowseCommand {
│  static override description =
│    "Download Browserbase session files as a ZIP archive.";
│  static override examples = [
│    "browse cloud sessions downloads get <session-id>",
│    "browse cloud sessions downloads get <session-id> --output ./downloads.zip",
│  ];
│
│  static override args = {
│    id: Args.string({ required: true, description: "Session ID." }),
⋮

packages/cli/src/commands/cloud/sessions/list.ts:
⋮
│type SessionStatus = "RUNNING" | "ERROR" | "TIMED_OUT" | "COMPLETED";
│
⋮

packages/cli/src/lib/cloud/flags.ts:
⋮
│export interface ParsedApiCommonFlags {
│  "api-key"?: string;
│  "base-url"?: string;
⋮

packages/cli/src/lib/command-suggestions.ts:
⋮
│export interface CommandSuggestion {
│  /** Sanitized colon-separated tokens treated as the attempted command. */
│  attempted: string;
│  /** Colon-separated suggested command or topic, when a decent match exists. */
│  suggestion: string | null;
⋮

packages/cli/src/lib/driver/command-cli.ts:
⋮
│export type DriverFlags = DriverModeFlags & {
│  session?: string;
⋮
│export async function runDriverCommandFromFlags(
│  command: DriverCommandName,
│  params: unknown,
│  flags: DriverFlags,
⋮

packages/cli/src/lib/driver/commands/types.ts:
⋮
│export type DriverCommandName = z.infer<typeof DriverCommandNameSchema>;
│
⋮
│export type DriverCommandHandlers = Partial<
│  Record<DriverCommandName, DriverCommandHandler>
⋮

packages/cli/src/lib/driver/daemon/protocol.ts:
⋮
│export type DriverRequest = z.infer<typeof RequestSchema>;
⋮

packages/cli/src/lib/driver/errors.ts:
⋮
│export class DriverError extends Error {
│  readonly code: string;
│  readonly httpStatus?: number;
│
│  constructor(
│    message: string,
│    options: { cause?: unknown; code: string; httpStatus?: number },
│  ) {
│    super(message, options.cause === undefined ? {} : { cause: options.cause });
│    this.name = "DriverError";
⋮

packages/cli/src/lib/driver/flags.ts:
⋮
│export function sessionName(value?: string): string {
│  return value ?? process.env.BROWSE_SESSION ?? "default";
⋮

packages/cli/src/lib/driver/network-capture.ts:
⋮
│type CdpSession = {
│  off?: (event: string, listener: (...args: unknown[]) => void) => void;
│  on: (event: string, listener: (...args: unknown[]) => void) => void;
│  send: <T = unknown>(
│    method: string,
│    params?: Record<string, unknown>,
│  ) => Promise<T>;
⋮

packages/cli/src/lib/driver/session-manager.ts:
⋮
│export class DriverSessionManager {
│  readonly network: NetworkCapture;
│
│  private consecutiveInitFailures = 0;
│  private context: DriverContext | null = null;
│  private initFailure: InitFailure | null = null;
│  private initPromise: Promise<void> | null = null;
│  private refMaps: RefMaps = emptyRefMaps();
│  private selectedTargetId: string | undefined;
│  private stagehand: Stagehand | null = null;
│
⋮

packages/cli/src/lib/driver/types.ts:
│export type ConnectionTarget =
⋮

packages/cli/src/lib/errors.ts:
│export interface CommandFailureTelemetry {
⋮
│export class CommandFailure extends Error {
│  readonly exitCode: number;
│  readonly telemetry: CommandFailureTelemetry;
│
│  constructor(
│    message: string,
│    exitCode = 1,
│    telemetry: CommandFailureTelemetry = {},
│  ) {
│    super(message);
⋮

packages/cli/src/lib/functions/init.ts:
⋮
│export interface InitFunctionsProjectOptions {
│  packageManager: "npm" | "pnpm";
│  projectName: string;
⋮

packages/cli/src/lib/functions/invoke.ts:
⋮
│export interface InvokeFunctionOptions {
│  apiKey?: string;
│  baseUrl?: string;
│  checkStatus?: string;
│  functionId?: string;
│  noWait: boolean;
│  params?: string;
⋮

packages/cli/src/lib/functions/publish.ts:
⋮
│export interface PublishFunctionOptions {
│  apiKey?: string;
│  baseUrl?: string;
│  dryRun: boolean;
│  entrypoint: string;
⋮

packages/cli/src/lib/output.ts:
⋮
│export type OutputFormat = "json" | "table";
│
│export interface OutputFormatFlags {
│  format?: string;
│  json?: boolean;
│  wide?: boolean;
⋮

packages/cli/src/lib/telemetry.ts:
⋮
│export function recordCommandError(
│  type: CliTelemetryErrorType,
│  code: string | null,
│  telemetry: CommandFailureTelemetry = {},
⋮

packages/cli/tests/helpers/fake-browserbase-server.ts:
⋮
│export interface CapturedRequest {
│  method: string;
│  path: string;
│  headers: IncomingMessage["headers"];
│  bodyBuffer: Buffer;
│  bodyText: string;
│  jsonBody?: unknown;
⋮

packages/cli/tests/helpers/run-cli.ts:
⋮
│export interface RunCliOptions {
│  cwd?: string;
│  env?: NodeJS.ProcessEnv;
⋮

packages/core/examples/cua-replay.ts:
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

packages/core/examples/return-xpath.ts:
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

packages/core/examples/shadow-root.ts:
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

packages/core/examples/targeted-extract.ts:
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

packages/core/examples/v3-example.ts:
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

packages/core/examples/webmcp.ts:
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

packages/core/examples/wordle.ts:
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

packages/core/lib/logger.ts:
⋮
│export interface LoggerOptions {
│  pretty?: boolean;
│  level?: pino.Level;
│  destination?: pino.DestinationStream;
│  usePino?: boolean; // Whether to use pino (default: true)
⋮

packages/core/lib/v3/cache/CacheStorage.ts:
⋮
│export class CacheStorage {
│  private constructor(
│    private readonly logger: Logger,
│    private readonly dir?: string,
│    private readonly memoryStore?: Map<string, unknown>,
│  ) {}
│
│  static create(
│    cacheDir: string | undefined,
│    logger: Logger,
⋮

packages/core/lib/v3/dom/locatorScripts/xpathParser.ts:
│export type XPathPredicate =
⋮

packages/core/lib/v3/flowlogger/EventEmitter.ts:
⋮
│type WildcardEventListener = (...args: unknown[]) => void;
│
│export class EventEmitterWithWildcardSupport extends EventEmitter {
│  private readonly wildcardListeners = new Set<WildcardEventListener>();
│
│  override on(
│    eventName: string | symbol,
│    listener: (...args: unknown[]) => void,
│  ): this {
│    if (eventName === "*") {
│      this.wildcardListeners.add(listener);
│      return this;
⋮
│  override emit(eventName: string | symbol, ...args: unknown[]): boolean {
│    const handled = super.emit(eventName, ...args);
│
│    for (const listener of this.wildcardListeners) {
│      listener(...args);
│    }
│
│    return handled || this.wildcardListeners.size > 0;
⋮

packages/core/lib/v3/flowlogger/FlowLogger.ts:
⋮
│export class FlowEvent implements FlowEventFields {
│  // "ModuleMethodSomethingEvent" -> hashToSmallInt("Modu) -> 5. eventId = "...5"
│  private static deriveEventIdSuffix(eventType: string): string {
│    const prefixMatch = eventType.match(/^[A-Z][a-z0-9]*/);
│    const prefix = prefixMatch?.[0] ?? eventType.slice(0, 4);
│
│    let hash = 0;
│    for (const ch of prefix.slice(0, 4)) {
│      hash = (hash * 31 + ch.charCodeAt(0)) % 10;
│    }
⋮
│export interface FlowLoggerContext {
│  // Mirrors `FlowEvent.sessionId`; it is currently the Stagehand session id and often matches `bro
│  sessionId: string;
│  eventBus: EventEmitterWithWildcardSupport; // Shared per-session bus; `emit()` writes to it and V
│  parentEvents: FlowEvent[]; // Active parent stack for the current async chain; wrappers push/pop 
⋮

packages/core/lib/v3/llm/LLMClient.ts:
⋮
│export interface CreateChatCompletionOptions {
│  options: ChatCompletionOptions;
│  logger: (message: LogLine) => void;
│  retries?: number;
⋮
│export abstract class LLMClient {
│  public type: "openai" | "anthropic" | "cerebras" | "groq" | (string & {});
│  public modelName: AvailableModel | (string & {});
│  public hasVision: boolean;
│  public clientOptions: ClientOptions;
│  public userProvidedInstructions?: string;
│
│  constructor(modelName: AvailableModel, userProvidedInstructions?: string) {
│    this.modelName = modelName;
│    this.userProvidedInstructions = userProvidedInstructions;
⋮

packages/core/lib/v3/runtimePaths.ts:
⋮
│type CallSiteWithScriptName = NodeJS.CallSite & {
│  getScriptNameOrSourceURL?: () => string | null;
⋮

packages/core/lib/v3/shutdown/cleanupLocal.ts:
⋮
│export async function cleanupLocalBrowser(opts: {
│  killChrome?: () => Promise<void> | void;
│  userDataDir?: string;
│  createdTempProfile?: boolean;
│  preserveUserDataDir?: boolean;
⋮

packages/core/lib/v3/types/private/locator.ts:
⋮
│export interface NormalizedFilePayload {
│  name: string;
│  mimeType: string;
│  buffer: Buffer;
│  lastModified: number;
│  /** Absolute path to the source file when provided by the caller. */
│  absolutePath?: string;
⋮

packages/core/lib/v3/types/private/network.ts:
⋮
│export type NetworkRequestInfo = {
│  sessionId: string;
│  requestId: string;
│  requestKey: string;
│  frameId?: string;
│  loaderId?: string;
│  url?: string;
│  timestamp: number;
│  resourceType?: Protocol.Network.ResourceType;
│  documentRequest: boolean;
⋮

packages/core/lib/v3/types/private/shutdown.ts:
⋮
│export type ShutdownSupervisorConfig =
│  | {
│      kind: "LOCAL";
│      pid: number;
│      userDataDir?: string;
│      createdTempProfile?: boolean;
│      preserveUserDataDir?: boolean;
│    }
│  | {
│      kind: "STAGEHAND_API";
⋮

packages/core/lib/v3/types/private/snapshot.ts:
⋮
│export type FrameParentIndex = Map<string, string | null>;
│
⋮

packages/core/lib/v3/types/public/agent.ts:
⋮
│export type Variables = Record<string, VariableValue>;
│
⋮
│type StreamingCallbackNotAvailable =
⋮
│type SafetyConfirmationCallbackNotAvailable =
⋮
│export interface AgentExecuteCallbacks extends AgentCallbacks {
│  /**
│   * Callback called when each step (LLM call) is finished.
│   */
│  onStepFinish?: GenerateTextOnStepFinishCallback<ToolSet>;
│  /**
│   * Callback for handling safety confirmation requests from CUA providers.
│   * Only available when running an agent configured with mode: "cua".
│   */
│  onSafetyConfirmation?: SafetyConfirmationHandler;
│
⋮
│export interface AgentStreamCallbacks extends AgentCallbacks {
│  /**
│   * Callback called when each step (LLM call) is finished during streaming.
│   */
│  onStepFinish?: StreamTextOnStepFinishCallback<ToolSet>;
│  /**
│   * Callback called when an error occurs during streaming.
│   * Use this to log errors or handle error states.
│   */
│  onError?: StreamTextOnErrorCallback;
⋮
│export interface AgentExecuteOptionsBase {
│  instruction: string;
│  maxSteps?: number;
│  page?: PlaywrightPage | PuppeteerPage | PatchrightPage | Page;
│  highlightCursor?: boolean;
│  /**
│   * Previous conversation messages to continue from.
│   * Pass the `messages` from a previous AgentResult to continue that conversation.
│   * @experimental
│   */
⋮
│export type SafetyConfirmationHandler = (
│  safetyChecks: SafetyCheck[],
⋮
│export type AgentProviderType = AgentType;
│
⋮
│export type AgentToolMode = "dom" | "hybrid" | "cua";
│
⋮

packages/core/lib/v3/types/public/agentEvidenceEvents.ts:
⋮
│export type AgentEvidenceRole = "probe" | "agent";
│
│export type AgentEvidenceEvent =
│  | AgentScreenshotEvidenceEvent
│  | AgentStepFinishedEvent
│  | AgentStepObservedEvent
⋮
│export interface AgentFinalObservation {
│  /** Page URL at the time of terminal capture. */
│  url: string;
│  /** PNG bytes from page.screenshot(), when capture succeeds. */
│  screenshot?: Buffer;
│  /** Accessibility tree snapshot, when captured. */
│  ariaTree?: string;
⋮
│export type AgentEvidenceCallback = (
│  event: AgentEvidenceEvent,
⋮

packages/core/lib/v3/types/public/api.ts:
⋮
│export type GoogleServiceAccountCredentials = z.infer<
│  typeof GoogleServiceAccountCredentialsSchema
⋮
│export type ModelAuth = z.infer<typeof ModelAuthSchema>;
│export type VertexProviderOptions = z.infer<typeof VertexProviderOptionsSchema>;
│export type AzureProviderOptions = z.infer<typeof AzureProviderOptionsSchema>;
⋮
│export type ModelProviderOptions = z.infer<typeof ModelProviderOptionsSchema>;
⋮
│type _BrowserbaseSessionCreateParamsCheck =
⋮

packages/core/lib/v3/types/public/logs.ts:
│export type LogLevel = 0 | 1 | 2;
│
⋮
│export type LogLine = {
│  id?: string;
│  category?: string;
│  message: string;
│  level?: LogLevel;
│  timestamp?: string;
│  auxiliary?: {
│    [key: string]: {
│      value: string;
│      type: "object" | "string" | "html" | "integer" | "float" | "boolean";
⋮

packages/core/lib/v3/types/public/metrics.ts:
│export interface StagehandMetrics {
⋮

packages/core/lib/v3/types/public/model.ts:
⋮
│export interface GoogleServiceAccountCredentials {
│  type?: "service_account";
│  project_id?: string;
│  private_key_id?: string;
│  private_key: string;
│  client_email: string;
│  client_id?: string;
│  auth_uri?: string;
│  token_uri?: string;
│  auth_provider_x509_cert_url?: string;
⋮
│export type ModelAuth = GoogleServiceAccountAuth | AzureEntraIdAuth;
│
│export interface VertexProviderOptions {
│  project: string;
│  location: string;
│  baseURL?: string;
│  headers?: Record<string, string>;
⋮
│export interface AzureProviderOptions {
│  resourceName?: string;
│  baseURL?: string;
│  apiVersion?: string;
│  useDeploymentBasedUrls?: boolean;
│  headers?: Record<string, string>;
⋮
│export type ModelProviderOptions =
│  | { vertex: VertexProviderOptions; azure?: never }
⋮
│export type AvailableModel =
│  | "gpt-4.1"
│  | "gpt-4.1-mini"
│  | "gpt-4.1-nano"
│  | "o4-mini"
│  | "o3"
│  | "o3-mini"
│  | "o1"
│  | "o1-mini"
│  | "gpt-4o"
⋮
│export type ThinkingEffort =
│  | "none"
│  | "low"
│  | "medium"
│  | "high"
│  | "xhigh"
⋮
│export type ClientOptions = (OpenAIClientOptions | AnthropicClientOptions) & {
│  apiKey?: string;
│  provider?: AgentProviderType;
│  auth?: ModelAuth;
│  providerOptions?: ModelProviderOptions;
│  baseURL?: string;
│  /** OpenAI organization ID */
│  organization?: string;
│  /** Delay between agent actions in ms */
│  waitBetweenActions?: number;
⋮
│export type ModelConfiguration =
│  | AvailableModel
│  | (ClientOptions & {
│      modelName: AvailableModel;
│      /**
│       * Optional AI SDK middleware applied to every LanguageModelV2 created for this model.
│       * Use this to intercept LLM calls for usage tracking, logging, request transforms, etc.
│       *
│       * Only effective when running locally (direct mode). Cannot be serialized over HTTP,
│       */
⋮

packages/core/lib/v3/types/public/page.ts:
⋮
│export type WebMCPToolInvocationStatus = "Completed" | "Canceled" | "Error";
│
⋮

packages/core/lib/v3/types/public/sdkErrors.ts:
⋮
│export class StagehandError extends Error {
│  public readonly cause?: unknown;
│
│  constructor(message: string, cause?: unknown) {
│    super(message);
│    this.name = this.constructor.name;
│    if (cause !== undefined) {
│      this.cause = cause;
│    }
│  }
⋮
│export class StagehandInvalidArgumentError extends StagehandError {
│  constructor(message: string) {
│    super(`InvalidArgumentError: ${message}`);
│  }
⋮
│export class ResponseBodyError extends StagehandError {
│  constructor(message: string) {
│    super(`Failed to retrieve response body: ${message}`);
│  }
⋮
│export class ResponseParseError extends StagehandError {
│  constructor(message: string) {
│    super(`Failed to parse response: ${message}`);
│  }
⋮
│export class TimeoutError extends StagehandError {
│  constructor(operation: string, timeoutMs: number) {
│    super(`${operation} timed out after ${timeoutMs}ms`);
│  }
⋮
│export class PageNotFoundError extends StagehandError {
│  constructor(identifier: string) {
│    super(`No Page found for ${identifier}`);
│  }
⋮

packages/core/lib/v3/understudy/a11yInvocation.ts:
⋮
│export function buildA11yInvocation(
│  name: A11yScriptName,
│  args: string[],
⋮

packages/core/lib/v3/understudy/cdp.ts:
⋮
│export interface CDPSessionLike {
│  send<R = unknown>(method: string, params?: object): Promise<R>;
│  on<P = unknown>(event: string, handler: (params: P) => void): void;
│  off<P = unknown>(event: string, handler: (params: P) => void): void;
│  close(): Promise<void>;
│  readonly id: string | null;
⋮
│export class CdpSession implements CDPSessionLike {
│  constructor(
│    private readonly root: CdpConnection,
│    public readonly id: string,
│  ) {}
│
│  send<R = unknown>(method: string, params?: object): Promise<R> {
│    return this.root._sendViaSession<R>(this.id, method, params);
│  }
│
⋮

packages/core/lib/v3/understudy/consoleMessage.ts:
⋮
│export class ConsoleMessage {
│  constructor(
│    private readonly event: Protocol.Runtime.ConsoleAPICalledEvent,
│    private readonly pageRef?: Page,
│  ) {}
│
│  type(): Protocol.Runtime.ConsoleAPICalledEvent["type"] {
│    return this.event.type;
│  }
│
⋮

packages/core/lib/v3/understudy/locatorInvocation.ts:
⋮
│export function buildLocatorInvocation(
│  name: LocatorScriptName,
│  args: string[],
⋮

packages/core/lib/v3/understudy/response.ts:
⋮
│export class Response {
│  private readonly page: Page;
│  private readonly session: CDPSessionLike;
│  private readonly requestId: string;
│  private readonly frameId?: string;
│  private readonly loaderId?: string;
│  private readonly response: Protocol.Network.Response;
│  private readonly fromServiceWorkerFlag: boolean;
│  private readonly serverAddress?: ServerAddr | null;
│
⋮

packages/core/lib/v3/v3.ts:
⋮
│export class V3 {
│  private readonly opts: V3Options;
│  private state: InitState = { kind: "UNINITIALIZED" };
│  private actHandler: ActHandler | null = null;
│  private extractHandler: ExtractHandler | null = null;
│  private observeHandler: ObserveHandler | null = null;
│  private ctx: V3Context | null = null;
│  public llmClient!: LLMClient;
│
│  /**
⋮

packages/core/lib/v3/verifier/types.ts:
⋮
│export interface TrajectoryUsage {
│  input_tokens: number;
│  output_tokens: number;
│  reasoning_tokens?: number;
│  cached_input_tokens?: number;
│  inference_time_ms?: number;
⋮
│export interface TaskSpec {
│  /** Stable identifier (e.g., "united_13" for WebTailBench, task_id for Mind2Web). */
│  id: string;
│  /** Task instruction shown to the agent. */
│  instruction: string;
│  /** Starting URL, if any. */
│  initUrl?: string;
│  /** Rubric carried by the dataset or generated by a verifier backend. */
│  precomputedRubric?: Rubric;
│  /** Optional reference answer (set when dataset ships one). */
⋮
│export interface AgentEvidence {
│  modalities: AgentEvidenceModality[];
⋮
│export interface ProbeEvidence {
│  /** URL after the step's tool execution. */
│  url?: string;
│  /**
│   * Bus screenshot captured after the step. Path on disk is preferred once
│   * persisted; in-memory Buffer is used during a live run.
│   */
│  screenshot?: Buffer;
│  /** Reference to the persisted screenshot file under the trajectory dir. */
│  screenshotPath?: string;
⋮
│export interface ToolOutput {
│  ok: boolean;
│  /**
│   * The tool's return value. Same payload that flowed into agentEvidence
│   * modalities, but in its native shape (e.g., the extract result, the act
│   * describe-string) rather than serialized for the LLM.
│   */
│  result: unknown;
│  error?: string;
⋮
│export type TrajectoryStatus = "complete" | "aborted" | "stalled" | "error";
│
⋮
│export interface Trajectory {
│  task: TaskSpec;
│  steps: TrajectoryStep[];
│  finalAnswer?: string;
│  /** Terminal page observation captured after the agent finishes. */
│  finalObservation?: ProbeEvidence;
│  status: TrajectoryStatus;
│  usage: TrajectoryUsage;
⋮
│export interface FirstPointOfFailure {
│  stepIndex: number;
│  /** Sub-code from the error taxonomy (e.g., "2.3" for a specific hallucination type). */
│  errorCode: string;
│  /** Top-level category name (Selection, Hallucination, etc.). */
│  category: string;
│  /** Verifier's reasoning for selecting this point. */
│  description?: string;
⋮
│export interface VerifierRawSteps {
│  backend?: "legacy" | "verifier";
│  reason?: string;
│  primaryIntent?: string;
│  reasoning?: string;
│  rubricSource?: "precomputed" | "generated" | "none";
│  approach?: "a" | "b" | "outcome-only";
│  optionalsMode?: "folded" | "separate" | "skip";
│  totalEarned?: number;
│  totalMax?: number;
⋮
│export interface TaskValidity {
│  /** True if the task is underspecified / has multiple valid interpretations. */
│  isAmbiguous: boolean;
│  /** Explanation for why the task is ambiguous, when available. */
│  ambiguityReason?: string;
│  /** True if the task is impossible / illegal / NSFW / otherwise infeasible. */
│  isInvalid: boolean;
│  /** Explanation for why the task is invalid, when available. */
│  invalidReason?: string;
│  /** Optional sub-codes from the task-classification taxonomy. */
⋮

packages/core/lib/v3/zodCompat.ts:
⋮
│export type StagehandZodSchema = Zod4TypeAny | z3.ZodTypeAny;
│
│export type StagehandZodObject =
│  | Zod4Object<Zod4RawShape>
⋮
│export type JsonSchemaDocument = Record<string, unknown>;
│
⋮

packages/core/scripts/gen-version.ts:
⋮
│type PackageJson = { version: string };
│
⋮

packages/core/tests/unit/helpers/mockCDPSession.ts:
⋮
│type Handler = (params?: Record<string, unknown>) => Promise<unknown> | unknown;
⋮
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

packages/core/tests/unit/xpath-resolver.test.ts:
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

packages/evals/core/contracts/representation.ts:
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

packages/evals/core/contracts/results.ts:
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

packages/evals/core/contracts/targets.ts:
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

packages/evals/core/contracts/tool.ts:
⋮
│export type StartupProfile =
│  | "runner_provided_local_cdp"
│  | "runner_provided_browserbase_cdp"
│  | "tool_launch_local"
│  | "tool_attach_local_cdp"
│  | "tool_create_browserbase"
⋮

packages/evals/core/tools/cdp_code.ts:
⋮
│class CdpSession implements CoreSession {
│  private readonly pages = new Map<string, CdpPageState>();
│  private activePageId: string | null = null;
│  private closed = false;
│
│  private constructor(private readonly connection: CdpConnection) {}
│
│  static async connect(input: {
│    providedEndpoint: {
│      kind: "ws" | "http";
⋮

packages/evals/env.ts:
⋮
│export function getEnv(): "BROWSERBASE" | "LOCAL" {
│  return process.env.EVAL_ENV?.toLowerCase() === "browserbase"
│    ? "BROWSERBASE"
│    : "LOCAL";
⋮

packages/evals/errors.ts:
│export class EvalsError extends Error {
⋮

packages/evals/framework/types.ts:
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

packages/evals/lib/braintrust-report.ts:
⋮
│export type FetchOptions = {
│  /**
│   * Braintrust API key. If omitted, pulled from:
│   *   1. packages/evals/.env (BRAINTRUST_API_KEY)
│   *   2. process.env.BRAINTRUST_API_KEY
│   */
│  apiKey?: string;
│  /**
│   * Max concurrent Braintrust fetches for fan-out helpers. Defaults to 1
│   * because report commands are interactive and Braintrust rate limits are
⋮

packages/evals/logger.ts:
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

packages/evals/runtimePaths.ts:
⋮
│type CallSiteWithScriptName = NodeJS.CallSite & {
│  getScriptNameOrSourceURL?: () => string | null;
⋮

packages/evals/tasks/bench/experimental/extract_press_releases.ts:
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

packages/evals/tests/tui/doctor.test.ts:
⋮
│type DoctorJsonReport = {
│  verdict: string;
│  reasons: string[];
│  [key: string]: unknown;
⋮

packages/evals/tests/tui/experiments.test.ts:
⋮
│function makeChildProcess(args: string[]): EventEmitter & {
│  stdout: EventEmitter;
│  stderr: EventEmitter;
⋮

packages/evals/tui/commands/config.ts:
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
│export type ConfigFile = {
│  defaults: Defaults;
│  benchmarks?: Record<string, unknown>;
│  core?: CoreConfigSection;
│  _meta?: WelcomeMeta;
⋮

packages/evals/tui/format.ts:
⋮
│export type TaskStatus = "pending" | "running" | "passed" | "failed" | "error";
│
⋮

packages/evals/tui/tokenize.ts:
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

packages/evals/types/evals.ts:
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

packages/evals/utils/imageResize.ts:
⋮
│export async function imageResize(
│  img: Buffer,
│  scaleFactor: number,
⋮

packages/server-v3/scripts/runtimePaths.ts:
⋮
│type CallSiteWithScriptName = NodeJS.CallSite & {
│  getScriptNameOrSourceURL?: () => string | null;
⋮

packages/server-v3/src/lib/errorHandler.ts:
⋮
│export class AppError extends Error {
│  statusCode: number;
│  isInternal: boolean;
│
│  constructor(
│    message: string,
│    statusCode = StatusCodes.BAD_REQUEST,
│    isInternal = false,
│  ) {
│    super(message);
⋮
│  getClientMessage(): string {
│    if (this.isInternal) {
│      return this.statusCode >= StatusCodes.INTERNAL_SERVER_ERROR
│        ? "An internal server error occurred"
│        : "An error occurred while processing your request";
│    }
│    return this.message;
⋮
│export function withErrorHandling<
│  T extends RouteGenericInterface = RouteGenericInterface,
│  R = unknown,
⋮

packages/server-v3/src/lib/listenHost.ts:
⋮
│export type ListenHostConfig = {
│  host: string;
│  warning?: string;
⋮

packages/server-v3/src/server.ts:
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

packages/server-v3/src/types/error.ts:
⋮
│export class AttemptedCloseOnNonActiveSessionError extends AppError {
│  constructor() {
│    super(
│      "Attempted to close session that is not currently active",
│      StatusCodes.CONFLICT,
│    );
│  }
⋮

packages/server-v3/src/types/fastify.d.ts:
⋮
│declare module "fastify" {
│  interface FastifyRequest {
│    metrics: {
│      startTime: number;
│    };
│  }
⋮

packages/server-v3/src/types/rrweb.ts:
│export interface Node {
⋮
```