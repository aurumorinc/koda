---
name: windmill
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging windmill. Use this skill whenever modifying windmill configurations or adding related functionality.
---
# windmill

## File Tree

```text
windmill/
├── modules
│   └── windmill (See AST Map below)
└── SKILL.md
```

### AST Map: `modules/windmill`

```python
ai_evals/core/types.ts:
⋮
│export type EvalMode = (typeof EVAL_MODES)[number];
│
⋮
│export interface CliValidationSpec {
│  requiredSkills?: string[];
│  forbiddenSkills?: string[];
│  requiredSkillsBeforeFirstMutation?: string[];
│  requiredAssistantMentions?: string[];
│  forbiddenAssistantMentions?: string[];
│  orderedAssistantMentions?: string[];
│  requiredProposedCommands?: string[];
│  forbiddenProposedCommands?: string[];
│  orderedProposedCommands?: string[];
⋮
│export interface ToolValidationSpec {
│  requiredToolsUsed?: string[];
│  /**
│   * Each inner array is an alternatives group: the check passes when at least
│   * one tool in the group was used. Use when several tools satisfy the same
│   * intent so a model that picks any valid path passes — e.g. inspecting an
│   * app's files via either `read_app_file` or `search_app`.
│   */
│  requiredToolsAnyOf?: string[][];
│  forbiddenToolsUsed?: string[];
⋮
│export interface EvalCase {
│  id: string;
│  prompt: string;
│  initialPath?: string;
│  expectedPath?: string;
│  validate?: EvalValidationSpec;
│  toolExpect?: ToolValidationSpec;
│  cliExpect?: CliValidationSpec;
│  judgeChecklist?: string[];
│  skipJudge?: boolean;
⋮
│export interface ModeRunContext {
│  evalCase?: EvalCase;
│  caseId: string;
│  caseNumber: number;
│  totalCases: number;
│  attempt: number;
│  runs: number;
│  verbose: boolean;
│  onAssistantMessageStart?: () => void;
│  onAssistantChunk?: (chunk: string) => void;
⋮

ai_evals/core/windmillBackendSettings.ts:
│export interface WindmillBackendSettings {
⋮

ai_evals/fixtures/frontend/app/initial/shopping_cart/backend/addToCart/main.ts:
│interface Product {
⋮

ai_evals/fixtures/frontend/app/initial/shopping_cart/backend/calculateTotal/main.ts:
│interface Product {
⋮

ai_evals/fixtures/frontend/app/initial/shopping_cart/backend/removeFromCart/main.ts:
│interface Product {
⋮

ai_evals/fixtures/frontend/app/initial/shopping_cart/frontend/index.tsx:
⋮
│export interface Product {
│	id: string
│	name: string
│	price: number
│	image: string
⋮

ai_evals/fixtures/frontend/global/initial/analytics_dashboard/backend/computeSummary/main.ts:
│type OrderStatus = 'paid' | 'shipped' | 'delivered' | 'pending' | 'refunded' | 'cancelled'
│
⋮

ai_evals/fixtures/frontend/global/initial/analytics_dashboard/backend/loadOrders/main.ts:
│type OrderStatus = 'paid' | 'shipped' | 'delivered' | 'pending' | 'refunded' | 'cancelled'
│
⋮

ai_evals/fixtures/frontend/global/initial/analytics_dashboard/frontend/data/seedData.ts:
⋮
│export type OrderStatus =
│	| 'paid'
│	| 'shipped'
│	| 'delivered'
│	| 'pending'
│	| 'refunded'
⋮

ai_evals/fixtures/frontend/global/initial/analytics_dashboard/frontend/lib/api.ts:
⋮
│export interface DateRange {
│	from: string
│	to: string
⋮

backend/parsers/windmill-parser-wasm/lib/windmill_parser_wasm.generated.d.ts:
⋮
│export interface InstantiateOptions {
│  /** Optional url to the Wasm file to instantiate. */
│  url?: URL;
│  /** Callback to decompress the raw Wasm file bytes before instantiating. */
│  decompress?: (bytes: Uint8Array) => Uint8Array;
⋮

backend/src/monitor.rs:
⋮
│async fn handle_zombie_jobs(db: &Pool<Postgres>, base_internal_url: &str, node_name: &str) {
│    let mut zombie_jobs_uuid_restart_limit_reached = vec![];
│
│    if *RESTART_ZOMBIE_JOBS {
│        let restarted = sqlx::query!(
│            "WITH to_update AS (
│                SELECT q.id, q.workspace_id, r.ping, COALESCE(zjc.counter, 0) as counter
│                FROM v2_job_queue q
│                JOIN v2_job j ON j.id = q.id
│                JOIN v2_job_runtime r ON r.id = j.id
⋮
│    impl ErrorMessage {
│        fn to_string(&self) -> String {
│            match self {
│                ErrorMessage::RestartLimit => format!("RestartLimit ({})", RESTART_LIMIT),
│                ErrorMessage::SameWorker => "SameWorker".to_string(),
│                ErrorMessage::RestartDisabled => "RestartDisabled".to_string(),
│            }
│        }
⋮

backend/tests/scripts/test_volume_with_claude.ts:
⋮
│type Anthropic = {
│  api_key: string;
│  model?: string;
⋮

backend/windmill-ai/src/types.rs:
⋮
│impl TokenUsage {
│    /// Create a new TokenUsage with basic token counts
│    pub fn new(input: Option<i32>, output: Option<i32>, total: Option<i32>) -> Self {
│        Self {
│            input_tokens: input,
│            output_tokens: output,
│            total_tokens: total,
│            cache_read_input_tokens: None,
│            cache_write_input_tokens: None,
│        }
⋮
│    pub fn is_empty(&self) -> bool {
│        self.input_tokens.is_none()
│            && self.output_tokens.is_none()
│            && self.total_tokens.is_none()
│            && self.cache_read_input_tokens.is_none()
│            && self.cache_write_input_tokens.is_none()
⋮
│impl OpenAPISchema {
│    pub fn from_str(typ: &str) -> Self {
│        OpenAPISchema { r#type: Some(SchemaType::Single(typ.to_string())), ..Default::default() }
│    }
│
│    pub fn from_str_with_enum(typ: &str, enu: &Option<Vec<String>>) -> Self {
│        OpenAPISchema {
│            r#type: Some(SchemaType::Single(typ.to_string())),
│            r#enum: enu.clone(),
│            ..Default::default()
⋮
│    /// - Ensuring all properties are in the required array
│    pub fn make_strict(&mut self) {
│        // First, flatten any allOf schemas since OpenAI strict mode doesn't support them
│        self.flatten_all_of();
│
│        // Handle this schema if it's an object type
│        if let Some(SchemaType::Single(ref type_str)) = self.r#type {
│            if type_str == "object" {
│                // Only set additionalProperties to false if not already set
│                // If user provided a value (bool or schema), preserve it and let OpenAI handle it
│                if self.additional_properties.is_none() {
⋮
│    /// See https://github.com/windmill-labs/windmill/issues/7759
│    pub fn sanitize_for_google(&mut self) {
│        let mut schema_value = match serde_json::to_value(&*self) {
│            Ok(value) => value,
│            Err(err) => {
│                tracing::error!("Failed to serialize OpenAPISchema for Google AI: {err}");
│                return;
│            }
│        };
│
│        sanitize_schema_for_google(&mut schema_value);
│
⋮
│mod tests {
│    use super::*;
│    use std::collections::HashMap;
│
│    /// Helper to create a simple string type schema
│    fn string_schema() -> OpenAPISchema {
│        OpenAPISchema {
│            r#type: Some(SchemaType::Single("string".to_string())),
│            ..Default::default()
│        }
⋮
│    /// Helper to create an object schema with given properties
│    fn object_schema(properties: Vec<(&str, OpenAPISchema)>) -> OpenAPISchema {
│        OpenAPISchema {
│            r#type: Some(SchemaType::Single("object".to_string())),
│            properties: Some(
│                properties
│                    .into_iter()
│                    .map(|(k, v)| (k.to_string(), Box::new(v)))
│                    .collect(),
│            ),
│            ..Default::default()
⋮

backend/windmill-api-auth/src/ee_oss.rs:
⋮
│pub struct ExternalJwks;
│
⋮

backend/windmill-api-client/src/lib.rs:
⋮
│pub mod types {
│    use super::*;
│
│    /// Script language
│    #[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq, Hash)]
│    pub enum ScriptLang {
│        #[serde(rename = "python3")]
│        Python3,
│        #[serde(rename = "deno")]
│        Deno,
│        #[serde(rename = "go")]
│        Go,
│        #[serde(rename = "bash")]
│        Bash,
│        #[serde(rename = "powershell")]
⋮
│    impl std::str::FromStr for ScriptLang {
│        type Err = &'static str;
│        fn from_str(value: &str) -> Result<Self, Self::Err> {
│            match value {
│                "python3" => Ok(Self::Python3),
│                "deno" => Ok(Self::Deno),
│                "go" => Ok(Self::Go),
│                "bash" => Ok(Self::Bash),
│                "powershell" => Ok(Self::Powershell),
│                "postgresql" => Ok(Self::Postgresql),
⋮
│    pub struct FlowModule {
│        #[serde(default, skip_serializing_if = "Option::is_none")]
│        pub cache_ttl: Option<f64>,
│        #[serde(default, skip_serializing_if = "Option::is_none")]
│        pub continue_on_error: Option<bool>,
│        #[serde(default, skip_serializing_if = "Option::is_none")]
│        pub delete_after_secs: Option<i32>,
│        pub id: String,
│        #[serde(default, skip_serializing_if = "Option::is_none")]
│        pub mock: Option<serde_json::Value>,
⋮

backend/windmill-common/src/auth.rs:
⋮
│pub struct PermsCache(Cache<(u64, u64), ()>, AtomicI64);
│
⋮
│impl ToString for IdToken {
│    fn to_string(&self) -> String {
│        self.token.clone()
│    }
⋮
│pub struct JWTAuthClaims {
│    pub email: String,
│    pub username: String,
│    pub is_admin: bool,
│    pub is_operator: bool,
│    pub groups: Vec<String>,
│    pub folders: Vec<(String, bool, bool)>,
│    pub label: Option<String>,
│    pub workspace_id: Option<String>,
│    pub workspace_ids: Option<Vec<String>>,
⋮
│pub async fn is_super_admin_email(db: &DB, email: &str) -> Result<bool> {
│    if email == SUPERADMIN_SECRET_EMAIL || email == SUPERADMIN_NOTIFICATION_EMAIL {
│        return Ok(true);
│    }
│
│    let is_admin = sqlx::query_scalar!("SELECT super_admin FROM password WHERE email = $1", email)
│        .fetch_optional(db)
│        .await
│        .map_err(|e| Error::internal_err(format!("fetching super admin: {e:#}")))?
│        .unwrap_or(false);
│
⋮
│pub fn fetch_authed_from_permissioned_as<'a, A>(
│    permissioned_as: &'a str,
│    email: &'a str,
│    w_id: &'a str,
│    db: A,
⋮
│async fn fetch_authed_from_permissioned_as_inner(
│    permissioned_as: &str,
│    email: &str,
│    w_id: &str,
│    conn: &mut sqlx::PgConnection,
⋮
│pub async fn get_folders_for_user<'e, E: sqlx::PgExecutor<'e>>(
│    w_id: &str,
│    username: &str,
│    groups: &[String],
│    db: E,
⋮
│pub async fn get_groups_for_user<'e, E: sqlx::PgExecutor<'e>>(
│    w_id: &str,
│    username: &str,
│    email: &str,
│    db: E,
⋮
│pub async fn get_job_perms<'a, E: sqlx::PgExecutor<'a>>(
│    db: E,
│    job_id: &Uuid,
│    w_id: &str,
⋮
│pub async fn create_jwt_token(
│    authed: Authed,
│    workspace_id: &str,
│    expires_in_seconds: u64,
│    job_id: Option<Uuid>,
│    label: Option<String>,
│    audit_span: Option<String>,
│    scopes: Option<Vec<String>>,
⋮
│pub mod aws {
│
│    use super::*;
│    use crate::utils::empty_as_none;
│    use aws_config::{BehaviorVersion, Region};
│    use aws_sdk_sts::{
│        config::Credentials as AwsCredentials,
│        operation::{
│            assume_role_with_saml::AssumeRoleWithSamlOutput,
│            assume_role_with_web_identity::{
⋮
│    pub trait GetAuthenticationOutput {
│        fn get_credentials(&self) -> Result<&Credentials>;
⋮

backend/windmill-common/src/email_oss.rs:
⋮
│pub async fn send_email(
│    _subject: &str,
│    _content: &str,
│    _to: Vec<String>,
│    _smtp: Smtp,
│    _client_timeout: Option<tokio::time::Duration>,
⋮

backend/windmill-common/src/instance_config.rs:
⋮
│pub enum ScriptLang {
│    Python3,
│    Deno,
│    Go,
│    Bash,
│    Powershell,
│    Postgresql,
│    Bun,
│    Bunnative,
│    Mysql,
⋮

backend/windmill-common/src/otel_oss.rs:
⋮
│pub trait FutureExt: Sized {
│    fn with_context(self, _otel_cx: ()) -> Self {
│        self
│    }
⋮

backend/windmill-common/src/user_drafts.rs:
⋮
│pub enum UserDraftItemKind {
│    Script,
│    Flow,
│    App,
│    RawApp,
│    Resource,
│    Variable,
│    TriggerSchedule,
│    TriggerWebhook,
│    TriggerDefaultEmail,
⋮

backend/windmill-common/src/utils.rs:
⋮
│impl IsEmpty for String {
│    fn is_empty(&self) -> bool {
│        self.is_empty()
│    }
⋮
│impl<T> IsEmpty for Vec<T> {
│    fn is_empty(&self) -> bool {
│        self.is_empty()
│    }
⋮
│impl<T> IsEmpty for Option<T>
⋮
│{
│    fn is_empty(&self) -> bool {
│        match self {
│            Some(v) => v.is_empty(),
│            None => true,
│        }
⋮
│pub fn is_empty<T>(value: &T) -> bool
⋮
│pub trait WarnAfterExt: Future + Sized {
│    /// Warns if the future takes longer than the specified number of seconds to complete.
│    #[track_caller]
│    fn warn_after_seconds(self, seconds: u8) -> WarnAfterFuture<Self> {
│        let caller = Location::caller();
│        self.build_from_caller(seconds, caller, None)
│    }
│
│    fn build_from_caller(
│        self,
⋮

backend/windmill-common/src/workspace_dependencies.rs:
⋮
│fn map_err(e: String) -> error::Error {
│    error::Error::FeatureUnavailable(e)
⋮

backend/windmill-trigger-mqtt/src/listener.rs:
⋮
│impl EventLoop for V5EventLoop {
│    type Event = V5Event;
│    type Error = rumqttc::v5::ConnectionError;
│
│    async fn poll(&mut self) -> Result<Self::Event> {
│        self.poll().await.map_err(|err| to_anyhow(err).into())
│    }
│
│    async fn verify_connection(&mut self) -> Result<()> {
│        let start = std::time::Instant::now();
│
⋮
│impl EventLoop for V3EventLoop {
│    type Event = V3Event;
│    type Error = rumqttc::ConnectionError;
│
│    async fn poll(&mut self) -> Result<Self::Event> {
│        self.poll().await.map_err(|err| to_anyhow(err).into())
│    }
│
│    async fn verify_connection(&mut self) -> Result<()> {
│        let start = std::time::Instant::now();
│
⋮

backend/windmill-types/src/flows.rs:
⋮
│pub struct FlowModule {
│    #[serde(default = "default_id")]
│    pub id: String,
│    pub value: Box<RawValue>,
│    #[serde(skip_serializing_if = "Option::is_none")]
│    pub stop_after_if: Option<StopAfterIf>,
│    #[serde(skip_serializing_if = "Option::is_none")]
│    pub stop_after_all_iters_if: Option<StopAfterIf>,
│    #[serde(skip_serializing_if = "Option::is_none")]
│    pub summary: Option<String>,
⋮

backend/windmill-types/src/lib.rs:
⋮
│/// windmill-types cannot depend on windmill-common (it would be circular).
│pub fn to_raw_value<T: serde::Serialize>(result: &T) -> Box<serde_json::value::RawValue> {
│    serde_json::value::to_raw_value(result)
│        .unwrap_or_else(|_| serde_json::value::RawValue::from_string("{}".to_string()).unwrap())
⋮

backend/windmill-types/src/scripts.rs:
⋮
│pub enum ScriptLang {
│    Nativets,
│    #[default]
│    Deno,
│    Python3,
│    Go,
│    Bash,
│    Powershell,
│    Postgresql,
│    Bun,
⋮
│impl FromStr for ScriptLang {
│    type Err = anyhow::Error;
│    fn from_str(s: &str) -> Result<Self, Self::Err> {
│        let language = match s.to_lowercase().as_str() {
│            "bun" => ScriptLang::Bun,
│            "bunnative" => ScriptLang::Bunnative,
│            "nativets" => ScriptLang::Nativets,
│            "deno" => ScriptLang::Deno,
│            "python3" => ScriptLang::Python3,
│            "go" => ScriptLang::Go,
⋮
│pub struct ScriptHash(pub i64);
│
⋮

backend/windmill-worker/src/worker.rs:
⋮
│impl JobOutcome {
│    /// True when the job completed successfully on this worker. Used by
│    /// callers that previously matched on `Ok(true)`.
│    pub fn is_success(&self) -> bool {
│        matches!(self, Self::Completed)
│    }
⋮

cli/src/commands/instance/instance.ts:
⋮
│export interface Instance {
│  remote: string;
│  name: string;
│  token: string;
│  prefix: string;
⋮
│export type InstanceSyncOptions = {
│  skipUsers?: boolean;
│  skipSettings?: boolean;
│  skipConfigs?: boolean;
│  skipGroups?: boolean;
│  includeWorkspaces?: boolean;
│  instance?: string;
│  baseUrl?: string;
│  token?: string;
│  folderPerInstance?: boolean;
⋮

cli/src/commands/queues/queues.ts:
⋮
│type GlobalOptions = {
│  instance?: string;
│  baseUrl?: string;
⋮

cli/src/commands/worker-groups/worker-groups.ts:
⋮
│type GlobalOptions = {
│  instance?: string;
│  baseUrl?: string;
⋮

cli/src/commands/workers/workers.ts:
⋮
│type GlobalOptions = {
│  instance?: string;
│  baseUrl?: string;
⋮

cli/src/core/conf.ts:
⋮
│export interface SpecificItemsConfig_Yaml {
│  variables?: string[];
│  resources?: string[];
│  triggers?: string[];
│  schedules?: string[];
│  folders?: string[];
│  settings?: boolean;
⋮
│export interface WorkspaceEntryConfig extends SyncOptions {
│  gitBranch?: string;
│  workspaceId?: string;
│  baseUrl?: string;
│  overrides?: Partial<SyncOptions>;
│  promotionOverrides?: Partial<SyncOptions>;
│  specificItems?: SpecificItemsConfig_Yaml;
⋮
│type LegacyBranchesConfig = {
│  commonSpecificItems?: SpecificItemsConfig_Yaml;
⋮
│export interface SyncOptions {
│  stateful?: boolean;
│  raw?: boolean;
│  yes?: boolean;
│  dryRun?: boolean;
│  skipPull?: boolean;
│  failConflicts?: boolean;
│  plainSecrets?: boolean;
│  json?: boolean;
│  skipVariables?: boolean;
⋮

cli/src/core/permissioned_as.ts:
⋮
│export interface PermissionedAsContext {
│  userCache: Map<string, { username: string; email: string }>;
│  userIsAdminOrDeployer: boolean;
│  userEmail: string;
⋮

cli/src/core/settings.ts:
⋮
│export interface PushWorkspaceKeyOptions {
│  // True when no prompt may be shown (e.g. `--yes` was passed or stdin is not a
│  // TTY). In that case the re-encryption decision is taken from `skipReencrypt`
│  // / the WMILL_NO_REENCRYPT_ON_KEY_CHANGE env var instead of an interactive
│  // confirmation.
│  noninteractive?: boolean;
│  // Explicit re-encryption decision from `--skip-reencrypt-on-key-change`.
│  // When set it takes precedence over the prompt and the env var.
│  skipReencrypt?: boolean;
⋮

cli/src/types.ts:
⋮
│export type GlobalOptions = {
│  baseUrl: string | undefined;
│  workspace: string | undefined;
│  token: string | undefined;
│  configDir: string | undefined;
⋮

cli/src/utils/script_common.ts:
│export type ScriptLanguage =
⋮

cli/test/test_backend.ts:
⋮
│export interface TestBackend {
│  readonly baseUrl: string;
│  readonly workspace: string;
│  readonly testConfigDir: string;
│  readonly token?: string;
│
│  start(): Promise<void>;
│  stop(): Promise<void>;
│  reset(): Promise<void>;
│
⋮

debugger/test_dap_server.py:
⋮
│class DAPTestClient:
⋮

debugger/test_dap_server_bun.ts:
⋮
│class DAPTestClient {
│	private url: string
│	private ws: WebSocket | null = null
│	private seq = 1
│	private pendingRequests = new Map<
│		number,
│		{ resolve: (value: DAPMessage) => void; reject: (error: Error) => void }
│	>()
│	private events: DAPMessage[] = []
│	private output: string[] = []
⋮
│async function runComprehensiveTest(): Promise<void> {
│	const client = new DAPTestClient()
│	const results: TestResult[] = []
│	let passed = 0
│	let failed = 0
│
│	function assert(condition: boolean, testName: string, details?: string): void {
│		if (condition) {
│			console.log(`[PASS] ${testName}`)
│			passed++
│			results.push({ test: testName, passed: true, details })
│		} else {
│			console.log(`[FAIL] ${testName}${details ? ': ' + details : ''}`)
│			failed++
│			results.push({ test: testName, passed: false, error: details })
│		}
⋮
│async function testDynamicImports(): Promise<void> {
│	console.log('='.repeat(60))
│	console.log('DYNAMIC IMPORT TEST')
│	console.log('='.repeat(60))
│	console.log('\nThis test verifies that external npm packages are automatically installed.')
│	console.log('Make sure the server is started with: --windmill /path/to/windmill\n')
│
│	const client = new DAPTestClient('ws://localhost:5680')
│	let passed = 0
│	let failed = 0
⋮
│	function assert(condition: boolean, message: string, error?: string) {
│		if (condition) {
│			passed++
│			console.log(`✓ ${message}`)
│			results.push({ test: message, passed: true })
│		} else {
│			failed++
│			console.log(`✗ ${message}` + (error ? `: ${error}` : ''))
│			results.push({ test: message, passed: false, error })
│		}
⋮

debugger/test_debug_service.ts:
⋮
│class TestClient {
│	private ws: WebSocket | null = null
│	private seq = 1
│	private pendingRequests = new Map<
│		number,
│		{ resolve: (value: DAPMessage) => void; reject: (error: Error) => void }
│	>()
│	private events: DAPMessage[] = []
│	private output: string[] = []
│	private result: unknown = undefined
⋮

docker/test_windmill_extra.ts:
⋮
│class DAPTestClient {
│	private ws: WebSocket | null = null
│	private seq = 1
│	private pendingRequests = new Map<
│		number,
│		{ resolve: (value: DAPMessage) => void; reject: (error: Error) => void }
│	>()
│	private events: DAPMessage[] = []
│	private output: string[] = []
│	private result: unknown = undefined
⋮

ephemeral-backends/worktree-pool.ts:
⋮
│export interface WorktreeInfo {
│  id: number;
│  path: string;
│  inUse: boolean;
│  currentCommit?: string;
⋮

examples/deploy/aws-ecs-terraform/vpc.tf:
│resource "aws_vpc" "windmill_cluster_vpc" {
⋮
│resource "aws_subnet" "windmill_cluster_subnet_public1" {
⋮
│resource "aws_subnet" "windmill_cluster_subnet_public2" {
⋮
│resource "aws_subnet" "windmill_cluster_subnet_private1" {
⋮
│resource "aws_subnet" "windmill_cluster_subnet_private2" {
⋮
│resource "aws_route_table" "windmill_cluster_rtb_public" {
⋮

frontend/src/lib/ata/apis.ts:
⋮
│export interface ResLimit {
│	usage: number
⋮

frontend/src/lib/common.ts:
⋮
│export interface SchemaProperty {
│	type: string | undefined
│	description?: string
│	pattern?: string
│	default?: any
│	enum?: EnumType
│	contentEncoding?: 'base64' | 'binary'
│	format?: string
│	items?: {
│		type?: 'string' | 'number' | 'bytes' | 'object' | 'resource'
⋮

frontend/src/lib/components/apps/svelte-grid/utils/other.ts:
│export function throttle(func, timeFrame) {
⋮

frontend/src/lib/components/common/fileInput/model.ts:
│export type ReadFileAs = 'buffer' | 'binary' | 'base64' | 'text'

frontend/src/lib/components/copilot/chat/monaco-adapter.ts:
⋮
│export interface ReviewChangesOpts {
│	applyAll?: boolean
│	mode?: 'apply' | 'revert'
│	onFinishedReview?: () => void
⋮

frontend/src/lib/components/copilot/chat/pasteTokens.ts:
⋮
│export type PasteAttachment = {
│	id: number
│	lines: number
│	content: string
⋮

frontend/src/lib/components/copilot/chat/tokenUsage.ts:
│export interface ChatTokenUsage {
⋮

frontend/src/lib/components/copilot/shared.ts:
⋮
│export type VisualChange =
│	| {
│			type: 'added_inline'
│			position: {
│				line: number
│				column: number
│			}
│			value: string
│			options?: {
│				greenHighlight?: boolean
⋮

frontend/src/lib/components/graph/groupedModulesProxy.svelte.ts:
⋮
│export type PreparedStructureDelete = {
│	affectedGroups: FlowGroup[]
│	duplicateGroups: FlowGroup[]
│	commit: (commitOpts?: { removeDuplicates?: boolean }) => void
⋮

frontend/src/lib/components/graph/noteColors.ts:
⋮
│export enum NoteColor {
│	YELLOW = 'yellow',
│	BLUE = 'blue',
│	GREEN = 'green',
│	PURPLE = 'purple',
│	PINK = 'pink',
│	ORANGE = 'orange',
│	RED = 'red',
│	CYAN = 'cyan',
│	LIME = 'lime',
⋮

frontend/src/lib/components/runs/timeframes.ts:
⋮
│export type Timeframe =
│	| {
│			label: string
│			computeMinMax: () => { minTs: string | null; maxTs: string | null }
│			type: 'dynamic'
│	  }
│	| {
│			label: string
│			computeMinMax: () => { minTs: string | null; maxTs: string | null }
│			minTs: string | null
⋮

frontend/src/lib/git-sync.ts:
⋮
│export interface SettingsObject {
│	include_path: string[]
│	exclude_path: string[]
│	extra_include_path: string[]
│	include_type: GitSyncObjectType[]
⋮

frontend/src/lib/monaco_workers/graphql.worker.bundle.js:
│(()=>{var x5=Object.create;var ql=Object.defineProperty;var y5=Object.getOwnPropertyDescriptor;var 
⋮
│`)return!0;return!1}function IN(e,t,n={}){return Xr(e,n.backwards?t-1:t,n)!==t}function kN(e,t,n){l
│ `,u.gutter(S.replace(/\d/g," "))," ",I,u.marker("^").repeat(k)].join(""),q&&a.message&&(G+=" "+u.m
│`);return a.message&&!m&&(E=`${" ".repeat(g+1)}${a.message}
│${E}`),E}e.codeFrameColumns=i}),L_={};ih(L_,{__debug:()=>d4,check:()=>h4,doc:()=>gh,format:()=>Th,f
⋮
│`)),Z_(s,n.loggerPrintWidth)};W1=[],c_=[];K_=(e,t,{descriptor:n,logger:r,schemas:i})=>{let s=[`Igno
⋮
│`,kt=F.split(/\r\n|[\n\r]/g),Vi=kt[x];if(Vi.length>120){let ir=Math.floor(rt/80),Gl=rt%80,$t=[];for
│`)}function q4(p){let _=p[0];return _==null||"kind"in _||"length"in _?{nodes:_,source:p[1],position
│
⋮
│spurious results.`)}}return!1},$h=class{constructor(p,_="GraphQL request",D={line:1,column:1}){type
│
│`+t.stack):new Error(t.message+`
│
│`+t.stack):t},0)}}addListener(t){return this.listeners.push(t),()=>{this._removeListener(t)}}emit(t
⋮
│`}return r.length>t&&(o+=`
│
│
│... and ${r.length-t} more leaking disposables
│
│`),{leaks:r,details:o}}};function tc(e){return ho?.trackDisposable(e),e}function nc(e){ho?.markAsDi
│`).slice(2).join(`
│`))}},ac=class extends Error{constructor(t,n){super(t),this.name="ListenerLeakError",this.stack=n}}
│`||e==="	"}var Ut;(function(e){e[e.None=0]="None",e[e.NonBasicASCII=1]="NonBasicASCII",e[e.Invisibl
│`?(n++,r=0):r++;return new e(n,r)}static ofSubstr(t,n){return e.ofText(n.substring(t))}static sum(t
⋮
│`+this._getLineContent(t.endLineNumber).substring(0,t.endColumn-1),n}getLineLength(t){return this._
│`,w);if(L===-1)throw new Oe("Text length mismatch");w=L+1,k++}return w+=I,[q.substring(0,w),q.subst
│`):typeof t=="string"?this.toString(new Bn(t)):this.replacements.length===0?"":this.replacements.ma
│`)}},xt=class e{static joinReplacements(t,n){if(t.length===0)throw new Oe;if(t.length===1)return t[
⋮
│`),i=Ki(n,r),s=xn.ofText(n.substring(0,n.length-i)).addToPosition(this.range.getStartPosition()),o=
│`,`
│`),r=t.getValueOfRange(this.range).replaceAll(`\r
│`,`
│`),i=Zi(n,r);n=n.substring(i),r=r.substring(i);let s=Ki(n,r);return n=n.substring(0,n.length-s),r=r
│`);this.histogram[a]=(this.histogram[a]||0)+1}this.totalCount=i}computeSimilarity(t){let n=0,r=Math
│`).length>=15&&eD(f,m=>m.length>=2)>=2}),o=iD(e,o),o}function eD(e,t){let n=0;for(let r of e)t(r)&&
│`)}isStronglyEqual(t,n){return this.lines[t]===this.lines[n]}};function sm(e){let t=0;for(;t<e.leng
│`);s.lastIndex=0;let c;for(;(c=s.exec(l))!==null;){let f=l.substring(0,c.index),d=(f.match(/\n/g)||
│`),E=g.length,T=m+E-1,v=f.lastIndexOf(`
│`)+1,A=c.index-v+1,S=g[g.length-1],C=E===1?A+c[0].length:S.length+1,q={startLineNumber:m,startColum
│`,c=r.split(/\r\n|[\n\r]/g),f=c[i];if(f.length>120){let d=Math.floor(u/80),m=u%80,g=[];for(let E=0;
│`)}function AD(e){let t=e[0];return t==null||"kind"in t||"length"in t?{nodes:t,source:e[1],position
│
⋮
│  `))}function Um(e){var t;return(t=e?.some(n=>n.includes(`
│`)))!==null&&t!==void 0?t:!1}function Wo(e,t){switch(e.kind){case b.NULL:return null;case b.INT:ret
│
⋮
│`))}var yf=class{constructor(t){this._errors=[],this.schema=t}reportError(t,n){let r=Array.isArray(
│
│`))}function Ju(e){return{Field(t){let n=e.getFieldDef(),r=n?.deprecationReason;if(n&&r!=null){let 
⋮

frontend/src/lib/navigation.ts:
⋮
│export function goto(path: string, options = {}) {
│	if (svelteBase == '' || path.startsWith('?')) {
│		return svelteGoto(path, options)
│	} else {
│		const fullPath = path.startsWith(svelteBase) ? path : `${svelteBase}${path}`
│		return svelteGoto(fullPath, options)
│	}
⋮

frontend/src/lib/newDraftFlag.test.ts:
⋮
│function stubWindow(href: string): { current: () => string } {
│	const win: any = {
│		location: { href },
│		history: {
│			state: null as unknown,
│			replaceState(state: unknown, _title: string, url: string) {
│				this.state = state
│				win.location.href = new URL(url, win.location.href).toString()
│			}
│		}
⋮

frontend/src/lib/stores.ts:
⋮
│type SQLBaseSchema = {
│	[schemaKey: string]: {
│		[tableKey: string]: {
│			[columnKey: string]: {
│				type: string
│				default: string
│				required: boolean
│			}
│		}
│	}
⋮

frontend/src/lib/userScopedDb.ts:
⋮
│export interface UserScopedDbMigrateDeps {
│	openDB: typeof idbOpenDB
│	deleteDB: typeof idbDeleteDB
⋮

frontend/src/lib/utils.ts:
⋮
│export function assert(msg: string, condition: boolean, value?: any) {
│	if (!condition) {
│		let m = 'Assertion failed: ' + msg
│		if (value) m += '\nValue: ' + JSON.stringify(value, null, 2)
│		m += '\nPlease alert the Windmill team about this'
│		sendUserToast(m, true)
│		console.error(m)
│	}
⋮

frontend/static/tailwind.js:
⋮
│In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}return t=r[Sym
⋮
│`,"	"];return Br.split(r,e)},comma(r){return Br.split(r,[","],!0)}};Ec.exports=Br;Br.default=Br});v
│`);i=new Array(s.length);let a=0;for(let o=0,u=s.length;o<u;o++)i[o]=a,a+=s[o].length+1;this[ma]=i}
│https://evilmartians.com/chronicles/postcss-8-plugin-migration`),m.env.LANG&&m.env.LANG.startsWith(
│https://www.w3ctech.com/topic/2226`));let o=t(...a);return o.postcssPlugin=e,o.postcssVersion=new b
│`).slice(1,-1).map(q=>q.trim()).map(q=>`      ${q}`).join(`
│`)).join(`
│
│`);x.push(`  Use \`${r.replace("[",`[${D}:`)}\` for \`${M.trim()}\``);break}N.warn([`The class \`${
⋮

frontend/static/web-components.min.js:
⋮
│(()=>{var e,t,n={7560:(e,t,n)=>{"use strict";function r(){return r=Object.assign||function(e){for(v
⋮

integration_tests/ai_agent_tests/providers.py:
⋮
│def make_provider_input_transform(kind: str, model: str, resource_path: str) -> dict[str, Any]:
⋮

python-client/docs/search.js:
⋮
│/** elasticlunr - http://weixsong.github.io * Copyright (C) 2017 Oliver Nightingale * Copyright (C)
⋮

python-client/wmill/wmill/client.py:
⋮
│class SqlQuery:
│    """Query result handler for DataTable and DuckLake queries."""
│
⋮
│    def fetch_one(self):
⋮
│class _RecordingSqlQuery:
│    """Wraps a ducklake materialize query so that, on a successful run, the
│    trailing summary (row count + snapshot id) is captured and the
│    materialized_partition state is recorded (best-effort). Only used in pipeline
│    context — outside it the helpers return a plain SqlQuery. Mirrors SqlQuery's
⋮
│    def fetch_one(self):
⋮

typescript-client/docs/assets/main.js:
⋮
│"use strict";(()=>{var Ce=Object.create;var ie=Object.defineProperty;var Oe=Object.getOwnPropertyDe
⋮

typescript-client/sqlUtils.d.ts:
⋮
│export interface SqlTemplateFunction {
│  <T = any>(strings: TemplateStringsArray, ...values: any[]): SqlStatement<T>;
│  raw(value: string): RawSql;
│}
│export interface DatatableSqlTemplateFunction extends SqlTemplateFunction {
│  query<T = any>(sql: string, ...params: any[]): SqlStatement<T>;
⋮
│export interface DucklakeMaterializeOptions {
│  ducklake?: string;
│  table: string;
│  selectSql: string;
│  partition?: string;
│  uniqueKey?: string;
│  partitionCol?: string;
⋮

typescript-client/sqlUtils.ts:
⋮
│export interface SqlTemplateFunction {
│  <T = any>(strings: TemplateStringsArray, ...values: any[]): SqlStatement<T>;
│  /** Create a raw SQL fragment that will be inlined without parameterization */
│  raw(value: string): RawSql;
⋮
│export interface DatatableSqlTemplateFunction extends SqlTemplateFunction {
│  query<T = any>(sql: string, ...params: any[]): SqlStatement<T>;
⋮
│interface SqlProvider {
│  formatArgDecl(argNum: number, argType: string): string;
│  formatArgUsage(
│    argNum: number,
│    explicitType: string | undefined,
│    inferredType: string
│  ): string;
│  preamble(): string;
│  language: "postgresql" | "duckdb";
│  extraArgs: Record<string, any>;
⋮
│export interface DucklakeMaterializeOptions {
│  /** ducklake name (default "main"), optionally "name:schema". */
│  ducklake?: string;
│  /** target table within the ducklake. */
│  table: string;
│  /** the SELECT producing the rows for this slice. */
│  selectSql: string;
│  /** the partition value (bound). Omit for a whole-table materialization — no
│   * partition column, and replace becomes a `CREATE OR REPLACE TABLE`. */
│  partition?: string;
⋮

typescript-client/tests/sqlUtils.test.ts:
⋮
│interface SqlProvider {
│  formatArgDecl(argNum: number, argType: string): string;
│  formatArgUsage(
│    argNum: number,
│    explicitType: string | undefined,
│    inferredType: string
│  ): string;
│  preamble(): string;
│  language: "postgresql" | "duckdb";
│  extraArgs: Record<string, any>;
⋮

wm-ts-nav/src/main.rs:
⋮
│enum Command {
│    /// Index/re-index the codebase
│    Index,
│    /// Show symbols in a file
│    Outline {
│        /// File path
│        file: PathBuf,
│    },
│    /// Search symbols by name pattern
│    Search {
⋮
```