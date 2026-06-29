---
name: crawlee
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging crawlee. Use this skill whenever modifying crawlee configurations or adding related functionality.
---
# crawlee

## File Tree

```text
crawlee/
├── assets
├── modules
│   └── crawlee-python (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/crawlee-python`

```python
docs\guides\code_examples\http_crawlers\selectolax_context.py:
⋮
│@dataclass(frozen=True)
│class SelectolaxLexborContext(ParsedHttpCrawlingContext[LexborHTMLParser]):
│    """Crawling context providing access to the parsed page.
│
│    This context is passed to request handlers and includes all standard
│    context methods (push_data, enqueue_links, etc.) plus custom helpers.
⋮
│    @property
│    def parser(self) -> LexborHTMLParser:
⋮
│    @classmethod
│    def from_parsed_http_crawling_context(
│        cls, context: ParsedHttpCrawlingContext[LexborHTMLParser]
⋮

src\crawlee\_autoscaling\_types.py:
⋮
│@dataclass
│class LoadRatioInfo:
⋮

src\crawlee\_autoscaling\autoscaled_pool.py:
⋮
│@docs_group('Autoscaling')
│class AutoscaledPool:
│    """Manages a pool of asynchronous resource-intensive tasks that are executed in parallel.
│
│    The pool only starts new tasks if there is enough free CPU and memory available. If an exceptio
│    any of the tasks, it is propagated and the pool is stopped.
⋮
│    async def run(self) -> None:
⋮

src\crawlee\_autoscaling\snapshotter.py:
⋮
│@docs_group('Autoscaling')
│class Snapshotter:
│    """Monitors and logs system resource usage at predefined intervals for performance optimization
│
│    The class monitors and records the state of various system resources (CPU, memory, event loop, 
│    at predefined intervals. This continuous monitoring helps in identifying resource overloads and
│    performance of the application. It is utilized in the `AutoscaledPool` module to adjust task al
│    dynamically based on the current demand and system load.
⋮
│    @classmethod
│    def from_config(cls, config: Configuration | None = None) -> Snapshotter:
⋮

src\crawlee\_request.py:
⋮
│class CrawleeRequestData(BaseModel):
⋮
│@docs_group('Storage data')
│class Request(BaseModel):
│    """Represents a request in the Crawlee framework, containing the necessary information for craw
│
│    The `Request` class is one of the core components in Crawlee, utilized by various components su
│    providers, HTTP clients, crawlers, and more. It encapsulates the essential data for executing w
│    including the URL, HTTP method, headers, payload, and user data. The user data allows custom in
│    to be stored and persisted throughout the request lifecycle, including its retries.
│
│    Key functionalities include managing the request's identifier (`id`), unique key (`unique_key`)
│    for request deduplication, controlling retries, handling state management, and enabling configu
│    rotation and proxy handling.
│
⋮
│    @classmethod
│    def from_url(
│        cls,
│        url: str,
│        *,
│        method: HttpMethod = 'GET',
│        headers: HttpHeaders | dict[str, str] | None = None,
│        payload: HttpPayload | str | None = None,
│        label: str | None = None,
│        session_id: str | None = None,
│        unique_key: str | None = None,
⋮

src\crawlee\_service_locator.py:
⋮
│@docs_group('Configuration')
│class ServiceLocator:
│    """Service locator for managing the services used by Crawlee.
│
│    All services are initialized to its default value lazily.
⋮
│    def get_configuration(self) -> Configuration:
⋮
│    def get_event_manager(self) -> EventManager:
⋮
│    def get_storage_client(self) -> StorageClient:
⋮

src\crawlee\_types.py:
⋮
│@docs_group('Other')
│class HttpHeaders(RootModel, Mapping[str, str]):
⋮
│@docs_group('Configuration')
│class ConcurrencySettings:
⋮
│class AddRequestsKwargs(EnqueueLinksKwargs):
⋮
│class PushDataFunctionCall(PushDataKwargs):
⋮
│@dataclass()
│class KeyValueStoreValue:
⋮
│class KeyValueStoreChangeRecords:
⋮
│@docs_group('Other')
│@dataclasses.dataclass
│class PageSnapshot:
⋮

src\crawlee\_utils\byte_size.py:
⋮
│@dataclass(frozen=True)
│class ByteSize:
⋮

src\crawlee\_utils\crypto.py:
⋮
│def crypto_random_object_id(length: int = 17) -> str:
⋮

src\crawlee\_utils\docs.py:
⋮
│def docs_group(group_name: GroupName) -> Callable[[T], T]:  # noqa: ARG001
│    """Mark a symbol for rendering and grouping in documentation.
│
│    This decorator is used solely for documentation purposes and does not modify the behavior
│    of the decorated callable.
│
│    Args:
│        group_name: The documentation group to which the symbol belongs.
│
│    Returns:
│        The original callable without modification.
⋮
│    def wrapper(func: T) -> T:
⋮

src\crawlee\_utils\file.py:
⋮
│@overload
│async def atomic_write(
│    path: Path,
│    data: str,
│    *,
│    retry_count: int = 0,
⋮
│@overload
│async def atomic_write(
│    path: Path,
│    data: bytes,
│    *,
│    retry_count: int = 0,
⋮
│async def atomic_write(
│    path: Path,
│    data: str | bytes,
│    *,
│    retry_count: int = 0,
⋮

src\crawlee\_utils\raise_if_too_many_kwargs.py:
⋮
│def raise_if_too_many_kwargs(max_kwargs: int = 1, **kwargs: Any) -> None:
⋮

src\crawlee\_utils\recoverable_state.py:
⋮
│class RecoverableState(Generic[TStateModel]):
⋮

src\crawlee\_utils\recurring_task.py:
⋮
│class RecurringTask:
│    """Class for creating and managing recurring tasks.
│
│    Attributes:
│        func: The function to be executed repeatedly.
│        delay: The time delay (in seconds) between function calls.
│        task: The underlying task object.
⋮
│    def start(self) -> None:
⋮
│    async def stop(self) -> None:
⋮

src\crawlee\_utils\retry.py:
⋮
│def retry_on_error(
│    *exception_types: type[Exception],
│    max_attempts: int = 3,
│    base_delay: timedelta = timedelta(milliseconds=500),
⋮

src\crawlee\_utils\robots.py:
⋮
│class RobotsTxtFile:
│    def __init__(
│        self,
│        url: str,
│        robots: Protego,
│        http_client: HttpClient | None = None,
│        proxy_info: ProxyInfo | None = None,
⋮
│    def get_sitemaps(self, *, enqueue_strategy: EnqueueStrategy) -> list[str]:
⋮

src\crawlee\_utils\sitemap.py:
⋮
│class SitemapSource(TypedDict):
⋮
│class _XMLSaxSitemapHandler(ContentHandler):
│    def __init__(self) -> None:
│        super().__init__()
│        self._root_tag_name: str | None = None
│        self._current_tag: str | None = None
│        self._current_url: _SitemapItem = {}
│        self._buffer: str = ''
⋮
│    @property
│    def items(self) -> list[_SitemapItem]:
⋮

src\crawlee\_utils\time.py:
⋮
│@dataclass
│class TimerResult:
⋮

src\crawlee\_utils\try_import.py:
⋮
│@dataclass
│class FailedImport:
⋮

src\crawlee\_utils\urls.py:
⋮
│def is_url_absolute(url: str) -> bool:
⋮
│def convert_to_absolute_url(base_url: str, relative_url: str) -> str:
⋮
│def validate_http_url(value: str | None) -> str | None:
⋮
│def filter_url(
│    *,
│    target: str | URL,
│    strategy: EnqueueStrategy,
│    origin: str | URL,
⋮
│@lru_cache(maxsize=2048)
│def _domain_under_public_suffix(host: str) -> str:
⋮

src\crawlee\_utils\wait.py:
⋮
│async def wait_for(
│    operation: Callable[[], Awaitable[T]],
│    *,
│    timeout: timedelta,
│    timeout_message: str | None = None,
│    max_retries: int = 1,
│    logger: Logger,
⋮

src\crawlee\_utils\web.py:
⋮
│def is_status_code_client_error(value: int) -> bool:
⋮
│def is_status_code_server_error(value: int) -> bool:
⋮
│def is_status_code_successful(value: int) -> bool:
⋮

src\crawlee\configuration.py:
⋮
│@docs_group('Configuration')
│class Configuration(BaseSettings):
│    """Configuration settings for the Crawlee project.
│
│    This class stores common configurable parameters for Crawlee. Default values are provided for a
│    so typically, no adjustments are necessary. However, you may modify settings for specific use c
│    such as changing the default storage directory, the default storage IDs, the timeout for intern
│    operations, and more.
│
│    Settings can also be configured via environment variables, prefixed with `CRAWLEE_`.
⋮
│    @classmethod
│    def get_global_configuration(cls) -> Self:
⋮

src\crawlee\crawlers\_adaptive_playwright\_adaptive_playwright_crawling_context.py:
⋮
│class AdaptiveContextError(RuntimeError):
⋮
│@dataclass(frozen=True)
│@docs_group('Crawling contexts')
│class AdaptivePlaywrightCrawlingContext(
│    ParsedHttpCrawlingContext[TStaticParseResult],
│    Generic[TStaticParseResult, TStaticSelectResult],
│):
│    _static_parser: AbstractHttpParser[TStaticParseResult, TStaticSelectResult]
⋮
│    async def wait_for_selector(self, selector: str, timeout: timedelta = timedelta(seconds=5)) -> 
⋮
│    async def query_selector_all(
│        self, selector: str, timeout: timedelta = timedelta(seconds=5)
⋮
│    @classmethod
│    def from_parsed_http_crawling_context(
│        cls,
│        context: ParsedHttpCrawlingContext[TStaticParseResult],
│        parser: AbstractHttpParser[TStaticParseResult, TStaticSelectResult],
⋮

src\crawlee\crawlers\_basic\_basic_crawler.py:
⋮
│@docs_group('Crawlers')
│class BasicCrawler(Generic[TCrawlingContext, TStatisticsState]):
│    """A basic web crawler providing a framework for crawling websites.
│
│    The `BasicCrawler` provides a low-level functionality for crawling websites, allowing users to 
│    own page download and data extraction logic. It is designed mostly to be subclassed by crawlers
│    purposes. In most cases, you will want to use a more specialized crawler, such as `HttpCrawler`
│    `BeautifulSoupCrawler`, `ParselCrawler`, or `PlaywrightCrawler`. If you are an advanced user an
│    control over the crawling process, you can subclass the `BasicCrawler` and implement the reques
│    yourself.
│
│    The crawling process begins with URLs provided by a `RequestProvider` instance. Each request is
⋮
│    def stop(self, reason: str = 'Stop was called externally.') -> None:
⋮
│    async def run(
│        self,
│        requests: Sequence[str | Request] | None = None,
│        *,
│        purge_request_queue: bool = True,
⋮
│    def _create_enqueue_links_function(
│        self, context: BasicCrawlingContext, extract_links: ExtractLinksFunction
│    ) -> EnqueueLinksFunction:
│        """Create a callback function for extracting links from parsed content and enqueuing them t
│
│        Args:
│            context: The current crawling context.
│            extract_links: Function used to extract links from the page.
│
│        Returns:
│            Awaitable that is used for extracting links from parsed content and enqueuing them to t
⋮
│        async def enqueue_links(
│            *,
│            selector: str | None = None,
│            attribute: str | None = None,
│            label: str | None = None,
│            user_data: Mapping[str, JsonSerializable] | None = None,
│            transform_request_function: Callable[[RequestOptions], RequestOptions | RequestTransfor
│            | None = None,
│            requests: Sequence[str | Request] | None = None,
│            rq_id: str | None = None,
⋮

src\crawlee\crawlers\_basic\_logging_utils.py:
⋮
│def reduce_asyncio_timeout_error_to_relevant_traceback_parts(
│    timeout_error: asyncio.exceptions.TimeoutError | crawlee.errors.UserHandlerTimeoutError,
⋮

src\crawlee\crawlers\_beautifulsoup\_beautifulsoup_crawler.py:
⋮
│@docs_group('Crawlers')
│class BeautifulSoupCrawler(AbstractHttpCrawler[BeautifulSoupCrawlingContext, BeautifulSoup, Tag]):
⋮

src\crawlee\crawlers\_beautifulsoup\_beautifulsoup_crawling_context.py:
⋮
│@dataclass(frozen=True)
│@docs_group('Crawling contexts')
│class BeautifulSoupCrawlingContext(ParsedHttpCrawlingContext[BeautifulSoup]):
│    """The crawling context used by the `BeautifulSoupCrawler`.
│
│    It provides access to key objects as well as utility functions for handling crawling tasks.
⋮
│    @classmethod
│    def from_parsed_http_crawling_context(cls, context: ParsedHttpCrawlingContext[BeautifulSoup]) -
⋮

src\crawlee\crawlers\_beautifulsoup\_utils.py:
⋮
│def html_to_text(source: str | Tag) -> str:
│    """Convert markup string or `BeautifulSoup` to newline separated plain text without tags using 
│
│    Args:
│        source: Input markup string or `BeautifulSoup` object.
│
│    Returns:
│        Newline separated plain text without tags.
⋮
│    def _page_element_to_text(page_elements: Iterable[PageElement]) -> None:
⋮

src\crawlee\crawlers\_http\_http_crawler.py:
⋮
│@docs_group('Crawlers')
│class HttpCrawler(AbstractHttpCrawler[ParsedHttpCrawlingContext[bytes], bytes, bytes]):
⋮

src\crawlee\crawlers\_parsel\_parsel_crawler.py:
⋮
│@docs_group('Crawlers')
│class ParselCrawler(AbstractHttpCrawler[ParselCrawlingContext, Selector, Selector]):
⋮

src\crawlee\crawlers\_parsel\_parsel_crawling_context.py:
⋮
│@dataclass(frozen=True)
│@docs_group('Crawling contexts')
│class ParselCrawlingContext(ParsedHttpCrawlingContext[Selector]):
│    """The crawling context used by the `ParselCrawler`.
│
│    It provides access to key objects as well as utility functions for handling crawling tasks.
⋮
│    @classmethod
│    def from_parsed_http_crawling_context(cls, context: ParsedHttpCrawlingContext[Selector]) -> Sel
⋮
│    def html_to_text(self) -> str:
⋮

src\crawlee\crawlers\_parsel\_utils.py:
⋮
│def html_to_text(source: str | Selector) -> str:
│    """Convert markup string or `Selector` to newline-separated plain text without tags using Parse
│
│    Args:
│        source: Input markup string or `Selector` object.
│
│    Returns:
│        Newline separated plain text without tags.
⋮
│    def _extract_text(elements: list[Selector], *, compress: bool = True) -> None:
⋮

src\crawlee\crawlers\_playwright\_playwright_crawler.py:
⋮
│@docs_group('Crawlers')
│class PlaywrightCrawler(
│    BasicCrawler[TCrawlingContext, StatisticsState],
│    Generic[TPreNavContext, TPostNavContext, TCrawlingContext],
⋮

src\crawlee\crawlers\_playwright\_types.py:
⋮
│@dataclass(frozen=True)
│class PlaywrightHttpResponse:
│    """Wrapper class for playwright `Response` and `APIResponse` objects to implement `HttpResponse
│
⋮
│    @classmethod
│    async def from_playwright_response(cls, response: Response | APIResponse, protocol: str) -> Sel
⋮

