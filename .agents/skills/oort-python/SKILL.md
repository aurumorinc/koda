---
name: oort-python
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging oort-python. Use this skill whenever modifying oort-python configurations or adding related functionality.
---
# oort-python

## File Tree

```text
oort-python/
├── assets
├── modules
│   └── oort-python (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/oort-python`

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

.agents/skills/koda/SKILL.md

.agents/skills/mox/SKILL.md

.agents/skills/sift/SKILL.md

.agents/skills/worldline-python/SKILL.md

.github/pull_request_template.md

.github/workflows/release.yaml

.rune/config

.rune/index

.runemodules

AGENTS.md

CHANGELOG.md

LICENSE

README.md

pdm.lock

pyproject.toml

references/koda/tests/utils/test_file.py:
⋮
│@pytest.fixture
│def mock_s3_upload():
⋮
│@pytest.fixture
│def mock_s3_presigned():
⋮
│@pytest.fixture
│def mock_settings():
⋮
│class TestFile:
│    
│    def test_from_bytes(self):
│        data = b"test bytes"
│        with File.from_bytes(data, "test.txt", "text/plain") as f:
│            assert os.path.exists(f.path)
│            assert f.filename == "test.txt"
│            assert f.mimetype == "text/plain"
│            assert f.bytes == data
│        
│        assert not os.path.exists(f.path)
⋮
│    def test_from_base64(self):
⋮
│    def test_from_path(self):
⋮
│    @patch("requests.get")
│    def test_from_url(self, mock_get):
⋮
│    @pytest.mark.asyncio
│    async def test_from_playwright_download(self):
│        mock_download = MagicMock()
⋮
│        async def mock_save_as(path):
⋮
│    def test_to_playwright_input(self):
⋮
│    def test_presigned_url(self, mock_s3_upload, mock_s3_presigned, mock_settings):
⋮

references/koda/tests/utils/webhook/test_service.py:
⋮
│@pytest.fixture
│def webhook():
⋮
│@pytest.mark.asyncio
│async def test_dispatch_webhook_success(webhook):
⋮
│@pytest.mark.asyncio
│async def test_dispatch_webhook_no_webhook():
⋮
│@pytest.mark.asyncio
│async def test_dispatch_webhook_event_not_in_list(webhook):
⋮
│@pytest.mark.asyncio
│async def test_dispatch_webhook_http_error(webhook, caplog):
⋮
│class MockRequest(BaseModel):
⋮
│class MockResponse(BaseModel):
⋮
│@webhook_dispatch
│async def dummy_success_func(request, webhook=None):
⋮
│@webhook_dispatch
│async def dummy_failure_func(request, webhook=None):
⋮
│@webhook_dispatch
│async def dummy_exception_func(request, webhook=None):
⋮
│@pytest.mark.asyncio
│async def test_webhook_dispatch_success(webhook):
⋮
│@pytest.mark.asyncio
│async def test_webhook_dispatch_handled_failure(webhook):
⋮
│@pytest.mark.asyncio
│async def test_webhook_dispatch_unhandled_exception(webhook):
⋮
│@pytest.mark.asyncio
│async def test_webhook_dispatch_no_webhook():
⋮
│def test_serialize_files():
⋮

references/koda/utils/__init__.py:
⋮
│def images_are_identical(img1: Image.Image, img2: Image.Image) -> bool:
⋮
│def sanitize_filename(url: str) -> str:
⋮

references/koda/utils/file/__init__.py

references/koda/utils/file/main.py:
⋮
│class File:
│    """
│    A wrapper around a local temporary file, with a mandatory filename and mimetype.
│    Supports lazy uploading to S3 to generate a presigned URL.
│    """
│    def __init__(self, path: str, filename: str, mimetype: str, url: Optional[str] = None):
⋮
│    def __enter__(self) -> "File":
⋮
│    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
⋮
│    def cleanup(self) -> None:
⋮
│    @property
│    def bytes(self) -> bytes:
⋮
│    @property
│    def base64(self) -> str:
⋮
│    @property
│    def presigned_url(self) -> Optional[str]:
⋮
│    def to_playwright_input(self) -> dict:
⋮
│    @classmethod
│    def _get_temp_path(cls, filename: str) -> str:
⋮
│    @classmethod
│    def create_empty(cls, filename: str, mimetype: Optional[str] = None, touch: bool = False) -> "F
⋮
│    @classmethod
│    def from_bytes(cls, data: bytes, filename: str, mimetype: Optional[str] = None) -> "File":
⋮
│    @classmethod
│    def from_base64(cls, base64_string: str, filename: str, mimetype: Optional[str] = None) -> "Fil
⋮
│    @classmethod
│    def from_url(cls, url: str, filename: Optional[str] = None, mimetype: Optional[str] = None) -> 
⋮
│    @classmethod
│    def from_path(cls, source_path: str, filename: Optional[str] = None) -> "File":
⋮
│    @classmethod
│    async def from_playwright_download(cls, download: any, filename: Optional[str] = None) -> "File
⋮

