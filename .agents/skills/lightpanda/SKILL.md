---
name: lightpanda
description: Provides specialized context, rules, and tools for implementing, configuring, and debugging lightpanda. Use this skill whenever modifying lightpanda configurations or adding related functionality.
---
# lightpanda

## File Tree

```text
lightpanda/
├── assets
├── modules
│   └── browser (See AST Map below)
├── references
├── scripts
└── SKILL.md
```

> **Agent Instructions:** The AST maps below provide a high-level overview of the `modules/` directory. Note that the complete repository source code is available within the `modules/` folder. You can and should use your file reading tools to access the actual source code within `modules/` for complete details, implementation logic, and context beyond what the AST map provides.

### AST Map: `modules/browser`

```python
src/agent/SlashCommand.zig:
⋮
│//! REPL-only meta slash commands (`/help`, `/quit`, `/verbosity`, `/effort`,
⋮
│const std = @import("std");
│const lp = @import("lightpanda");
│const Command = lp.Command;
│const Config = lp.Config;
│
│/// Row format for the `/help` listing — `name` carries no leading `/`.
│pub const Help = struct {
│    name: []const u8,
│    description: []const u8,
⋮
│pub const MetaCommand = struct {
│    tag: Tag,
│    name: [:0]const u8,
│    /// Ghost-text fragment shown after the name + space. Empty when the command
│    /// takes no args (`/help`, `/quit`).
│    hint: []const u8,
│    /// Tab-completion candidates for the first positional arg.
│    values: []const []const u8,
│    /// Terse one-liner for the `/help` listing; longer per-command detail is
│    /// rendered by `Agent.printSlashHelp`.
⋮
│    /// Dispatched by `Agent.handleMeta` via an exhaustive switch, so a new meta
│    /// command is a compile error until it's wired up there too.
│    const Tag = enum { help, quit, verbosity, effort, usage, clear, reset, save, load, model, provi
⋮
│const tagNames = Config.tagNames;
│const tagHint = Config.tagHint;
│
│pub const meta_commands = [_]MetaCommand{
│    .{ .tag = .help, .name = "help", .hint = "[command]", .values = &.{}, .description = "List comm
│    .{ .tag = .quit, .name = "quit", .hint = "", .values = &.{}, .description = "Exit the REPL" },
│    .{ .tag = .verbosity, .name = "verbosity", .hint = tagHint(Config.AgentVerbosity), .values = ta
│    .{ .tag = .effort, .name = "effort", .hint = tagHint(Config.Effort), .values = tagNames(Config.
│    .{ .tag = .usage, .name = "usage", .hint = "", .values = &.{}, .description = "Show token usage
│    .{ .tag = .clear, .name = "clear", .hint = "", .values = &.{}, .description = "Clear conversati
│    .{ .tag = .reset, .name = "reset", .hint = "", .values = &.{}, .description = "Reset conversati
│    .{ .tag = .save, .name = "save", .hint = "[filename.js] [prompt]", .values = &.{}, .description
│    .{ .tag = .load, .name = "load", .hint = "<path>", .values = &.{}, .description = "Load and run
⋮
│/// Derived from `Command.LlmCommand` — name and description both come from the
│/// enum, so a new trigger there surfaces here automatically.
│pub const llm_commands = blk: {
│    const values = std.enums.values(Command.LlmCommand);
│    var rows: [values.len]Help = undefined;
│    for (values, &rows) |lc, *row| row.* = .{ .name = @tagName(lc), .description = lc.description()
│    break :blk rows;
⋮
│pub fn findMeta(name: []const u8) ?*const MetaCommand {
│    for (&meta_commands) |*m| {
│        if (std.ascii.eqlIgnoreCase(m.name, name)) return m;
│    }
│    return null;
⋮

src/agent/welcome.zig:
⋮
│//! The agent REPL's startup banner: a pre-colored braille panda logo with the
⋮
│const std = @import("std");
│const lp = @import("lightpanda");
│const Terminal = @import("Terminal.zig");
│
⋮
│const logo =
│    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m\n" ++
│    "⠀⠀⠀⠀⠀⠀⠀\x1b[38;2;247;247;239m⣀⣴⣶⣿⣿⣿⣿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀\x1b[0m\n" ++
│    "⠀⠀⠀⠀\x1b[38;2;247;247;239m⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣆⠀⠀⠀\x1b[0m\n" ++
│    "⠀⠀⠀\x1b[38;2;247;247;239m⢠⣾⣿⣿⣿⣿⠉⠈⣉⣭⣭⣥⣤⡀⣿⣿⣿⣿⣷⡀⠀\x1b[0m\n" ++
│    "⠀⠀\x1b[38;2;247;247;239m⢀⣿⠿⠟⠛⠛⠛⢠⣾⣿⠟⠛⢿⣿⠛⢎⢿⣿⣿⣿⣷⡀\x1b[0m\n" ++
│    "⠀⠀\x1b[38;2;247;247;239m⢸⣀⠀⠀⠀⠀⠀⣿⣿⣿⠀⢠⣼⡿⠾⣺⢸⣿⣿⣿⣿⡇\x1b[0m\n" ++
│    "⠀⠀\x1b[38;2;247;247;239m⢸⣿⣿⣷⣶⣤⡀⠹⣿⣿⣿⣿⣟⣗⣐⠟⠸⣿⣿⣿⣿⡇\x1b[0m\n" ++
│    "⠀⠀\x1b[38;2;247;247;239m⠸⣿⣿⣿⣿⡿⠓⠀⠈⠛⠻⠿⠟⠛⠁⠀⠀⠘⣿⣿⣿⠇\x1b[0m\n" ++
│    "⠀⠀\x1b[38;2;8;132;177m⢀⣼⣿⣿⣿⣶⣶\x1b[38;2;247;247;239m⣼⣶⡇⠀⠀⠀⠀⠀⢀⠀⠀⠘⣿⠏⠀\x1b[0m\n" ++
⋮
│const logo_cols = 24; // braille cells per row
│const logo_rows = blk: {
│    @setEvalBranchQuota(20000);
│    var n: usize = 0;
│    var it = std.mem.splitScalar(u8, logo, '\n');
│    while (it.next()) |line| {
│        if (line.len != 0) n += 1;
│    }
│    break :blk n;
│};
│const welcome_gap = "   ";
│
│/// Banner text. Kept narrow enough that logo + gap + widest line fits in 80
⋮
│const banner_tagline_llm = "Control the browser with natural language";
│const banner_tagline_basic = "Basic REPL (--no-llm) — commands only";
│const banner_setup = "Set an API key, then run /provider <name>";
│const banner_hints = [_][]const u8{
│    "/goto <url> to navigate",
│    "/save to generate a reproducible script",
│    "/help to list commands   /quit to exit",
│    "! to run JavaScript on the current page",
⋮
│comptime {
│    // Excludes the version line: it's build-environment-controlled (nightly tags
│    // add a commit count + hash), so asserting it would break the build over an
│    // input this file doesn't own.
│    const fixed = [_][]const u8{
│        "Lightpanda Agent",
│        banner_tagline_llm,
│        banner_tagline_basic,
│        banner_setup,
│    } ++ banner_hints;
│    var maxw: usize = 0;
⋮
│/// Prints the welcome banner: the logo on the left with the title and command
│/// hints beside it, vertically centered. `llm_active` picks the tagline.
│pub fn print(llm_active: bool) void {
│    const a = Terminal.ansi;
│
│    var version_buf: [192]u8 = undefined;
│    const version: []const u8 = std.fmt.bufPrint(&version_buf, a.dim ++ "{s}" ++ a.reset, .{lp.buil
│
│    var lines: [9][]const u8 = undefined;
│    var n: usize = 0;
│    lines[n] = a.bold ++ "Lightpanda Agent" ++ a.reset;
│    n += 1;
⋮
│    const text = lines[0..n];
│
│    const start = (logo_rows - text.len) / 2;
│    std.debug.print("\n", .{});
│    var row: usize = 0;
│    var it = std.mem.splitScalar(u8, logo, '\n');
│    while (it.next()) |logo_line| {
│        if (logo_line.len == 0) continue;
│        std.debug.print("{s}", .{logo_line});
│        if (row >= start and row - start < text.len) {
│            const line = text[row - start];
│            if (line.len != 0) std.debug.print("{s}{s}", .{ welcome_gap, line });
│        }
│        std.debug.print("\n", .{});
│        row += 1;
⋮

src/browser/js/Identity.zig:
⋮
│const std = @import("std");
│const js = @import("js.zig");
│
│const v8 = js.v8;
│
│const Identity = @This();
│
⋮
│pub fn deinit(self: *Identity) void {
│    var it = self.identity_map.valueIterator();
│    while (it.next()) |global| {
│        v8.v8__Global__Reset(global);
│    }
⋮

src/browser/js/Integer.zig:
⋮
│const js = @import("js.zig");
│
│const v8 = js.v8;
│
│const Integer = @This();
│
⋮
│pub fn init(isolate: *v8.Isolate, value: anytype) Integer {
│    const handle = switch (@TypeOf(value)) {
│        i8, i16, i32 => v8.v8__Integer__New(isolate, value).?,
│        u8, u16, u32 => v8.v8__Integer__NewFromUnsigned(isolate, value).?,
│        else => |T| @compileError("cannot create v8::Integer from: " ++ @typeName(T)),
│    };
│    return .{ .handle = handle };
⋮

src/browser/js/Number.zig:
⋮
│const js = @import("js.zig");
│
│const v8 = js.v8;
│
│const Number = @This();
│
⋮
│pub fn init(isolate: *v8.Isolate, value: anytype) Number {
│    const handle = v8.v8__Number__New(isolate, value).?;
│    return .{ .handle = handle };
⋮

src/browser/js/Platform.zig:
⋮
│const js = @import("js.zig");
│const v8 = js.v8;
│
│const Platform = @This();
⋮
│pub fn init() !Platform {
│    if (v8.v8__V8__InitializeICU() == false) {
│        return error.FailedToInitializeICU;
│    }
│    // 0 - threadpool size, 0 == let v8 decide
│    // 1 - idle_task_support, 1 == enabled
│    const handle = v8.v8__Platform__NewDefaultPlatform(0, 1).?;
│    v8.v8__V8__InitializePlatform(handle);
│    v8.v8__V8__Initialize();
│    return .{ .handle = handle };
⋮
│pub fn deinit(self: Platform) void {
│    _ = v8.v8__V8__Dispose();
│    v8.v8__V8__DisposePlatform();
│    v8.v8__Platform__DELETE(self.handle);
⋮

src/browser/js/PromiseRejection.zig:
⋮
│const js = @import("js.zig");
│const v8 = js.v8;
│
│const PromiseRejection = @This();
│
⋮
│pub fn promise(self: PromiseRejection) js.Promise {
│    return .{
│        .local = self.local,
│        .handle = v8.v8__PromiseRejectMessage__GetPromise(self.handle).?,
│    };
⋮
│pub fn reason(self: PromiseRejection) ?js.Value {
│    const value_handle = v8.v8__PromiseRejectMessage__GetValue(self.handle) orelse return null;
│
│    return .{
│        .local = self.local,
│        .handle = value_handle,
│    };
⋮

src/browser/js/TaggedOpaque.zig:
⋮
│const js = @import("js.zig");
│const v8 = js.v8;
│const bridge = js.bridge;
│
⋮
│const TaggedOpaque = @This();
│
⋮
│pub const PrototypeChainEntry = struct {
│    index: bridge.JsApiLookup.BackingInt,
│    offset: u16, // offset to the _proto field
⋮
│pub fn fromJS(comptime R: type, js_obj_handle: *const v8.Object) !R {
│    const ti = @typeInfo(R);
│    if (ti != .pointer) {
│        @compileError("non-pointer Zig parameter type: " ++ @typeName(R));
│    }
│
│    const T = ti.pointer.child;
│    const JsApi = bridge.Struct(T).JsApi;
│
│    if (@hasDecl(JsApi.Meta, "empty_with_no_proto")) {
⋮
│    const internal_field_count = v8.v8__Object__InternalFieldCount(js_obj_handle);
⋮
│    const tao_ptr = v8.v8__Object__GetAlignedPointerFromInternalField(js_obj_handle, 0).?;
│    const tao: *TaggedOpaque = @ptrCast(@alignCast(tao_ptr));
│    const expected_type_index = bridge.JsApiLookup.getId(JsApi);
│
│    const prototype_chain = tao.prototype_chain[0..tao.prototype_len];
⋮
│    var ptr = @intFromPtr(tao.value);
│    for (prototype_chain[1..]) |proto| {
│        ptr += proto.offset; // the offset to the _proto field
│        const proto_ptr: **anyopaque = @ptrFromInt(ptr);
│        if (proto.index == expected_type_index) {
│            return @ptrCast(@alignCast(proto_ptr.*));
│        }
│        ptr = @intFromPtr(proto_ptr.*);
⋮

src/browser/reflect.zig:
⋮
│pub fn Struct(comptime T: type) type {
│    return switch (@typeInfo(T)) {
│        .pointer => |ptr| ptr.child,
│        .@"struct" => T,
│        .void => T,
│        else => unreachable,
│    };
⋮

src/browser/tests/page/modules/circular-b.js:
⋮
│export function getBValue() {
│  return bValue;
⋮
│export function getFromA() {
│  return aValue;
⋮

src/browser/tests/page/modules/dynamic-chain-b.js:
│export async function loadNext() {
⋮

src/browser/tests/page/modules/dynamic-circular-x.js:
⋮
│export async function loadY() {
│  const y = await import('./dynamic-circular-y.js');
│  return y.yValue;
⋮

src/browser/tests/page/modules/dynamic-circular-y.js:
⋮
│export async function loadX() {
│  const x = await import('./dynamic-circular-x.js');
│  return x.xValue;
⋮

src/browser/tests/page/modules/mixed-circular-dynamic.js:
⋮
│export function getStaticValue() {
│  return staticValue;
⋮

src/browser/tests/page/modules/mixed-circular-static.js:
⋮
│export async function loadDynamicSide() {
│  const dynamic = await import('./mixed-circular-dynamic.js');
│  return dynamic.dynamicValue;
⋮

src/browser/tests/page/modules/shared.js:
⋮
│export function increment() {
│  return ++counter;
⋮
│export function getCount() {
│  return counter;
⋮

src/browser/tests/testing.js:
⋮
│  function expectTrue(actual) {
│     expectEqual(true, actual);
⋮
│  function expectEqual(expected, actual, opts) {
│    if (_equal(expected, actual)) {
│      _registerObservation('ok', opts);
│      return;
│    }
│    failed = true;
│    _registerObservation('fail', opts);
│    let err = `expected: ${_displayValue(expected)}, got: ${_displayValue(actual)}\n  script_id: ${
│    if (async_capture) {
│      err += `\n stack: ${async_capture.stack}`;
⋮
│  function fail(reason) {
│    failed = true;
│    console.error(reason);
│    throw new Error('testing.fail()');
⋮
│  function expectError(expected, fn) {
│    withError((err) => {
│      if (!err.toString().includes(expected)) {
│        console.error(`Expecte error to contains: ${expected}, was: ${err.toString()}`);
│        expectEqual(true, false);
│      } else {
│        // to record a successful case
│        expectTrue(true);
│      }
│    }, fn);
⋮
│  function withError(cb, fn) {
│    try{
│      fn();
│    } catch (err) {
│      cb(err);
│      return;
│    }
│
│    console.error(`expected error but no error received\n`);
│    throw new Error('no error');
⋮
│  async function async() {
│    const script_id = (IS_TEST_RUNNER) ? document.currentScript.id : 'cannot track module id in FF/
│
│    if (async_seen.has(script_id)) {
│      throw new Error(`testing.async() called more than once for script '${script_id}'. A script ma
│    }
│    async_seen.add(script_id);
│
│    let resolve = null
│    const promise = new Promise((r) => { resolve = r});
⋮
│    return {
│      promise: promise,
│      resolve: resolve,
│      capture: {script_id: script_id, stack: new Error().stack},
│      done: async function(cb) {
│        const res = await this.promise;
│        async_pending.delete(script_id);
│        async_capture = this.capture;
│        try {
│          cb(res);
│        } catch (err) {
│          console.warn(script_id, err);
│          failed = true;
│        }
⋮
│  function _registerObservation(status, opts) {
│    script_id = opts?.script_id || _currentScriptId();
│    if (!script_id) {
│      return;
│    }
│    if (observed_ids[script_id] === 'fail') {
│      return;
│    }
│
│    observed_ids[script_id] = status;
│
⋮
│  function _currentScriptId() {
│    if (current_script_id) {
│      return current_script_id;
│    }
│
│    if (async_capture) {
│      return async_capture.script_id;
│    }
│
│    const current_script = document.currentScript;
│
⋮
│  function _displayValue(value) {
│    if (value instanceof Element) {
│      return `HTMLElement: ${value.outerHTML}`;
│    }
│    if (value instanceof Attr) {
│      return `Attribute: ${value.name}: ${value.value}`;
│    }
│    if (value instanceof Node) {
│      return value.nodeName;
│    }
⋮

src/browser/tests/worker/import-module.js:
⋮
│export function multiply(a, b) {
│  return a * b;
⋮

src/browser/tests/worker/modules/circular-b.js:
⋮
│export function getBValue() {
│  return bValue;
⋮
│export function getFromA() {
│  return aValue;
⋮

src/browser/tests/worker/modules/shared.js:
⋮
│export function increment() {
│  return ++counter;
⋮
│export function getCount() {
│  return counter;
⋮

src/browser/tests/worker/timers-worker.js:
⋮
│(async function() {
│  try {
│    const results = {};
│
│    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
│
│    // setTimeout: returns a number; passes extra args through; `this` is self.
│    {
│      let timeout_this = null;
│      const sum = await new Promise((resolve) => {
│        const id = setTimeout(function (a, b) {
⋮

src/browser/webapi/cdata/CDATASection.zig:
⋮
│const js = @import("../../js/js.zig");
│
│const Text = @import("Text.zig");
│
│const CDATASection = @This();
│
⋮
│pub const JsApi = struct {
│    pub const bridge = js.Bridge(CDATASection);
│
│    pub const Meta = struct {
│        pub const name = "CDATASection";
│        pub const prototype_chain = bridge.prototypeChain();
│        pub var class_id: bridge.ClassId = undefined;
│    };
⋮

src/browser/webapi/cdata/Comment.zig:
⋮
│const js = @import("../../js/js.zig");
│const Frame = @import("../../Frame.zig");
│
│const CData = @import("../CData.zig");
│
│const Comment = @This();
│
⋮
│pub fn init(str: ?js.NullableString, frame: *Frame) !*Comment {
│    const node = try Frame.node_factory.createComment(frame, if (str) |s| s.value else "");
│    return node.as(Comment);
⋮
│pub const JsApi = struct {
│    pub const bridge = js.Bridge(Comment);
│
│    pub const Meta = struct {
│        pub const name = "Comment";
│        pub const prototype_chain = bridge.prototypeChain();
│        pub var class_id: bridge.ClassId = undefined;
│        pub const enumerable = false;
│    };
│
│    pub const constructor = bridge.constructor(Comment.init, .{});
⋮
│const testing = @import("../../../testing.zig");
⋮

src/browser/webapi/cdata/ProcessingInstruction.zig:
⋮
│const js = @import("../../js/js.zig");
│
│const CData = @import("../CData.zig");
│
│const ProcessingInstruction = @This();
│
⋮
│pub fn getTarget(self: *const ProcessingInstruction) []const u8 {
│    return self._target;
⋮
│pub const JsApi = struct {
│    pub const bridge = js.Bridge(ProcessingInstruction);
│
│    pub const Meta = struct {
│        pub const name = "ProcessingInstruction";
│        pub const prototype_chain = bridge.prototypeChain();
│        pub var class_id: bridge.ClassId = undefined;
│        pub const enumerable = false;
│    };
│
│    pub const target = bridge.accessor(ProcessingInstruction.getTarget, null, .{});
⋮
│const testing = @import("../../../testing.zig");
⋮

src/browser/webapi/collections.zig:
⋮
│pub const NodeLive = @import("collections/node_live.zig").NodeLive;
│pub const ChildNodes = @import("collections/ChildNodes.zig");
│pub const DOMTokenList = @import("collections/DOMTokenList.zig");
│pub const RadioNodeList = @import("collections/RadioNodeList.zig");
│pub const HTMLCollection = @import("collections/HTMLCollection.zig");
│pub const HTMLAllCollection = @import("collections/HTMLAllCollection.zig");
│pub const HTMLOptionsCollection = @import("collections/HTMLOptionsCollection.zig");
│pub const HTMLFormControlsCollection = @import("collections/HTMLFormControlsCollection.zig");
│
│pub fn registerTypes() []const type {
│    return &.{
│        HTMLCollection,
│        HTMLCollection.Iterator,
│        @import("collections/NodeList.zig"),
│        @import("collections/NodeList.zig").KeyIterator,
│        @import("collections/NodeList.zig").ValueIterator,
│        @import("collections/NodeList.zig").EntryIterator,
│        @import("collections/HTMLAllCollection.zig"),
│        @import("collections/HTMLAllCollection.zig").Iterator,
⋮

src/browser/webapi/element/svg/Rect.zig:
⋮
│const Node = @import("../../Node.zig");
⋮
│pub fn asElement(self: *Rect) *Element {
│    return self._proto._proto;
│}
│pub fn asNode(self: *Rect) *Node {
│    return self.asElement().asNode();
⋮
│pub const JsApi = struct {
│    pub const bridge = js.Bridge(Rect);
│
│    pub const Meta = struct {
│        pub const name = "SVGRectElement";
│        pub const prototype_chain = bridge.prototypeChain();
│        pub var class_id: bridge.ClassId = undefined;
│    };
⋮

src/browser/webapi/encoding/TextEncoder.zig:
⋮
│const std = @import("std");
│const js = @import("../../js/js.zig");
│
│const TextEncoder = @This();
⋮
│pub fn init() TextEncoder {
│    return .{};
⋮
│pub fn encode(_: *const TextEncoder, v_: ?js.Value) !js.TypedArray(u8) {
│    const v = v_ orelse return .{ .values = "" };
│
│    if (v.isUndefined()) {
│        return .{ .values = "" };
│    }
│
│    if (v.isNull()) {
│        return .{ .values = "null" };
│    }
│
│    const str = try v.toStringSlice();
⋮
│pub const JsApi = struct {
│    pub const bridge = js.Bridge(TextEncoder);
│
│    pub const Meta = struct {
│        pub const name = "TextEncoder";
│        pub const prototype_chain = bridge.prototypeChain();
│        pub var class_id: bridge.ClassId = undefined;
│        pub const empty_with_no_proto = true;
│    };
│
│    pub const constructor = bridge.constructor(TextEncoder.init, .{});
│    pub const encode = bridge.function(TextEncoder.encode, .{ .as_typed_array = true });
│    pub const encoding = bridge.property("utf-8", .{ .template = false });
⋮
│const testing = @import("../../../testing.zig");
⋮

src/browser/webapi/navigation/root.zig:
⋮
│const std = @import("std");
│
│const js = @import("../../js/js.zig");
│
│const NavigationHistoryEntry = @import("NavigationHistoryEntry.zig");
│
│pub const NavigationType = enum {
│    push,
│    replace,
│    traverse,
│    reload,
⋮
│pub const NavigationKind = union(NavigationType) {
│    push: ?[]const u8,
│    replace: ?[]const u8,
│    traverse: usize,
│    reload,
│
│    pub fn toNavigationType(self: NavigationKind) NavigationType {
│        return std.meta.activeTag(self);
│    }
⋮
│pub const NavigationState = struct {
│    source: enum { history, navigation },
│    value: ?[]const u8,
⋮
│pub const NavigationTransition = struct {
│    finished: js.Promise.Global,
│    from: NavigationHistoryEntry,
│    navigation_type: NavigationType,
⋮

src/browser/xpath/ast.zig:
⋮
│//! XPath 1.0 AST.
⋮
│pub const Expr = union(enum) {
│    /// Absolute or relative location path: `/foo/bar`, `//x`, `foo/bar`.
│    path: Path,
│    /// Filter expression followed by a location-path tail:
│    /// `(//a)/b`, `(expr)//c`.
│    filter_path: FilterPath,
│    /// Filter expression with a single predicate: `(expr)[n]`.
│    /// Multi-predicate filters nest: `(e)[1][2]` → filter(filter(e,1),2).
│    filter: Filter,
│    binop: BinOp,
⋮
│pub const Path = struct {
│    absolute: bool,
│    steps: []const Step,
⋮
│pub const FilterPath = struct {
│    filter: *Expr,
│    steps: []const Step,
⋮
│pub const Filter = struct {
│    expr: *Expr,
│    predicate: *Expr,
⋮
│pub const BinOp = struct {
│    op: BinOpKind,
│    left: *Expr,
│    right: *Expr,
⋮
│pub const BinOpKind = enum {
│    or_,
│    and_,
│    eq,
│    neq,
│    lt,
│    gt,
│    lte,
│    gte,
│    add,
⋮
│pub const FnCall = struct {
│    name: []const u8,
│    args: []const *Expr,
⋮
│pub const Step = struct {
│    axis: Axis,
│    node_test: NodeTest,
│    predicates: []const *Expr,
⋮
│pub const Axis = enum {
│    child,
│    descendant,
│    descendant_or_self,
│    self,
│    parent,
│    ancestor,
│    ancestor_or_self,
│    following_sibling,
│    preceding_sibling,
⋮
│pub const NodeTest = union(enum) {
│    /// Element / attribute name. `"*"` is the wildcard. Namespaced forms
│    /// (`prefix:*`, `prefix:local`) are stored verbatim — the evaluator
│    /// does not split them, so they fall through to a literal `mem.eql`
│    /// against the node name (consistent with the `namespace::` axis stub
│    /// per decision #3).
│    /// TODO: real namespace support if the polyfill ever drops the stub.
│    name: []const u8,
│    /// `node()`, `text()`, `comment()`, `processing-instruction()`.
│    /// The optional target literal of `processing-instruction("foo")`
⋮
│pub const TypeTest = enum {
│    node,
│    text,
│    comment,
│    processing_instruction,
⋮

src/cdp/domains/audits.zig:
⋮
│const std = @import("std");
│const CDP = @import("../CDP.zig");
│
│pub fn processMessage(cmd: *CDP.Command) !void {
│    const action = std.meta.stringToEnum(enum {
│        enable,
│        disable,
│    }, cmd.input.action) orelse return error.UnknownMethod;
│
│    switch (action) {
│        .enable => return enable(cmd),
│        .disable => return disable(cmd),
│    }
│}
│fn enable(cmd: *CDP.Command) !void {
│    return cmd.sendResult(null, .{});
⋮
│fn disable(cmd: *CDP.Command) !void {
│    return cmd.sendResult(null, .{});
⋮

src/cdp/domains/css.zig:
⋮
│const std = @import("std");
│const CDP = @import("../CDP.zig");
│
│pub fn processMessage(cmd: *CDP.Command) !void {
│    const action = std.meta.stringToEnum(enum {
│        enable,
│    }, cmd.input.action) orelse return error.UnknownMethod;
│
│    switch (action) {
│        .enable => return cmd.sendResult(null, .{}),
│    }
⋮

src/cdp/domains/inspector.zig:
⋮
│const std = @import("std");
│const CDP = @import("../CDP.zig");
│
│pub fn processMessage(cmd: *CDP.Command) !void {
│    const action = std.meta.stringToEnum(enum {
│        enable,
│        disable,
│    }, cmd.input.action) orelse return error.UnknownMethod;
│
│    switch (action) {
│        .enable => return cmd.sendResult(null, .{}),
│        .disable => return cmd.sendResult(null, .{}),
│    }
⋮

src/cdp/domains/log.zig:
⋮
│const std = @import("std");
│const CDP = @import("../CDP.zig");
│
│pub fn processMessage(cmd: *CDP.Command) !void {
│    const action = std.meta.stringToEnum(enum {
│        enable,
│        disable,
│    }, cmd.input.action) orelse return error.UnknownMethod;
│
│    switch (action) {
│        .enable, .disable => return cmd.sendResult(null, .{}),
│    }
⋮

src/cdp/domains/performance.zig:
⋮
│const std = @import("std");
│const CDP = @import("../CDP.zig");
│
│pub fn processMessage(cmd: *CDP.Command) !void {
│    const action = std.meta.stringToEnum(enum {
│        enable,
│        disable,
│    }, cmd.input.action) orelse return error.UnknownMethod;
│
│    switch (action) {
│        .enable => return cmd.sendResult(null, .{}),
│        .disable => return cmd.sendResult(null, .{}),
│    }
⋮

src/cdp/domains/security.zig:
⋮
│const std = @import("std");
│const CDP = @import("../CDP.zig");
│
│pub fn processMessage(cmd: *CDP.Command) !void {
│    const action = std.meta.stringToEnum(enum {
│        enable,
│        disable,
│        setIgnoreCertificateErrors,
│    }, cmd.input.action) orelse return error.UnknownMethod;
│
│    switch (action) {
│        .enable => return cmd.sendResult(null, .{}),
│        .disable => return cmd.sendResult(null, .{}),
⋮
│fn setIgnoreCertificateErrors(cmd: *CDP.Command) !void {
│    const params = (try cmd.params(struct {
│        ignore: bool,
│    })) orelse return error.InvalidParams;
│
│    try cmd.cdp.browser.http_client.setTlsVerify(!params.ignore);
│    return cmd.sendResult(null, .{});
⋮
│const testing = @import("../testing.zig");
│
│test "cdp.Security: setIgnoreCertificateErrors" {
│    var ctx = try testing.context();
│    defer ctx.deinit();
│
│    _ = try ctx.loadBrowserContext(.{ .id = "BID-9" });
│
│    try ctx.processMessage(.{
│        .id = 8,
│        .method = "Security.setIgnoreCertificateErrors",
│        .params = .{ .ignore = true },
⋮

src/data/public_suffix_list.zig:
│const std = @import("std");
│const builtin = @import("builtin");
│
│pub fn lookup(value: []const u8) bool {
│    return public_suffix_list.has(value);
⋮
│const public_suffix_list = std.StaticStringMap(void).initComptime(entries);
│
│const entries: []const struct { []const u8, void } =
│    if (builtin.is_test) &.{
│        .{ "api.gov.uk", {} },
│        .{ "gov.uk", {} },
│    } else &.{
│        .{ "ac", {} },
│        .{ "com.ac", {} },
│        .{ "edu.ac", {} },
│        .{ "gov.ac", {} },
│        .{ "mil.ac", {} },
⋮

src/data/public_suffix_list_gen.go:
│package main
│
⋮
│func main() {
│	resp, err := http.Get("https://publicsuffix.org/list/public_suffix_list.dat")
│	if err != nil {
│		panic(err)
│	}
│	defer resp.Body.Close()
│
│	var domains []string
│
│	scanner := bufio.NewScanner(resp.Body)
⋮

src/html5ever/lib.rs:
⋮
│mod url;
│
⋮
│pub struct Memory {
│    pub resident: usize,
│    pub allocated: usize,
⋮
│pub struct StreamingParser {
│    #[allow(dead_code)]
│    arena: Box<typed_arena::Arena<sink::ElementData>>,
│    parser: Box<dyn std::any::Any>,
⋮

src/html5ever/sink.rs:
⋮
│type Arena<'arena> = &'arena typed_arena::Arena<ElementData>;
│
⋮
│pub struct ElementData {
│    pub qname: QualName,
│    pub mathml_annotation_xml_integration_point: bool,
⋮
│pub struct Sink<'arena> {
│    pub ctx: Ref,
│    pub document: Ref,
│    pub arena: Arena<'arena>,
│    pub quirks_mode: Cell<QuirksMode>,
│    pub pop_callback: PopCallback,
│    pub append_callback: AppendCallback,
│    pub get_data_callback: GetDataCallback,
│    pub parse_error_callback: ParseErrorCallback,
│    pub create_element_callback: CreateElementCallback,
⋮
│impl<'arena> TreeSink for Sink<'arena> {
│    type Handle = *const c_void;
│    type Output = ();
│    type ElemName<'a>
│        = &'a QualName
│    where
│        Self: 'a;
│
│    fn finish(self) -> () {
│        return ();
⋮
│    fn parse_error(&self, err: Cow<'static, str>) {
│        unsafe {
│            (self.parse_error_callback)(
│                self.ctx,
│                StringSlice {
│                    ptr: err.as_ptr(),
│                    len: err.len(),
│                },
│            );
│        }
⋮
│    fn get_document(&self) -> *const c_void {
│        return self.document;
⋮
│    fn set_quirks_mode(&self, mode: QuirksMode) {
│        self.quirks_mode.set(mode);
⋮
│    fn same_node(&self, x: &Ref, y: &Ref) -> bool {
│        ptr::eq::<c_void>(*x, *y)
⋮
│    fn elem_name(&self, target: &Ref) -> Self::ElemName<'_> {
│        let opaque = unsafe { (self.get_data_callback)(*target) };
│        let data = opaque as *mut ElementData;
│        return unsafe { &(*data).qname };
⋮
│    fn get_template_contents(&self, target: &Ref) -> Ref {
│        unsafe {
│            return (self.get_template_contents_callback)(self.ctx, *target);
│        }
⋮
│    fn is_mathml_annotation_xml_integration_point(&self, target: &Ref) -> bool {
│        let opaque = unsafe { (self.get_data_callback)(*target) };
│        let data = opaque as *mut ElementData;
│        return unsafe { (*data).mathml_annotation_xml_integration_point };
⋮
│    fn create_pi(&self, target: StrTendril, data: StrTendril) -> Ref {
│        let str_target = StringSlice{ ptr: target.as_ptr(), len: target.len()};
│        let str_data = StringSlice{ ptr: data.as_ptr(), len: data.len()};
│        unsafe {
│            return (self.create_processing_instruction)(self.ctx, str_target, str_data);
│        }
⋮
│    fn append(&self, parent: &Ref, child: NodeOrText<Ref>) {
│        match child {
│            NodeOrText::AppendText(ref t) => {
│                // The child exists for the duration of the append_callback call,
│                // but sometimes the memory on the Zig side, in append_callback,
│                // is zeroed. If you try to refactor this code a bit, and do:
│                //   unsafe {
│                //       (self.append_callback)(self.ctx, *parent, CNodeOrText::create(child));
│                //   }
│                // Where CNodeOrText::create returns the property CNodeOrText,
⋮
│    fn allow_declarative_shadow_roots(&self, _intended_parent: &Ref) -> bool {
│        self.allow_declarative_shadow
⋮

src/html5ever/types.rs:
⋮
│pub type CreateElementCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    data: *const c_void,
│    name: CQualName,
│    attributes: *mut c_void,
⋮
│pub type CreateCommentCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    str: StringSlice,
⋮
│pub type AppendDoctypeToDocumentCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    name: StringSlice,
│    public_id: StringSlice,
│    system_id: StringSlice,
⋮
│pub type CreateProcessingInstruction = unsafe extern "C" fn(
│    ctx: Ref,
│    target: StringSlice,
│    data: StringSlice,
⋮
│pub type GetDataCallback = unsafe extern "C" fn(ctx: Ref) -> *mut c_void;
│
│pub type AppendCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    parent: Ref,
│    node_or_text: CNodeOrText
⋮
│pub type ParseErrorCallback = unsafe extern "C" fn(ctx: Ref, str: StringSlice) -> ();
│
│pub type PopCallback = unsafe extern "C" fn(ctx: Ref, node: Ref) -> ();
│
│pub type AddAttrsIfMissingCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    target: Ref,
│    attributes: *mut c_void,
⋮
│pub type GetTemplateContentsCallback = unsafe extern "C" fn(ctx: Ref, target: Ref) -> Ref;
│
│pub type AttachDeclarativeShadowCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    host: Ref,
│    template: Ref,
│    mode_is_open: u8,
⋮
│pub type RemoveFromParentCallback = unsafe extern "C" fn(ctx: Ref, target: Ref) -> ();
│
│pub type ReparentChildrenCallback = unsafe extern "C" fn(ctx: Ref, node: Ref, new_parent: Ref) -> (
│
│pub type AppendBeforeSiblingCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    sibling: Ref,
│    node_or_text: CNodeOrText
⋮
│pub type AppendBasedOnParentNodeCallback = unsafe extern "C" fn(
│    ctx: Ref,
│    element: Ref,
│    prev_element: Ref,
│    node_or_text: CNodeOrText
⋮
│pub type Ref = *const c_void;
│
⋮
│pub struct CNullable<T> {
│    tag: u8, // 0 = None, 1 = Some
│    value: T,
│}
│impl<T: Default> CNullable<T> {
│    pub fn none() -> CNullable<T> {
│        return Self{tag: 0, value: T::default()};
│    }
│
│    pub fn some(v: T) -> CNullable<T> {
│        return Self{tag: 1, value: v};
│    }
⋮
│impl<T> Default for Slice<T> {
│    fn default() -> Self {
│        return Self{ptr: ptr::null(), len: 0};
│    }
⋮
│pub struct CQualName {
│    prefix: CNullable<StringSlice>,
│    ns: StringSlice,
│    local: StringSlice,
│}
│impl CQualName {
│    pub fn create(q: &QualName) -> Self {
│        let ns = StringSlice { ptr: q.ns.as_ptr(), len: q.ns.len()};
│        let local = StringSlice { ptr: q.local.as_ptr(), len: q.local.len()};
│        let prefix = match &q.prefix {
│            None => CNullable::<StringSlice>::none(),
│            Some(prefix) => CNullable::<StringSlice>::some(StringSlice { ptr: prefix.as_ptr(), len:
│        };
│        CQualName{
│            // inner: q as *const _ as *const c_void,
│            ns: ns,
⋮
│impl Default for CQualName {
│    fn default() -> Self {
│        Self{
│            prefix: CNullable::<StringSlice>::none(),
│            ns: StringSlice::default(),
│            local: StringSlice::default(),
│        }
│    }
⋮
│pub struct CAttribute {
│    pub name: CQualName,
│    pub value: StringSlice,
│}
│impl Default for CAttribute {
│    fn default() -> Self {
│        return Self{name: CQualName::default(), value: StringSlice::default()};
│    }
⋮
│pub struct CAttributeIterator {
│    pub vec: Vec<Attribute>,
│    pub pos: usize,
⋮
│pub struct CNodeOrText {
│    pub tag: u8, // 0 = node, 1 = text
│    pub node: Ref,
│    pub text: StringSlice,
⋮

src/html5ever/url.rs:
⋮
│fn str_from(ptr: *const c_uchar, len: usize) -> Option<&'static str> {
│    // Zig hands empty slices a non-null but dangling pointer, so length must
│    // be checked before forming a slice from raw parts.
│    if ptr.is_null() || len == 0 {
│        return Some("");
│    }
│    let bytes = unsafe { slice::from_raw_parts(ptr, len) };
│    std::str::from_utf8(bytes).ok()
⋮
│fn ffi_guard<F: FnOnce() -> i32>(f: F) -> i32 {
│    std::panic::catch_unwind(std::panic::AssertUnwindSafe(f)).unwrap_or(1)
⋮

src/mcp.zig:
│const std = @import("std");
│
│pub const protocol = @import("mcp/protocol.zig");
│pub const Version = protocol.Version;
│pub const router = @import("mcp/router.zig");
│pub const Server = @import("mcp/Server.zig");
│
⋮

src/storage/Blackhole.zig:
⋮
│const std = @import("std");
│const Allocator = std.mem.Allocator;
│
│const Blackhole = @This();
│
│pub fn deinit(_: *Blackhole, _: Allocator) void {}

src/storage/sqlite/migrations.zig:
⋮
│const lp = @import("lightpanda");
│
│const Sqlite = @import("Sqlite.zig");
│
│const log = lp.log;
│
│pub fn run(conn: Sqlite.Conn) !i64 {
│    const version = try getVersion(conn);
│    return version;
⋮
│fn getVersion(conn: Sqlite.Conn) !i64 {
│    const exists_sql = "select exists (select 1 from sqlite_schema where type='table' and name='mig
│    if (try conn.scalar(bool, exists_sql, .{}) orelse false) {
│        if (try conn.scalar(i64, "select max(id) from migrations", .{})) |version| {
│            return version;
│        }
│
│        log.fatal(.storage, "corrupt database", .{ .engine = "sqlite", .note = "The sqlite database
│        return error.CorruptDatabase;
│    }
│
⋮
│    const create_sql =
│        \\ create table migrations as
│        \\ select 1 as id, current_timestamp as created_at
⋮
```
