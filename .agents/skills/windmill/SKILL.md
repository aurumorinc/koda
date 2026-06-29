---
name: windmill
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging windmill. Use this skill whenever modifying windmill configurations or adding related functionality.
---
# windmill

## File Tree

```text
windmill/
├── assets
├── modules
│   └── windmill (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/windmill`

```python
ai_evals\adapters\frontend\core\script\fileHelpers.ts:
⋮
│export interface ScriptEvalState {
│	code: string
│	lang: ScriptLang | 'bunnative'
│	path: string
│	args: Record<string, any>
⋮

ai_evals\adapters\frontend\datatableSqlEngine.ts:
⋮
│export interface BenchmarkDatatableSeed {
│	datatable_name: string
│	schemas: {
│		[schema: string]: {
│			[table: string]: BenchmarkDatatableTableSeed
│		}
│	}
⋮

ai_evals\core\types.ts:
⋮
│export type EvalMode = (typeof EVAL_MODES)[number];
│
│export interface EvalCaseRuntimeBackendPreview {
│  args?: Record<string, unknown>;
│  timeoutSeconds?: number;
⋮
│export interface EvalCaseRuntimeAppContextSpec {
│  additional?: EvalCaseRuntimeAppAdditionalContext[];
⋮
│export interface EvalCaseRuntimeSpec {
│  maxTurns?: number;
│  backendPreview?: EvalCaseRuntimeBackendPreview;
│  appContext?: EvalCaseRuntimeAppContextSpec;
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
│export type EvalValidationSpec =
│  | FlowValidationSpec
│  | AppValidationSpec
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

ai_evals\core\windmillBackendSettings.ts:
│export interface WindmillBackendSettings {
⋮

ai_evals\fixtures\frontend\app\initial\shopping_cart\backend\addToCart\main.ts:
│interface Product {
⋮

ai_evals\fixtures\frontend\app\initial\shopping_cart\backend\calculateTotal\main.ts:
│interface Product {
⋮

ai_evals\fixtures\frontend\app\initial\shopping_cart\backend\removeFromCart\main.ts:
│interface Product {
⋮

ai_evals\fixtures\frontend\app\initial\shopping_cart\frontend\index.tsx:
⋮
│export interface Product {
│	id: string
│	name: string
│	price: number
│	image: string
⋮

ai_evals\fixtures\frontend\global\initial\analytics_dashboard\backend\computeSummary\main.ts:
│type OrderStatus = 'paid' | 'shipped' | 'delivered' | 'pending' | 'refunded' | 'cancelled'
│
⋮

ai_evals\fixtures\frontend\global\initial\analytics_dashboard\backend\loadOrders\main.ts:
│type OrderStatus = 'paid' | 'shipped' | 'delivered' | 'pending' | 'refunded' | 'cancelled'
│
⋮

ai_evals\fixtures\frontend\global\initial\analytics_dashboard\frontend\components\FilterBar.tsx:
⋮
│interface FilterBarProps {
│	region: string
│	status: string
│	preset: string
│	range: DateRange
│	onRegionChange: (region: string) => void
│	onStatusChange: (status: string) => void
│	onPresetChange: (preset: string, range: DateRange) => void
⋮

ai_evals\fixtures\frontend\global\initial\analytics_dashboard\frontend\data\seedData.ts:
⋮
│export type OrderStatus =
│	| 'paid'
│	| 'shipped'
│	| 'delivered'
│	| 'pending'
│	| 'refunded'
⋮

backend\parsers\windmill-parser-py-imports\src\mapping.rs:
⋮
│type PyMap = phf::Map<&'static str, &'static str>;
│
⋮

backend\parsers\windmill-parser-wasm\pkg\windmill_parser_wasm.d.ts:
⋮
│export interface InitOutput {
│  readonly memory: WebAssembly.Memory;
│  readonly parse_deno: (a: number, b: number, c: number) => void;
│  readonly parse_outputs: (a: number, b: number, c: number) => void;
│  readonly parse_ts_imports: (a: number, b: number, c: number) => void;
│  readonly parse_bash: (a: number, b: number, c: number) => void;
│  readonly parse_powershell: (a: number, b: number, c: number) => void;
│  readonly parse_go: (a: number, b: number, c: number) => void;
│  readonly parse_python: (a: number, b: number, c: number) => void;
│  readonly parse_sql: (a: number, b: number, c: number) => void;
⋮
│export type SyncInitInput = BufferSource | WebAssembly.Module;
⋮

backend\parsers\windmill-parser-wasm\wasm-sysroot\unistd.h:
⋮
│int dup(int);

backend\src\monitor.rs:
⋮
│pub async fn reload_option_setting_with_tracing<T: FromStr + DeserializeOwned>(
│    conn: &Connection,
│    setting_name: &str,
│    std_env_var: &str,
│    lock: Arc<RwLock<Option<T>>>,
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

backend\tests\scripts\test_volume_with_claude.ts:
⋮
│type Anthropic = {
│  api_key: string;
│  model?: string;
⋮

backend\windmill-ai\src\types.rs:
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

backend\windmill-api-auth\src\ee_oss.rs:
⋮
│pub struct ExternalJwks;
│
⋮

backend\windmill-api-client\src\lib.rs:
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

backend\windmill-api-jobs\src\jobs.rs:
⋮
│pub fn _benchmark_test_fn() -> bool { true }

backend\windmill-api-sse\src\lib.rs:
⋮
│impl Hash for JobUpdate {
│    fn hash<H: Hasher>(&self, state: &mut H) {
│        self.running.hash(state);
│        self.completed.hash(state);
│        self.log_offset.hash(state);
│        self.mem_peak.hash(state);
│        self.progress.hash(state);
│        self.stream_offset.hash(state);
│        self.flow_stream_job_id.hash(state);
│        if !self.completed.unwrap_or(false) {
│            self.flow_status.as_ref().map(|x| x.get().hash(state));
⋮

backend\windmill-autoscaling\src\autoscaling_oss.rs:
⋮
│pub async fn apply_all_autoscaling(_db: &DB) -> anyhow::Result<()> {
│    // Autoscaling is an ee feature
│    Ok(())
⋮

backend\windmill-common\src\auth.rs:
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
│pub async fn is_super_admin_email<'c>(db: impl sqlx::PgExecutor<'c>, email: &str) -> Result<bool> {
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

backend\windmill-common\src\db.rs:
⋮
│pub trait Authable {
│    fn email(&self) -> &str;
│    fn username(&self) -> &str;
│    fn is_admin(&self) -> bool;
│    fn is_operator(&self) -> bool;
│    fn groups(&self) -> &[String];
│    fn folders(&self) -> &[(String, bool, bool)];
│    fn scopes(&self) -> Option<&[String]>;
⋮

backend\windmill-common\src\email_oss.rs:
⋮
│pub async fn send_email(
│    _subject: &str,
│    _content: &str,
│    _to: Vec<String>,
│    _smtp: Smtp,
│    _client_timeout: Option<tokio::time::Duration>,
⋮

backend\windmill-common\src\global_settings.rs:
⋮
│pub async fn load_value_from_global_settings(
│    db: &Pool<Postgres>,
│    setting_name: &str,
⋮

backend\windmill-common\src\min_version.rs:
⋮
│impl VersionConstraint {
│    pub fn version(&self) -> &Version {
│        &self.available_since
│    }
│
│    pub async fn met(&self) -> bool {
│        let min = MIN_VERSION.load();
│        // If MIN_VERSION is 0.0.0, it hasn't been set yet - assume met
│        if **min == Version::new(0, 0, 0) {
│            tracing::warn!(
⋮
│    pub async fn assert(&self) -> error::Result<()> {
│        if self.met().await {
│            Ok(())
│        } else {
│            Err(Error::WorkersAreBehind {
│                feature: self.name.to_string(),
│                min_version: self.available_since.to_string(),
│            })
│        }
⋮

backend\windmill-common\src\otel_oss.rs:
⋮
│pub trait FutureExt: Sized {
│    fn with_context(self, _otel_cx: ()) -> Self {
│        self
│    }
⋮

backend\windmill-common\src\utils.rs:
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
│pub fn merge_nested_raw_values_to_array<
│    'a,
│    It1: Iterator<Item = It2>,
│    It2: Iterator<Item = &'a Box<serde_json::value::RawValue>>,
⋮

backend\windmill-common\src\worker.rs:
⋮
│impl SqlResultCollectionStrategy {
│    pub fn parse(s: &str) -> Self {
│        use SqlResultCollectionStrategy::*;
│        match s {
│            "last_statement_all_rows" => LastStatementAllRows,
│            "last_statement_first_row" => LastStatementFirstRow,
│            "last_statement_all_rows_scalar" => LastStatementAllRowsScalar,
│            "last_statement_first_row_scalar" => LastStatementFirstRowScalar,
│            "all_statements_all_rows" => AllStatementsAllRows,
│            "all_statements_first_row" => AllStatementsFirstRow,
⋮
│    pub fn collect(
│        &self,
│        values: Vec<Vec<Box<serde_json::value::RawValue>>>,
⋮

backend\windmill-common\src\workspace_dependencies.rs:
⋮
│fn map_err(e: String) -> error::Error {
│    error::Error::FeatureUnavailable(e)
⋮

backend\windmill-dep-map\src\ci_tests.rs:
⋮
│pub async fn trigger_ci_tests_for_item(
│    _db: &sqlx::Pool<sqlx::Postgres>,
│    _w_id: &str,
│    _item_path: &str,
│    _item_kind: &str,
│    _email: &str,
│    _username: &str,
⋮

backend\windmill-types\src\flows.rs:
⋮
│impl TryFrom<UntaggedInputTransform> for InputTransform {
│    type Error = anyhow::Error;
│    fn try_from(value: UntaggedInputTransform) -> Result<Self, Self::Error> {
│        let input_transform = match value.type_.as_str() {
│            "static" => InputTransform::new_static_value(value.value.unwrap_or_else(default_null)),
│            "javascript" => InputTransform::new_javascript_expr(&value.expr.unwrap_or_default()),
│            "ai" => InputTransform::Ai,
│            other => {
│                return Err(anyhow::anyhow!(
│                    "got value: {other} for field `type`, expected value: `static` or `javascript`"
⋮
│impl Into<Box<RawValue>> for FlowModuleValue {
│    fn into(self) -> Box<RawValue> {
│        to_raw_value(&self)
│    }
⋮

backend\windmill-types\src\lib.rs:
⋮
│/// windmill-types cannot depend on windmill-common (it would be circular).
│pub fn to_raw_value<T: serde::Serialize>(result: &T) -> Box<serde_json::value::RawValue> {
│    serde_json::value::to_raw_value(result)
│        .unwrap_or_else(|_| serde_json::value::RawValue::from_string("{}".to_string()).unwrap())
⋮

backend\windmill-types\src\s3.rs:
⋮
│pub struct S3Object {
│    pub s3: String,
│    #[serde(skip_serializing_if = "Option::is_none")]
│    pub storage: Option<String>,
│    #[serde(skip_serializing_if = "Option::is_none")]
│    pub filename: Option<String>,
│    #[serde(skip_serializing_if = "Option::is_none")]
│    pub presigned: Option<String>,
⋮

backend\windmill-types\src\scripts.rs:
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

backend\windmill-worker\src\universal_pkg_installer.rs:
⋮
│impl<T: Clone + Send + Sync> DependencyGraph<T> {
│    pub fn new() -> Self {
│        Self { nodes: HashMap::new(), deps: HashMap::new() }
│    }
│
│    /// Insert a dependency and the names of packages it depends on.
│    /// References to packages not in the graph are silently ignored during layering.
│    pub fn insert(
│        &mut self,
│        key: impl Into<String>,
│        dep: RequiredDependency<T>,
│        depends_on: Vec<String>,
⋮

backend\windmill-worker\src\worker.rs:
⋮
│impl JobOutcome {
│    /// True when the job completed successfully on this worker. Used by
│    /// callers that previously matched on `Ok(true)`.
│    pub fn is_success(&self) -> bool {
│        matches!(self, Self::Completed)
│    }
⋮

benchmarks\worker.ts:
⋮
│async function getQueueCount() {
│  return (
│    await (
│      await fetch(
│        config.server + "/api/w/" + config.workspace_id + "/jobs/queue/count",
│        { headers: { ["Authorization"]: "Bearer " + config.token } }
│      )
│    ).json()
│  ).database_length;
⋮

cli\src\commands\datatable\pg_wire.ts:
⋮
│export interface RawOutputEnvelope {
│  columns: RawOutputColumn[];
│  rows: (string | null)[][];
⋮

cli\src\commands\lint\lint.ts:
⋮
│interface LintOptions extends GlobalOptions {
│  json?: boolean;
│  failOnWarn?: boolean;
│  locksRequired?: boolean;
⋮

cli\src\commands\queues\queues.ts:
⋮
│type GlobalOptions = {
│  instance?: string;
│  baseUrl?: string;
⋮

cli\src\commands\worker-groups\worker-groups.ts:
⋮
│type GlobalOptions = {
│  instance?: string;
│  baseUrl?: string;
⋮

cli\src\commands\workers\workers.ts:
⋮
│type GlobalOptions = {
│  instance?: string;
│  baseUrl?: string;
⋮

cli\src\core\conf.ts:
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
│export type WorkspacesConfig = {
│  commonSpecificItems?: SpecificItemsConfig_Yaml;
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

cli\src\core\permissioned_as.ts:
⋮
│export interface PermissionedAsContext {
│  userCache: Map<string, { username: string; email: string }>;
│  userIsAdminOrDeployer: boolean;
│  userEmail: string;
⋮

cli\src\core\settings.ts:
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

cli\src\core\specific_items.ts:
⋮
│export interface SpecificItemsConfig {
│  variables?: string[];
│  resources?: string[];
│  triggers?: string[];
│  schedules?: string[];
│  folders?: string[];
│  settings?: boolean;
⋮

cli\src\types.ts:
⋮
│export type GlobalOptions = {
│  baseUrl: string | undefined;
│  workspace: string | undefined;
│  token: string | undefined;
│  configDir: string | undefined;
⋮

cli\src\utils\script_common.ts:
│export type ScriptLanguage =
⋮

cli\src\utils\upgrade.ts:
⋮
│export type NpmProviderOptions = { main?: string; logger?: any } & (
│  | {
│      package: string;
│    }
│  | {
│      scope: string;
│      name?: string;
│    }
⋮

cli\src\utils\yaml.ts:
⋮
│type YamlParseOptions = ParseOptions & DocumentOptions & SchemaOptions & ToJSOptions;
│
⋮

cli\test\containerized_backend.ts:
⋮
│export class ContainerizedBackend {
│  private config: Required<ContainerConfig>;
│  private isRunning = false;
│
│  constructor(config: Partial<ContainerConfig> = {}) {
│    this.config = {
│      composeFile: config.composeFile || new URL('./docker-compose.test.yml', import.meta.url).path
│      baseUrl: config.baseUrl || 'http://localhost:8001',
│      workspace: config.workspace || 'test', // Use test workspace
│      token: config.token || '',
⋮

cli\test\fixtures\yaml-snapshots\regenerate.ts:
⋮
│interface Fixture {
│  filename: string;
│  source: Record<string, unknown>;
⋮

cli\test\test_backend.ts:
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

debugger\test_dap_server.py:
⋮
│class DAPTestClient:
⋮

debugger\test_dap_server_bun.ts:
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

debugger\test_debug_service.ts:
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

docker\test_windmill_extra.ts:
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

docs\clone_repo_and_upload_to_instance_storage.bun.ts:
⋮
│type GitRepository = {
│  url: string;
│  branch: string;
│  folder: string;
│  gpg_key: any;
│  is_github_app: boolean;
⋮

ephemeral-backends\worktree-pool.ts:
⋮
│export interface WorktreeInfo {
│  id: number;
│  path: string;
│  inUse: boolean;
│  currentCommit?: string;
⋮

examples\deploy\aws-ecs-terraform\rds.tf:
⋮
│resource "aws_db_instance" "windmill_cluster_rds" {
⋮

examples\deploy\aws-ecs-terraform\vpc.tf:
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

frontend\e2e\global-setup.ts:
⋮
│async function globalSetup(config: FullConfig) {
│	process.env.TEST_UNIQUE_ID = Date.now().toString()
│
│	const browser = await chromium.launch()
│	const context = await browser.newContext({
│		permissions: ['clipboard-read', 'clipboard-write']
│	})
│	const page = await context.newPage()
│
│	// Use baseURL from config
⋮

frontend\sharedUtils\sharedUtils.d.ts:
⋮
│interface ImportMetaEnv {
│	readonly VITE_APP_TITLE: string
│	// Add other env variables as needed
│	readonly REMOTE?: string
│	readonly REMOTE_LSP?: string
⋮

frontend\src\.d.ts:
⋮
│	interface HTMLAttributes<T> {
│		'on:click_outside'?: (event: CustomEvent) => void
│		'on:pointerdown_outside'?: (event: CustomEvent) => void
│		'on:pointerdown_connecting'?: (event: CustomEvent) => void
⋮

frontend\src\global.d.ts:
⋮
│interface ImportMetaEnv {
│	readonly VITE_APP_TITLE: string
│	// Add other env variables as needed
│	readonly REMOTE?: string
│	readonly REMOTE_LSP?: string
⋮

frontend\static\tailwind.js:
⋮
│In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}return t=r[Sym
⋮
│`)){let a=this.raw(e,null,"indent");if(a.length)for(let o=0;o<s;o++)i+=a}return i}rawValue(e,t){let
│`?(i=1,n+=1):i+=1;return{line:n,column:i}}positionBy(e){let t=this.source.start;if(e.index)t=this.p
│`.charCodeAt(0),Nr=" ".charCodeAt(0),ji="\f".charCodeAt(0),Vi="	".charCodeAt(0),Ui="\r".charCodeAt(
│`,"	"];return Br.split(r,e)},comma(r){return Br.split(r,[","],!0)}};Ec.exports=Br;Br.default=Br});v
│`);i=new Array(s.length);let a=0;for(let o=0,u=s.length;o<u;o++)i[o]=a,a+=s[o].length+1;this[ma]=i}
│https://evilmartians.com/chronicles/postcss-8-plugin-migration`),m.env.LANG&&m.env.LANG.startsWith(
│https://www.w3ctech.com/topic/2226`));let o=t(...a);return o.postcssPlugin=e,o.postcssVersion=new b
│`).slice(1,-1).map(q=>q.trim()).map(q=>`      ${q}`).join(`
│`)).join(`
│
│`);x.push(`  Use \`${r.replace("[",`[${D}:`)}\` for \`${M.trim()}\``);break}N.warn([`The class \`${
⋮

frontend\static\web-components.min.js:
⋮
│(()=>{var e,t,n={7560:(e,t,n)=>{"use strict";function r(){return r=Object.assign||function(e){for(v
⋮

integration_tests\ai_agent_tests\providers.py:
⋮
│def make_provider_input_transform(kind: str, model: str, resource_path: str) -> dict[str, Any]:
⋮

python-client\docs\search.js:
⋮
│/** elasticlunr - http://weixsong.github.io * Copyright (C) 2017 Oliver Nightingale * Copyright (C)
⋮

python-client\wmill\wmill\client.py:
⋮
│class SqlQuery:
│    """Query result handler for DataTable and DuckLake queries."""
│
⋮
│    def fetch_one(self):
⋮
│    def execute(self):
⋮
│class _RecordingSqlQuery:
│    """Wraps a ducklake materialize query so that, on a successful run, the
│    trailing summary (row count + snapshot id) is captured and the
│    materialized_partition state is recorded (best-effort). Only used in pipeline
│    context — outside it the helpers return a plain SqlQuery. Mirrors SqlQuery's
⋮
│    def execute(self):
⋮
│    def fetch_one(self):
⋮

python-client\wmill\wmill\s3_types.py:
⋮
│class S3Object(dict):
⋮

typescript-client\docs\assets\main.js:
⋮
│"use strict";(()=>{var Ce=Object.create;var ie=Object.defineProperty;var Oe=Object.getOwnPropertyDe
│`,e)},t.Pipeline.load=function(e){var n=new t.Pipeline;return e.forEach(function(r){var i=t.Pipelin
⋮

typescript-client\s3Types.d.ts:
│export type S3Object = S3ObjectURI | S3ObjectRecord;
│
⋮

typescript-client\s3Types.ts:
⋮
│export type S3Object = S3ObjectURI | S3ObjectRecord;
│
⋮

typescript-client\sqlUtils.d.ts:
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

typescript-client\sqlUtils.ts:
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

typescript-client\tests\sqlUtils.test.ts:
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

wm-ts-nav\src\main.rs:
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