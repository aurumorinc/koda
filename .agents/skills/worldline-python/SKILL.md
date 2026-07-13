---
name: worldline-python
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging worldline-python. Use this skill whenever modifying worldline-python configurations or adding related functionality.
---
# worldline-python

## File Tree

```text
worldline-python/
├── assets
├── modules
│   └── worldline-python (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/worldline-python`

```python
.agents/rules/architecture-application.md

.agents/rules/architecture-business.md

.agents/rules/architecture-data.md

.agents/rules/architecture-integration.md

.agents/rules/architecture-technology.md

.agents/rules/language-python/anti-patterns.md

.agents/rules/language-python/architecture-and-structure.md

.agents/rules/language-python/code-style-and-formatting.md

.agents/rules/language-python/configuration-and-environment.md

.agents/rules/language-python/dependency-management.md

.agents/rules/language-python/documentation-and-comments.md

.agents/rules/language-python/error-handling.md

.agents/rules/language-python/logging-and-observability.md

.agents/rules/language-python/naming-conventions.md

.agents/rules/language-python/performance-and-optimization.md

.agents/rules/language-python/security-and-validation.md

.agents/rules/language-python/testing-standards.md

.agents/rules/language-python/type-safety.md

.agents/skills/langfuse-python/SKILL.md

.agents/skills/posthog/SKILL.md

.agents/skills/sentry/SKILL.md

.agents/skills/structlog/SKILL.md

.agents/skills/windmill/SKILL.md

.github/pull_request_template.md

.github/workflows/release.yaml

.rune/config

.rune/index

.runemodules

AGENTS.md

CHANGELOG.md

LICENSE

README.md

docs/configuration.md

docs/usage.md

pdm.lock

pyproject.toml

src/worldline/__init__.py

src/worldline/config.py:
⋮
│def generate_traceparent() -> str:
⋮
│def resolve_traceparent() -> str:
⋮
│class WorldlineSettings(BaseSettings):
│    """Configuration for the lume package."""
│
⋮
│    @computed_field  # type: ignore
│    @property
│    def is_windmill_env(self) -> bool:
⋮
│    @computed_field  # type: ignore
│    @property
│    def trace_id(self) -> str:
⋮
│    @computed_field  # type: ignore
│    @property
│    def span_id(self) -> str:
⋮
│    def model_post_init(self, __context: Any) -> None:
⋮

src/worldline/integrations/__init__.py

src/worldline/integrations/structlog.py:
⋮
│def setup_structlog(settings: Optional["WorldlineSettings"] = None) -> None:
⋮

src/worldline/integrations/windmill.py:
⋮
│def get_windmill_traceparent() -> Optional[str]:
⋮

src/worldline/service.py:
⋮
│def setup(settings_override: Optional[Any] = None) -> None:
⋮
│def remove_otel_context(
│    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
⋮
│def get_console_format() -> Tuple[List[Any], List[logging.Handler]]:
⋮
│def add_otel_context(
│    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
⋮
│def setup_otel_provider(
│    settings_override: Optional[Any] = None,
⋮

tests/conftest.py:
⋮
│@pytest.fixture(autouse=True)
│def clean_structlog():
⋮
│@pytest.fixture(autouse=True)
│def env_reset():
⋮
│@pytest.fixture
│def in_memory_otel_exporters():
⋮

tests/integration/internal/worldline/test_service_integration.py:
⋮
│@pytest.fixture(autouse=True)
│def reset_state():
⋮
│def test_standard_logging_capture():
⋮
│def test_setup_configures_otel(in_memory_otel_exporters):
⋮

tests/performance/test_logging_concurrency.py:
⋮
│def test_thread_safe_contextvars():
│    """
│    Test that bound contextvars in structlog do not bleed across threads
│    under concurrent load.
⋮
│    with mock.patch("sys.stdout", out):
│        setup(settings)
⋮
│        def worker(thread_idx: int):
⋮

tests/property/test_logging_properties.py:
⋮
│@given(
│    st.dictionaries(
│        st.text(), st.text() | st.integers() | st.none() | st.floats(allow_nan=False)
│    )
│)
│def test_remove_otel_context_never_crashes(event_dict):
⋮
│@mock.patch("worldline.service.settings")
⋮
│def test_add_otel_context_never_crashes(mock_settings, event_dict):
⋮

tests/unit/worldline/integrations/test_structlog.py:
⋮
│@pytest.fixture(autouse=True)
│def reset_structlog_state():
⋮
│@mock.patch("structlog.configure", spec=True)
│@mock.patch("worldline.service.setup_otel_provider", spec=True)
│def test_setup_structlog(mock_setup_otel, mock_configure):
⋮
│@mock.patch("worldline.service.setup_otel_provider", spec=True)
│def test_setup_structlog_with_otel(mock_setup_otel):
⋮

tests/unit/worldline/integrations/test_windmill.py:
⋮
│@mock.patch.dict(
│    os.environ,
│    {"WM_TRACEPARENT": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"},
│    clear=True,
│)
│def test_get_windmill_traceparent_valid():
⋮
│@mock.patch.dict(os.environ, {}, clear=True)
│def test_get_windmill_traceparent_missing():
⋮

tests/unit/worldline/test_config.py:
⋮
│def test_default_settings():
⋮
│@mock.patch.dict(
│    os.environ,
│    {
│        "LOG_LEVEL": "DEBUG",
│        "STDOUT_FORMAT": "rich",
│        "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
│        "TRACEPARENT": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
│    },
│    clear=True,
│)
│def test_settings_from_env():
⋮
│@mock.patch.dict(
│    os.environ,
│    {
│        "WM_TRACEPARENT": "00-windmilltraceid1234567890123456-windmillspanid12-01",
│    },
│    clear=True,
│)
│def test_settings_from_windmill_env():
⋮
│@mock.patch.dict(
│    os.environ,
│    {
│        "TRACEPARENT": "00-envtraceid1234567890123456789012-envspanid1234567-01",
│        "WM_TRACEPARENT": "00-windmilltraceid1234567890123456-windmillspanid12-01",
│    },
│    clear=True,
│)
│def test_settings_precedence_env_over_windmill():
⋮
│def test_is_windmill_env():
⋮
│def test_vendor_defaults():
⋮
│@mock.patch.dict(os.environ, {}, clear=True)
│def test_worldline_settings_populates_environ():
⋮
│@mock.patch.dict(os.environ, {}, clear=True)
│def test_worldline_settings_populates_environ_with_langfuse_host():
⋮
│def test_generate_traceparent():
⋮
│def test_malformed_traceparent_fails():
⋮

tests/unit/worldline/test_init.py:
⋮
│@pytest.fixture(autouse=True)
│def reset_worldline_init_state():
⋮
│@mock.patch.dict(os.environ, {"WORLDLINE_DISABLE_AUTO_INSTRUMENTATION": "true"})
│@mock.patch("worldline.service.setup")
│def test_init_disabled_via_env(mock_setup):
⋮
│@mock.patch.dict(os.environ, {"WORLDLINE_DISABLE_AUTO_INSTRUMENTATION": "false"})
│@mock.patch("worldline.service.setup")
│def test_init_executes_setup(mock_setup):
⋮
│@mock.patch.dict(os.environ, {"WORLDLINE_DISABLE_AUTO_INSTRUMENTATION": "false"})
│@mock.patch("worldline.service.setup")
│def test_init_catches_setup_exceptions(mock_setup):
⋮
│@mock.patch("worldline.service.setup")
│def test_init_idempotency(mock_setup):
⋮

tests/unit/worldline/test_service.py:
⋮
│def test_add_otel_context_with_active_span():
⋮
│@mock.patch("worldline.service.settings")
│def test_add_otel_context_fallback_to_settings(mock_settings):
⋮
│@mock.patch("worldline.service.settings")
│def test_add_otel_context_empty_event_dict(mock_settings):
⋮
│@mock.patch("worldline.service.settings")
│def test_setup_otel_provider_no_endpoint(mock_settings):
⋮
│@mock.patch("worldline.service.settings")
│def test_setup_otel_provider_with_endpoint(mock_settings):
⋮
│def test_remove_otel_context():
⋮
│def test_remove_otel_context_missing_keys():
⋮
│def test_get_console_format():
⋮
│@mock.patch.dict("os.environ", {}, clear=True)
⋮
│def test_setup_orchestration(
│    mock_sentry_init,
│    mock_posthog_host,
│    mock_posthog_api_key,
│    mock_langfuse,
│    mock_setup_structlog,
⋮
│@mock.patch("worldline.integrations.structlog.setup_structlog")
│def test_setup_idempotency(mock_setup_structlog):
⋮

worldline.pth
```