references/koda/utils/file/service.py:
⋮
│def upload(data: Union[bytes, str], object_name: str, mimetype: str) -> None:
⋮
│def generate_presigned_url(object_name: str, expires_in: int = 3600) -> str:
⋮
│def _get_client():
⋮

references/koda/utils/webhook/__init__.py

references/koda/utils/webhook/schema.py:
⋮
│class WebhookEvent(str, Enum):
⋮
│class Webhook(BaseModel):
⋮

references/koda/utils/webhook/service.py:
⋮
│def _serialize_files(obj: Any) -> Any:
⋮
│async def dispatch_webhook(
│    webhook: Optional[Webhook], event: WebhookEvent, payload: Dict[str, Any]
│) -> None:
│    """Trigger an HTTP callback based on the webhook spec asynchronously."""
⋮
│    async def _send() -> None:
⋮
│def webhook_dispatch(func: Callable[..., Any]) -> Callable[..., Any]:
│    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""
│    @functools.wraps(func)
│    async def wrapper(*args: Any, **kwargs: Any) -> Any:
⋮

references/mox/utils/__init__.py

references/mox/utils/s3.py:
⋮
│class S3Config(BaseModel):
⋮
│def upload_and_presign(file_path: str, object_name: str, mimetype: str, s3_config: Dict[str, Any]) 
⋮

references/mox/utils/webhook.py:
⋮
│class WebhookSuccessPayload(BaseModel):
⋮
│class WebhookErrorPayload(BaseModel):
⋮
│def _send_webhook(url: str, payload: dict) -> None:
⋮
│def webhook_response(func: Callable) -> Callable:
│    """
│    Decorator that intercepts the return value or exception of a function
│    and sends it to a webhook URL if `callback_url` is present in the first argument.
│    """
│    @wraps(func)
│    def wrapper(request, *args, **kwargs):
⋮

references/sift/tests/utils/webhook/__init__.py

references/sift/tests/utils/webhook/test_service.py:
⋮
│@pytest.fixture
│def webhook():
⋮
│def test_dispatch_webhook_success(webhook):
⋮
│def test_dispatch_webhook_no_webhook():
⋮
│def test_dispatch_webhook_http_error(webhook, caplog):
⋮
│class MockResponse:
│    def __init__(self, success=True, data="resp_data"):
│        self.success = success
⋮
│    def model_dump(self):
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_success_func(data: str, webhook: Optional[dict] = None):
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_failure_func(data: str, webhook: Optional[dict] = None):
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_exception_func(data: str, webhook: Optional[dict] = None):
⋮
│@patch("uuid.uuid4")
│@patch("os.getenv")
│def test_webhook_dispatch_success(mock_getenv, mock_uuid4, webhook):
⋮
│@patch("uuid.uuid4")
│@patch("os.getenv")
│def test_webhook_dispatch_handled_failure(mock_getenv, mock_uuid4, webhook):
⋮
│@patch("uuid.uuid4")
│@patch("os.getenv")
│def test_webhook_dispatch_unhandled_exception(mock_getenv, mock_uuid4, webhook):
⋮
│def test_webhook_dispatch_no_webhook():
⋮
│def test_webhook_dispatch_webhook_object(webhook):
⋮
│class MockResponseWithOutput:
│    def __init__(self, success=True, output=[{"result": "ok"}]):
│        self.success = success
⋮
│@webhook_dispatch(event_prefix="test")
│def dummy_output_func(data: str, webhook: Optional[dict] = None):
⋮
│def test_webhook_dispatch_with_output(webhook):
⋮

references/sift/utils/__init__.py

references/sift/utils/webhook/__init__.py

references/sift/utils/webhook/schema.py:
⋮
│class WebhookEvent(str, Enum):
⋮
│class WebhookRequest(BaseModel):
⋮
│class WebhookResponse(BaseModel):
⋮

