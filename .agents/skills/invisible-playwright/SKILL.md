---
name: invisible-playwright
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging invisible-playwright. Use this skill whenever modifying invisible-playwright configurations or adding related functionality.
---
# invisible-playwright

## File Tree

```text
invisible-playwright/
├── modules
│   └── invisible_playwright (See AST Map below)
└── SKILL.md
```

### AST Map: `modules/invisible_playwright`

```python
examples/basic.py:
⋮
│def main() -> None:
⋮

examples/with_proxy.py:
⋮
│def main() -> None:
⋮

scripts/audit_cpt_realism.py:
⋮
│def write_pair_table(table, fname, meta):
⋮
│def write_class_table(table, fname, meta):
⋮
│def main():
⋮

scripts/ci_drive_gate.py:
⋮
│def main(exe: str, full: bool) -> int:
⋮

scripts/gen_release_notes.py:
⋮
│def changelog_bullets(source_repo: str, prev_sha: str, current_sha: str,
⋮
│def build_body(tag: str, current_sha: str, bullets: list[str]) -> str:
⋮
│def main() -> int:
⋮

scripts/run_e2e.py:
⋮
│def main() -> int:
⋮

src/invisible_playwright/_fpforge/_network.py:
⋮
│class Node:
│    """Single Bayesian node."""
│
⋮
│    def sample(self, context: Dict[str, Any], rng: random.Random) -> Any:
⋮
│class Network:
│    """Collection of nodes with topological sampling."""
│
⋮
│    def sample(
│        self,
│        rng: random.Random,
│        evidence: Optional[Dict[str, Any]] = None,
⋮
│def _weighted_pick(table: List[Dict[str, Any]], rng: random.Random) -> Any:
⋮
│def _parent_key(parents: List[str], context: Dict[str, Any]) -> str:
⋮
│def _topsort(nodes: List[Node]) -> List[Node]:
│    """Topological sort by parent-before-child."""
⋮
│    def visit(n: Node, path: set):
⋮

src/invisible_playwright/_fpforge/_sampler.py:
⋮
│def classify_gpu(gpu_value: Dict[str, str]) -> str:
⋮
│def _gpu_marginal():
⋮
│def _cpt_from_table(table: Dict[str, Any]) -> Dict[str, list]:
⋮
│def derive_font_prefs(gpu_class: str, rng) -> Dict[str, str]:
⋮
│def derive_browsing_history(gpu_class: str, rng) -> list:
⋮
│class Forge:
│    """Fingerprint forge — single seed → coherent bundle."""
│
⋮
│    def sample(self, fixed_gpu_class: Optional[str] = None) -> Dict[str, Any]:
⋮
│def sample(seed: int, fixed_gpu_class: Optional[str] = None) -> Dict[str, Any]:
⋮

src/invisible_playwright/_fpforge/profile.py:
⋮
│@dataclass(frozen=True)
│class GPUProfile:
⋮
│@dataclass(frozen=True)
│class ScreenProfile:
⋮
│@dataclass(frozen=True)
│class HardwareProfile:
⋮
│@dataclass(frozen=True)
│class AudioProfile:
⋮
│@dataclass(frozen=True)
│class CodecProfile:
⋮
│@dataclass(frozen=True)
│class WebGLProfile:
⋮
│def _validate_pin_key(key: str) -> None:
⋮
│@dataclass(frozen=True)
│class Profile:
⋮
│def _apply_pins_to_raw(raw: Dict[str, Any], pin: Dict[str, Any]) -> Dict[str, Any]:
⋮
│def generate_profile(
│    seed: int,
│    pin: Optional[Dict[str, Any]] = None,
│    fixed_gpu_class: Optional[str] = None,
⋮

src/invisible_playwright/_geo.py:
⋮
│class GeoTimezoneError(RuntimeError):
⋮
│def _proxy_is_set(proxy: Optional[Dict[str, str]]) -> bool:
⋮
│def _proxies_for_requests(proxy: Dict[str, str]) -> Dict[str, str]:
⋮
│def discover_egress_ip(
│    proxy: Optional[Dict[str, str]] = None, *, timeout: float = 10.0
⋮
│def ip_to_timezone(ip: str, mmdb_path: Any) -> str:
⋮
│class SessionGeo(NamedTuple):
⋮
│def prepare_session_geo(
│    timezone: str, proxy: Optional[Dict[str, str]]
⋮
│def resolve_session_timezone(
│    timezone: str, proxy: Optional[Dict[str, str]]
⋮

src/invisible_playwright/_headless.py:
⋮
│class _LinuxVirtualDisplay:
│    """Standalone Xvfb instance owned by this InvisiblePlaywright session."""
│
⋮
│    def start(self) -> None:
⋮
│    def _pick_display(self) -> str:
⋮
│    def _wait_until_ready(self, display: str) -> None:
⋮
│    def _apply_env(self, display: str) -> None:
⋮
│    def stop(self) -> None:
⋮
│def cloak_prefs() -> dict:
⋮
│def make_virtual_display():
⋮
│def _binary_on_path(name: str) -> bool:
⋮

src/invisible_playwright/_proxy.py:
⋮
│def configure_proxy(
│    proxy: Optional[Dict[str, str]],
│    prefs: Dict[str, Any],
⋮
│def _is_socks_scheme(server: str) -> bool:
⋮
│def _strip_scheme(server: str) -> str:
⋮

src/invisible_playwright/_recaptcha_seed.py:
⋮
│def _sub_seed(seed: int, tag: str) -> int:
⋮
│def _b64_rand(rng: random.Random, length: int) -> str:
⋮
│def _hex_rand(rng: random.Random, length: int) -> str:
⋮
│def _yyyymmdd_utc(ts: int) -> str:
⋮
│def _consent_region_lang(timezone: Optional[str]) -> tuple:
⋮
│def _google_cookies(rng: random.Random, now: int,
⋮
│def _norm_domain(domain: str) -> str:
⋮
│def _ga_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _gid_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _cf_bm_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _onetrust_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _cookieyes_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _clarity_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _fbp_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _gtm_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _hssrc_cookie(rng: random.Random, now: int, domain: str) -> dict:
⋮
│def _cookies_for_profile(profile: str, rng: random.Random,
⋮
│def build_cookies(seed: int,
│                  browsing_history: Optional[List[dict]] = None,
│                  now: Optional[int] = None,
⋮
│def _extract_seed_and_history(profile: Any) -> tuple:
⋮
│async def seed_recaptcha_cookies_async(context: Any, profile: Any,
⋮
│def seed_recaptcha_cookies_sync(context: Any, profile: Any,
⋮

src/invisible_playwright/_webgl_personas.py:
⋮
│def _gpu_pool() -> List[Dict]:
⋮
│def select_persona(seed: int) -> Optional[Dict]:
⋮
│def forced_gpu_class(seed: int) -> Optional[str]:
⋮
│def render_noise_seed(seed: int) -> int:
⋮

src/invisible_playwright/async_api.py:
⋮
│class InvisiblePlaywright:
│    """Async context manager — see invisible_playwright.InvisiblePlaywright for the sync variant.""
│
⋮
│    def _default_context_kwargs(self) -> Dict[str, Any]:
⋮
│    async def _teardown(self) -> None:
⋮

src/invisible_playwright/cli.py:
⋮
│def build_parser() -> argparse.ArgumentParser:
⋮
│def main(argv: list[str] | None = None) -> int:
⋮

src/invisible_playwright/config.py:
⋮
│def get_default_stealth_prefs(
│    seed: Optional[int] = None,
│    *,
│    pin: Optional[Dict[str, Any]] = None,
│    locale: str = "en-US",
│    timezone: str = "",
│    extra_prefs: Optional[Dict[str, Any]] = None,
│    humanize: Union[bool, float] = True,
│    virtual_display: bool = False,
⋮

src/invisible_playwright/constants.py:
⋮
│BINARY_VERSION: str = "firefox-12"
│
⋮
│BROKEN_VERSIONS: frozenset[str] = frozenset({"firefox-8"})
│
⋮
│FIREFOX_UPSTREAM_VERSION: str = "150.0.1"
│
⋮
│BINARY_BASENAME: str = f"firefox-{FIREFOX_UPSTREAM_VERSION}-stealth"
│
⋮
│def ARCHIVE_NAME(platform_key: str, machine: str) -> str:
⋮
│BINARY_ENTRY_REL = {
│    "win32": "firefox.exe",
│    "linux": "firefox",
│    "darwin": "Firefox.app/Contents/MacOS/firefox",
⋮
│RELEASE_URL_TEMPLATE = (
│    "https://github.com/feder-cr/invisible_playwright/releases/download/{tag}/{asset}"
⋮
│GEOIP_REPO: str = "daijro/geoip-all-in-one"
│GEOIP_ASSET: str = "geoip-aio-all.mmdb.zip"
│GEOIP_MMDB_NAME: str = "geoip-aio-all.mmdb"
│GEOIP_RELEASE_URL_TEMPLATE: str = (
│    "https://github.com/daijro/geoip-all-in-one/releases/download/{tag}/{asset}"
⋮

src/invisible_playwright/download.py:
⋮
│def _github_token() -> str | None:
⋮
│def cache_root() -> Path:
⋮
│def cache_dir_for_version(version: str = BINARY_VERSION) -> Path:
⋮
│def _resolve_asset_url(tag: str, asset_name: str) -> str:
⋮
│def _download_file(url: str, dst: Path, chunk_size: int = 1 << 16) -> None:
⋮
│def _parse_checksums(text: str) -> dict[str, str]:
⋮
│def _extract(archive: Path, dst: Path) -> None:
⋮
│def ensure_binary(version: str = BINARY_VERSION) -> Path:
⋮
│def _geoip_root() -> Path:
⋮
│def _cached_geoip_mmdb() -> Path | None:
⋮
│def _resolve_latest_geoip_tag() -> str | None:
⋮
│def ensure_geoip_mmdb() -> Path:
⋮

src/invisible_playwright/launcher.py:
⋮
│class InvisiblePlaywright:
│    """Context manager launching a patched Firefox with a deterministic profile.
│
│    Usage:
│
│        from invisible_playwright import InvisiblePlaywright
│
│        # random seed (different fingerprint each call)
│        with InvisiblePlaywright() as browser:
│            page = browser.new_page()
│            page.goto("https://example.com")
│
⋮
│    def _default_context_kwargs(self) -> Dict[str, Any]:
⋮

src/invisible_playwright/prefs.py:
⋮
│def translate_profile_to_prefs(
│    profile: Profile,
│    *,
│    locale: str = "en-US",
│    timezone: str = "",
│    extra_prefs: Optional[Dict[str, Any]] = None,
│    virtual_display: bool = False,
⋮

tests/test_build.py:
⋮
│@pytest.mark.slow
│def test_built_wheel_has_no_duplicate_entries(tmp_path):
⋮

tests/test_detectors_e2e.py:
⋮
│class _DetectorSite:
│    """Localhost server: `/` → BotD+FPJS+fpscanner page, `/creepjs` → CreepJS page,
⋮
│    def close(self):
⋮

tests/test_e2e.py:
⋮
│@pytest.mark.e2e
│def test_e10_linux_resolve_headless_invokes_xvfb_dispatcher(monkeypatch):
│    """E10: ``_resolve_headless`` with ``headless=True`` on Linux must
│    call ``make_virtual_display().start()`` and store the result on
│    ``self._virtual_display``. We stub the dispatcher so no real Xvfb
│    is spawned — the dispatcher's platform routing is covered separately
⋮
│    class _FakeDisplay:
│        def start(self) -> None:
⋮
│@pytest.mark.e2e
│def test_e11_linux_teardown_stops_virtual_display_and_is_idempotent(monkeypatch):
│    """E11: ``_teardown`` stops the Linux virtual display, clears the
│    reference, and a second invocation is a no-op. Guards the cleanup
⋮
│    class _FakeDisplay:
│        def start(self) -> None:
⋮

tests/test_geo.py:
⋮
│class _FakeResp:
│    def __init__(self, text, status=200):
│        self.text = text
⋮
│    def raise_for_status(self):
⋮
│class _FakeReader:
│    def __init__(self, record):
⋮
│    def get(self, ip):
⋮
│def _install_fake_maxminddb(monkeypatch, record):
⋮

tests/test_imports.py:
⋮
│def test_top_level_import():
⋮
│def test_version_string():
⋮
│def test_sync_api_module():
⋮
│def test_async_api_module_importable():
⋮
│def test_async_class_is_distinct_from_sync():
⋮
│@pytest.mark.parametrize("name", [
│    "constants",
│    "download",
│    "prefs",
│    "launcher",
│    "cli",
│    "_proxy",
│    "_fpforge",
│])
│def test_submodule_importable(name):
⋮
│def test_dunder_all_is_complete():
⋮

tests/test_proxy_socks_auth_e2e.py:
⋮
│class _Socks5AuthRecorder:
│    """SOCKS5 that REQUIRES RFC1929 user/pass auth, records the creds it saw,
⋮
│    def close(self):
⋮
│class _LocalHTTP:
│    """A tiny localhost HTTP server — the CONNECT target relayed by the proxy."""
│
⋮
│    def close(self):
⋮

tests/test_release_e2e.py:
⋮
│def _venv_python(venv: Path) -> Path:
⋮

tests/test_webrtc_realness.py:
⋮
│def parse_candidate(line):
⋮
│def decode_priority(prio):
⋮
│def host_candidates(cands):
⋮
│def srflx_candidates(cands):
⋮
│def host_is_mdns(cands):
⋮
│def srflx_realness(cand, expected_ip=None):
⋮
│def creep_get_ipaddress(sdp):
⋮
│class _Socks5TcpOnly:
│    """Minimal SOCKS5: no-auth, CONNECT (TCP) relayed, UDP ASSOCIATE refused.
│
│    Reproduces a residential TCP-only proxy: pages load over TCP, but WebRTC's
│    UDP path is dead — which (for a no-camera page in default_address_only mode)
│    is exactly what made the default-route probe fail and ICE return zero
│    candidates before Fix C.
⋮
│    def close(self):
⋮

tests/vendor/botd-2.0.0.esm.js:
⋮
│class BotdError extends Error {
│    /**
│     * Creates a new BotdError.
│     *
│     * @class
│     */
│    constructor(state, message) {
│        super(message);
│        this.state = state;
│        this.name = 'BotdError';
⋮
│function arrayIncludes(arr, value) {
│    return arr.indexOf(value) !== -1;
│}
│function strIncludes(str, value) {
│    return str.indexOf(value) !== -1;
│}
│function arrayFind(array, callback) {
│    if ('find' in array)
│        return array.find(callback);
│    for (let i = 0; i < array.length; i++) {
│        if (callback(array[i], i, array))
│            return array[i];
│    }
│    return undefined;
⋮
│function getObjectProps(obj) {
│    return Object.getOwnPropertyNames(obj);
│}
│function includes(arr, ...keys) {
│    for (const key of keys) {
│        if (typeof key === 'string') {
│            if (arrayIncludes(arr, key))
│                return true;
│        }
│        else {
│            const match = arrayFind(arr, (value) => key.test(value));
│            if (match != null)
│                return true;
⋮
│function countTruthy(values) {
│    return values.reduce((sum, value) => sum + (value ? 1 : 0), 0);
⋮
│function getBrowserEngineKind() {
│    var _a, _b;
│    // Based on research in October 2020. Tested to detect Chromium 42-86.
│    const w = window;
│    const n = navigator;
│    if (countTruthy([
│        'webkitPersistentStorage' in n,
│        'webkitTemporaryStorage' in n,
│        n.vendor.indexOf('Google') === 0,
│        'webkitResolveLocalFileSystemURL' in w,
⋮
│function isChromium86OrNewer() {
│    // Checked in Chrome 85 vs Chrome 86 both on desktop and Android. Checked in macOS Chrome 128, 
│    const w = window;
│    return (countTruthy([
│        !('MediaSettingsRange' in w),
│        'RTCEncodedAudioFrame' in w,
│        '' + w.Intl === '[object Intl]',
│        '' + w.Reflect === '[object Reflect]',
│    ]) >= 3);
⋮
│class BotDetector {
│    constructor() {
│        this.components = undefined;
│        this.detections = undefined;
│    }
│    getComponents() {
│        return this.components;
│    }
│    getDetections() {
│        return this.detections;
⋮
│async function load({ monitoring = true } = {}) {
│    if (monitoring) {
│        monitor();
│    }
│    const detector = new BotDetector();
│    await detector.collect();
│    return detector;
⋮

tests/vendor/creepjs-10aa672.js:
⋮
│    const getUserAgentPlatform = ({ userAgent, excludeBuild = true }) => {
│        if (!userAgent) {
│            return 'unknown';
│        }
│        // patterns
│        const nonPlatformParenthesis = /\((khtml|unlike|vizio|like gec|internal dummy|org\.eclipse|
│        const parenthesis = /\((.+)\)/;
│        const android = /((android).+)/i;
│        const androidNoise = /^(linux|[a-z]|wv|mobile|[a-z]{2}(-|_)[a-z]{2}|[a-z]{2})$|windows|(rv:
│        const androidBuild = /build\/.+\s|\sbuild\/.+/i;
⋮
│        const isDevice = (list, device) => list.filter((x) => device.test(x)).length;
⋮
│    const createPerformanceLogger = () => {
│        const log = {};
│        let total = 0;
│        return {
│            logTestResult: ({ test, passed, time = 0 }) => {
│                total += time;
│                const timeString = `${time.toFixed(2)}ms`;
│                log[test] = timeString;
│                const color = passed ? '#4cca9f' : 'lightcoral';
│                const result = passed ? 'passed' : 'failed';
│                const symbol = passed ? '✔' : '-';
│                return console.log(`%c${symbol}${time ? ` (${timeString})` : ''} ${test} ${result}`
│            },
⋮
│    const createTimer = () => {
│        let start = 0;
│        const log = [];
│        return {
│            stop: () => {
│                if (start) {
│                    log.push(performance.now() - start);
│                    return log.reduce((acc, n) => acc += n, 0);
│                }
│                return start;
│            },
│            start: () => {
│                start = performance.now();
│                return start;
⋮
│    const queueEvent = (timer, delay = 0) => {
│        timer.stop();
│        return new Promise((resolve) => setTimeout(() => resolve(timer.start()), delay))
│            .catch((e) => { });
│    };
│    const formatEmojiSet = (emojiSet, limit = 3) => {
│        const maxLen = (limit * 2) + 3;
│        const list = (emojiSet || []);
│        return list.length > maxLen ? `${emojiSet.slice(0, limit).join('')}...${emojiSet.slice(-lim
│            list.join('');
⋮
│    const hashSlice = (x) => !x ? x : x.slice(0, 8);
⋮
│    const createErrorsCaptured = () => {
│        const errors = [];
│        return {
│            getErrors: () => errors,
│            captureError: (error, customMessage = '') => {
│                const type = {
│                    Error: true,
│                    EvalError: true,
│                    InternalError: true,
│                    RangeError: true,
│                    ReferenceError: true,
│                    SyntaxError: true,
│                    TypeError: true,
│                    URIError: true,
⋮
│    function createLieRecords() {
│        const records = {};
│        return {
│            getRecords: () => records,
│            documentLie: (name, lie) => {
│                const isArray = lie instanceof Array;
│                if (records[name]) {
│                    if (isArray) {
│                        return (records[name] = [...records[name], ...lie]);
│                    }
│                    return records[name].push(lie);
│                }
│                return isArray ? (records[name] = lie) : (records[name] = [lie]);
⋮
│    function getRandomValues() {
│        return (String.fromCharCode(Math.random() * 26 + 97) +
│            Math.random().toString(36).slice(-7));
⋮
│    function failsTypeError({ spawnErr, withStack, final }) {
│        try {
│            spawnErr();
│            throw Error();
│        }
│        catch (err) {
│            if (!isTypeError(err))
│                return true;
│            return withStack ? withStack(err) : false;
│        }
⋮
│    function hasValidStack(err, reg, i = 1) {
│        if (i === 0)
│            return reg.test(err.message);
│        return reg.test(err.stack.split('\n')[i]);
⋮
│    function createLieDetector(scope) {
│        const isSupported = (obj) => typeof obj != 'undefined' && !!obj;
│        const props = {}; // lie list and detail
│        const propsSearched = []; // list of properties searched
│        return {
│            getProps: () => props,
│            getPropsSearched: () => propsSearched,
│            searchLies: (fn, config) => {
│                const { target, ignore } = config || {};
│                let obj;
│                // check if api is blocked or not supported
│                try {
│                    obj = fn();
│                    if (!isSupported(obj)) {
│                        return;
│                    }
│                }
⋮
│    const createTrashBin = () => {
│        const bin = [];
│        return {
│            getBin: () => bin,
│            sendToTrash: (name, val, response = undefined) => {
│                const proxyLike = proxyBehavior(val);
│                const value = !proxyLike ? val : 'proxy behavior detected';
│                bin.push({ name, value });
│                return response;
│            },
⋮
│    async function spawnWorker() {
│        const ask = (fn) => {
│            try {
│                return fn();
│            }
│            catch (e) {
│                return;
│            }
│        };
│        function getWorkerPrototypeLies(scope) {
⋮
│        const getUserAgentData = async (navigator) => {
│            if (!('userAgentData' in navigator)) {
│                return;
│            }
│            const data = await navigator.userAgentData.getHighEntropyValues(['platform', 'platformV
│            const { brands, mobile } = navigator.userAgentData || {};
│            const compressedBrands = (brands, captureVersion = false) => brands
│                .filter((obj) => !/Not/.test(obj.brand)).map((obj) => `${obj.brand}${captureVersion
│            const removeChromium = (brands) => (brands.length > 1 ? brands.filter((brand) => !/Chro
│            // compress brands
⋮
│        const computeTimezoneOffset = () => {
│            const date = new Date().getDate();
│            const month = new Date().getMonth();
│            // @ts-ignore
│            const year = Date().split ` `[3]; // current year
│            const format = (n) => ('' + n).length == 1 ? `0${n}` : n;
│            const dateString = `${month + 1}/${format(date)}/${year}`;
│            const dateStringUTC = `${year}-${format(month + 1)}-${format(date)}`;
│            // @ts-ignore
│            const utc = Date.parse(new Date(dateString));
⋮
│    const hashMini = (x) => {
│        const json = `${JSON.stringify(x)}`;
│        const hash = json.split('').reduce((hash, char, i) => {
│            return Math.imul(31, hash) + json.charCodeAt(i) | 0;
│        }, 0x811c9dc5);
│        return ('0000000' + (hash >>> 0).toString(16)).substr(-8);
⋮
│    const paintCanvas = ({ canvas, context, strokeText = false, cssFontFamily = '', area = { width:
│        if (!context) {
│            return;
│        }
│        context.clearRect(0, 0, canvas.width, canvas.height);
│        canvas.width = area.width;
│        canvas.height = area.height;
│        if (canvas.style) {
│            canvas.style.display = 'none';
│        }
│        const createPicassoSeed = ({ seed, offset, multiplier }) => {
│            let current = Number(seed) % Number(offset);
│            const getNextSeed = () => {
│                current = (Number(multiplier) * current) % Number(offset);
│                return current;
│            };
│            return {
│                getNextSeed,
│            };
⋮
│        const patchSeed = (current, offset, maxBound, computeFloat) => {
│            const result = (((current - 1) / offset) * (maxBound || 1)) || 0;
│            return computeFloat ? result : Math.floor(result);
⋮
│    async function getClientRects() {
│        try {
│            const timer = createTimer();
│            await queueEvent(timer);
│            const toNativeObject = (domRect) => {
│                return {
│                    bottom: domRect.bottom,
│                    height: domRect.height,
│                    left: domRect.left,
│                    right: domRect.right,
│                    width: domRect.width,
│                    top: domRect.top,
│                    x: domRect.x,
│                    y: domRect.y,
⋮
│    function clientRectsHTML(fp) {
│        if (!fp.clientRects) {
│            return `
│		<div class="col-six undefined">
│			<strong>DOMRect</strong>
│			<div>elems A: ${HTMLNote.BLOCKED}</div>
│			<div>elems B: ${HTMLNote.BLOCKED}</div>
│			<div>range A: ${HTMLNote.BLOCKED}</div>
│			<div>range B: ${HTMLNote.BLOCKED}</div>
│			<div class="block-text">${HTMLNote.BLOCKED}</div>
⋮
│        const computeDiffs = (rects) => {
│            if (!rects || !rects.length) {
│                return;
│            }
│            const expectedSum = rects.reduce((acc, rect) => {
│                const { right, left, width, bottom, top, height } = rect;
│                const expected = {
│                    width: right - left,
│                    height: bottom - top,
│                    right: left + width,
⋮
│    function getPlatformEstimate() {
│        if (!IS_BLINK)
│            return [];
│        const v80 = 'getVideoPlaybackQuality' in HTMLVideoElement.prototype;
│        const v81 = CSS.supports('color-scheme: initial');
│        const v84 = CSS.supports('appearance: initial');
│        const v86 = 'DisplayNames' in Intl;
│        const v88 = CSS.supports('aspect-ratio: initial');
│        const v89 = CSS.supports('border-end-end-radius: initial');
│        const v95 = 'randomUUID' in Crypto.prototype;
⋮
│        const hasFeature = (version, condition) => {
│            return (version ? [condition] : []);
⋮
│    async function getNavigator(workerScope) {
│        try {
│            const timer = createTimer();
│            await queueEvent(timer);
│            let lied = (lieProps['Navigator.appVersion'] ||
│                lieProps['Navigator.deviceMemory'] ||
│                lieProps['Navigator.doNotTrack'] ||
│                lieProps['Navigator.hardwareConcurrency'] ||
│                lieProps['Navigator.language'] ||
│                lieProps['Navigator.languages'] ||
│                lieProps['Navigator.maxTouchPoints'] ||
⋮
│            const getUserAgentData = () => attempt(() => {
│                // @ts-ignore
│                if (!navigator.userAgentData ||
│                    // @ts-ignore
│                    !navigator.userAgentData.getHighEntropyValues) {
│                    return;
│                }
│                // @ts-ignore
│                return navigator.userAgentData.getHighEntropyValues(['platform', 'platformVersion',
│                    // @ts-ignore
│                    const { brands, mobile } = navigator.userAgentData || {};
│                    const compressedBrands = (brands, captureVersion = false) => brands
│                        .filter((obj) => !/Not/.test(obj.brand)).map((obj) => `${obj.brand}${captur
│                    const removeChromium = (brands) => (brands.length > 1 ? brands.filter((brand) =
│                    // compress brands
│                    if (!data.brands) {
│                        data.brands = brands;
│                    }
⋮
│            const getPermissions = () => attempt(() => {
│                const getPermissionState = (name) => navigator.permissions.query({ name })
│                    .then((res) => ({ name, state: res.state }))
│                    .catch((error) => ({ name, state: 'unknown' }));
│                // https://w3c.github.io/permissions/#permission-registry
│                const permissions = !('permissions' in navigator) ? undefined : Promise.all([
│                    getPermissionState('accelerometer'),
│                    getPermissionState('ambient-light-sensor'),
│                    getPermissionState('background-fetch'),
│                    getPermissionState('background-sync'),
⋮
│    async function getResistance() {
│        try {
│            const timer = createTimer();
│            await queueEvent(timer);
│            const data = {
│                privacy: undefined,
│                security: undefined,
│                mode: undefined,
│                extension: undefined,
│                engine: (IS_BLINK ? 'Blink' :
│                    IS_GECKO ? 'Gecko' :
⋮
│            const getExtension = ({ pattern, hash, prototypeLiesLen }) => {
│                const { noscript, trace, cydec, canvasblocker, chameleon, duckduckgo, privacybadger
│                const disabled = 'c767712b';
│                if (prototypeLiesLen) {
│                    if (prototypeLiesLen >= 7 &&
│                        trace.contentDocumentHash.includes(hash.contentDocumentHash) &&
│                        trace.contentWindowHash.includes(hash.contentWindowHash) &&
│                        trace.createElementHash.includes(hash.createElementHash) &&
│                        trace.getElementByIdHash.includes(hash.getElementByIdHash) &&
│                        trace.toDataURLHash.includes(hash.toDataURLHash) &&
⋮
│    async function getVoices() {
│        // Don't run voice immediately. This is unstable
│        // wait a bit for services to load
│        await new Promise((resolve) => setTimeout(() => resolve(undefined), 50));
│        return new Promise(async (resolve) => {
│            try {
│                const timer = createTimer();
│                await queueEvent(timer);
│                // use window since iframe is unstable in FF
│                const supported = 'speechSynthesis' in window;
│                supported && speechSynthesis.getVoices(); // warm up
│                if (!supported) {
│                    logTestResult({ test: 'speech', passed: false });
│                    return resolve(null);
│                }
⋮
│                const getVoices = () => {
│                    const data = speechSynthesis.getVoices();
│                    const localServiceDidLoad = (data || []).find((x) => x.localService);
│                    if (!data || !data.length || (IS_BLINK && !localServiceDidLoad)) {
│                        return;
│                    }
│                    clearTimeout(giveUpOnVoices);
│                    // filter first occurrence of unique voiceURI data
│                    const getUniques = (data, voiceURISet) => data
│                        .filter((x) => {
⋮
│    function getTimezone() {
│        // inspired by https://arkenfox.github.io/TZP
│        // https://github.com/vvo/tzdb/blob/master/time-zones-names.json
│        const cities = [
│            'UTC',
│            'GMT',
│            'Etc/GMT+0',
│            'Etc/GMT+1',
│            'Etc/GMT+10',
│            'Etc/GMT+11',
⋮
│        const getTimezoneOffset = () => {
│            const [year, month, day] = JSON.stringify(new Date())
│                .slice(1, 11)
│                .split('-');
│            const dateString = `${month}/${day}/${year}`;
│            const dateStringUTC = `${year}-${month}-${day}`;
│            const now = +new Date(dateString);
│            const utc = +new Date(dateStringUTC);
│            const offset = +((now - utc) / 60000);
│            return ~~offset;
⋮
│        const decryptLocation = ({ year, timeZone }) => {
│            const system = getTimezoneOffsetHistory({ year });
│            const resolvedOptions = getTimezoneOffsetHistory({ year, city: timeZone });
│            const filter = (cities) => cities
│                .filter((city) => system == getTimezoneOffsetHistory({ year, city }));
│            // get city region set
│            const decryption = (system == resolvedOptions ? [timeZone] : binarySearch(cities, filte
│            // reduce set to one city
│            const decrypted = (decryption.length == 1 && decryption[0] == timeZone ? timeZone : has
│            return decrypted;
⋮
│    async function getCanvasWebgl() {
│        // use short list to improve performance
│        const getParamNames = () => [
│            // 'BLEND_EQUATION',
│            // 'BLEND_EQUATION_RGB',
│            // 'BLEND_EQUATION_ALPHA',
│            // 'BLEND_DST_RGB',
│            // 'BLEND_SRC_RGB',
│            // 'BLEND_DST_ALPHA',
│            // 'BLEND_SRC_ALPHA',
⋮
│        try {
│            const timer = createTimer();
│            await queueEvent(timer);
│            // detect lies
│            const dataLie = lieProps['HTMLCanvasElement.toDataURL'];
│            const contextLie = lieProps['HTMLCanvasElement.getContext'];
│            const parameterOrExtensionLie = (lieProps['WebGLRenderingContext.getParameter'] ||
│                lieProps['WebGL2RenderingContext.getParameter'] ||
│                lieProps['WebGLRenderingContext.getExtension'] ||
│                lieProps['WebGL2RenderingContext.getExtension']);
⋮
│            const getContext = (canvas, contextType) => {
│                try {
│                    if (contextType == 'webgl2') {
│                        return (canvas.getContext('webgl2') ||
│                            canvas.getContext('experimental-webgl2'));
│                    }
│                    return (canvas.getContext('webgl') ||
│                        canvas.getContext('experimental-webgl') ||
│                        canvas.getContext('moz-webgl') ||
│                        canvas.getContext('webkit-3d'));
⋮
│            const getShaderPrecisionFormat = (gl, shaderType) => {
│                if (!gl) {
│                    return;
│                }
│                const LOW_FLOAT = attempt(() => gl.getShaderPrecisionFormat(gl[shaderType], gl.LOW_
│                const MEDIUM_FLOAT = attempt(() => gl.getShaderPrecisionFormat(gl[shaderType], gl.M
│                const HIGH_FLOAT = attempt(() => gl.getShaderPrecisionFormat(gl[shaderType], gl.HIG
│                const HIGH_INT = attempt(() => gl.getShaderPrecisionFormat(gl[shaderType], gl.HIGH_
│                return {
│                    LOW_FLOAT,
⋮
│            const getSupportedExtensions = (gl) => {
│                if (!gl) {
│                    return [];
│                }
│                const ext = attempt(() => gl.getSupportedExtensions());
│                if (!ext) {
│                    return [];
│                }
│                return ext;
⋮
│    const getCapabilities = (sdp) => {
│        const videoDescriptors = ((/m=video [^\s]+ [^\s]+ ([^\n|\r]+)/.exec(sdp) || [])[1] || '').s
│        const audioDescriptors = ((/m=audio [^\s]+ [^\s]+ ([^\n|\r]+)/.exec(sdp) || [])[1] || '').s
│        const rtxCounter = createCounter();
│        return {
│            audio: constructDescriptions({
│                mediaType: 'audio',
│                sdp,
│                sdpDescriptors: audioDescriptors,
│                rtxCounter,
⋮
│    !async function () {
│        const scope = await spawnWorker();
│        if (scope == 0 /* Scope.WORKER */) {
│            return;
│        }
│        const isBrave = IS_BLINK ? await braveBrowser() : false;
│        const braveMode = isBrave ? getBraveMode() : {};
│        const braveFingerprintingBlocking = isBrave && (braveMode.standard || braveMode.strict);
│        const fingerprint = async () => {
│            const timeStart = timer();
⋮
│        const hardenEntropy = (workerScope, prop) => {
│            return (!workerScope ? prop :
│                (workerScope.localeEntropyIsTrusty && workerScope.localeIntlEntropyIsTrusty) ? prop
│                    undefined);
⋮

tests/vendor/fingerprintjs-5.2.0.umd.min.js:
⋮
│!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?e(exports):"function"==typeof d

tests/vendor/fpscanner-1.0.6.es.js:
⋮
│function f(t) {
│  let e = 0;
│  for (let n = 0, i = t.length; n < i; n++) {
│    let a = t.charCodeAt(n);
│    e = (e << 5) - e + a, e |= 0;
│  }
│  return e.toString(16).padStart(8, "0");
⋮
│function c(t) {
│  try {
│    return t();
│  } catch {
│    return !1;
│  }
⋮
│function b(t) {
│  return typeof t != "string" || t.length === 0 ? !0 : t === s || t === l || t === v || t === r;
⋮
│class vt {
│  constructor() {
│    this.fingerprint = {
│      signals: {
│        // Automation/Bot detection signals
│        automation: {
│          webdriver: r,
│          webdriverWritable: r,
│          selenium: r,
│          cdp: r,
⋮
│  async collectSignal(e) {
│    try {
│      return await e();
│    } catch {
│      return l;
│    }
⋮
│  generateFingerprintScannerId() {
│    try {
│      const e = this.fingerprint.signals, n = this.fingerprint.fastBotDetectionDetails, i = "FS1", 
│        n.headlessChromeScreenResolution.detected,
│        n.hasWebdriver.detected,
│        n.hasWebdriverWritable.detected,
│        n.hasSeleniumProperty.detected,
│        n.hasCDP.detected,
│        n.hasPlaywright.detected,
│        n.hasImpossibleDeviceMemory.detected,
⋮
│  async encryptFingerprint(e) {
│    const n = "__DEFAULT_FPSCANNER_KEY__";
│    return n.length > 20 && n.indexOf("DEFAULT") > 0 && n.indexOf("FPSCANNER") > 0 && console.warn(
│      '[fpscanner] WARNING: Using default encryption key! Run "npx fpscanner build --key=your-secre
│    ), await pt(JSON.stringify(e), n);
⋮
│  getDetectionRules() {
│    return [
│      { name: "headlessChromeScreenResolution", severity: h, test: $e },
│      { name: "hasWebdriver", severity: h, test: Qe },
│      { name: "hasWebdriverWritable", severity: h, test: st },
│      { name: "hasSeleniumProperty", severity: h, test: qe },
│      { name: "hasCDP", severity: h, test: Ke },
│      { name: "hasPlaywright", severity: h, test: Je },
│      { name: "hasImpossibleDeviceMemory", severity: h, test: Ye },
│      { name: "hasHighCPUCount", severity: h, test: Ze },
⋮
│  runDetectionRules() {
│    const e = this.getDetectionRules(), n = {
│      headlessChromeScreenResolution: { detected: !1, severity: "high" },
│      hasWebdriver: { detected: !1, severity: "high" },
│      hasWebdriverWritable: { detected: !1, severity: "high" },
│      hasSeleniumProperty: { detected: !1, severity: "high" },
│      hasCDP: { detected: !1, severity: "high" },
│      hasPlaywright: { detected: !1, severity: "high" },
│      hasImpossibleDeviceMemory: { detected: !1, severity: "high" },
│      hasHighCPUCount: { detected: !1, severity: "high" },
⋮
```