---
name: crawl4ai
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging crawl4ai. Use this skill whenever modifying crawl4ai configurations or adding related functionality.
---
# crawl4ai

## File Tree

```text
crawl4ai/
├── modules
│   └── crawl4ai (See AST Map below)
└── SKILL.md
```

### AST Map: `modules/crawl4ai`

```python
crawl4ai/async_configs.py:
⋮
│class UntrustedConfigError(ValueError):
⋮
│def to_serializable_dict(obj: Any, ignore_default_value : bool = False):
⋮
│def from_serializable_dict(data: Any, provenance: "Provenance" = None) -> Any:
⋮
│def is_empty_value(value: Any) -> bool:
⋮
│class GeolocationConfig:
│    def __init__(
│        self,
│        latitude: float,
│        longitude: float,
│        accuracy: Optional[float] = 0.0
⋮
│    @staticmethod
│    def from_dict(geo_dict: Dict) -> "GeolocationConfig":
⋮
│    def to_dict(self) -> Dict:
⋮
│class ProxyConfig:
│    DIRECT = "direct"  # Sentinel: use in proxy_config list to mean "no proxy"
│
⋮
│    @staticmethod
│    def from_string(proxy_str: str) -> "ProxyConfig":
⋮
│    @staticmethod
│    def from_dict(proxy_dict: Dict) -> "ProxyConfig":
⋮
│    def to_dict(self) -> Dict:
⋮
│@_with_defaults
│class BrowserConfig:
│    """
│    Configuration class for setting up a browser instance and its context in AsyncPlaywrightCrawler
│
│    This class centralizes all parameters that affect browser and context creation. Instead of pass
│    scattered keyword arguments, users can instantiate and modify this configuration object. The cr
│    code will then reference these settings to initialize the browser in a consistent, documented m
│
│    Attributes:
│        browser_type (str): The type of browser to launch. Supported values: "chromium", "firefox",
│                            Default: "chromium".
⋮
│    @staticmethod
│    def from_kwargs(kwargs: dict) -> "BrowserConfig":
⋮
│class VirtualScrollConfig:
│    """Configuration for virtual scroll handling.
│    
│    This config enables capturing content from pages with virtualized scrolling
│    (like Twitter, Instagram feeds) where DOM elements are recycled as user scrolls.
⋮
│    def to_dict(self) -> dict:
⋮
│    @classmethod
│    def from_dict(cls, data: dict) -> "VirtualScrollConfig":
⋮
│class LinkPreviewConfig:
│    """Configuration for link head extraction and scoring."""
│    
⋮
│    @staticmethod
│    def from_dict(config_dict: Dict[str, Any]) -> "LinkPreviewConfig":
⋮
│    def to_dict(self) -> Dict[str, Any]:
⋮
│class HTTPCrawlerConfig:
│    """HTTP-specific crawler configuration"""
│
⋮
│    @staticmethod
│    def from_kwargs(kwargs: dict) -> "HTTPCrawlerConfig":
⋮
│@_with_defaults
│class CrawlerRunConfig():
│
│    """
│    Configuration class for controlling how the crawler runs each crawl operation.
│    This includes parameters for content extraction, page manipulation, waiting conditions,
│    caching, and other runtime behaviors.
│
│    This centralizes parameters that were previously scattered as kwargs to `arun()` and related me
│    By using this class, you have a single place to understand and adjust the crawling options.
│
│    Attributes:
│        # Deep Crawl Parameters
⋮
│    @staticmethod
│    def from_kwargs(kwargs: dict) -> "CrawlerRunConfig":
⋮
│    def to_dict(self):
⋮
│class LLMConfig:
│    def __init__(
│        self,
│        provider: str = DEFAULT_PROVIDER,
│        api_token: Optional[str] = None,
│        base_url: Optional[str] = None,
│        temperature: Optional[float] = None,
│        max_tokens: Optional[int] = None,
│        top_p: Optional[float] = None,
│        frequency_penalty: Optional[float] = None,
│        presence_penalty: Optional[float] = None,
⋮
│    @staticmethod
│    def from_kwargs(kwargs: dict) -> "LLMConfig":
⋮
│    def to_dict(self):
⋮
│class SeedingConfig:
│    """
│    Configuration class for URL discovery and pre-validation via AsyncUrlSeeder.
⋮
│    def to_dict(self) -> Dict[str, Any]:
⋮
│    @staticmethod
│    def from_kwargs(kwargs: Dict[str, Any]) -> 'SeedingConfig':
⋮
│class DomainMapperConfig:
│    """
│    Configuration for comprehensive domain URL discovery via DomainMapper.
│
│    Discovers all URLs under a domain using multiple sources (sitemap, Common Crawl,
│    Wayback Machine, Certificate Transparency, path probing, robots.txt mining,
│    RSS/Atom feeds, homepage link extraction) without deep crawling.
⋮
│    def to_dict(self) -> Dict[str, Any]:
⋮
│    @staticmethod
│    def from_kwargs(kwargs: Dict[str, Any]) -> 'DomainMapperConfig':
⋮

crawl4ai/async_logger.py:
⋮
│class AsyncLoggerBase(ABC):
│    @abstractmethod
│    def debug(self, message: str, tag: str = "DEBUG", **kwargs):
⋮
│    @abstractmethod
│    def warning(self, message: str, tag: str = "WARNING", **kwargs):
⋮
│class AsyncLogger(AsyncLoggerBase):
│    """
│    Asynchronous logger with support for colored console output and file logging.
│    Supports templated messages with colored components.
⋮
│    def warning(self, message: str, tag: str = "WARNING", **kwargs):
⋮
│class AsyncFileLogger(AsyncLoggerBase):
│    """
│    File-only asynchronous logger that writes logs to a specified file.
⋮
│    def warning(self, message: str, tag: str = "WARNING", **kwargs):
⋮

crawl4ai/async_url_seeder.py:
⋮
│class AsyncUrlSeeder:
⋮

crawl4ai/async_webcrawler.py:
⋮
│class AsyncWebCrawler:
│    """
│    Asynchronous web crawler with flexible caching capabilities.
│
│    There are two ways to use the crawler:
│
│    1. Using context manager (recommended for simple cases):
│        ```python
│        async with AsyncWebCrawler() as crawler:
│            result = await crawler.arun(url="https://example.com")
│        ```
│
⋮
│    async def arun_many(
│        self,
│        urls: List[str],
│        config: Optional[Union[CrawlerRunConfig, List[CrawlerRunConfig]]] = None,
│        dispatcher: Optional[BaseDispatcher] = None,
│        # Legacy parameters maintained for backwards compatibility
│        # word_count_threshold=MIN_WORD_THRESHOLD,
│        # extraction_strategy: ExtractionStrategy = None,
│        # chunking_strategy: ChunkingStrategy = RegexChunking(),
│        # content_filter: RelevantContentFilter = None,
⋮

crawl4ai/browser_adapter.py:
⋮
│class BrowserAdapter(ABC):
│    """Abstract adapter for browser-specific operations"""
│    
⋮
│    @abstractmethod
│    async def retrieve_console_messages(self, page: Page) -> List[Dict]:
⋮
│class PlaywrightAdapter(BrowserAdapter):
│    """Adapter for standard Playwright"""
│    
⋮
│    async def retrieve_console_messages(self, page: Page) -> List[Dict]:
⋮
│class StealthAdapter(BrowserAdapter):
│    """Adapter for Playwright with stealth features using playwright_stealth"""
│
⋮
│    async def apply_stealth(self, page: Page):
⋮
│    async def retrieve_console_messages(self, page: Page) -> List[Dict]:
⋮
│class UndetectedAdapter(BrowserAdapter):
│    """Adapter for undetected browser automation with stealth features"""
│    
⋮
│    async def retrieve_console_messages(self, page: UndetectedPage) -> List[Dict]:
⋮

crawl4ai/cache_context.py:
⋮
│class CacheMode(Enum):
⋮
│class CacheContext:
│    """
│    Encapsulates cache-related decisions and URL handling.
│
│    This class centralizes all cache-related logic and URL type checking,
│    making the caching behavior more predictable and maintainable.
│
│    Attributes:
│        url (str): The URL being processed.
│        cache_mode (CacheMode): The cache mode for the current operation.
│        always_bypass (bool): If True, bypasses caching for this operation.
⋮
│    @property
│    def display_url(self) -> str:
⋮
│def _legacy_to_cache_mode(
│    disable_cache: bool = False,
│    bypass_cache: bool = False,
│    no_cache_read: bool = False,
│    no_cache_write: bool = False,
⋮

crawl4ai/chunking_strategy.py:
⋮
│class RegexChunking(ChunkingStrategy):
⋮
│class TopicSegmentationChunking(ChunkingStrategy):
│    """
│    Chunking strategy that segments text into topics using NLTK's TextTilingTokenizer.
│
│    How it works:
│    1. Segment the text into topics using TextTilingTokenizer
│    2. Extract keywords for each topic segment
⋮
│    def extract_keywords(self, text: str) -> list:
⋮

crawl4ai/content_scraping_strategy.py:
⋮
│class LXMLWebScrapingStrategy(ContentScrapingStrategy):
│    """
│    LXML-based implementation for fast web content scraping.
│    
│    This is the primary scraping strategy in Crawl4AI, providing high-performance
│    HTML parsing and content extraction using the lxml library.
│    
│    Note: WebScrapingStrategy is now an alias for this class to maintain
│    backward compatibility.
⋮
│    def find_closest_parent_with_useful_text(
│        self, element: lhtml.HtmlElement, **kwargs
⋮
│    def flatten_nested_elements(self, element: lhtml.HtmlElement) -> lhtml.HtmlElement:
⋮
│    def process_image(
│        self, img: lhtml.HtmlElement, url: str, index: int, total_images: int, **kwargs
⋮

crawl4ai/deep_crawling/base_strategy.py:
⋮
│class DeepCrawlStrategy(ABC):
│    """
│    Abstract base class for deep crawling strategies.
│    
│    Core functions:
│      - arun: Main entry point that returns an async generator of CrawlResults.
│      - shutdown: Clean up resources.
│      - can_process_url: Validate a URL and decide whether to process it.
│      - _process_links: Extract and process links from a CrawlResult.
⋮
│    async def arun(
│        self,
│        start_url: str,
│        crawler: AsyncWebCrawler,
│        config: Optional[CrawlerRunConfig] = None,
⋮

crawl4ai/deep_crawling/crazy.py:
⋮
│class BloomFilter:
│    """Optimal Bloom filter using murmur3 hash avalanche"""
⋮
│    def add(self, item: str) -> None:
⋮

crawl4ai/deep_crawling/scorers.py:
⋮
│class ScoringStats:
│    __slots__ = ('_urls_scored', '_total_score', '_min_score', '_max_score')
│    
⋮
│    def update(self, score: float) -> None:
⋮

crawl4ai/extraction_strategy.py:
⋮
│class JsonCssExtractionStrategy(JsonElementExtractionStrategy):
⋮

crawl4ai/html2text/__init__.py:
⋮
│class HTML2Text(html.parser.HTMLParser):
⋮
│class CustomHTML2Text(HTML2Text):
⋮

crawl4ai/html2text/utils.py:
⋮
│def dumb_property_dict(style: str) -> Dict[str, str]:
⋮
│def reformat_table(lines: List[str], right_margin: int) -> List[str]:
⋮

crawl4ai/hub.py:
⋮
│class CrawlerHub:
│    _crawlers: Dict[str, Type[BaseCrawler]] = {}
│
⋮
│    @classmethod
│    def get(cls, name: str) -> Union[Type[BaseCrawler], None]:
⋮

crawl4ai/legacy/cli.py:
⋮
│@docs.command()
│def update():
⋮
│@docs.command()
│def list():
⋮

crawl4ai/legacy/docs_manager.py:
⋮
│class DocsManager:
│    def __init__(self, logger=None):
│        self.docs_dir = Path.home() / ".crawl4ai" / "docs"
│        self.local_docs = Path(__file__).parent.parent / "docs" / "llm.txt"
│        self.docs_dir.mkdir(parents=True, exist_ok=True)
│        self.logger = logger or AsyncLogger(verbose=True)
⋮
│    def list(self) -> list[str]:
⋮

crawl4ai/legacy/version_manager.py:
⋮
│class VersionManager:
│    def __init__(self):
│        self.home_dir = Path.home() / ".crawl4ai"
⋮
│    def get_installed_version(self):
⋮

crawl4ai/markdown_generation_strategy.py:
⋮
│class DefaultMarkdownGenerator(MarkdownGenerationStrategy):
⋮

crawl4ai/model_loader.py:
⋮
│def set_model_device(model):
⋮
│@lru_cache()
│def get_home_folder():
⋮
│@lru_cache()
│def load_nltk_punkt():
⋮

crawl4ai/models.py:
⋮
│class MarkdownGenerationResult(BaseModel):
⋮
│class CrawlResult(BaseModel):
│    url: str
⋮
│    def model_dump(self, *args, **kwargs):
⋮
│class StringCompatibleMarkdown(str):
⋮

crawl4ai/proxy_strategy.py:
⋮
│class ProxyConfig:
│    def __init__(
│        self,
│        server: str,
│        username: Optional[str] = None,
│        password: Optional[str] = None,
│        ip: Optional[str] = None,
⋮
│    @staticmethod
│    def from_string(proxy_str: str) -> "ProxyConfig":
⋮
│    @staticmethod
│    def from_dict(proxy_dict: Dict) -> "ProxyConfig":
⋮
│    def to_dict(self) -> Dict:
⋮
│class ProxyRotationStrategy(ABC):
│    """Base abstract class for proxy rotation strategies"""
│
│    @abstractmethod
│    async def get_next_proxy(self) -> Optional[ProxyConfig]:
⋮
│    @abstractmethod
│    def add_proxies(self, proxies: List[ProxyConfig]):
⋮
│class RoundRobinProxyStrategy(ProxyRotationStrategy):
│    """Simple round-robin proxy rotation strategy using ProxyConfig objects.
│
│    Supports sticky sessions where a session_id can be bound to a specific proxy
│    for the duration of the session. This is useful for deep crawling where
│    you want to maintain the same IP address across multiple requests.
⋮
│    def add_proxies(self, proxies: List[ProxyConfig]):
⋮
│    async def get_next_proxy(self) -> Optional[ProxyConfig]:
⋮

crawl4ai/script/c4a_compile.py:
⋮
│class C4ACompiler:
│    """Main compiler with result-based API"""
│    
⋮
│    @classmethod
│    def compile(cls, script: Union[str, List[str]], root: Optional[pathlib.Path] = None) -> Compila
⋮
│    @classmethod
│    def compile_file(cls, path: Union[str, pathlib.Path]) -> CompilationResult:
⋮
│def compile(script: Union[str, List[str]], root: Optional[pathlib.Path] = None) -> CompilationResul
⋮
│def compile_file(path: Union[str, pathlib.Path]) -> CompilationResult:
⋮

crawl4ai/script/c4a_result.py:
⋮
│@dataclass
│class Suggestion:
│    """A suggestion for fixing an error"""
⋮
│    def to_dict(self) -> dict:
⋮
│@dataclass
│class ErrorDetail:
│    """Detailed information about a compilation error"""
⋮
│    def to_dict(self) -> dict:
⋮
│@dataclass
│class WarningDetail:
│    """Information about a compilation warning"""
⋮
│    def to_dict(self) -> dict:
⋮
│@dataclass
│class CompilationResult:
│    """Result of C4A-Script compilation"""
⋮
│    def to_dict(self) -> dict:
⋮
│@dataclass
│class ValidationResult:
│    """Result of script validation"""
⋮
│    def to_dict(self) -> dict:
⋮

crawl4ai/script/c4ai_script.py:
⋮
│class Compiler:
│    def __init__(self, root: pathlib.Path|None=None):
│        self.parser = Lark(GRAMMAR,start="start",parser="lalr")
│        self.root   = pathlib.Path(root or ".").resolve()
│        self.vars: Dict[str,Any] = {}
⋮
│    def compile(self, text: Union[str, List[str]]) -> List[str]:
⋮
│    def _apply_set_vars(self,ir):
│        def sub(s): return re.sub(r"\$(\w+)",lambda m:str(self.vars.get(m.group(1),m.group(0))) ,s)
⋮
│def compile_string(script: Union[str, List[str]], *, root: Union[pathlib.Path, None] = None) -> Lis
⋮
│def compile_file(path: pathlib.Path) -> List[str]:
⋮

crawl4ai/table_extraction.py:
⋮
│class DefaultTableExtraction(TableExtractionStrategy):
⋮

crawl4ai/types.py:
⋮
│AsyncLogger = Union['AsyncLoggerType']
│
⋮
│AsyncWebCrawler = Union['AsyncWebCrawlerType']
⋮
│AsyncUrlSeeder = Union['AsyncUrlSeederType']
│
⋮
│BrowserConfig = Union['BrowserConfigType']
│CrawlerRunConfig = Union['CrawlerRunConfigType']
│HTTPCrawlerConfig = Union['HTTPCrawlerConfigType']
│LLMConfig = Union['LLMConfigType']
│# NEW: Add SeedingConfigType
│SeedingConfig = Union['SeedingConfigType']
│
⋮
│LXMLWebScrapingStrategy = Union['LXMLWebScrapingStrategyType']
⋮
│JsonCssExtractionStrategy = Union['JsonCssExtractionStrategyType']
⋮
│RegexChunking = Union['RegexChunkingType']
│
⋮
│DefaultMarkdownGenerator = Union['DefaultMarkdownGeneratorType']
│MarkdownGenerationResult = Union['MarkdownGenerationResultType']
│
⋮

crawl4ai/user_agent_generator.py:
⋮
│class UAGen(ABC):
│   @abstractmethod
│   def generate(self, 
│               browsers: Optional[List[str]] = None,
│               os: Optional[Union[str, List[str]]] = None,
│               min_version: float = 0.0,
│               platforms: Optional[Union[str, List[str]]] = None,
│               pct_threshold: Optional[float] = None,
│               fallback: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0
⋮
│   @staticmethod
│   def generate_client_hints( user_agent: str) -> str:
⋮
│class ValidUAGenerator(UAGen):
⋮
│class OnlineUAGenerator(UAGen):
⋮
│class UserAgentGenerator():
│    """
│    Generate random user agents with specified constraints.
│
│    Attributes:
│        desktop_platforms (dict): A dictionary of possible desktop platforms and their correspondin
│        mobile_platforms (dict): A dictionary of possible mobile platforms and their corresponding 
│        browser_combinations (dict): A dictionary of possible browser combinations and their corres
│        rendering_engines (dict): A dictionary of possible rendering engines and their correspondin
│        chrome_versions (list): A list of possible Chrome browser versions.
│        firefox_versions (list): A list of possible Firefox browser versions.
⋮
│    def get_browser_stack(self, num_browsers: int = 1) -> List[str]:
⋮
│    def get_random_platform(self, device_type, os_type, device_brand):
⋮
│    def parse_user_agent(self, user_agent: str) -> Dict[str, str]:
⋮
│    def generate_client_hints(self, user_agent: str) -> str:
⋮

crawl4ai/utils.py:
⋮
│class VersionManager:
│    def __init__(self):
│        self.home_dir = Path(os.getenv("CRAWL4_AI_BASE_DIRECTORY", Path.home())) / ".crawl4ai"
⋮
│    def get_installed_version(self):
⋮
│class InvalidCSSSelectorError(Exception):
⋮
│def create_box_message(
│    message: str,
│    type: str = "info",
│    width: int = 120,
│    add_newlines: bool = True,
│    double_line: bool = False,
⋮
│def get_home_folder():
⋮
│def sanitize_html(html):
⋮
│def sanitize_input_encode(text: str) -> str:
⋮
│def escape_json_string(s):
⋮
│def get_content_of_website(
│    url, html, word_count_threshold=MIN_WORD_THRESHOLD, css_selector=None, **kwargs
│):
│    """
│    Extract structured content, media, and links from website HTML.
│
│    How it works:
│    1. Parses the HTML content using BeautifulSoup.
│    2. Extracts internal/external links and media (images, videos, audios).
│    3. Cleans the content by removing unwanted tags and attributes.
│    4. Converts cleaned HTML to Markdown.
│    5. Collects metadata and returns the extracted information.
│
⋮
│    try:
│        if not html:
⋮
│        def flatten_nested_elements(node):
⋮
│def get_content_of_website_optimized(
│    url: str,
│    html: str,
│    word_count_threshold: int = MIN_WORD_THRESHOLD,
│    css_selector: str = None,
│    **kwargs,
│) -> Dict[str, Any]:
│    """
│    Extracts and cleans content from website HTML, optimizing for useful media and contextual infor
│    
│    Parses the provided HTML to extract internal and external links, filters and scores images for 
│    
│    Args:
│        url: The URL of the website being processed.
│        html: The raw HTML content to extract from.
│        word_count_threshold: Minimum word count for elements to be retained.
│        css_selector: Optional CSS selector to restrict extraction to specific elements.
│    
⋮
│    def find_closest_parent_with_useful_text(tag):
⋮
│    def process_image(img, url, index, total_images):
⋮
│    def flatten_nested_elements(node):
⋮
│def extract_xml_data(tags, string):
⋮
│def perform_completion_with_backoff(
│    provider,
│    prompt_with_variables,
│    api_token,
│    json_response=False,
│    base_url=None,
│    base_delay=2,
│    max_attempts=3,
│    exponential_factor=2,
│    messages=None,
⋮
│def normalize_url_for_deep_crawl(href, base_url, preserve_https=False, original_scheme=None):
⋮
│def get_base_domain(url: str) -> str:
⋮
│def is_external_url(url: str, base_domain: str) -> bool:
⋮
│async def get_text_embeddings(
│    texts: List[str], 
│    llm_config: Optional[Dict] = None,
│    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
│    batch_size: int = 32
⋮
│def get_true_available_memory_gb() -> float:
⋮

deploy/docker/auth.py:
⋮
│def resolve_secret_key(*, required: bool) -> str:
⋮
│def get_principal(request: Request) -> Optional[Dict]:
⋮

deploy/docker/egress_broker.py:
⋮
│class EgressBlocked(Exception):
⋮
│@dataclass
│class PinnedTarget:
⋮
│def resolve_and_pin(url: str) -> PinnedTarget:
⋮

deploy/docker/tests/conftest.py:
⋮
│class _FakeResolver:
│    """Drop-in for socket.getaddrinfo with a controllable host->IP map.
│
│    Unknown hosts resolve to a stable public-ish default so accidental real
│    lookups never escape the test process.
⋮
│    def set(self, host, ip):
⋮

deploy/docker/utils.py:
⋮
│def validate_webhook_url(url: str) -> None:
⋮

deploy/docker/webhook.py:
⋮
│class _PinnedResolver(AbstractResolver):
│    """aiohttp resolver that returns a single pre-pinned IP for the target host.
│
│    aiohttp connects to this IP but still performs TLS SNI / certificate
│    verification against the original hostname, so this pins the connection
│    (closing DNS rebinding) without weakening TLS or doing a MITM.
⋮
│    async def resolve(self, host, port=0, family=socket.AF_INET):
⋮
│def sanitize_webhook_headers(headers: Optional[Dict[str, str]]) -> Dict[str, str]:
⋮

docs/examples/website-to-api/web_scraper_lib.py:
⋮
│class ModelConfig:
│    """Configuration for LLM models."""
│    
⋮
│    def to_dict(self) -> Dict[str, Any]:
⋮
│    @classmethod
│    def from_dict(cls, data: Dict[str, Any]) -> 'ModelConfig':
⋮

docs/md_v2/apps/c4a-script/assets/c4a-generator.js:
⋮
│c4aGenerator.getFieldValue = function(block, fieldName) {
│    return block.getFieldValue(fieldName);
⋮

docs/md_v2/apps/crawl4ai-assistant/libs/marked.min.js:
⋮
│(function(g,f){if(typeof exports=="object"&&typeof module<"u"){module.exports=f()}else if("function
│"use strict";var H=Object.defineProperty;var be=Object.getOwnPropertyDescriptor;var Te=Object.getOw
│]`).replace("lheading",oe).replace("|table","").replace("blockquote"," {0,3}>").replace("|fences","
│`).map(i=>{let r=i.match(t.other.beginningSpace);if(r===null)return i;let[o]=r;return o.length>=s.l
│`)}var S=class{options;rules;lexer;constructor(e){this.options=e||w}space(e){let t=this.rules.block
│`)}}}fences(e){let t=this.rules.block.fences.exec(e);if(t){let n=t[0],s=rt(n,t[3]||"",this.rules);r
│`)}}blockquote(e){let t=this.rules.block.blockquote.exec(e);if(t){let n=A(t[0],`
│`).split(`
│`),s="",i="",r=[];for(;n.length>0;){let o=!1,a=[],c;for(c=0;c<n.length;c++)if(this.rules.other.bloc
│`),u=p.replace(this.rules.other.blockquoteSetextReplace,`
⋮
│${u}`:u;let d=this.lexer.state.top;if(this.lexer.state.top=!0,this.lexer.blockTokens(u,r,!0),this.l
│`+n.join(`
│`),y=this.blockquote(f);r[r.length-1]=y,s=s.substring(0,s.length-T.raw.length)+y.raw,i=i.substring(
│`+n.join(`
│`),y=this.list(f);r[r.length-1]=y,s=s.substring(0,s.length-g.raw.length)+y.raw,i=i.substring(0,i.le
│`);continue}}return{type:"blockquote",raw:s,tokens:r,text:i}}}list(e){let t=this.rules.block.list.e
⋮
│`?t[1].slice(0,-1):t[1];return{type:"paragraph",raw:t[0],text:n,tokens:this.lexer.inline(n)}}}text(
│`),this.blockTokens(e,this.tokens);for(let t=0;t<this.inlineQueue.length;t++){let n=this.inlineQueu
⋮
│`+s.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=r.text):t.push(s),n=i.length!==e.length
│`+s.raw,r.text+=`
│`+s.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=r.text):t.push(s);continue}if(e){let r=
⋮
│`}hr(e){return`<hr>
│`}list(e){let t=e.ordered,n=e.start,s="";for(let o=0;o<e.items.length;o++){let a=e.items[o];s+=this
⋮
│`}tablecell(e){let t=this.parser.parseInline(e.tokens),n=e.header?"th":"td";return(e.align?`<${n} a
│`}strong({tokens:e}){return`<strong>${this.parser.parseInline(e)}</strong>`}em({tokens:e}){return`<
│`+this.renderer.text(o);t?n+=this.renderer.paragraph({type:"paragraph",raw:a,text:a,tokens:[{type:"
│Please report this to https://github.com/markedjs/marked.`,e){let s="<p>An error occurred:</p><pre>
│
⋮

docs/md_v2/assets/gtag.js:
⋮
│  function gtag(){dataLayer.push(arguments);}
⋮

docs/md_v2/assets/highlight.min.js:
⋮
│  var hljs=function(){"use strict";function e(n){
│    return n instanceof Map?n.clear=n.delete=n.set=()=>{
│    throw Error("map is read-only")}:n instanceof Set&&(n.add=n.clear=n.delete=()=>{
│    throw Error("set is read-only")
│    }),Object.freeze(n),Object.getOwnPropertyNames(n).forEach((t=>{
│    const a=n[t],i=typeof a;"object"!==i&&"function"!==i||Object.isFrozen(a)||e(a)
│    })),n}class n{constructor(e){
│    void 0===e.data&&(e.data={}),this.data=e.data,this.isMatchIgnored=!1}
│    ignoreMatch(){this.isMatchIgnored=!0}}function t(e){
│    return e.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")
⋮
│    ;class r{constructor(e,n){
│    this.buffer="",this.classPrefix=n.classPrefix,e.walk(this)}addText(e){
│    this.buffer+=t(e)}openNode(e){if(!i(e))return;const n=((e,{prefix:n})=>{
│    if(e.startsWith("language:"))return e.replace("language:","language-")
│    ;if(e.includes(".")){const t=e.split(".")
│    ;return[`${n}${t.shift()}`,...t.map(((e,n)=>`${e}${"_".repeat(n+1)}`))].join(" ")
│    }return`${n}${e}`})(e.scope,{prefix:this.classPrefix});this.span(n)}
│    closeNode(e){i(e)&&(this.buffer+="</span>")}value(){return this.buffer}span(e){
│    this.buffer+=`<span class="${e}">`}}const s=(e={})=>{const n={children:[]}
│    ;return Object.assign(n,e),n};class o{constructor(){
│    this.rootNode=s(),this.stack=[this.rootNode]}get top(){
│    return this.stack[this.stack.length-1]}get root(){return this.rootNode}add(e){
│    this.top.children.push(e)}openNode(e){const n=s({scope:e})
│    ;this.add(n),this.stack.push(n)}closeNode(){
⋮
│    },M=x("//","$"),S=x("/\\*","\\*/"),A=x("#","$");var C=Object.freeze({
│    __proto__:null,APOS_STRING_MODE:O,BACKSLASH_ESCAPE:v,BINARY_NUMBER_MODE:{
│    scope:"number",begin:w,relevance:0},BINARY_NUMBER_RE:w,COMMENT:x,
│    C_BLOCK_COMMENT_MODE:S,C_LINE_COMMENT_MODE:M,C_NUMBER_MODE:{scope:"number",
│    begin:N,relevance:0},C_NUMBER_RE:N,END_SAME_AS_BEGIN:e=>Object.assign(e,{
│    "on:begin":(e,n)=>{n.data._beginMatch=e[1]},"on:end":(e,n)=>{
│    n.data._beginMatch!==e[1]&&n.ignoreMatch()}}),HASH_COMMENT_MODE:A,IDENT_RE:f,
│    MATCH_NOTHING_RE:/\b\B/,METHOD_GUARD:{begin:"\\.\\s*"+E,relevance:0},
│    NUMBER_MODE:{scope:"number",begin:y,relevance:0},NUMBER_RE:y,
│    PHRASAL_WORDS_MODE:{
⋮
│    G;Z(e,e.end,{key:"endScope"}),e.end=h(e.end,{joinWith:""})}})(e)}function Q(e){
│    function n(n,t){
│    return RegExp(c(n),"m"+(e.case_insensitive?"i":"")+(e.unicodeRegex?"u":"")+(t?"g":""))
│    }class t{constructor(){
│    this.matchIndexes={},this.regexes=[],this.matchAt=1,this.position=0}
│    addRule(e,n){
│    n.position=this.position++,this.matchIndexes[this.matchAt]=n,this.regexes.push([n,e]),
│    this.matchAt+=p(e)+1}compile(){0===this.regexes.length&&(this.exec=()=>null)
│    ;const e=this.regexes.map((e=>e[1]));this.matcherRe=n(h(e,{joinWith:"|"
│    }),!0),this.lastIndex=0}exec(e){this.matcherRe.lastIndex=this.lastIndex
⋮
│    ;return n.splice(0,t),Object.assign(n,a)}}class i{constructor(){
│    this.rules=[],this.multiRegexes=[],
│    this.count=0,this.lastIndex=0,this.regexIndex=0}getMatcher(e){
│    if(this.multiRegexes[e])return this.multiRegexes[e];const n=new t
│    ;return this.rules.slice(e).forEach((([e,t])=>n.addRule(e,t))),
│    n.compile(),this.multiRegexes[e]=n,n}resumingScanAtSamePosition(){
│    return 0!==this.regexIndex}considerAll(){this.regexIndex=0}addRule(e,n){
⋮

docs/md_v2/marketplace/frontend/marketplace.js:
⋮
│class MarketplaceCache {
│    constructor() {
│        this.prefix = 'c4ai_market_';
│    }
│
│    get(key) {
│        const item = localStorage.getItem(this.prefix + key);
│        if (!item) return null;
│
│        const data = JSON.parse(item);
⋮
│    set(key, value, ttl = CACHE_TTL) {
│        const data = {
│            value: value,
│            expires: Date.now() + ttl
│        };
│        localStorage.setItem(this.prefix + key, JSON.stringify(data));
⋮

docs/md_v2/marketplace/marketplace.js:
⋮
│class MarketplaceCache {
│    constructor() {
│        this.prefix = 'c4ai_market_';
│    }
│
│    get(key) {
│        const item = localStorage.getItem(this.prefix + key);
│        if (!item) return null;
│
│        const data = JSON.parse(item);
⋮
│    set(key, value, ttl = CACHE_TTL) {
│        const data = {
│            value: value,
│            expires: Date.now() + ttl
│        };
│        localStorage.setItem(this.prefix + key, JSON.stringify(data));
⋮
│class MarketplaceUI {
│    constructor() {
│        this.api = new MarketplaceAPI();
│        this.currentCategory = 'all';
│        this.currentType = '';
│        this.searchTimeout = null;
│        this.loadedApps = 10;
│        this.init();
│    }
│
⋮
│    async loadMainContent() {
│        // Load apps column
│        const apps = await this.api.getApps({ limit: 8 });
│        if (apps && apps.length) {
│            const appsGrid = document.getElementById('apps-grid');
│            appsGrid.innerHTML = apps.map(app => `
│                <div class="app-compact" onclick="marketplace.showAppDetail(${JSON.stringify(app).r
│                    <div class="app-compact-header">
│                        <span>${app.category}</span>
│                        <span>★ ${app.rating}/5</span>
⋮
│    showAppDetail(app) {
│        // Navigate to detail page instead of showing modal
│        const slug = app.slug || app.name.toLowerCase().replace(/\s+/g, '-');
│        window.location.href = `app-detail.html?app=${slug}`;
⋮

docs/releases_review/v0_4_3b2_features_demo.py:
⋮
│async def demo_proxy_rotation():
│    """
│    8. Proxy Rotation Demo
│    ===================
│    Demonstrates how to rotate proxies for each request using Crawl4ai.
⋮
│    async def get_next_proxy(proxy_file: str = "proxies.txt") -> Optional[Dict]:
⋮

tests/adaptive/compare_performance.py:
⋮
│def read_baseline():
⋮

tests/deep_crawling/test_deep_crawl_contextvar.py:
⋮
│class TestContextVarCrossContext:
│    """Tests that deep_crawl_active ContextVar works across task boundaries."""
│
│    @pytest.mark.asyncio
│    async def test_streaming_generator_consumed_in_different_task(self):
│        """
│        Core reproduction of issue #1917:
│        Create the generator in one task, consume it in another.
│        Before the fix, this raised ValueError.
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│    @pytest.mark.asyncio
│    async def test_batch_mode_in_different_task(self):
│        """Non-streaming mode should also work across task boundaries."""
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│class TestContextVarState:
│    """Tests that deep_crawl_active is properly managed."""
│
│    @pytest.mark.asyncio
│    async def test_flag_is_false_after_streaming_completes(self):
│        """deep_crawl_active should be False after the generator is exhausted."""
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│    @pytest.mark.asyncio
│    async def test_flag_is_false_after_batch_completes(self):
│        """deep_crawl_active should be False after batch mode completes."""
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│    @pytest.mark.asyncio
│    async def test_flag_is_true_during_deep_crawl(self):
│        """deep_crawl_active should be True while the generator is being consumed."""
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│    @pytest.mark.asyncio
│    async def test_flag_prevents_recursive_deep_crawl(self):
│        """When deep_crawl_active is True, nested calls should skip deep crawl."""
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│    @pytest.mark.asyncio
│    async def test_flag_reset_after_streaming_error(self):
│        """deep_crawl_active should be reset even if the generator raises."""
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│    @pytest.mark.asyncio
│    async def test_flag_reset_after_streaming_error_in_different_task(self):
│        """
│        Combines #1917 fix with error handling: generator raises in a different task.
│        Both the cross-context issue and error cleanup must work together.
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮
│class TestConcurrentRequests:
│    """Tests that multiple concurrent streaming deep crawls don't interfere."""
│
│    @pytest.mark.asyncio
│    async def test_concurrent_streaming_in_separate_tasks(self):
│        """
│        Multiple concurrent streaming requests consumed in separate tasks.
│        This simulates multiple clients hitting /crawl/stream simultaneously.
⋮
│        async def original_arun(url, config=None, **kwargs):
⋮

tests/docker/test_pool_release.py:
⋮
│class TestReleaseCrawler:
│    """Tests for the release_crawler function."""
│
⋮
│    @pytest.mark.asyncio
│    async def test_concurrent_releases_are_safe(self):
│        """Concurrent releases should not corrupt the counter."""
⋮
│        async def release_n_times(n):
⋮

tests/docker/test_serialization.py:
⋮
│def to_serializable_dict(obj: Any) -> Dict:
⋮
│def from_serializable_dict(data: Any) -> Any:
⋮
│def is_empty_value(value: Any) -> bool:
⋮

tests/loggers/test_logger.py:
⋮
│class AsyncFileLogger(AsyncLoggerBase):
│    """
│    File-only asynchronous logger that writes logs to a specified file.
⋮
│    def _write_to_file(self, level: str, message: str, tag: str):
⋮
│    def info(self, message: str, tag: str = "INFO", **kwargs):
⋮
│    def warning(self, message: str, tag: str = "WARNING", **kwargs):
⋮
│    def error(self, message: str, tag: str = "ERROR", **kwargs):
⋮

tests/memory/test_docker_config_gen.py:
⋮
│BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:11235"
⋮
│CASES = [
│    # --- CrawlRunConfig variants ---
│    "CrawlerRunConfig()",
│    "CrawlerRunConfig(stream=True, cache_mode=CacheMode.BYPASS)",
│    "CrawlerRunConfig(js_only=True, wait_until='networkidle')",
│
│    # --- BrowserConfig variants ---
│    "BrowserConfig()",
│    "BrowserConfig(headless=False, extra_args=['--disable-gpu'])",
│    "BrowserConfig(browser_mode='builtin', proxy_config={'server': 'http://1.2.3.4:8080'})",
⋮

tests/memory/test_stress_docker_api.py:
⋮
│def parse_args() -> argparse.Namespace:
⋮

tests/test_async_logger_stderr.py:
⋮
│AsyncLogger = _mod.AsyncLogger
⋮

tests/unit/test_sitemap_namespace_parsing.py:
⋮
│class _FakeBM25:
│    def __init__(self, corpus):
⋮
│    def get_scores(self, tokens):
⋮
│class DummyResponse:
│    def __init__(self, request_url: str, text: str):
│        self.status_code = 200
│        self._content = text.encode("utf-8")
⋮
│    def raise_for_status(self):
⋮
│class DummyAsyncClient:
⋮
```