src\crawlee\crawlers\_playwright\_utils.py:
⋮
│async def infinite_scroll(page: Page) -> None:
│    """Scroll to the bottom of a page, handling loading of additional items."""
⋮
│    async def check_finished() -> None:
⋮

src\crawlee\crawlers\_types.py:
⋮
│@dataclass(frozen=True)
│class BlockedInfo:
│    """Information about whether the crawling is blocked. If reason is empty, then it means it is n
│
⋮
│    def __bool__(self) -> bool:
⋮

src\crawlee\errors.py:
⋮
│@docs_group('Errors')
│class ServiceConflictError(Exception):
⋮

src\crawlee\events\_local_event_manager.py:
⋮
│@docs_group('Event managers')
│class LocalEventManager(EventManager):
│    """Event manager for local environments.
│
│    It extends the `EventManager` to emit `SystemInfo` events at regular intervals. The `LocalEvent
│    is intended to be used in local environments, where the system metrics are required managing th
│    and `AutoscaledPool`.
⋮
│    @classmethod
│    def from_config(cls, config: Configuration | None = None) -> LocalEventManager:
⋮

src\crawlee\http_clients\_impit.py:
⋮
│@docs_group('HTTP clients')
│class ImpitHttpClient(HttpClient):
⋮

src\crawlee\proxy_configuration.py:
⋮
│@docs_group('Configuration')
│class ProxyConfiguration:
│    """Configures connection to a proxy server with the provided options.
│
│    Proxy servers are used to prevent target websites from blocking your crawlers based on IP addre
│    blacklists. Setting proxy configuration in your crawlers automatically configures them to use t
│    for all connections. You can get information about the currently used proxy by inspecting the {
│    property in your crawler's page function. There, you can inspect the proxy's URL and other attr
│
│    If you want to use your own proxies, use the {@apilink ProxyConfigurationOptions.proxyUrls} opt
│    proxy URLs will be rotated by the configuration if this option is provided.
⋮
│    async def new_proxy_info(
│        self, session_id: str | None, request: Request | None, proxy_tier: int | None
⋮

src\crawlee\request_loaders\_request_manager.py:
⋮
│@docs_group('Request loaders')
│class RequestManager(RequestLoader, ABC):
│    """Base class that extends `RequestLoader` with the capability to enqueue new requests and recl
│
⋮
│    @abstractmethod
│    async def add_request(
│        self,
│        request: str | Request,
│        *,
│        forefront: bool = False,
⋮

src\crawlee\request_loaders\_request_manager_tandem.py:
⋮
│@docs_group('Request loaders')
│class RequestManagerTandem(RequestManager):
│    """Implements a tandem behaviour for a pair of `RequestLoader` and `RequestManager`.
│
│    In this scenario, the contents of the "loader" get transferred into the "manager", allowing pro
│    from both sources and also enqueueing new requests (not possible with plain `RequestManager`).
⋮
│    @override
│    async def add_request(self, request: str | Request, *, forefront: bool = False) -> ProcessedReq
⋮

src\crawlee\request_loaders\_sitemap_request_loader.py:
⋮
│@docs_group('Request loaders')
│class SitemapRequestLoader(RequestLoader):
│    """A request loader that reads URLs from sitemap(s).
│
│    The loader is designed to handle sitemaps that follow the format described in the Sitemaps prot
│    (https://www.sitemaps.org/protocol.html). It supports both XML and plain text sitemap formats.
│    Note that HTML pages containing links are not supported - those should be handled by regular cr
│    and the `enqueue_links` functionality.
│
│    The loader fetches and parses sitemaps in the background, allowing crawling to start
│    before all URLs are loaded. It supports filtering URLs using glob and regex patterns.
│
⋮
│    async def start(self) -> None:
⋮

src\crawlee\request_loaders\_throttling_request_manager.py:
⋮
│@docs_group('Request loaders')
│class ThrottlingRequestManager(RequestManager, Generic[TRequestManager]):
│    """A request manager that wraps another and enforces per-domain delays.
│
│    Requests for explicitly configured domains are routed into dedicated sub-managers at insertion 
│    lives in exactly one manager, eliminating duplication and simplifying deduplication.
│
│    When `fetch_next_request()` is called, it returns requests from the sub-manager whose domain ha
│    longest. If all configured domains are throttled, it falls back to the inner manager for non-th
│    the inner manager is also empty and all sub-managers are throttled, it sleeps until the earlies
│
│    Delay sources:
⋮
│    @override
│    async def add_request(self, request: str | Request, *, forefront: bool = False) -> ProcessedReq
⋮

src\crawlee\sessions\_cookies.py:
⋮
│@docs_group('Session management')
│class CookieParam(TypedDict, total=False):
⋮
│class PlaywrightCookieParam(TypedDict, total=False):
⋮
│@docs_group('Session management')
│class SessionCookies:
│    """Storage cookies for session with browser-compatible serialization and deserialization."""
│
⋮
│    def set(
│        self,
│        name: str,
│        value: str,
│        *,
│        domain: str = '',
│        path: str = '/',
│        expires: int | None = None,
│        http_only: bool = False,
│        secure: bool = False,
⋮
│    def get_cookies_as_dicts(self) -> list[CookieParam]:
⋮
│    def store_cookie(self, cookie: Cookie) -> None:
⋮

src\crawlee\sessions\_session.py:
⋮
│@docs_group('Session management')
│class Session:
│    """Represent a single user session, managing cookies, error states, and usage limits.
│
│    A `Session` simulates a specific user with attributes like cookies, IP (via proxy), and potenti
│    a unique browser fingerprint. It maintains its internal state, which can include custom user da
│    (e.g., authorization tokens or headers) and tracks its usability through metrics such as error 
│    usage count, and expiration.
⋮
│    @overload
│    def get_state(self, *, as_dict: Literal[True]) -> dict: ...
│
│    @overload
│    def get_state(self, *, as_dict: Literal[False]) -> SessionModel: ...
│
│    def get_state(self, *, as_dict: bool = False) -> SessionModel | dict:
⋮

src\crawlee\sessions\_session_pool.py:
⋮
│@docs_group('Session management')
│class SessionPool:
│    """A pool of sessions that are managed, rotated, and persisted based on usage and age.
│
│    It ensures effective session management by maintaining a pool of sessions and rotating them bas
│    usage count, expiration time, or custom rules. It provides methods to retrieve sessions, manage
│    lifecycle, and optionally persist the state to enable recovery.
⋮
│    @overload
│    def get_state(self, *, as_dict: Literal[True]) -> dict: ...
│
│    @overload
│    def get_state(self, *, as_dict: Literal[False]) -> SessionPoolModel: ...
│
│    @ensure_context
│    def get_state(self, *, as_dict: bool = False) -> SessionPoolModel | dict:
⋮

src\crawlee\statistics\_error_snapshotter.py:
⋮
│class ErrorSnapshotter:
│    MAX_ERROR_CHARACTERS = 30
⋮
│    async def capture_snapshot(
│        self,
│        error_message: str,
│        file_and_line: str,
│        context: BasicCrawlingContext,
⋮

src\crawlee\statistics\_error_tracker.py:
⋮
│class ErrorTracker:
⋮

src\crawlee\statistics\_statistics.py:
⋮
│class RequestProcessingRecord:
│    """Tracks information about the processing of a request."""
│
⋮
│    def run(self) -> int:
⋮

src\crawlee\storage_clients\_file_system\_storage_client.py:
⋮
│@docs_group('Storage clients')
│class FileSystemStorageClient(StorageClient):
⋮

src\crawlee\storage_clients\_memory\_storage_client.py:
⋮
│@docs_group('Storage clients')
│class MemoryStorageClient(StorageClient):
⋮

src\crawlee\storage_clients\_redis\_utils.py:
⋮
│@overload
│async def await_redis_response(response: Awaitable[T]) -> T: ...
│@overload
│async def await_redis_response(response: T) -> T: ...
│
⋮
│async def await_redis_response(response: Awaitable[T] | T) -> T:
⋮

src\crawlee\storage_clients\_sql\_client_mixin.py:
⋮
│class SqlClientMixin(ABC):
│    """Mixin class for SQL clients.
│
│    This mixin provides common SQL operations and basic methods for SQL storage clients.
⋮
│    @asynccontextmanager
│    async def get_session(self, *, with_simple_commit: bool = False) -> AsyncIterator[AsyncSession]
⋮

src\crawlee\storage_clients\models.py:
⋮
│@docs_group('Storage data')
│class KeyValueStoreRecordMetadata(BaseModel):
⋮

src\crawlee\storages\_request_queue.py:
⋮
│@docs_group('Storages')
│class RequestQueue(Storage, RequestManager):
│    """Request queue is a storage for managing HTTP requests.
│
│    The request queue class serves as a high-level interface for organizing and managing HTTP reque
│    during web crawling. It provides methods for adding, retrieving, and manipulating requests thro
│    the crawling lifecycle, abstracting away the underlying storage implementation details.
│
│    Request queue maintains the state of each URL to be crawled, tracking whether it has been proce
│    is currently being handled, or is waiting in the queue. Each URL in the queue is uniquely ident
│    by a `unique_key` property, which prevents duplicate processing unless explicitly configured ot
│
⋮
│    @override
│    async def add_request(
│        self,
│        request: str | Request,
│        *,
│        forefront: bool = False,
⋮

src\crawlee\storages\_storage_instance_manager.py:
⋮
│class StorageInstanceManager:
⋮

tests\unit\_autoscaling\test_autoscaled_pool.py:
⋮
│@pytest.mark.run_alone
│async def test_runs_concurrently(system_status: SystemStatus | Mock) -> None:
│    done_count = 0
│
│    async def run() -> None:
⋮
│async def test_abort_works(system_status: SystemStatus | Mock) -> None:
│    async def run() -> None:
⋮
│async def test_propagates_exceptions(system_status: SystemStatus | Mock) -> None:
│    done_count = 0
│
│    async def run() -> None:
⋮
│async def test_propagates_exceptions_after_finished(system_status: SystemStatus | Mock) -> None:
│    started_count = 0
│
│    async def run() -> None:
⋮
│async def test_autoscales(
│    monkeypatch: pytest.MonkeyPatch,
│    system_status: SystemStatus | Mock,
│) -> None:
│    done_count = 0
│
│    async def run() -> None:
⋮
│async def test_autoscales_uses_desired_concurrency_ratio(
│    monkeypatch: pytest.MonkeyPatch,
│    system_status: SystemStatus | Mock,
│) -> None:
│    """Test that desired concurrency ratio can limit desired concurrency.
│
│    This test creates situation where only one task is ready and then no other task is ever ready.
│    This creates situation where the system could scale up desired concurrency, but it will not do 
│    desired_concurrency_ratio=1 means that first the system would have to increase current concurre
│    desired concurrency and due to no other task ever being ready, it will never happen. Thus desir
│    stay 2 as was the initial setup, even though other conditions would allow the increase. (max_co
│    system being idle).
⋮
│    async def run() -> None:
⋮
│async def test_max_tasks_per_minute_works(system_status: SystemStatus | Mock) -> None:
│    done_count = 0
│
│    async def run() -> None:
⋮
│async def test_allows_multiple_run_calls(system_status: SystemStatus | Mock) -> None:
│    done_count = 0
│
│    async def run() -> None:
⋮

tests\unit\_autoscaling\test_system_status.py:
⋮
│@pytest.fixture
│def now() -> datetime:
⋮

tests\unit\_utils\test_retry.py:
⋮
│async def test_success_on_first_attempt() -> None:
│    call_mock = AsyncMock()
│
│    @retry_on_error(ValueError)
│    async def func() -> bool:
⋮
│async def test_retries_and_succeeds() -> None:
│    call_mock = AsyncMock()
│
│    @retry_on_error(ValueError, max_attempts=3)
│    async def func() -> bool:
⋮
│async def test_reraises_after_max_attempts() -> None:
│    @retry_on_error(ValueError, max_attempts=3)
│    async def func() -> None:
⋮
│async def test_does_not_retry_on_unspecified_exception() -> None:
│    call_mock = AsyncMock()
│
│    @retry_on_error(ValueError, max_attempts=3)
│    async def func() -> None:
⋮
│async def test_exponential_backoff_delays() -> None:
│    @retry_on_error(ValueError, max_attempts=4, base_delay=timedelta(seconds=1))
│    async def func() -> None:
⋮

tests\unit\_utils\test_timedelta_ms.py:
⋮
│class _ModelWithTimedeltaMs(BaseModel):
⋮

tests\unit\server.py:
⋮
│def get_headers_dict(scope: dict[str, Any]) -> dict[str, str]:
⋮
│def get_query_params(query_string: bytes) -> dict[str, str]:
⋮
│async def send_json_response(send: Send, data: Any, status: int = 200) -> None:
⋮
│async def send_html_response(send: Send, html_content: bytes, status: int = 200) -> None:
⋮
│class TestServer(Server):
│    """A test HTTP server implementation based on Uvicorn Server."""
│
⋮
│    def run(self, sockets: list[socket] | None = None) -> None:
⋮

tests\unit\storage_clients\_redis\test_redis_storage_client.py:
⋮
│def test_import_error_handled() -> None:
⋮

tests\unit\utils.py:
⋮
│async def maybe_await(value: Awaitable[T] | T) -> T:
⋮

website\roa-loader\index.js:
⋮
│async function encodeAndSign(source) {
│    if (!process.env.APIFY_SIGNING_TOKEN) {
│        return 'invalid-token';
│    }
│
│    if (working) {
│        return new Promise((resolve, reject) => {
│            queue.push(() => {
│                return getHash(source).then(resolve, reject);
│            });
⋮

website\src\components\ApiLink.jsx:
⋮
│const ApiLink = ({ to, children }) => {
│    const version = useDocsVersion();
│    const { siteConfig } = useDocusaurusContext();
│
│    if (siteConfig.presets[0][1].docs.disableVersioning || version.isLast) {
│        return <Link to={`/api/${to}`}>{children}</Link>;
│    }
│
│    return <Link to={`/api/${version.version === 'current' ? 'next' : version.version}/${to}`}>{chi
⋮

website\src\components\Button.jsx:
⋮
│export default function Button({ children, to, withIcon, type = 'primary', className, isBig }) {
│    return (
│        <Link to={to} target="_self" rel="dofollow">
│            <span
│                className={clsx(
│                    className,
│                    styles.button,
│                    type === 'primary' && styles.buttonPrimary,
│                    type === 'secondary' && styles.buttonSecondary,
│                    isBig && styles.big,
⋮

website\src\components\Homepage\HomepageCtaSection.jsx:
⋮
│export default function HomepageCtaSection() {
│    const { colorMode } = useColorMode();
│    return (
│        <section className={styles.ctaSection}>
│            <h2 className={styles.ctaTitle}>Get started now!</h2>
│            <div className={styles.ctaDescription}>
│                Crawlee won’t fix broken selectors for you (yet), but it makes building and maintai
│                crawlers faster and easier—so you can focus on what matters most.
│            </div>
│            <div className={styles.ctaButtonContainer}>
⋮

website\src\components\Homepage\LanguageInfoWidget.jsx:
⋮
│export default function LanguageInfoWidget({ language, command, to, githubUrl }) {
│    const { colorMode } = useColorMode();
│    return (
│        <div className={styles.languageGetStartedContainer}>
│            {language === 'JavaScript' && (
│                <ThemedImage
│                    sources={{
│                        light: 'img/crawlee-javascript-light.svg',
│                        dark: 'img/crawlee-javascript-dark.svg',
│                    }}
⋮

website\src\components\Homepage\LanguageSwitch.jsx:
⋮
│export default function LanguageSwitch({ options = ['JavaScript', 'Python'], defaultOption = 'JavaS
│    const [activeOption, setActiveOption] = useState(defaultOption);
│    const [backgroundStyle, setBackgroundStyle] = useState({});
│    const optionRefs = useRef([]);
│
│    const updateBackgroundStyle = useCallback(() => {
│        const activeIndex = options.indexOf(activeOption);
│        const activeElement = optionRefs.current[activeIndex];
│        if (activeElement) {
│            const { offsetLeft, offsetWidth } = activeElement;
⋮
│    const handleOptionClick = (option) => {
│        setActiveOption(option);
│        onChange?.(option);
⋮

website\src\components\Homepage\RiverSection.jsx:
⋮
│export default function RiverSection({ title, description, content, reversed, to }) {
│    return (
│        <div className={styles.riverWrapper}>
│            <div className={clsx(styles.riverContainer, { [styles.riverReversed]: reversed })}>
│                <div className={clsx(styles.riverSection, styles.riverText)}>
│                    <h3 className={styles.riverTitle}>{title}</h3>
│                    <p className={styles.riverDescription}>{description}</p>
│                    <Link className={styles.riverButton} to={to}>
│                        Learn more
│                    </Link>
⋮

website\src\components\Homepage\ThreeCardsWithIcon.jsx:
⋮
│export default function ThreeCardsWithIcon({ cards }) {
│    return (
│        <div className={styles.cardsWrapper}>
│            {cards?.map((card, index) => {
│                const content = (
│                    <>
│                        <div className={styles.cardIcon}>{card.icon}</div>
│                        <h3 className={styles.cardTitle}>{card.title}</h3>
│                        <p className={styles.cardDescription}>{card.description}</p>
│                        {card.actionLink && (
⋮

website\src\components\RunnableCodeBlock.jsx:
⋮
│const RunnableCodeBlock = ({ children, actor, hash, ...props }) => {
│    hash = hash ?? children.hash;
│
│    if (!children.code) {
│        throw new Error(`RunnableCodeBlock requires "code" and "hash" props
│Make sure you are importing the code block contents with the roa-loader.`);
│    }
│
│    if (!hash) {
│        return <CodeBlock {...props}>{children.code}</CodeBlock>;
⋮

website\src\theme\ColorModeToggle\index.js:
⋮
│function ColorModeToggle({ className, value, onChange }) {
│    const isBrowser = useIsBrowser();
│    const title = translate(
│        {
│            message: 'Switch between dark and light mode (currently {mode})',
│            id: 'theme.colorToggle.ariaLabel',
│            description: 'The ARIA label for the navbar color mode toggle',
│        },
│        {
│            mode:
⋮

website\src\theme\DocItem\Content\index.js:
⋮
│function useSyntheticTitle() {
│    const { metadata, frontMatter, contentTitle } = useDoc();
│    const shouldRender = !frontMatter.hide_title && typeof contentTitle === 'undefined';
│
│    if (!shouldRender) {
│        return null;
│    }
│
│    return metadata.title;
⋮

website\src\theme\DocItem\Layout\index.js:
⋮
│function useDocTOC() {
│    const { frontMatter, toc } = useDoc();
│    const windowSize = useWindowSize();
│    const hidden = frontMatter.hide_table_of_contents;
│    const canRender = !hidden && toc.length > 0;
│    const mobile = canRender ? <DocItemTOCMobile /> : undefined;
│    const desktop = canRender && (windowSize === 'desktop' || windowSize === 'ssr') ? <DocItemTOCDe
│    return {
│        hidden,
│        mobile,
⋮

website\src\theme\Footer\LinkItem\index.js:
⋮
│export default function FooterLinkItem({ item }) {
│    const ExternalLinkIcon = require('../../../../static/img/external-link.svg').default;
│
│    const { to, href, label, prependBaseUrlToHref, className, ...props } = item;
│    const toUrl = useBaseUrl(to);
│    const normalizedHref = useBaseUrl(href, { forcePrependBaseUrl: true });
│
│    return (
│        <Link
│            className={clsx('footer__link-item', className, styles.footerLink)}
⋮

website\src\theme\MDXComponents\A.js:
⋮
│export default function MDXA(props) {
│    const { siteConfig } = useDocusaurusContext();
│    if (props.href?.startsWith(siteConfig.url)) {
│        const { href, ...rest } = props;
│        rest.to = props.href.replace(siteConfig.url + siteConfig.baseUrl, '/');
│        props = rest;
│    }
│
│    return <Link {...props} />;
⋮

website\src\theme\NavbarItem\apiVersionUtils.js:
⋮
│export function getApiPath(version) {
│    if (version.isLast) {
│        return API_ROUTE_BASE;
│    }
│    if (version.name === 'current') {
│        return `${API_ROUTE_BASE}/next`;
│    }
│    return `${API_ROUTE_BASE}/${version.name}`;
⋮

website\src\theme\Navbar\Content\index.js:
⋮
│function useNavbarItems() {
│    return useThemeConfig().navbar.items;
⋮

website\src\theme\Navbar\Logo\index.js:
⋮
│export default function LogoWrapper() {
│    const ArrowsIcon = require('../../../../static/img/menu-arrows.svg').default;
│    const CheckIcon = require('../../../../static/img/check.svg').default;
│    const {
│        navbar: { logo },
│    } = useThemeConfig();
│    const javascriptLogo = {
│        light: useBaseUrl('img/crawlee-javascript-light.svg'),
│        dark: useBaseUrl('img/crawlee-javascript-dark.svg'),
│    };
⋮

website\src\theme\Navbar\MobileSidebar\Layout\index.js:
⋮
│export default function NavbarMobileSidebarLayout({ header, primaryMenu, secondaryMenu }) {
│    const { shown: secondaryMenuShown } = useNavbarSecondaryMenu();
│    return (
│        <div className="navbar-sidebar">
│            {header}
│            <div
│                className={clsx('navbar-sidebar__items', {
│                    'navbar-sidebar__items--show-secondary': secondaryMenuShown,
│                })}
│            >
⋮

website\src\theme\Navbar\MobileSidebar\PrimaryMenu\index.js:
⋮
│function useNavbarItems() {
│    return useThemeConfig().navbar.items;
⋮

website\src\theme\Navbar\MobileSidebar\index.js:
⋮
│export default function NavbarMobileSidebar() {
│    const mobileSidebar = useNavbarMobileSidebar();
│    const windowSize = useWindowSize({
│        desktopBreakpoint: 1200,
│    });
│
│    useLockBodyScroll(mobileSidebar.shown);
│    const shouldRender = !mobileSidebar.disabled && windowSize === 'mobile';
│    if (!shouldRender) {
│        return null;
⋮

website\versioned_docs\version-1.7\guides\code_examples\http_crawlers\selectolax_context.py:
⋮
│@dataclass(frozen=True)
│class SelectolaxLexborContext(ParsedHttpCrawlingContext[LexborHTMLParser]):
│    """Crawling context providing access to the parsed page.
│
│    This context is passed to request handlers and includes all standard
│    context methods (push_data, enqueue_links, etc.) plus custom helpers.
⋮
│    @property
│    def parser(self) -> LexborHTMLParser:
⋮
│    @classmethod
│    def from_parsed_http_crawling_context(
│        cls, context: ParsedHttpCrawlingContext[LexborHTMLParser]
⋮
```