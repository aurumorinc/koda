---
name: playwright
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging playwright. Use this skill whenever modifying playwright configurations or adding related functionality.
---
# playwright

## File Tree

```text
playwright/
├── assets
├── modules
│   └── playwright (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

### AST Map: `modules/playwright`

```python
browser_patches/webkit/embedder/Playwright/win/PlaywrightReplace.h:
⋮
│static void processCrashReport(const wchar_t* fileName) { ::MessageBox(0, fileName, L"Crash Report"

packages/dashboard/src/imageLayout.ts:
⋮
│export type ImageLayout = {
│  rect: DOMRect;
│  renderW: number;
│  renderH: number;
│  offsetX: number;
│  offsetY: number;
⋮

packages/extension/src/protocolHandlers.ts:
⋮
│export type ProtocolCommand = {
│  id: number;
│  method: string;
│  params?: any;
⋮
│export interface RelayContext {
│  readonly attachedTabs: ReadonlySet<number>;
│  sendMessage(message: any): void;
│  // Records that a tab's debugger is now attached. Fires ontabattached on the
│  // owning RelayConnection.
│  notifyTabAttached(tabId: number): void;
│  // Records that a tab's debugger is now detached. Fires ontabdetached on the
│  // owning RelayConnection.
│  notifyTabDetached(tabId: number): void;
⋮

packages/html-reporter/src/headerView.tsx:
⋮
│          const currentParams = new URLSearchParams(url.hash.slice(1));
⋮

packages/injected/src/layoutSelectorUtils.ts:
⋮
│export type LayoutSelectorName = 'left-of' | 'right-of' | 'above' | 'below' | 'near';
⋮

packages/injected/src/selectorEngine.ts:
⋮
│export type SelectorRoot = Element | ShadowRoot | Document;
│
⋮

packages/injected/src/utilityScript.ts:
⋮
│export type Builtins = {
│  setTimeout: Window['setTimeout'],
│  clearTimeout: Window['clearTimeout'],
│  setInterval: Window['setInterval'],
│  clearInterval: Window['clearInterval'],
│  requestAnimationFrame: Window['requestAnimationFrame'],
│  cancelAnimationFrame: Window['cancelAnimationFrame'],
│  requestIdleCallback: Window['requestIdleCallback'],
│  cancelIdleCallback: Window['cancelIdleCallback'],
│  performance: Window['performance'],
⋮

packages/isomorphic/colors.ts:
⋮
│export type Colors = typeof webColors;
│
⋮

packages/isomorphic/cssParser.ts:
⋮
│export class InvalidSelectorError extends Error {
⋮
│export type CSSSimpleSelector = { css?: string, functions: CSSFunction[] };
│export type CSSComplexSelector = { simples: { selector: CSSSimpleSelector, combinator: ClauseCombin
⋮

packages/isomorphic/headers.ts:
⋮
│type HeadersArray = { name: string, value: string }[];
⋮

packages/isomorphic/imageUtils.ts:
⋮
│export type ImageData = { width: number, height: number, data: Buffer };
│
⋮

packages/isomorphic/jsonSchema.ts:
⋮
│export type JsonSchema = {
│  type?: string;
│  properties?: Record<string, JsonSchema>;
│  required?: string[];
│  items?: JsonSchema;
│  oneOf?: JsonSchema[];
│  pattern?: string;
│  patternError?: string;
⋮

packages/isomorphic/locatorUtils.ts:
⋮
│export type ByRoleOptions = {
│  checked?: boolean;
│  description?: string | RegExp;
│  disabled?: boolean;
│  exact?: boolean;
│  expanded?: boolean;
│  includeHidden?: boolean;
│  level?: number;
│  name?: string | RegExp;
│  pressed?: boolean;
⋮

packages/isomorphic/manualPromise.ts:
⋮
│export class ManualPromise<T = void> extends Promise<T> {
│  private _resolve!: (t: T) => void;
│  private _reject!: (e: Error) => void;
│  private _isDone: boolean;
│
│  constructor() {
│    let resolve: (t: T) => void;
│    let reject: (e: Error) => void;
│    super((f, r) => {
│      resolve = f;
⋮

packages/isomorphic/platform.ts:
⋮
│export type Platform = {
│  name: 'node' | 'web' | 'empty';
│
│  boxedStackPrefixes: () => string[];
│  calculateSha1: (text: string) => Promise<string>;
│  colors: Colors;
│  coreDir?: string;
│  createGuid: () => string;
│  defaultMaxListeners: () => number;
│  env: Record<string, string | undefined>;
⋮

packages/isomorphic/trace/versions/traceV3.ts:
⋮
│type CallMetadata = {
│  id: string;
│  startTime: number;
│  endTime: number;
│  pauseStartTime?: number;
│  pauseEndTime?: number;
│  type: string;
│  method: string;
│  params: any;
│  apiName?: string;
⋮
│export type NodeSnapshot =
│  string |
│  [ [number, number] ] |
│  [ string ] |
⋮

packages/isomorphic/trace/versions/traceV4.ts:
⋮
│type NodeSnapshot =
⋮

packages/isomorphic/trace/versions/traceV5.ts:
⋮
│type NodeSnapshot =
⋮

packages/isomorphic/trace/versions/traceV6.ts:
⋮
│type NodeSnapshot =
⋮

packages/isomorphic/trace/versions/traceV7.ts:
⋮
│type NodeSnapshot =
⋮

packages/isomorphic/trace/versions/traceV8.ts:
⋮
│type NodeSnapshot =
⋮

packages/isomorphic/types.ts:
⋮
│export type HeadersArray = NameValue[];

packages/isomorphic/urlMatch.ts:
⋮
│export type URLMatch = string | RegExp | ((url: URL) => boolean) | URLPattern;
⋮

packages/playwright-client/types/types.d.ts:
⋮
│type DeviceDescriptor = {
│  viewport: ViewportSize;
│  userAgent: string;
│  deviceScaleFactor: number;
│  isMobile: boolean;
│  hasTouch: boolean;
│  defaultBrowserType: 'chromium' | 'firefox' | 'webkit';
⋮
│export interface WebSocket {
│  /**
│   * Fired when the websocket closes.
│   */
│  on(event: 'close', listener: (webSocket: WebSocket) => any): this;
│
│  /**
│   * Fired when the websocket receives a frame.
│   */
│  on(event: 'framereceived', listener: (data: {
⋮
│export interface BrowserContextOptions {
│  /**
│   * Whether to automatically download all the attachments. Defaults to `true` where all the downlo
│   */
│  acceptDownloads?: boolean;
│
│  /**
│   * When using [page.goto(url[, options])](https://playwright.dev/docs/api/class-page#page-goto),
│   * [page.route(url, handler[, options])](https://playwright.dev/docs/api/class-page#page-route),
│   * [page.waitForURL(url[, options])](https://playwright.dev/docs/api/class-page#page-wait-for-url
⋮

packages/playwright-core/src/client/artifact.ts:
⋮
│export class Artifact extends ChannelOwner<channels.ArtifactChannel> {
│  static from(channel: channels.ArtifactChannel): Artifact {
│    return (channel as any)._object;
│  }
│
│  async pathAfterFinished(): Promise<string> {
│    if (this._connection.isRemote())
│      throw new Error(`Path is not available when connecting remotely. Use saveAs() to save a local
│    return (await this._channel.pathAfterFinished()).value;
│  }
│
⋮

packages/playwright-core/src/client/channelOwner.ts:
⋮
│export abstract class ChannelOwner<T extends channels.Channel = channels.Channel> extends EventEmit
│  readonly _connection: Connection;
│  private _parent: ChannelOwner | undefined;
│  private _objects = new Map<string, ChannelOwner>();
│
│  readonly _type: string;
│  readonly _guid: string;
│  readonly _channel: T;
│  readonly _initializer: channels.InitializerTraits<T>;
│  _logger: Logger | undefined;
⋮

packages/playwright-core/src/client/channels.d.ts:
⋮
│export type Metadata = {
│  location?: {
│    file: string,
│    line?: number,
│    column?: number,
│  },
│  title?: string,
│  internal?: boolean,
│  stepId?: string,
⋮
│export type SerializedValue = {
│  n?: number,
│  b?: boolean,
│  s?: string,
│  v?: 'null' | 'undefined' | 'NaN' | 'Infinity' | '-Infinity' | '-0',
│  d?: string,
│  u?: string,
│  bi?: string,
│  ta?: {
│    b: Binary,
⋮

packages/playwright-core/src/client/disposable.ts:
⋮
│export class DisposableObject<T extends channels.DisposableChannel = channels.DisposableChannel> ex
│  static from(channel: channels.DisposableChannel): DisposableObject {
│    return (channel as any)._object;
│  }
│
│  async [Symbol.asyncDispose]() {
│    await this.dispose();
│  }
│
│  async dispose() {
⋮

packages/playwright-core/src/client/eventEmitter.ts:
⋮
│export class EventEmitter implements EventEmitterType {
│
│  private _events: EventMap | undefined = undefined;
│  private _eventsCount = 0;
│  private _maxListeners: number | undefined = undefined;
│  readonly _pendingHandlers = new Map<EventType, Set<Promise<void>>>();
│  private _rejectionHandler: ((error: Error) => void) | undefined;
│  readonly _platform: Platform;
│
│  constructor(platform: Platform) {
⋮

packages/playwright-core/src/client/network.ts:
⋮
│export class WebSocket extends ChannelOwner<channels.WebSocketChannel> implements api.WebSocket {
│  private _page: Page;
│  private _isClosed: boolean;
│
│  static from(webSocket: channels.WebSocketChannel): WebSocket {
│    return (webSocket as any)._object;
│  }
│
│  constructor(parent: ChannelOwner, type: string, guid: string, initializer: channels.WebSocketInit
│    super(parent, type, guid, initializer);
⋮

packages/playwright-core/src/client/types.ts:
⋮
│type LoggerSeverity = 'verbose' | 'info' | 'warning' | 'error';
⋮
│export type BrowserContextOptions = Omit<channels.BrowserNewContextOptions, 'viewport' | 'noDefault
│  viewport?: Size | null;
│  extraHTTPHeaders?: Headers;
│  logger?: Logger;
│  storageState?: string | SetStorageState;
│  har?: {
│    path: string;
│    fallback?: 'abort'|'continue';
│    urlFilter?: string|RegExp;
│  };
⋮
│export type AnnotatePosition = 'top-left' | 'top' | 'top-right' | 'bottom-left' | 'bottom' | 'botto
⋮

packages/playwright-core/src/client/webError.ts:
⋮
│type WebErrorLocation = channels.BrowserContextPageErrorEvent['location'];
│
⋮

packages/playwright-core/src/protocol/validatorPrimitives.ts:
⋮
│export class ValidationError extends Error {}
│export type Validator = (arg: any, path: string, context: ValidatorContext) => any;
│export type ValidatorContext = {
│  tChannelImpl: (names: '*' | string[], arg: any, path: string, context: ValidatorContext) => any;
│  binary: 'toBase64' | 'fromBase64' | 'buffer';
│  isUnderTest: () => boolean;
⋮

packages/playwright-core/src/server/artifact.ts:
⋮
│export class Artifact extends SdkObject {
│  private _localPath: string;
│  private _unaccessibleErrorMessage: string | undefined;
│  private _cancelCallback: CancelCallback | undefined;
│  private _finishedPromise = new ManualPromise<void>();
│  private _saveCallbacks: SaveCallback[] = [];
│  private _finished: boolean = false;
│  private _deleted = false;
│  private _failureErrorValue: Error | undefined;
│
⋮

packages/playwright-core/src/server/bidi/third_party/bidiProtocolCore.ts:
⋮
│export type EmptyParams = Extensible;
⋮

packages/playwright-core/src/server/channels.d.ts:
⋮
│export type Metadata = {
│  location?: {
│    file: string,
│    line?: number,
│    column?: number,
│  },
│  title?: string,
│  internal?: boolean,
│  stepId?: string,
⋮

packages/playwright-core/src/server/chromium/crConnection.ts:
⋮
│export class CRSession extends SdkObject<Protocol.EventMap & ConnectionEventMap> {
│  private readonly _connection: CRConnection;
│  private _eventListener?: SessionEventListener;
│  private readonly _callbacks = new Map<number, { resolve: (o: any) => void, reject: (e: ProtocolEr
│  private readonly _sessionId: string;
│  private readonly _parentSession: CRSession | null;
│  private _crashed: boolean = false;
│  private _closed = false;
│
│  constructor(connection: CRConnection, parentSession: CRSession | null, sessionId: string, eventLi
⋮

packages/playwright-core/src/server/disposable.ts:
⋮
│export abstract class DisposableObject extends SdkObject implements Disposable {
│  readonly parent: Page | BrowserContext;
│
│  constructor(parent: Page | BrowserContext) {
│    super(parent, 'disposable');
│    this.parent = parent;
│  }
│
│  abstract dispose(): Promise<void>;
⋮

packages/playwright-core/src/server/instrumentation.ts:
⋮
│export class SdkObject<EM extends EventMap = EventMap> extends EventEmitter<EM> {
│  guid: string;
│  attribution: Attribution;
│  instrumentation: Instrumentation;
│  logName?: LogName;
│
│  constructor(parent: SdkObject, guidPrefix?: string, guid?: string) {
│    super();
│    this.guid = guid || `${guidPrefix || ''}@${createGuid()}`;
│    this.setMaxListeners(0);
⋮
│export type CallMetadata = {
│  id: string;
│  startTime: number;
│  endTime: number;
│  pauseStartTime?: number;
│  pauseEndTime?: number;
│  type: string;
│  method: string;
│  params: any;
│  title?: string;
⋮

packages/playwright-core/src/server/network.ts:
⋮
│export class WebSocket extends SdkObject {
│  private _url: string;
│  private _notified = false;
│  private _wallTimeMs: number | undefined;
│  private _status: number | undefined;
│  private _statusText: string | undefined;
│  private _requestHeaders: HeadersArray | undefined;
│  private _responseHeaders: HeadersArray | undefined;
│
│  static Events = {
⋮

packages/playwright-core/src/server/progress.ts:
⋮
│export interface Progress {
│  timeout: number;
│  deadline: number;
│  disableTimeout(): void;
│  log(message: string): void;
│  race<T>(promise: Promise<T> | Promise<T>[]): Promise<T>;
│  wait(timeout: number): Promise<void>; // timeout = 0 here means "wait 0 ms", not forever.
│  signal: AbortSignal;
│  metadata: CallMetadata;
│  setAllowConcurrentOrNestedRaces(allow: boolean): void;
⋮
│export class ProgressController {
│  private _forceAbortPromise = new ManualPromise<any>();
│  private _donePromise = new ManualPromise<void>();
│  private _state: 'before' | 'running' | { error: Error } | 'finished' = 'before';
│  private _onCallLog?: (message: string) => void;
│
│  readonly metadata: CallMetadata;
│  private _controller: AbortController;
│
│  constructor(metadata?: CallMetadata, onCallLog?: (message: string) => void) {
⋮

packages/playwright-core/src/server/registry/index.ts:
⋮
│export type BrowserName = 'chromium' | 'firefox' | 'webkit';
⋮

packages/playwright-core/src/server/screencast.ts:
⋮
│type AnnotatePosition = 'top-left' | 'top' | 'top-right' | 'bottom-left' | 'bottom' | 'bottom-right
│
⋮

packages/playwright-core/src/server/transport.ts:
⋮
│export type ProtocolResponse = {
│  id?: number;
│  method?: string;
│  sessionId?: string;
│  error?: { message: string; data: any; code?: number };
│  params?: any;
│  result?: any;
│  pageProxyId?: string;
│  browserContextId?: string;
⋮

packages/playwright-core/src/server/types.ts:
⋮
│export type BrowserContextOptions = channels.BrowserNewContextOptions & {
│  proxyOverride?: ProxySettings;
│  internalIgnoreHTTPSErrors?: boolean;
⋮

packages/playwright-core/src/serverRegistry.ts:
⋮
│export type BrowserDescriptor = EndpointInfo & {
│  playwrightVersion: string;
│  playwrightLib: string;
│  browser: BrowserInfo;
⋮

packages/playwright-core/src/tools/backend/context.ts:
⋮
│export type ContextConfig = {
│  allowUnrestrictedFileAccess?: boolean;
│  capabilities?: ToolCapability[];
│  codegen?: 'typescript' | 'none';
│  console?: { level?: 'error' | 'warning' | 'info' | 'debug' };
│  imageResponses?: 'allow' | 'omit';
│  network?: {
│    allowedOrigins?: string[];
│    blockedOrigins?: string[];
│  };
⋮
│type ContextOptions = {
│  config: ContextConfig;
│  sessionLog?: SessionLog;
│  cwd: string;
⋮

packages/playwright-core/src/tools/backend/tab.ts:
⋮
│type Download = {
│  download: playwright.Download;
│  finished: boolean;
│  outputFile: string;
⋮

packages/playwright-core/src/tools/cli-client/registry.ts:
⋮
│export type ClientInfo = {
│  version: string;
│  workspaceDirHash: string;
│  daemonProfilesDir: string;
│  workspaceDir: string | undefined;
│  homeDir: string;
⋮

packages/playwright-core/src/tools/mcp/cdpRelayHandler.ts:
⋮
│export type CDPMessage = {
│  id?: number;
│  sessionId?: string;
│  method?: string;
│  params?: any;
│  result?: any;
│  error?: { code?: number; message: string };
⋮
│export type SendToCDPClient = (message: CDPMessage) => void;
│
⋮

packages/playwright-core/src/tools/mcp/config.ts:
⋮
│export type CLIOptions = {
│  allowedHosts?: string[];
│  allowedOrigins?: string[];
│  allowUnrestrictedFileAccess?: boolean;
│  blockedOrigins?: string[];
│  blockServiceWorkers?: boolean;
│  browser?: string;
│  caps?: string[];
│  cdpEndpoint?: string;
│  cdpHeader?: Record<string, string>;
⋮
│export type MergedConfig = Config & {
│  browser: BrowserUserConfig & {
│    launchOptions: NonNullable<BrowserUserConfig['launchOptions']>;
│    contextOptions: NonNullable<BrowserUserConfig['contextOptions']>;
│  }
⋮
│export type FullConfig = MergedConfig & {
│  browser: MergedConfig['browser'] & {
│    browserName: 'chromium' | 'firefox' | 'webkit';
│  },
│  skillMode?: boolean;
│  configFile?: string;
⋮

packages/playwright-core/src/tools/utils/mcp/server.ts:
⋮
│export type ClientInfo = {
│  cwd: string;
│  clientName: string;
⋮

packages/playwright-core/types/types.d.ts:
⋮
│export interface BrowserType<Unused = {}> {
│  /**
│   * This method attaches Playwright to an existing browser instance using the Chrome DevTools Prot
│   *
│   * The default browser context is accessible via
│   * [browser.contexts()](https://playwright.dev/docs/api/class-browser#browser-contexts).
│   *
│   * **NOTE** Connecting over the Chrome DevTools Protocol is only supported for Chromium-based bro
│   *
│   * **NOTE** This connection is significantly lower fidelity than the Playwright protocol connecti
⋮
│type DeviceDescriptor = {
│  viewport: ViewportSize;
│  userAgent: string;
│  deviceScaleFactor: number;
│  isMobile: boolean;
│  hasTouch: boolean;
│  defaultBrowserType: 'chromium' | 'firefox' | 'webkit';
⋮
│export type AndroidSelector = {
│  checkable?: boolean,
│  checked?: boolean,
│  clazz?: string | RegExp,
│  clickable?: boolean,
│  depth?: number,
│  desc?: string | RegExp,
│  enabled?: boolean,
│  focusable?: boolean,
│  focused?: boolean,
⋮
│export interface APIRequestContext {
│  /**
│   * Sends HTTP(S) [DELETE](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE) reque
│   * response. The method will populate request cookies from the context and update context cookies
│   * The method will automatically follow redirects.
│   * @param url Target URL.
│   * @param options
│   */
│  delete(url: string, options?: {
│    /**
⋮
│export interface WebSocket {
│  /**
│   * Fired when the websocket closes.
│   */
│  on(event: 'close', listener: (webSocket: WebSocket) => any): this;
│
│  /**
│   * Fired when the websocket receives a frame.
│   */
│  on(event: 'framereceived', listener: (data: {
⋮
│export interface BrowserContextOptions {
│  /**
│   * Whether to automatically download all the attachments. Defaults to `true` where all the downlo
│   */
│  acceptDownloads?: boolean;
│
│  /**
│   * When using [page.goto(url[, options])](https://playwright.dev/docs/api/class-page#page-goto),
│   * [page.route(url, handler[, options])](https://playwright.dev/docs/api/class-page#page-route),
│   * [page.waitForURL(url[, options])](https://playwright.dev/docs/api/class-page#page-wait-for-url
⋮

packages/playwright-ct-core/index.d.ts:
⋮
│export type PlaywrightTestConfig<T = {}, W = {}> = Omit<BasePlaywrightTestConfig<T, W>, 'use'> & {
│  use?: BasePlaywrightTestConfig<T, W>['use'] & {
│    ctPort?: number;
│    ctTemplateDir?: string;
│    ctCacheDir?: string;
│    ctViteConfig?: InlineConfig | (() => Promise<InlineConfig>);
│  };
⋮

packages/playwright-ct-core/src/injected/importRegistry.ts:
⋮
│export class ImportRegistry {
│  private _registry = new Map<string, () => Promise<any>>();
│
│  initialize(components: Record<string, () => Promise<any>>) {
│    for (const [name, value] of Object.entries(components))
│      this._registry.set(name, value);
│  }
│
│  async resolveImportRef(importRef: ImportRef): Promise<any> {
│    const importFunction = this._registry.get(importRef.id);
⋮

packages/playwright-ct-core/src/tsxTransform.ts:
⋮
│type TsxTransformOptions = {
│  setTransformData: (key: string, value: any) => void;
⋮
│export type ImportInfo = {
│  id: string;
│  filename: string;
│  importSource: string;
│  remoteName: string | undefined;
⋮

packages/playwright/src/agents/agentParser.ts:
⋮
│type AgentSpecHeader = {
│  name: string;
│  description: string;
│  model: string;
│  color: string;
│  tools: string[];
⋮

packages/playwright/src/common/config.ts:
⋮
│export class FullConfigInternal {
│  readonly config: FullConfig;
│  readonly configDir: string;
│  readonly configCLIOverrides: ConfigCLIOverrides;
│  readonly webServers: NonNullable<FullConfig['webServer']>[];
│  readonly plugins: TestRunnerPluginRegistration[];
│  readonly projects: FullProjectInternal[] = [];
│  readonly singleTSConfigPath?: string;
│  readonly captureGitInfo: Config['captureGitInfo'];
│  defineConfigWasUsed = false;
│
⋮

packages/playwright/src/isomorphic/events.ts:
⋮
│export class EventEmitter<T> {
│  public event: Event<T>;
│
│  private _deliveryQueue?: {listener: (e: T) => void, event: T}[];
│  private _listeners = new Set<(e: T) => void>();
│
│  constructor() {
│    this.event = (listener: (e: T) => any, disposables?: Disposable[]) => {
│      this._listeners.add(listener);
│      let disposed = false;
⋮

packages/playwright/src/isomorphic/stringInternPool.ts:
⋮
│export class StringInternPool {
│  private _stringCache = new Map<string, string>();
│
│  public internString(s: string): string {
│    let result = this._stringCache.get(s);
│    if (!result) {
│      this._stringCache.set(s, s);
│      result = s;
│    }
│    return result;
⋮

packages/playwright/src/isomorphic/types.d.ts:
⋮
│export type GitCommitInfo = {
│  shortHash: string;
│  hash: string;
│  subject: string;
│  body: string;
│  author: {
│    name: string;
│    email: string;
│    time: number;
│  };
⋮

packages/playwright/src/matchers/matchers.ts:
⋮
│export type ExpectMatcherStateInternal = Omit<ExpectMatcherState, 'utils'> & {
│  utils: ExpectMatcherUtils & InternalMatcherUtils;
⋮

packages/playwright/src/reporters/teleEmitter.ts:
⋮
│export type TeleReporterEmitterOptions = {
│  omitOutput?: boolean;
│  omitBuffers?: boolean;
⋮

packages/playwright/src/runner/testGroups.ts:
⋮
│export type TestGroup = {
│  workerHash: string;
│  requireFile: string;
│  repeatEachIndex: number;
│  projectId: string;
│  tests: test.TestCase[];
⋮

packages/playwright/src/transform/portTransport.ts:
⋮
│export class PortTransport {
│  private _lastId = 0;
│  private _port: MessagePort;
│  private _callbacks = new Map<number, (result: any) => void>();
│
│  constructor(port: MessagePort, handler: (method: string, params: any) => Promise<any>) {
│    this._port = port;
│    port.addEventListener('message', async event => {
│      const message = event.data;
│      const { id, ackId, method, params, result } = message;
│
│      if (ackId) {
│        const callback = this._callbacks.get(ackId);
│        this._callbacks.delete(ackId);
│        this._resetRef();
⋮
│  private _resetRef() {
│    if (this._callbacks.size) {
│      // When we are waiting for a response, ref the port to prevent this process from exiting.
│      (this._port as any).ref();
│    } else {
│      // When we are not waiting for a response, unref the port to prevent this process
│      // from hanging forever.
│      (this._port as any).unref();
│    }
⋮

packages/playwright/types/test.d.ts:
⋮
│export type Metadata = { [key: string]: any };
│
⋮
│export interface FullConfig<TestArgs = {}, WorkerArgs = {}> {
│  /**
│   * List of resolved projects.
│   */
│  projects: FullProject<TestArgs, WorkerArgs>[];
│  /**
│   * See [testConfig.reporter](https://playwright.dev/docs/api/class-testconfig#test-config-reporte
│   */
│  reporter: ReporterDescription[];
│  /**
⋮
│export interface TestInfo {
│  /**
│   * Returns a path to a snapshot file with the given `name`. Pass
│   * [`kind`](https://playwright.dev/docs/api/class-testinfo#test-info-snapshot-path-option-kind) t
│   * path:
│   * - `kind: 'screenshot'` for
│   *   [expect(page).toHaveScreenshot(name[, options])](https://playwright.dev/docs/api/class-pagea
│   * - `kind: 'aria'` for
│   *   [expect(locator).toMatchAriaSnapshot(expected[, options])](https://playwright.dev/docs/api/c
│   * - `kind: 'snapshot'` for
⋮
│export type TestDetails = {
│  tag?: string | string[];
│  annotation?: TestDetailsAnnotation | TestDetailsAnnotation[];
⋮
│type BrowserName = 'chromium' | 'firefox' | 'webkit';
⋮
│export type PlaywrightTestConfig<TestArgs = {}, WorkerArgs = {}> = Config<PlaywrightTestOptions & C
│
⋮
│type AsymmetricMatcher = Record<string, any>;
│
⋮
│export type MatcherHintOptions = {
│  comment?: string;
│  expectedColor?: MatcherHintColor;
│  isDirectExpectCall?: boolean;
│  isNot?: boolean;
│  promise?: string;
│  receivedColor?: MatcherHintColor;
│  secondArgument?: string;
│  secondArgumentColor?: MatcherHintColor;
⋮

packages/playwright/types/testReporter.d.ts:
⋮
│export interface TestCase {
│  /**
│   * Whether the test is considered running fine. Non-ok tests fail the test run with non-zero exit
│   */
│  ok(): boolean;
│
│  /**
│   * Testing outcome for this test. Note that outcome is not the same as
│   * [testResult.status](https://playwright.dev/docs/api/class-testresult#test-result-status):
│   * - Test that is expected to fail and actually fails is `'expected'`.
⋮

packages/trace-viewer/src/sw/progress.ts:
⋮
│export type Progress = (done: number, total: number) => undefined;
│
⋮

packages/trace-viewer/src/sw/traceLoaderBackends.ts:
⋮
│type Progress = (done: number, total: number) => undefined;
│
⋮

packages/trace-viewer/src/ui/geometry.ts:
⋮
│export type Boundaries = {
│  minimum: number;
│  maximum: number;
⋮

packages/trace-viewer/src/ui/testUtils.ts:
⋮
│export type UITestStatus = 'none' | 'running' | 'scheduled' | 'passed' | 'failed' | 'skipped';
│
⋮

packages/trace/src/snapshot.ts:
⋮
│export type ResourceSnapshot = HAREntry;
│
⋮
│export type NodeSnapshot =
│  TextNodeSnapshot |
│  SubtreeReferenceSnapshot |
⋮

packages/utils/debugLogger.ts:
⋮
│class DebugLogger {
│  private _debuggers = new Map<string, debug.IDebugger>();
│
│  constructor() {
│    if (process.env.DEBUG_FILE) {
│      const ansiRegex = new RegExp([
│        '[\\u001B\\u009B][[\\]()#;?]*(?:(?:(?:[a-zA-Z\\d]*(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]*)*)?\\u0007
│        '(?:(?:\\d{1,4}(?:;\\d{0,4})*)?[\\dA-PR-TZcf-ntqry=><~]))'
│      ].join('|'), 'g');
│      const stream = fs.createWriteStream(process.env.DEBUG_FILE);
⋮

packages/utils/image_tools/imageChannel.ts:
⋮
│export class ImageChannel {
│  data: Uint8Array;
│  width: number;
│  height: number;
│
│  static intoRGB(width: number, height: number, data: Buffer, options: PaddingOptions = {}): ImageC
│    const {
│      paddingSize = 0,
│      paddingColorOdd = [255, 0, 255],
│      paddingColorEven = [0, 255, 0],
⋮

packages/utils/image_tools/stats.ts:
⋮
│export class FastStats implements Stats {
│  c1: ImageChannel;
│  c2: ImageChannel;
│
│  private _partialSumC1: number[];
│  private _partialSumC2: number[];
│  private _partialSumMult: number[];
│  private _partialSumSq1: number[];
│  private _partialSumSq2: number[];
│
⋮

packages/utils/linuxUtils.ts:
⋮
│function parseOSReleaseText(osReleaseText: string): Map<string, string> {
│  const fields = new Map();
│  for (const line of osReleaseText.split('\n')) {
│    const tokens = line.split('=');
│    const name = tokens.shift();
│    let value = tokens.join('=').trim();
│    if (value.startsWith('"') && value.endsWith('"'))
│      value = value.substring(1, value.length - 1);
│    if (!name)
│      continue;
⋮

packages/web/src/components/codeMirrorModule.tsx:
⋮
│export type CodeMirror = typeof codemirrorType;
⋮

packages/web/src/components/xtermWrapper.tsx:
⋮
│export type XtermDataSource = {
│  pending: (string | Uint8Array)[];
│  clear: () => void,
│  write: (data: string | Uint8Array) => void;
│  resize: (cols: number, rows: number) => void;
⋮

packages/web/src/theme.ts:
⋮
│type DocumentTheme = 'dark-mode' | 'light-mode';
⋮

tests/assets/reading-list/vue_2.6.14.js:
⋮
│(function (global, factory) {
│  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
│  typeof define === 'function' && define.amd ? define(factory) :
│  (global = global || self, global.Vue = factory());
│}(this, function () { 'use strict';
│
│  /*  */
│
│  var emptyObject = Object.freeze({});
│
│  // These helpers produce better VM code in JS engines due to their
│  // explicitness and function inlining.
│  function isUndef (v) {
│    return v === undefined || v === null
⋮
│  if (typeof Set !== 'undefined' && isNative(Set)) {
│    // use native Set when available.
│    _Set = Set;
│  } else {
│    // a non-standard Set polyfill that only works with primitive keys.
│    _Set = /*@__PURE__*/(function () {
│      function Set () {
│        this.set = Object.create(null);
│      }
│      Set.prototype.has = function has (key) {
│        return this.set[key] === true
│      };
│      Set.prototype.add = function add (key) {
│        this.set[key] = true;
│      };
⋮

tests/assets/reading-list/vue_3.1.5.js:
⋮
│  function startsWith(source, searchString) {
│      return source.startsWith(searchString);
⋮

tests/bidi/playwright.config.ts:
⋮
│type BrowserName = 'chromium' | 'firefox';
│
⋮

tests/components/ct-react-vite/src/components/CheckChildrenProp.tsx:
⋮
│type DefaultChildrenProps = PropsWithChildren<{}>;
│
⋮

tests/components/ct-react-vite/src/components/ComponentAsProp.tsx:
⋮
│type ComponentAsProp = {
│  component: ReactNode[] | ReactNode;
⋮
│export function ComponentAsProp({ component }: ComponentAsProp) {
│  return <div>{component}</div>
⋮

tests/components/ct-react-vite/src/components/Counter.tsx:
⋮
│ type CounterProps = {
│   count?: number;
│   onClick?(props: string): void;
│   children?: any;
⋮

tests/components/ct-react-vite/src/components/DefaultChildren.tsx:
│type DefaultChildrenProps = {
⋮

tests/components/ct-react-vite/src/components/EmptyFragment.tsx:
│export default function EmptyFragment(props: unknown) {
⋮

tests/components/ct-react-vite/src/pages/DashboardPage.tsx:
│export default function DashboardPage() {
⋮

tests/components/ct-react-vite/src/pages/LoginPage.tsx:
│export default function LoginPage() {
⋮

tests/components/ct-react17/src/components/CheckChildrenProp.tsx:
⋮
│type DefaultChildrenProps = PropsWithChildren<{}>;
│
⋮

tests/components/ct-react17/src/components/Counter.tsx:
⋮
│ type CounterProps = {
│   count?: number;
│   onClick?(props: string): void;
│   children?: any;
⋮

tests/components/ct-react17/src/components/DefaultChildren.tsx:
│type DefaultChildrenProps = {
⋮

tests/components/ct-react17/src/components/EmptyFragment.tsx:
│export default function EmptyFragment(props: unknown) {
⋮

tests/components/ct-react17/src/pages/DashboardPage.tsx:
│export default function DashboardPage() {
⋮

tests/components/ct-react17/src/pages/LoginPage.tsx:
│export default function LoginPage() {
⋮

tests/components/ct-vue-vite/playwright/index.ts:
⋮
│export type HooksConfig = {
│  routing?: boolean;
│  components?: Record<string, any>;
⋮

tests/config/commonFixtures.ts:
⋮
│type TestChildParams = {
│  command: string[],
│  cwd?: string,
│  env?: NodeJS.ProcessEnv,
│  shell?: boolean,
│  onOutput?: () => void;
⋮
│export class TestChildProcess {
│  params: TestChildParams;
│  process: ChildProcess;
│  output = '';
│  stdout = '';
│  stderr = '';
│  fullOutput = '';
│  onOutput?: (chunk: string | Buffer) => void;
│  exited: Promise<{ exitCode: number | null, signal: string | null }>;
│  exitCode: Promise<number | null>;
│
⋮

tests/image_tools/unit.spec.ts:
⋮
│type ImageChannel = InstanceType<typeof ImageChannel>;
│
⋮

tests/installation/registry.ts:
⋮
│export class Registry {
│  private _workDir: string;
│  private _url: string;
│  private _objectsDir: string;
│  private _packageMeta: Map<string, [any, string]> = new Map();
│  private _log: { pkg: string, status: 'PROXIED' | 'LOCAL', type?: 'tar' | 'metadata' }[] = [];
│  private _server: Server;
│
│  constructor(workDir: string, url: string) {
│    this._workDir = workDir;
│    this._objectsDir = path.join(this._workDir);
│    this._url = url;
⋮
│  public assertLocalPackage(pkg) {
│    const summary = this._log.reduce((acc, f) => {
│      if (f.pkg === pkg) {
│        acc.local = f.status === 'LOCAL' || acc.local;
│        acc.proxied = f.status === 'PROXIED' || acc.proxied;
│      }
│
│      return acc;
│    }, { local: false, proxied: false });
│
⋮
│  private async _addPackage(pkg: string, tarPath: string) {
│    const tmpDir = await fs.promises.mkdtemp(path.join(this._workDir, '.staging-package-'));
│    const { stderr, code } = await spawnAsync('tar', ['-xvzf', tarPath, '-C', tmpDir]);
│    if (!!code)
│      throw new Error(`Failed to untar ${pkg}: ${stderr}`);
│
│    const packageJson = JSON.parse((await fs.promises.readFile(path.join(tmpDir, 'package', 'packag
│    if (pkg !== packageJson.name)
│      throw new Error(`Package name mismatch: ${pkg} is called ${packageJson.name} in its package.j
│
⋮
│  private _logAccess(info: {status: 'PROXIED' | 'LOCAL', pkg: string, type?: 'tar' | 'metadata'}) {
│    this._log.push(info);
⋮

tests/library/chromium/connect-over-cdp.spec.ts:
⋮
│test('emulate media should not be affected by second connectOverCDP with noDefaults', async ({ brow
│  test.info().annotations.push({ type: 'issue', description: 'https://github.com/microsoft/playwrig
│  const port = 9339 + testInfo.workerIndex;
│  const browserServer = await browserType.launch({
│    args: ['--remote-debugging-port=' + port]
│  });
│  try {
│    async function isPrint(page) {
│      return await page.evaluate(() => matchMedia('print').matches);
│    }
│
│    const browser1 = await browserType.connectOverCDP(`http://localhost:${port}`);
│    const context1 = await browser1.newContext();
│    const page1 = await context1.newPage();
│    await page1.emulateMedia({ media: 'print' });
│    expect(await isPrint(page1)).toBe(true);
⋮

tests/library/events/utils.ts:
⋮
│export class EventEmitter extends (clientEventEmitter as any) {
│  constructor() {
│    super(nodePlatform(process.cwd()));
│  }
⋮

tests/library/playwright.config.ts:
⋮
│type BrowserName = 'chromium' | 'firefox' | 'webkit';
│
⋮

tests/library/unit/json-schema.spec.ts:
⋮
│type JsonSchema = iso.JsonSchema;
│
⋮

tests/page/page-evaluate.spec.ts:
⋮
│it('should work with overwritten Promise', async ({ page }) => {
│  await page.evaluate(() => {
│    const originalPromise = window.Promise;
│    class Promise2 {
│      _promise: Promise<any>;
│      static all(arg) {
│        return wrap(originalPromise.all(arg));
│      }
│      static race(arg) {
│        return wrap(originalPromise.race(arg));
│      }
│      static resolve(arg) {
│        return wrap(originalPromise.resolve(arg));
⋮

tests/third_party/proxy/index.ts:
⋮
│export interface ProxyServer extends http.Server {
│	authenticate?: (req: http.IncomingMessage) => boolean | Promise<boolean>;
│	localAddress?: string;
⋮

utils/generate_types/overrides-test.d.ts:
⋮
│export type Metadata = { [key: string]: any };
│
│export interface FullConfig<TestArgs = {}, WorkerArgs = {}> {
│  projects: FullProject<TestArgs, WorkerArgs>[];
│  reporter: ReporterDescription[];
│  webServer: TestConfigWebServer | null;
⋮
│export interface TestInfo {
│  snapshotPath(...name: ReadonlyArray<string>): string;
│  snapshotPath(name: string, options: { kind: 'snapshot' | 'screenshot' | 'aria' }): string;
⋮
│export type TestDetails = {
│  tag?: string | string[];
│  annotation?: TestDetailsAnnotation | TestDetailsAnnotation[];
⋮
│type BrowserName = 'chromium' | 'firefox' | 'webkit';
⋮
│export type PlaywrightTestConfig<TestArgs = {}, WorkerArgs = {}> = Config<PlaywrightTestOptions & C
│
⋮
```