references/sift/utils/webhook/service.py:
⋮
│def dispatch_webhook(
│    webhook: Optional[WebhookRequest], payload: WebhookResponse
⋮
│def webhook_dispatch(event_prefix: str = "") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
│    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""
│
│    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
│        @functools.wraps(func)
│        def wrapper(*args: Any, **kwargs: Any) -> Any:
│            sig = inspect.signature(func)
│            bound_args = sig.bind(*args, **kwargs)
│            bound_args.apply_defaults()
│            
│            webhook_data = bound_args.arguments.get("webhook")
│            webhook = None
│            if isinstance(webhook_data, dict):
│                webhook = WebhookRequest(**webhook_data)
⋮

src/oort/__init__.py

src/oort/config.py:
⋮
│class OortSettings(WorldlineSettings, BaseSettings):
│    """
│    Configuration for the oort package.
│    Inherits from worldline.config.WorldlineSettings and pydantic_settings.BaseSettings
│    as per the architectural blueprint.
⋮
│    @property
│    def s3(self) -> Optional[S3Config]:
⋮

src/oort/exceptions.py:
⋮
│class Error(Exception):
⋮
│class S3ConfigurationError(Error):
⋮
│class WebhookDispatchError(Error):
⋮

src/oort/file/__init__.py

src/oort/file/main.py:
⋮
│class File:
│    """
│    A wrapper around a local temporary file, with a mandatory filename and mimetype.
│    Supports lazy uploading to S3 to generate a presigned URL.
⋮
│    def __init__(
│        self, path: str, filename: str, mimetype: str, url: Optional[str] = None
⋮
│    def __enter__(self) -> "File":
⋮
│    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
⋮
│    def cleanup(self) -> None:
⋮
│    @property
│    def bytes(self) -> bytes:
⋮
│    @property
│    def base64(self) -> str:
⋮
│    @property
│    def presigned_url(self) -> Union[Optional[str], Awaitable[Optional[str]]]:
⋮
│    def _get_presigned_url(self) -> Optional[str]:
⋮
│    async def _aget_presigned_url(self) -> Optional[str]:
⋮
│    def to_playwright_input(self) -> dict[str, Any]:
⋮
│    @classmethod
│    def _get_temp_path(cls, filename: str) -> str:
⋮
│    @classmethod
│    def create_empty(
│        cls, filename: str, mimetype: Optional[str] = None, touch: bool = False
⋮
│    @classmethod
│    def from_bytes(
│        cls,
│        data: Union[builtins.bytes, str],
│        filename: str,
│        mimetype: Optional[str] = None,
⋮
│    @classmethod
│    def from_base64(
│        cls,
│        base64_string: Union[str, builtins.bytes],
│        filename: str,
│        mimetype: Optional[str] = None,
⋮
│    @classmethod
│    def from_url(
│        cls, url: str, filename: Optional[str] = None, mimetype: Optional[str] = None
⋮
│    @classmethod
│    def from_path(cls, source_path: str, filename: Optional[str] = None) -> "File":
⋮
│    @classmethod
│    def from_playwright_download(
│        cls, download: Any, filename: Optional[str] = None
⋮
│    @classmethod
│    def _from_playwright_download(
│        cls, download: Any, filename: Optional[str] = None
⋮
│    @classmethod
│    async def _afrom_playwright_download(
│        cls, download: Any, filename: Optional[str] = None
⋮

src/oort/file/schema.py:
⋮
│class S3Config(BaseModel):
⋮

src/oort/file/service.py:
⋮
│def _get_client(config: S3Config) -> Any:
⋮
│def _upload(
│    data: Union[bytes, str], object_name: str, mimetype: str, config: S3Config
⋮
│def _generate_presigned_url(
│    object_name: str, config: S3Config, expires_in: Optional[int] = None
⋮
│async def _aupload(
│    data: Union[bytes, str], object_name: str, mimetype: str, config: S3Config
⋮
│async def _agenerate_presigned_url(
│    object_name: str, config: S3Config, expires_in: Optional[int] = None
⋮
│def upload(
│    data: Union[bytes, str], object_name: str, mimetype: str, config: S3Config
⋮
│def generate_presigned_url(
│    object_name: str, config: S3Config, expires_in: Optional[int] = None
⋮

src/oort/utils.py:
⋮
│def is_async_context() -> bool:
⋮

src/oort/webhook/__init__.py

src/oort/webhook/schema.py:
⋮
│class WebhookEvent(str, Enum):
⋮
│class WebhookRequest(BaseModel):
⋮
│class WebhookResponse(BaseModel):
⋮

src/oort/webhook/service.py:
⋮
│def _extract_webhook_and_bind_args(
│    sig: inspect.Signature, args: tuple, kwargs: dict
⋮
│def _create_payload(
│    event: WebhookEvent,
│    event_prefix: str,
│    task_id: str,
│    webhook: WebhookRequest,
│    success: bool = True,
│    data: Any = None,
│    error: Optional[str] = None,
⋮
│def _extract_response_data(response: Any) -> Any:
⋮
│def _serialize_files(obj: Any) -> Any:
⋮
│async def _aserialize_files(obj: Any) -> Any:
⋮
│def _extract_webhook_and_bind_args(
│    sig: inspect.Signature, args: tuple, kwargs: dict
⋮
│def _create_payload(
│    event: WebhookEvent,
│    event_prefix: str,
│    task_id: str,
│    webhook: WebhookRequest,
│    success: bool = True,
│    data: Any = None,
│    error: Optional[str] = None,
⋮
│def _extract_response_data(response: Any) -> Any:
⋮
│async def adispatch_webhook(
│    webhook: Optional[WebhookRequest], payload: WebhookResponse
⋮
│def dispatch_webhook(
│    webhook: Optional[WebhookRequest], payload: WebhookResponse
⋮
│def webhook_dispatch(
│    event_prefix: str = "",
│) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
│    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED). Routes automatica
│
│    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
│        sig = inspect.signature(func)
⋮
│        if is_async:
│
│            @functools.wraps(func)
│            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
│                _, webhook = _extract_webhook_and_bind_args(sig, args, kwargs)
│                task_id = uuid.uuid4().hex
│
│                if webhook and (
│                    not webhook.events or WebhookEvent.STARTED in webhook.events
│                ):
│                    payload = _create_payload(
│                        WebhookEvent.STARTED, event_prefix, task_id, webhook
⋮
│        else:
│
│            @functools.wraps(func)
│            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
│                _, webhook = _extract_webhook_and_bind_args(sig, args, kwargs)
│                task_id = uuid.uuid4().hex
│
│                if webhook and (
│                    not webhook.events or WebhookEvent.STARTED in webhook.events
│                ):
│                    payload = _create_payload(
│                        WebhookEvent.STARTED, event_prefix, task_id, webhook
⋮

tests/__init__.py

tests/conftest.py:
⋮
│@pytest.fixture(autouse=True)
│def setup_oort_config():
⋮

tests/integration/__init__.py

tests/integration/external/file/cassettes/test_external_s3_upload_async.yaml

tests/integration/external/file/cassettes/test_external_s3_upload_sync.yaml

tests/integration/external/file/test_service.py:
⋮
│@pytest.fixture
│def external_s3_config():
⋮
│@my_vcr.use_cassette("test_external_s3_upload_sync.yaml")
│def test_external_s3_upload_and_presign_sync(external_s3_config):
⋮
│@pytest.mark.asyncio
│@my_vcr.use_cassette("test_external_s3_upload_async.yaml")
│async def test_external_s3_upload_and_presign_async(external_s3_config):
⋮

tests/integration/internal/__init__.py

tests/integration/internal/file/__init__.py

tests/integration/internal/file/test_service.py:
⋮
│@pytest.fixture(autouse=True)
│def setup_moto():
⋮
│def test_file_integration_sync():
⋮
│@pytest.mark.asyncio
│async def test_file_integration_async():
⋮

tests/integration/internal/webhook/__init__.py

tests/integration/internal/webhook/test_service.py:
⋮
│@pytest.fixture
│def webhook():
⋮
│@respx.mock
│@pytest.mark.asyncio
│async def test_webhook_integration_async(webhook):
│    request_mock = respx.post("https://example.com/webhook").mock(
│        return_value=httpx.Response(200)
⋮
│    class AsyncDummyFile:
│        def __init__(
│            self,
│            filename="test.png",
│            mimetype="image/png",
│            presigned_url="https://s3/test.png",
⋮
│        @property
│        async def presigned_url(self):
⋮
│    @webhook_dispatch(event_prefix="test")
│    async def process_data(data: str, webhook: WebhookRequest = None):
⋮
│@respx.mock
│def test_webhook_integration_sync(webhook):
│    request_mock = respx.post("https://example.com/webhook").mock(
│        return_value=httpx.Response(200)
⋮
│    @webhook_dispatch(event_prefix="test")
│    def process_data_sync(data: str, webhook: WebhookRequest = None):
⋮

tests/unit/__init__.py

tests/unit/file/__init__.py

tests/unit/file/test_main.py:
⋮
│def test_file_create_empty():
⋮
│def test_file_from_bytes():
⋮
│@patch("oort.file.main._upload")
│@patch("oort.file.main._generate_presigned_url")
│def test_file_presigned_url_sync(mock_gen, mock_upload):
⋮
│@patch("oort.file.main._aupload")
⋮
│async def test_file_presigned_url_async(mock_gen, mock_upload):
⋮
│@pytest.mark.asyncio
│async def test_file_from_playwright_download_async():
│    class MockDownload:
│        def __init__(self):
│            self.suggested_filename = "downloaded.txt"
│
│        async def save_as(self, path):
│            with open(path, "w") as f:
⋮

tests/unit/file/test_service.py:
⋮
│@pytest.fixture
│def s3_config():
⋮
│@patch("oort.file.service._s3_client", None)
│@patch("oort.file.service.boto3.Session", spec=True)
│def test_upload_bytes_sync(mock_session_cls, s3_config):
⋮
│@patch("oort.file.service._s3_client", None)
⋮
│async def test_upload_bytes_async(mock_session_cls, s3_config):
⋮
│@patch("oort.file.service._s3_client", None)
│@patch("oort.file.service.boto3.Session", spec=True)
│def test_upload_file_path_sync(mock_session_cls, s3_config):
⋮
│@patch("oort.file.service._s3_client", None)
⋮
│async def test_upload_file_path_async(mock_session_cls, s3_config):
⋮
│@patch("oort.file.service._s3_client", None)
│@patch("oort.file.service.boto3.Session", spec=True)
│def test_generate_presigned_url_sync(mock_session_cls, s3_config):
⋮
│@patch("oort.file.service._s3_client", None)
⋮
│async def test_generate_presigned_url_async(mock_session_cls, s3_config):
⋮

tests/unit/test_config.py:
⋮
│@patch.dict(os.environ, {}, clear=True)
│def test_oort_settings_s3_property_valid():
⋮
│@patch.dict(os.environ, {}, clear=True)
│def test_oort_settings_s3_property_missing_bucket():
⋮
│@patch.dict(os.environ, {}, clear=True)
│def test_oort_settings_s3_property_missing_access_key():
⋮
│@patch.dict(os.environ, {}, clear=True)
│def test_oort_settings_s3_property_missing_secret_key():
⋮
│@patch.dict(os.environ, {}, clear=True)
│def test_oort_settings_s3_property_all_missing():
⋮

tests/unit/test_utils.py:
⋮
│def test_is_async_context_sync():
⋮
│@pytest.mark.asyncio
│async def test_is_async_context_async():
⋮

tests/unit/webhook/__init__.py

tests/unit/webhook/test_service.py:
⋮
│@pytest.fixture
│def webhook():
⋮
│class MockResponseModel(BaseModel):
⋮
│@patch("oort.webhook.service.httpx.Client", spec=True)
│def test_dispatch_webhook_sync(mock_client_cls, webhook):
⋮
│@patch("oort.webhook.service.httpx.AsyncClient", spec=True)
│@pytest.mark.asyncio
│async def test_dispatch_webhook_async(mock_client_cls, webhook):
⋮
│@patch("oort.webhook.service.adispatch_webhook")
│@pytest.mark.asyncio
│async def test_webhook_dispatch_async_decorator(mock_dispatch, webhook):
│    @webhook_dispatch(event_prefix="test")
│    async def dummy_async_func(data: str, webhook: WebhookRequest = None):
⋮
│@patch("oort.webhook.service.dispatch_webhook")
│def test_webhook_dispatch_sync_decorator(mock_dispatch, webhook):
│    @webhook_dispatch(event_prefix="test")
│    def dummy_sync_func(data: str, webhook: WebhookRequest = None):
⋮
│def test_serialize_files():
│    class DummyFile:
│        def __init__(self, filename, mimetype, presigned_url):
│            self.filename = filename
│            self.mimetype = mimetype
⋮
│class AsyncDummyFile:
│    def __init__(
│        self,
│        filename="test.png",
│        mimetype="image/png",
│        presigned_url="https://s3/test.png",
│        delay=0.0,
⋮
│    @property
│    async def presigned_url(self):
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_single():
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_list():
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_dict():
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_mixed_and_nested():
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_missing_attributes():
│    class IncompleteFile:
│        @property
│        async def presigned_url(self):
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_upload_failure():
⋮
│@pytest.mark.asyncio
│async def test_aserialize_files_concurrency_timing():
⋮
```
