# Rules

## Elite Architecture & Coding Standards

This document condenses the master repository rules into a dense, actionable reference for AI coding agents. It preserves all critical constraints, patterns, and vocabulary from the foundational architecture texts.

### 1. Clean Architecture & SOLID Principles (Robert C. Martin)
- **The Dependency Rule**: Source code dependencies MUST point strictly inward toward high-level policies (Entities/Use Cases).
- **Entities**: Encapsulate enterprise-wide Critical Business Rules and Data. MUST NOT depend on frameworks, DBs, or UI.
- **Use Cases**: Application-specific business rules orchestrating Entities. MUST NOT contain SQL, HTML, or routing. Use simple Request/Response DTOs.
- **Interface Adapters**: Convert data between Use Cases and external agencies (Web, DB). Contains MVC components, Presenters, and DB Gateways.
- **Frameworks & Drivers**: Outermost layer. Treat frameworks as interchangeable details. Do NOT inherit core objects from framework base classes (avoid Asymmetric Marriages).
- **Boundaries**: Use Dependency Inversion (interfaces) to cross boundaries against the flow of control. Pass simple DTOs across boundaries, NEVER Entities or DB rows.
- **Main Component**: The dirtiest component. Centralizes DI, configuration, and instantiation. Plugs into high-level policy.
- **Screaming Architecture**: Top-level directories MUST reveal business intent (e.g., `/Checkout`), not frameworks (e.g., `/Controllers`).
- **SRP (Single Responsibility)**: A module should be responsible to one, and only one, actor. Separate code serving different actors.
- **OCP (Open-Closed)**: Open for extension, closed for modification. Protect high-level components from low-level changes.
- **LSP (Liskov Substitution)**: Subtypes MUST be substitutable for base types without altering caller behavior. Avoid type-checking conditionals (`instanceof`, `switch` on type).
- **ISP (Interface Segregation)**: Do not depend on unused methods. Segregate bloated interfaces into client-specific ones to avoid Architectural Baggage.
- **DIP (Dependency Inversion)**: Depend on abstractions, not concretions. Use Abstract Factories for volatile concrete object creation.
- **Component Cohesion (REP, CCP, CRP)**: Group classes that change together (CCP) and are reused together (CRP). Release as cohesive units (REP).
- **Component Coupling (ADP, SDP, SAP)**: Zero dependency cycles (ADP). Depend in the direction of stability (SDP). Stable components must be abstract (SAP).
- **Humble Object Pattern**: Split hard-to-test behaviors (UI/IO) into a Humble Object (View) and a testable object (Presenter/Interactor).
- **Partial Boundaries**: Use when full boundaries are too expensive: Skip the Last Step (same deployable), One-Dimensional (Strategy pattern), or Facade.
- **Clean Embedded Architecture**: Eliminate Target-Hardware Bottleneck using HAL, PAL, and OSAL. Test off-target.
- **The Missing Chapter (Packaging)**: Prefer Package by Component for monoliths. Use compiler access modifiers (`package-private`/`internal`) to enforce boundaries, not just folders.

### 2. Microservices Patterns (Chris Richardson & Sam Newman)
- **Bounded Contexts**: Align microservices to business domains, not technical layers. Each service MUST own its database. NO shared databases.
- **Fallacies of Distributed Computing**: Network is not reliable, latency is not zero. MUST use timeouts, retries (with backoff for transient errors), and Circuit Breakers for all remote calls.
- **Stamp Coupling**: Minimize payload size. Do not send 500kb if only 200 bytes are needed.
- **Sagas**: Use for distributed transactions. NO 2PC/XA. Use Choreography (events) for simple/cross-team workflows, Orchestration (central mediator) for complex/single-team workflows. Define Compensating Transactions for rollbacks.
- **API Gateway & BFF**: Use API Gateways for North-South traffic (auth, rate limiting). Use Backends for Frontends (BFF) for client-specific aggregation. Do NOT put business logic in gateways.
- **Strangler Fig Pattern**: Migrate monoliths incrementally. Extract vertical slices. Use Anti-Corruption Layers (ACL) to translate between legacy and new domain models.
- **Service Mesh**: Use for East-West traffic reliability (mTLS, retries, routing) via sidecars.
- **Communication**: Default to asynchronous messaging. Use synchronous (REST/gRPC) only when immediate response is required.
- **Architecture Quantum**: An independently deployable artifact with high functional cohesion and synchronous connascence. Dictates monolith vs distributed.
- **First Law of Distributed Object Design**: Don't distribute your objects! Use Clustering instead. Use Remote Facades and DTOs at strict distribution boundaries.
- **Testing Microservices**: Follow the Test Pyramid. Use Solitary Unit Tests for Domain Services/Controllers. Use Sociable Unit Tests for Entities/Value Objects. Use Consumer-Driven Contracts (CDC) like Pact instead of brittle E2E tests.
- **Deployment**: Serverless -> Containers -> VMs. One logical service per container. Use Deployments, Services, Liveness/Readiness probes. Externalize config via ConfigMaps/Secrets.
- **Progressive Delivery**: Separate deployment from release. Use Feature Toggles, Canary Releases, and Parallel Runs.
- **Security**: Zero Trust. mTLS for inter-service. Centralized Auth at Gateway, decentralized Authorization (via JWT claims) in services. Principle of Least Privilege. Datensparsamkeit (data frugality).
- **Scaling**: Evaluate Vertical -> Horizontal -> Partitioning -> Functional Decomposition. Implement Caching judiciously (Client, Server, Request).

### 3. Event-Driven Architecture & Streaming (Adam Bellemare & Ben Stopford)
- **Event Sourcing**: Store state as an immutable sequence of events. Rebuild state by replaying events. Use Snapshots and Upcasting.
- **CQRS**: Segregate Command (write) and Query (read) models. Update read models asynchronously via events.
- **Single Writer Principle**: Only ONE microservice may write to a specific event stream.
- **Kafka/Streaming**: Treat the event log as the single source of truth. Push data to code (materialized views/state stores) instead of remote DB queries.
- **Stateful Streaming**: Use local state stores (e.g., RocksDB) backed by compacted changelog topics.
- **Exactly-Once Processing**: Wrap consume-process-produce in Kafka transactions.
- **Schema Evolution**: Use explicit schemas (Avro/Protobuf). Prefer forward/backward compatibility. For breaking changes, use Dual Schema Upgrade Window (v1 and v2 topics).
- **Determinism**: Use Event Time (not wall-clock time). Handle late events via Grace Periods. Avoid external synchronous API calls in stream processors.
- **Dead Letter Queues (DLQ)**: Route unprocessable messages to a DLQ to prevent blocking the main stream.
- **Join-Filter-Process**: Standard streaming topology pattern. Use `selectKey` to rekey/copartition before joining.
- **Data Liberation**: Extract legacy data via Outbox Pattern, CDC (Log-Based), or Query-Based liberation.
- **FaaS/Serverless**: Map one function per microservice or per aggregate. Manage cold starts. Commit offsets ONLY after successful execution.
- **Basic Producer and Consumer (BPC)**: Use Sidecar Pattern for legacy integration, Gating Pattern for unordered prerequisites.
- **Heavyweight Frameworks**: Spark/Flink. Use Driver Mode, Checkpoints, External Shuffle Service.

### 4. Refactoring & Code Quality (Martin Fowler)
- **Two Hats**: Strictly separate adding functionality from refactoring. Do not do both simultaneously.
- **Code Smells**: Extract long functions, replace temps with queries, encapsulate mutable data, replace primitives with objects (Value Objects).
- **Conditional Logic**: Decompose complex conditionals. Use Guard Clauses for edge cases. Replace type-code switches with Polymorphism. Use Special Case (Null) Objects.
- **Testing**: Tests MUST be isolated and deterministic. Use Fresh Fixtures (no shared mutable state).
- **Test Boundary**: Tests are system components in the outermost circle. They depend on the system; the system NEVER depends on tests. Use a Testing API to bypass volatile GUIs.
- **Moving Features**: Slide Statements, Split Loop, Replace Loop with Pipeline.
- **Dealing with Inheritance**: Pull Up/Push Down methods. Replace Subclass/Superclass with Delegate (Composition over Inheritance).
- **Organizing Data**: Split Variable, Derived Variable, Value vs Reference Object.
- **Refactoring APIs**: Command-Query Separation, Flag Arguments, Preserve Whole Object.

### 5. Enterprise Application Architecture (Martin Fowler)
- **Database is a Detail**: Keep DB logic in the outermost circle. Business rules MUST be ignorant of SQL/ORM.
- **Data Source Patterns**: 
  - *Active Record*: Simple domain logic, isomorphic schema.
  - *Data Mapper*: Complex domain logic, divergent schema.
  - *Table/Row Data Gateway*: Transaction Scripts or Table Modules.
- **Unit of Work**: Track changes and commit all DB updates at the end of a business transaction.
- **Identity Map**: Cache loaded objects per session to prevent duplicate instances and inconsistent reads.
- **Lazy Load**: Defer loading related objects. Avoid Ripple Loading (N+1 queries) by using Ghost Lists.
- **Offline Concurrency**: 
  - *Optimistic Offline Lock*: Default choice. Use version numbers, check on update.
  - *Pessimistic Offline Lock*: Use only for high-conflict scenarios. Fail fast, do not block.
- **Session State**: Prefer Client Session State (encrypted DTOs) or Database Session State (Pending Tables). Avoid Server Session State in memory for clustered environments.
- **Object-Relational Structural Patterns**: Use Meaningless Keys (Identity Field). Map inheritance via Single Table, Class Table, or Concrete Table Inheritance.
- **Web Presentation Patterns**: MVC, Page/Front Controller, Template/Transform/Two Step View.
- **Base Patterns**: Gateway, Mapper, Layer Supertype, Registry, Value Object, Special Case.

### 6. Fundamentals of Software Architecture (Mark Richards)
- **Architecture Styles**: 
  - *Layered Architecture*: Enforce closed layers to maintain isolation. Beware the Architecture Sinkhole anti-pattern.
  - *Pipeline Architecture*: Unidirectional, stateless Pipes and Filters.
  - *Microkernel Architecture*: Core system + independent Plug-in components.
  - *Service-Based Architecture*: Coarse-grained services sharing a monolithic database.
  - *Space-Based Architecture*: Tuple space, Processing Units, Data Grids, Data Pumps. High elasticity, no synchronous DB bottlenecks.
  - *Orchestration-Driven SOA*: Legacy ESB pattern. High reuse, high coupling. Avoid for modern systems.
- **Architecture Characteristics**: Explicit vs Implicit, Operational vs Structural. Least Worst Architecture.
- **Measuring and Governing**: Performance Budgets, Cyclomatic Complexity, Fitness Functions, Chaos Engineering.
- **Component-Based Thinking**: Actor/Actions, Event Storming, Workflow Approach. Avoid Entity Trap.
- **Organizational & Soft Skills**:
  - *Conway's Law*: Align architecture with team structures (Stream-Aligned Teams).
  - *ADRs*: Document architecturally significant decisions using Architecture Decision Records (Context, Decision, Consequences).
  - *Risk Matrix*: Calculate risk as Impact × Likelihood. Unproven tech = 9 (High Risk).
  - *Elastic Leadership*: Adjust architectural control based on team size, familiarity, and project complexity.
  - *Negotiation*: Use "Divide-and-Conquer" for extreme requirements (e.g., 5 nines). "Demonstration Defeats Discussion". Use collaborative grammar.
  - *Diagramming*: Enforce Representational Consistency (macro before micro). Use C4 Model. Avoid "Irrational Artifact Attachment" by starting low-fidelity.
  - *Career Path*: Follow the 20-Minute Rule for daily learning. Maintain a Technology Radar (Hold, Assess, Trial, Adopt).

## Architecture & Business Standards (DDD)

### 🎯 Directives

#### 1. Domain Analysis & Subdomains
- ALWAYS classify subdomains: **Core** (complex, competitive edge -> build in-house, Domain Model/Event Sourcing), **Generic** (complex, solved -> buy/open-source), **Supporting** (simple CRUD -> build in-house, Transaction Script/Active Record).
- ALWAYS use the **Ubiquitous Language (UL)** for all class, method, and variable names. NEVER use technical jargon (e.g., `Manager`, `Processor`).
- ALWAYS resolve ambiguous or synonymous business terms into strict, single-meaning definitions.

#### 2. Bounded Contexts (BC) & Integration
- ALWAYS enforce Bounded Contexts as strict linguistic and physical boundaries. One team per BC.
- ALWAYS define integration patterns explicitly (Context Map):
  - **Anticorruption Layer (ACL)**: ALWAYS use for downstream Core Subdomains to translate and protect against upstream legacy/foreign models.
  - **Open-Host Service (OHS) & Published Language (PL)**: ALWAYS use upstream to expose a stable, decoupled API (e.g., JSON schema) hiding internal implementation.
  - **Shared Kernel**: ONLY use for sharing minimal integration contracts.
  - **Separate Ways**: Duplicate functionality if integration cost > duplication cost (NEVER for Core Subdomains).

#### 3. Tactical Design (Domain Model)
- ALWAYS prefer **Value Objects (VO)** (immutable, no identity, value-based equality, side-effect-free, conceptual whole) over Entities.
- ALWAYS model **Entities** with unique, immutable identity (using custom VOs, e.g., `TenantId`) and mutable state. Use self-encapsulation (private setters).
- ALWAYS design **Aggregates** as strict transactional boundaries:
  - NEVER modify more than ONE Aggregate instance per database transaction. Use Eventual Consistency (Domain Events) for multi-aggregate updates.
  - NEVER reference other Aggregates by object reference; ALWAYS reference by ID.
  - ALWAYS keep Aggregates as small as possible (true invariants only).
  - ALWAYS designate one Entity as the **Aggregate Root (AR)**. All external access MUST go through the AR.
  - ALWAYS use Intention-Revealing Interfaces (e.g., `commitTo()`) and hide state mutation.
  - ALWAYS implement Optimistic Concurrency (e.g., `version` field) on the AR.
- ALWAYS use **Domain Services** for stateless operations spanning multiple Aggregates or requiring technical infrastructure. NEVER use them to strip behavior from Entities (Anemic Domain Model).
- ALWAYS use **Factories** (Factory Methods on ARs or Domain Services) to encapsulate complex creation and enforce invariants. Hide constructors.
- ALWAYS restrict **Repositories** to Aggregate Roots ONLY. Hide persistence details. NEVER manage transactions inside Repositories.

#### 4. Business Logic & Architecture Patterns
- ALWAYS align architecture with business logic complexity:
  - **Transaction Script**: Simple procedural logic. Use Minimal Layered Architecture. Test via Reversed Pyramid (E2E).
  - **Active Record**: Simple logic, complex data mapping. Use Layered Architecture + Application Service. Test via Diamond (Integration).
  - **Domain Model**: Complex rules/invariants. Use Ports & Adapters (Hexagonal). Test via Pyramid (Unit).
  - **Event-Sourced Domain Model (A+ES)**: Financial/audit-heavy domains. State is an append-only stream of Domain Events. ALWAYS pair with CQRS. Separate `Apply` (append event) and `Mutate` (update state).
- ALWAYS keep **Application Services** thin. They MUST ONLY handle task coordination, transaction boundaries, and security. NEVER put business logic in Application Services. Use Command Objects for input.

#### 5. Communication & Event-Driven Architecture (EDA)
- ALWAYS classify asynchronous messages: **Events** (past tense, e.g., `OrderSubmitted`) or **Commands** (imperative, e.g., `SubmitOrder`).
- ALWAYS select the correct Event type:
  - **Event Notification**: Lightweight ping (ID/link). Use for sensitive data or strict concurrency.
  - **Event-Carried State Transfer (ECST)**: State snapshot. Use for local caching/high availability.
  - **Domain Event**: Internal BC modeling. NEVER expose raw Domain Events externally; translate to a Published Language.
- ALWAYS use the **Outbox Pattern** (atomic save of state + outgoing events) to guarantee at-least-once delivery.
- ALWAYS design consumers to be **Idempotent**.
- ALWAYS use **Sagas** for linear, multi-step processes across BCs (with compensating actions). Use **Process Managers** for complex workflows with conditional routing.

#### 6. Microservices & Modules
- ALWAYS design Microservices as "deep modules" aligned with Subdomains. Encapsulate the database. Compress public interfaces (OHS).
- NEVER create "shallow services" (e.g., single-method or single-aggregate services) that cause Distributed Big Balls of Mud.
- ALWAYS group cohesive domain concepts into **Modules** (namespaces/packages) using the UL (e.g., `com.company.context.domain.model.concept`). NEVER group mechanically (e.g., all exceptions together).

#### 7. Legacy Modernization & Data Mesh
- ALWAYS use the **Strangler Pattern** with a Façade to incrementally replace legacy systems.
- ALWAYS treat analytical data as a **Data Product** owned by the operational Bounded Context (Data Mesh).
- ALWAYS use CQRS to project operational events into analytical **Fact** (append-only) and **Dimension** (normalized) tables. Expose via Polyglot Data Endpoints. NEVER extract directly from operational DB schemas.

#### 8. EventStorming
- ALWAYS follow the 10-step process for complex domains: Domain Events (Orange, past tense) -> Timelines -> Pain Points (Pink) -> Pivotal Events -> Commands (Blue, imperative) & Actors (Yellow) -> Policies (Purple) -> Read Models (Green) -> External Systems (Pink) -> Aggregates (Yellow) -> Bounded Contexts.

### 📝 Examples

#### ✅ DO
```csharp
// DO: Small Aggregate, ID references, Intention-Revealing Interface, Eventual Consistency
public class Ticket : Entity 
{
    private TicketId _id;
    private CustomerId _customerId; // ID reference, not object
    private int _version;

    // Hidden constructor
    protected Ticket() { }

    // Intention-revealing command
    public void Escalate(EscalationReason reason) 
    {
        if (this.IsClosed) throw new DomainException("Cannot escalate closed ticket.");
        
        this.IsEscalated = true;
        this._version++;
        
        // Publish Domain Event for eventual consistency
        DomainEventPublisher.Instance.Publish(new TicketEscalated(_id, reason));
    }
}

// DO: Thin Application Service handling transactions and coordination
public class TicketService 
{
    [Transactional]
    public void EscalateTicket(TicketId id, EscalationReason reason) 
    {
        var ticket = _repository.Load(id);
        ticket.Escalate(reason);
        _repository.Save(ticket); // Outbox pattern handled by repository/infrastructure
    }
}
```

#### ❌ DON'T
```csharp
// DON'T: Large cluster, object references, anemic domain model, multi-aggregate transactions
public class Ticket 
{
    public Guid Id { get; set; }
    public Customer Customer { get; set; } // Direct object reference
    public bool IsEscalated { get; set; }
}

public class TicketService 
{
    [Transactional]
    public void EscalateTicket(Guid ticketId, string reason) 
    {
        var ticket = _repository.Load(ticketId);
        
        // Business logic leaked into Application Service
        if (ticket.Status == "Closed") return; 
        
        ticket.IsEscalated = true;
        
        // Modifying multiple aggregates in one transaction
        ticket.Customer.EscalationCount++; 
        
        _repository.Save(ticket);
        _customerRepository.Save(ticket.Customer);
        
        // Unsafe event publishing (prone to dual-write failure)
        _messageBus.Publish(new TicketEscalatedEvent(ticketId)); 
    }
}
```

## Data Architecture and Strategy Standards

### 🎯 Directives

#### 1. Data Modeling & Schema Design (Relational & Dimensional)
- ALWAYS separate intrinsic identity (`PARTY`, `PERSON`, `ORGANIZATION`) from contextual roles (`CUSTOMER`, `EMPLOYEE`). Use `PARTY_RELATIONSHIP` for interactions.
- ALWAYS decouple marketing offerings (`PRODUCT`) from physical inventory (`PART`, `INVENTORY_ITEM`).
- ALWAYS unify Sales and Purchase transactions under a generic `ORDER` supertype. Link shipping/billing to `ORDER_ITEM`.
- NEVER overwrite financial data or quantities for corrections; ALWAYS use recursive adjusting `INVOICE_ITEM`s. Separate business transactions from accounting transactions (`TRANSACTION_DETAIL` with debit/credit).
- ALWAYS separate `WORK_REQUIREMENT` (need), `WORK_ORDER_ITEM` (commitment), and `WORK_EFFORT` (execution). Track historical state using `from_date` and `thru_date`. Derive statuses where possible.
- ALWAYS abstract addresses/phones into `CONTACT_MECHANISM` linked via associative entities with `PURPOSE` and `USAGE`.
- ALWAYS enforce Normalization (1NF, 2NF, 3NF) in logical models. Denormalize (Rolldown/Rollup) in physical models ONLY for explicit performance gains.
- ALWAYS resolve logical subtypes in physical models via Identity, Rolldown, or Rollup based on access patterns.
- ALWAYS design Data Warehouses using Star Schemas: a central `FACT` table (numeric measures, composite primary keys) surrounded by flattened `DIMENSION` tables (e.g., `TIME_BY_DAY`). NEVER extract Data Marts directly from operational systems; source from the EDW.

#### 2. Distributed Systems & Database Reliability
- ALWAYS select storage engines based on workload: B-Trees for read-heavy/predictable latency, LSM-Trees for write-heavy, Columnar (Parquet/ORC) with Bitmap/RLE for OLAP.
- ALWAYS configure replication appropriately: Single-Leader for strong consistency, Multi-Leader for geo-distribution (requires CRDTs), Leaderless for high availability (requires Quorum $W+R>N$).
- NEVER use Last Write Wins (LWW) with wall-clock timestamps; ALWAYS use Version Vectors. 
- ALWAYS wrap multi-object mutations in explicit ACID transactions. Prevent Lost Updates via atomic operations or `FOR UPDATE`. Prevent Write Skew via Serializable isolation or index-range locks.
- ALWAYS mitigate hot keys using salting. NEVER use `hash % N` for routing; use Consistent Hashing.
- ALWAYS use Fencing Tokens for distributed locks. Use 2PC for distributed transactions. Rely on ZooKeeper/etcd for consensus.
- ALWAYS treat event logs as immutable Systems of Record. Derive read-optimized Materialized Views (CQRS) deterministically. Use pure functions.
- ALWAYS prioritize MTTR over MTBF. Implement automated failover with STONITH. Monitor USE (Utilization, Saturation, Errors). Alert ONLY on imminent SLO violations.
- ALWAYS enforce Datensparsamkeit (Data Minimization). Implement crypto-shredding for GDPR right-to-erasure in immutable logs. Use Prepared Statements. Enforce TLS 1.2+ and PFS.
- NEVER treat replication as a backup. ALWAYS implement tiered physical backups and continuously test restores.

#### 3. Information Architecture & Content Strategy
- ALWAYS separate content meaning from visual presentation. Break content into semantic chunks (Elements) within Content Types. NEVER use WYSIWYG HTML blobs.
- ALWAYS implement COPE (Create Once, Publish Everywhere) using Adaptive Content (filtered by device constraints) rather than relying solely on Responsive Design.
- ALWAYS use Controlled Vocabularies. Define Preferred Terms (PT) and Variant Terms (VT/UF). Enforce the "All/Some" rule for Hierarchical relationships (BT/NT). Use Associative relationships (RT) for cross-hierarchy links.
- ALWAYS use Faceted Classification (mutually exclusive dimensions like Topic, Audience, Geography) for complex, heterogeneous content instead of rigid single hierarchies.
- ALWAYS tune search systems by weighting structural metadata. Implement "No Dead Ends" policies for zero-result SERPs.
- ALWAYS use Open Card Sorts for discovery and Closed Card Sorts for validation. NEVER use card sorting to test findability; use task-based usability testing.
- ALWAYS establish a Governance Board. Define strict rules for content lifecycles (Create, Review, Manage, Deliver).
- ALWAYS use URIs for entities and structure data as RDF Triples (Subject-Predicate-Object). Embed Schema.org microdata in HTML.

### 📝 Examples

#### ✅ DO
```sql
-- DO: Use associative entities with date ranges for historical tracking
CREATE TABLE party_role (
    party_id INT REFERENCES party(party_id),
    role_type_id INT REFERENCES role_type(role_type_id),
    from_date DATE NOT NULL,
    thru_date DATE,
    PRIMARY KEY (party_id, role_type_id, from_date)
);

-- DO: Star Schema Fact Table with composite dimension keys
CREATE TABLE sales_fact (
    time_id INT REFERENCES time_dim(time_id),
    product_id INT REFERENCES product_dim(product_id),
    customer_id INT REFERENCES customer_dim(customer_id),
    quantity_sold INT,
    gross_revenue DECIMAL(15,2),
    PRIMARY KEY (time_id, product_id, customer_id)
);
```

```json
// DO: Semantic, format-free content modeling for omnichannel delivery
{
  "content_type": "Recipe",
  "id": "rec_123",
  "metadata": {
    "audience": "Beginner",
    "dietary_tags": ["Vegan", "Gluten-Free"]
  },
  "elements": {
    "title": "Roasted Carrots",
    "teaser_mobile": "Quick and easy roasted carrots.",
    "ingredients": ["Carrots", "Olive Oil", "Salt"],
    "steps": ["Preheat oven to 400F.", "Roast for 20 mins."]
  }
}
```

```python
## DO: Safe distributed locking with Fencing Tokens
lock_token = coordination_service.acquire_lock("resource_x")
db.execute(
    "UPDATE table SET val = %s WHERE id = %s AND last_token <= %s", 
    (new_val, resource_id, lock_token)
)
```

#### ❌ DON'T
```sql
-- DON'T: Hardcode volatile attributes or repeating groups (1NF/3NF violations)
CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    phone_1 VARCHAR(20),
    phone_2 VARCHAR(20),
    current_status VARCHAR(50) -- Loses history
);

-- DON'T: Use operational keys in Fact Tables
CREATE TABLE sales_fact (
    invoice_id INT PRIMARY KEY, -- Anti-pattern: Prevents dimensional aggregation
    gross_revenue DECIMAL(15,2)
);
```

```html
<!-- DON'T: WYSIWYG blobs mixing content and presentation -->
<div class="article-body">
  <font size="5"><b>Roasted Carrots</b></font><br><br>
  <i>Quick and easy roasted carrots.</i><br>
  <ul><li>Carrots</li></ul>
</div>
```

```python
## DON'T: Naive read-modify-write vulnerable to Lost Updates
row = db.execute("SELECT value FROM counters WHERE id = ?", counter_id)
new_value = row['value'] + 1
db.execute("UPDATE counters SET value = ? WHERE id = ?", new_value, counter_id)
```

## Architecture & Integration Standards

### 🎯 Directives

#### API Design & RESTful Principles
- ALWAYS use standard HTTP methods correctly: `GET` (read, idempotent), `POST` (create/action), `PUT` (replace, idempotent), `PATCH` (partial update), `DELETE` (remove, idempotent).
- ALWAYS use nouns for resource URIs (e.g., `/users/123`), NEVER verbs (e.g., `/getUser/123`).
- ALWAYS enforce statelessness. NEVER store client session state on the server.
- ALWAYS implement pagination (cursor-based preferred for large datasets) and filtering via query parameters.
- ALWAYS version APIs (e.g., via `Accept` header or URI `/v1/`) and maintain backward compatibility (additive changes only).
- ALWAYS return standard HTTP status codes (2xx, 3xx, 4xx, 5xx) and structured, machine-readable error payloads.
- NEVER use Basic Authentication for public APIs; ALWAYS use OAuth 2.0 or JWT with granular scopes.

#### Messaging & Enterprise Integration Patterns
- ALWAYS decouple applications using asynchronous messaging (Publish-Subscribe for events, Point-to-Point for commands/documents).
- ALWAYS separate routing/system metadata (Headers) from business data (Body) in messages.
- ALWAYS use a Dead Letter Channel for undeliverable/expired messages and an Invalid Message Channel for parsing errors.
- ALWAYS implement Idempotent Receivers to safely handle duplicate message deliveries.
- NEVER hardcode reply channels; ALWAYS use a `Return Address` and `Correlation Identifier` for Request-Reply patterns.
- NEVER mix different data schemas on the same channel; ALWAYS use Datatype Channels.
- ALWAYS use a Messaging Gateway to encapsulate messaging infrastructure APIs away from business logic.

#### Microservices & API Gateways
- ALWAYS route external traffic through an API Gateway (Layer 7) for cross-cutting concerns (auth, rate limiting, SSL termination).
- ALWAYS assign an isolated, exclusive database to each microservice (Polyglot Persistence). NEVER share databases or use cross-service SQL JOINs.
- ALWAYS use Circuit Breakers with fallbacks and Retries (with exponential backoff) for downstream service calls.
- ALWAYS pass a Correlation ID across all microservice boundaries for distributed tracing.
- NEVER store rate-limiting counters or state in the API Gateway's local memory; use a distributed cache (e.g., Redis).

### 📝 Examples

#### ✅ DO
```http
GET /api/v1/users/123/orders?limit=50&cursor=eyJpZCI6MTIzNDV9 HTTP/1.1
Authorization: Bearer <token>
Accept: application/json
```

```java
// Messaging Gateway abstracting infrastructure
public interface OrderGateway {
    void sendOrder(Order order);
}
```

#### ❌ DON'T
```http
// Anti-pattern: Verbs in URI, stateful session cookie, missing version
POST /api/updateUserOrder HTTP/1.1
Cookie: session_id=abcxyz
```

```java
// Anti-pattern: Infrastructure leaked into business logic
public void processOrder(Order order) {
    JMSContext context = connectionFactory.createContext();
    // ...
}
```

## Architecture & Technology Standards

### 🎯 Core Directives

#### 1. Stability & Resilience (Cynical Software)
- **Timeouts & Limits**: ALWAYS configure explicit connection/read timeouts for EVERY external integration, DB, and socket. NEVER use infinite blocking. Bound all resource pools and queues.
- **Circuit Breakers & Bulkheads**: ALWAYS wrap risky external calls in Circuit Breakers with fallback strategies (e.g., defensive caching). Isolate resources (Bulkheads) so one failure doesn't sink the system.
- **Demand Control**: ALWAYS implement Load Shedding (return HTTP 503) and Backpressure when capacity/SLA is exceeded. Keep TCP listen queues short.
- **Resource Cleanup**: ALWAYS isolate resource closures (e.g., `try-with-resources`) so one exception doesn't leak subsequent resources.
- **Dogpile Prevention**: ALWAYS add randomized jitter/slew to retries, cron jobs, and cache expirations.
- **Unbounded Results**: NEVER return unbounded result sets. ALWAYS enforce pagination and `LIMIT` clauses.
- **Session Bloat**: NEVER store large object graphs in memory sessions. Store only lightweight identifiers (e.g., User ID) and rely on cookies, not URL parameters.
- **Component Restarts**: Favor dynamic component-level restarts (via lifecycle hooks) over rolling cluster reboots during acute thread-exhaustion incidents.

#### 2. Microservices & Architecture
- **Horizontal Scaling**: ALWAYS design for stateless horizontal scaling (concurrency & partitioning). NEVER rely on vertical scaling.
- **Loose Clustering**: ALWAYS use Service Discovery (Consul, etcd) and logical DNS/VIPs. NEVER hardcode physical IPs or hostnames. Instances must not statically know peers.
- **Decoupling**: ALWAYS prefer asynchronous decoupling (message queues, pub/sub) over synchronous RPC/HTTP where business logic permits.
- **Explicit Context (URL Dualism)**: ALWAYS use full URLs as identifiers in payloads instead of bare database IDs to prevent concept leakage and decouple authority.
- **Federated Data**: Reject the "Single System of Record" fallacy. Allow different bounded contexts to own their distinct facets of data.
- **Service Extinction**: ALWAYS delete unsuccessful/redundant services rather than merging them into complex monoliths.

#### 3. Zero-Downtime Deployment & CI/CD
- **Immutable Infrastructure**: ALWAYS deploy via immutable images (Containers, AMIs). NEVER write scripts to patch or mutate running production instances (Convergence).
- **Deployinator**: ALWAYS automate deployments completely. NEVER use manual playbooks, SSH into production, or require "Go/No-Go" meetings.
- **Database Migrations (Relational)**: ALWAYS split into two phases: 1) **Expansion** (add tables/nullable columns/shims, backward-compatible) -> Code Rollout -> 2) **Contraction** (cleanup, strict constraints, `NOT NULL`). NEVER apply breaking schema changes synchronously.
- **Database Migrations (NoSQL)**: ALWAYS use "Trickle, then Batch" (migrate documents on-read in app code, batch cleanup later).
- **Asset Versioning**: ALWAYS version static web assets by embedding the hash in the filename/path (e.g., `/v1a2b3c/app.css`). NEVER use query strings for cache-busting.
- **Health Checks & Draining**: ALWAYS implement deep `/health` checks verifying dependencies. Toggle to 503 to gracefully drain traffic before shutdown. Wait for cache warm-up before passing.

#### 4. API Evolution & Versioning
- **Postel's Law**: ALWAYS be conservative in what you send, liberal in what you accept.
- **Safe vs. Breaking**: Adding required fields, removing response fields, or tightening constraints are BREAKING changes. Adding optional inputs or new outputs are SAFE (Covariant/Contravariant).
- **Versioning**: ALWAYS implement breaking changes via explicit URL versioning (e.g., `/v2/`). Bump all routes simultaneously.
- **Controller Translation**: ALWAYS route old API versions through adapters to the current business logic. NEVER duplicate business logic.
- **Contract Testing**: ALWAYS split integration tests into outbound (spec compliance) and inbound (fuzzing/generative). NEVER rely on brittle end-to-end tests against live providers.

#### 5. Security & Access Control
- **Injection**: ALWAYS use parameterized queries. NEVER concatenate strings for SQL/NoSQL. Disable XXE in XML parsers.
- **Session Management**: ALWAYS use high-entropy, PRNG-generated session IDs stored ONLY in `Secure`, `HttpOnly`, `SameSite=Strict` cookies. Regenerate IDs on login.
- **Access Control**: ALWAYS return `404 Not Found` instead of `403 Forbidden` for unauthorized access to obscure resource existence. Use random UUIDs, not sequential IDs.
- **XSS & CSRF**: ALWAYS scrub input and contextually escape output. Require anti-CSRF tokens for state-changing requests.
- **Least Privilege**: ALWAYS run processes as unprivileged users, disable OS core dumps, and vault all secrets (KMS/Vault). NEVER log PII or secrets.

#### 6. Observability & Control Plane
- **Metrics & Logs**: ALWAYS inject Correlation/Trace IDs into logs. Log to stdout/external volume. Separate Host metrics (CPU/RAM) from Microservice metrics (RPS/Latency).
- **Actionable Alerts**: ALWAYS restrict `ERROR`/`SEVERE` logs to actionable system failures requiring operator intervention. Log user errors as `WARN`/`INFO`. Every alert MUST have a Runbook.
- **Governors**: ALWAYS implement "Governors" on automation scripts to hard-limit the blast radius of destructive actions (e.g., max 10% termination without human approval).
- **Admin APIs**: ALWAYS expose administrative APIs on private/internal NICs. NEVER implement "flush cache" or schema wipe commands in production APIs.

#### 7. Chaos Engineering
- **Empirical Resilience**: ALWAYS validate resilience empirically via Chaos Engineering. Define a steady state, formulate an externally observable hypothesis, and limit the blast radius.
- **Fault Injection**: Use Instance Death for autoscaling tests, Latency Injection for race conditions, and Failure Injection Testing (FIT) via request tagging for downstream failures.

### 📝 Examples

#### ✅ DO: Safe Resource Cleanup & Timeouts
```java
// Explicit timeouts and isolated cleanup via try-with-resources
HikariConfig config = new HikariConfig();
config.setConnectionTimeout(3000); // 3s timeout, no infinite blocking
HikariDataSource ds = new HikariDataSource(config);

try (Connection conn = ds.getConnection();
     PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users LIMIT 100")) {
    stmt.setQueryTimeout(5);
    ResultSet rs = stmt.executeQuery();
} catch (SQLException e) {
    log.error("Database integration failed", e);
    throw new ServiceDegradedException();
}
```

#### ❌ DON'T: Unbounded Queries & Leaky Cleanup
```java
Connection conn = null;
Statement stmt = null;
try {
    conn = pool.getConnection(); // Blocks infinitely if pool exhausted
    stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery("SELECT * FROM audit_logs"); // Unbounded result set (OOM risk)
} finally {
    if (stmt != null) stmt.close(); // If this throws, conn is leaked!
    if (conn != null) conn.close();
}
```

#### ✅ DO: API Versioning via Controller Translation
```javascript
// V2 Controller (Current Business Logic)
async function createApplicationV2(req, res) {
    const result = await BusinessLogic.createApplication(req.body);
    res.json(result);
}

// V1 Controller (Adapter)
async function createApplicationV1(req, res) {
    // Translate V1 to V2 (provide defaults for new required fields)
    const v2Data = { ...req.body, newRequiredField: 'DEFAULT' };
    const result = await BusinessLogic.createApplication(v2Data);
    // Translate V2 back to V1 (strip new fields)
    res.json(mapToV1Response(result));
}
```

#### ❌ DON'T: Breaking API Changes
```javascript
// Adding a required field to an existing endpoint breaks all current consumers
async function createApplicationV1(req, res) {
    if (!req.body.newRequiredField) {
        return res.status(400).send("Missing newRequiredField"); // BREAKS CONSUMERS
    }
}
```

#### ✅ DO: Zero-Downtime Database Expansion
```sql
-- Phase 1: Expansion (Run before code deploy)
ALTER TABLE users ADD COLUMN first_name VARCHAR(255);
-- Shim to keep old code working
CREATE TRIGGER sync_names BEFORE INSERT OR UPDATE ON users FOR EACH ROW EXECUTE FUNCTION split_full_name();

-- Phase 2: Contraction (Run AFTER 100% code deploy)
DROP TRIGGER sync_names ON users;
ALTER TABLE users DROP COLUMN full_name;
ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
```

#### ❌ DON'T: Synchronous Breaking Schema Changes
```sql
-- Causes immediate downtime for running instances
ALTER TABLE users RENAME COLUMN full_name TO first_name;
ALTER TABLE users ADD COLUMN last_name VARCHAR(255) NOT NULL;
```

## CLI Command Standards

### 🎯 Directives
- ALWAYS output the result of all commands to a `.txt` file.
- NEVER run a command without redirecting its output to a text file (e.g., `command > output.txt 2>&1`).

## Configuration and Environment Standards

### 🎯 Directives
- ALWAYS use the setting module in `packages/koda/src/koda/config/main.py` for all the config.
- ALL modules or any part of the system MUST update the setting module and get config from the setting module.

### 📝 Examples

#### ✅ DO
```python
from koda.config.main import settings

def connect_to_db():
    db_url = settings.consul_base_url
    # use db_url
```

#### ❌ DON'T
```python
import os

def connect_to_db():
    # DON'T use os.getenv directly in modules
    db_url = os.getenv("CONSUL_BASE_URL", "http://localhost:8500")
```

## language-python

### Anti-Patterns Standards

#### 🎯 Directives
- NEVER violate the Law of Least Surprise; if a function's behavior or implementation is surprising, it MUST be refactored or heavily documented.
- NEVER use mutable objects (`list`, `dict`, `set`) as default arguments in function signatures.
- NEVER use `time.sleep()` to wait for UI or asynchronous state changes; ALWAYS use explicit polling/wait loops.
- NEVER use `monkeypatching` or `mock.patch` for internal application dependencies; ALWAYS use Dependency Injection and Fakes.
- NEVER use `Any` in type hints unless absolutely necessary; it defeats static analysis.
- NEVER use `IntEnum` or `IntFlag`; they allow implicit integer conversion and break type safety.
- NEVER use `dict` or `tuple` for heterogeneous domain concepts; ALWAYS use `@dataclass` or standard classes.
- NEVER use `list` to store millions of numeric primitives; ALWAYS use `array.array` or `numpy.array`.
- NEVER use `map()` or `filter()` with lambdas; ALWAYS use list comprehensions or generator expressions.
- NEVER use `is` to compare values (like strings or integers); ALWAYS use `==`. `is` is strictly for identity (e.g., `is None`).
- NEVER implement `__del__` for resource cleanup; ALWAYS use context managers (`with`).
- NEVER raise `NotImplementedError` in a subclass to disable inherited behavior; this violates the Liskov Substitution Principle.
- NEVER use the ORM for complex read queries that cause SELECT N+1 issues; ALWAYS use raw SQL or denormalized views for read models.
- NEVER use the `time` module for timezone math; ALWAYS use `datetime` and `pytz` (or `zoneinfo`).
- NEVER use timezone-unaware `datetime` objects (e.g., `datetime.utcnow()`, `datetime.now()`). ALWAYS use timezone-aware objects (e.g., `datetime.now(tz=...)`).
- NEVER use `pickle` for untrusted data; ALWAYS use JSON or another safe serialization format.
- NEVER use `float` for exact math (e.g., currency); ALWAYS use `decimal.Decimal`.
- NEVER use `list.pop(0)` for queues; ALWAYS use `collections.deque`.
- NEVER use `list.index()` on sorted lists; ALWAYS use `bisect`.
- NEVER use `list` with `.sort()` for priority queues; ALWAYS use `heapq`.
- NEVER slice `bytes` for large I/O; ALWAYS use `memoryview` or `bytearray` for zero-copy operations.
- NEVER use `eval()` on untrusted strings; ALWAYS use `ast.literal_eval()`.
- NEVER use wildcard imports (`from module import *`).
- NEVER use blocking I/O (e.g., `requests`, `time.sleep()`) inside `async def` coroutines.
- NEVER use `ThreadPoolExecutor` for CPU-bound tasks; ALWAYS use `ProcessPoolExecutor` or `multiprocessing`.
- NEVER use `ProcessPoolExecutor` for I/O-bound tasks; ALWAYS use `ThreadPoolExecutor` or `asyncio`.
- NEVER use `__dict__` for classes with millions of instances; ALWAYS use `__slots__`.
- NEVER write long `isinstance` chains; ALWAYS use `@functools.singledispatch`.
- NEVER call `super(Class, self)` in Python 3; ALWAYS use the zero-argument `super()`.
- NEVER define `__init__` or state in Mixin classes.
- NEVER implement `__getattr__` without also implementing `__setattr__` to prevent state desynchronization.
- NEVER use `__new__` in metaclasses for simple subclass validation or registration; ALWAYS use `__init_subclass__`.
- NEVER use metaclasses for composable class extensions; ALWAYS prefer class decorators.
- NEVER unpack more than three variables when functions return multiple values; ALWAYS use a small class or `namedtuple`.
- NEVER use more than two control subexpressions in comprehensions; they become unreadable.
- NEVER inject data into generators with `send` or cause state transitions with `throw`; they add unnecessary complexity.
- NEVER use setter and getter methods; ALWAYS use plain attributes or `@property`.
- NEVER create new thread instances for on-demand fan-out; ALWAYS use `ThreadPoolExecutor`.
- NEVER block the `asyncio` event loop; ALWAYS use `run_in_executor` for blocking I/O.
- NEVER read `__annotations__` directly; ALWAYS use `inspect.get_annotations()`.
- NEVER use `TypedDict` for runtime validation; ALWAYS use `pydantic`.
- NEVER use `Union` of concrete classes for shared behavior; ALWAYS use `typing.Protocol`.
- NEVER use `issubclass()` on a Protocol that contains data attributes.
- NEVER use `assert` for runtime data validation; ALWAYS raise `ValueError` or custom exceptions.
- NEVER use `assertContains` with raw HTML strings in tests; ALWAYS parse HTML with `lxml` or similar.
- NEVER use raw `assert` in `unittest.TestCase`; ALWAYS use `self.assertEqual`, `self.assertTrue`, etc.
- NEVER mock internal framework utilities (e.g., Django messages); assert against the resulting state.
- NEVER patch a dependency where it is defined; ALWAYS patch it in the target namespace where it is used.
- NEVER use `mock.patch` without `spec=True` or passing the target class to `spec`.
- NEVER couple Domain Models to ORM classes (e.g., inheriting from `db.Model` or `Base`). ALWAYS use classical mapping or separate ORM models.
- NEVER pass Domain Objects into Service Layer functions from the outside (e.g., from API endpoints); ALWAYS pass primitives to fully decouple the Service Layer from the Domain Model.
- NEVER subclass built-in types like `dict`, `list`, or `str` directly; ALWAYS use `collections.UserDict`, `collections.UserList`, or `collections.UserString` to avoid C-level method bypass bugs.
- NEVER create instance attributes outside of `__init__`; it defeats the PEP 412 Key-Sharing Dictionary memory optimization.
- NEVER depend on string or integer interning for equality checks. ALWAYS use `==` instead of `is` to compare strings or integers.
- NEVER use `functools.reduce()` for boolean checks; ALWAYS use `all()` or `any()` to benefit from short-circuiting.
- NEVER organize code by types (e.g., `exceptions.py`, `functions.py`); ALWAYS organize by features.
- NEVER perform a `SELECT` to check for existence before an `INSERT` to enforce uniqueness; ALWAYS rely on database `UNIQUE` constraints and catch the exception to avoid race conditions.

#### 📝 Examples

##### ❌ DON'T
```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

##### ✅ DO
```python
def add_item(item, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### Architecture and Structure Standards

#### 🎯 Directives
- ALWAYS separate domain logic from infrastructure concerns (Domain-Driven Design).
- ALWAYS distinguish between Entities (identity equality, mutable) and Value Objects (value equality, immutable).
- ALWAYS use `@dataclass(frozen=True)` for Value Objects.
- ALWAYS implement `__eq__` and `__hash__` for Entities based on their unique reference/identity, not their attributes.
- ALWAYS use Domain Service functions for business logic that doesn't naturally fit inside a single Entity or Value Object.
- ALWAYS use the Repository Pattern to abstract data access. Repositories MUST only return and accept Aggregate Roots.
- ALWAYS use the Unit of Work (UoW) pattern to abstract atomic operations. Use context managers (`with uow:`).
- ALWAYS require explicit commits (`uow.commit()`) and rollback by default on exceptions or early exits.
- ALWAYS encapsulate use cases in a Service Layer. Service functions MUST accept primitive types, not domain objects.
- ALWAYS use a Message Bus to route Commands (1:1 routing) and Events (1:N routing).
- ALWAYS separate read operations from write operations (CQRS). Use raw SQL or denormalized views for read models.
- ALWAYS decouple microservices using Event-Driven Architecture and message brokers (e.g., Redis, Kafka).
- ALWAYS compose classes instead of nesting many levels of built-in types (e.g., dict of dicts).
- ALWAYS accept functions instead of classes for simple interfaces (e.g., using `__call__` or passing a callable).
- ALWAYS use `@classmethod` polymorphism to construct objects generically instead of `__init__` overloading.
- ALWAYS inherit from `collections.abc` for custom container types to ensure all required methods are implemented.
- ALWAYS use packages to organize modules and provide stable APIs (using `__all__` in `__init__.py`).
- ALWAYS apply the Functional Core, Imperative Shell pattern: pure functions for business logic, imperative shell for I/O and state.
- ALWAYS use Dependency Injection. Pass dependencies explicitly to handlers/services.
- ALWAYS centralize dependency wiring in a Composition Root (e.g., `bootstrap.py`).
- ALWAYS use `mkinit` to automatically generate `__init__.py` files.
- ALWAYS define `__all__` in your modules to explicitly declare public APIs for `mkinit` to pick up.
- ALWAYS redirect after a POST request (Post/Redirect/Get pattern) to prevent duplicate submissions.
- ALWAYS follow YAGNI (You Aren't Gonna Need It) and build the Minimum Viable App first. Do not add features or infrastructure until tests demand them.
- ALWAYS apply the "Unicode Sandwich" pattern for text processing: decode bytes to `str` as early as possible on input, process exclusively with `str`, and encode to bytes as late as possible on output.
- ALWAYS use a proxy/load-balancer (e.g., NGINX, Traefik) in front of ASGI/WSGI servers to handle static assets and use a CDN when possible.
- ALWAYS subclass `collections.UserDict`, `collections.UserList`, or `collections.UserString` when extending built-in collections. NEVER subclass `dict`, `list`, or `str` directly, as their C implementations bypass overridden methods.
- ALWAYS organize code based on features, not on types. NEVER create modules like `exceptions.py` or `functions.py` that group code by type.
- ALWAYS isolate ORM libraries in a specific storage module (e.g., `myapp.storage`) to easily swap them out and prevent ORM objects from leaking.
- ALWAYS rely on RDBMS constraints (e.g., `UNIQUE`) and catch the resulting exceptions (e.g., `UniqueViolationError`) instead of performing a `SELECT` followed by an `INSERT` to prevent race conditions.
- NEVER place database queries, orchestration logic, or domain rules inside API endpoints (e.g., Flask/Django views).
- NEVER allow the Domain Model to import or invoke infrastructure code (e.g., ORMs, email clients).
- NEVER couple Domain Models to ORM classes (e.g., inheriting from `db.Model` or `Base`). ALWAYS use classical mapping or separate ORM models to ensure the ORM depends on the model, not the other way around.

#### 📝 Examples

##### ✅ DO
```python
def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        batchref = product.allocate(line)
        uow.commit()
    return batchref
```

##### ❌ DON'T
```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    batches = session.query(Batch).all()
    line = OrderLine(request.json['orderid'], request.json['sku'], request.json['qty'])
    model.allocate(line, batches)
    session.commit()
    return jsonify({'status': 'ok'})
```

### Code Style and Formatting Standards

#### 🎯 Directives
- ALWAYS choose the collection type that explicitly communicates your intent: `list` for mutable sequences, `tuple` for fixed-size immutable records, `set` for uniqueness, and `dict` for key-value mapping.
- ALWAYS use specialized collections (`collections.Counter`, `collections.defaultdict`, `frozenset`) when they match the domain problem to reduce boilerplate and communicate intent.
- ALWAYS use `for` loops for side effects, `while` loops for condition-based iteration, and comprehensions for transforming collections without side effects.
- NEVER use static indexing (e.g., `my_list[4]`) on dynamic collections like lists or dicts; ALWAYS use dynamic indexing or iteration. Static indexing is only acceptable for tuples or fixed-format parsing.
- ALWAYS adhere strictly to PEP 8 formatting guidelines.
- ALWAYS prefer Pythonic code and module-level functions instead of Java-like class spaghetti (e.g., avoid creating classes with only static methods or a single `__init__` and `run` method).
- ALWAYS use 4 spaces for indentation. NEVER use tabs.
- ALWAYS limit line length to 79 characters.
- ALWAYS use interpolated f-strings (`f"{var}"`) for string formatting. NEVER use `%s` or `.format()`.
- ALWAYS prefer multiple assignment unpacking over explicit numeric indexing (e.g., `a, b = b, a`).
- ALWAYS use `enumerate()` when iterating over a sequence and needing the index.
- ALWAYS use `zip()` to iterate over multiple sequences in parallel.
- ALWAYS use the walrus operator (`:=`) to assign and evaluate expressions simultaneously, avoiding redundant computation.
- ALWAYS prefer list, dict, and set comprehensions over `map()` and `filter()`.
- ALWAYS use generator expressions `(...)` instead of list comprehensions `[...]` for large datasets to prevent memory exhaustion.
- ALWAYS use `yield from` to compose multiple nested generators.
- ALWAYS use `match/case` (Python 3.10+) for structural parsing and destructuring.
- ALWAYS enforce clarity with keyword-only and positional-only arguments.
- ALWAYS define function decorators with `functools.wraps` to preserve metadata.
- ALWAYS use `functools.partial` instead of `lambda` functions for better readability, reusability, and to overcome lambda's single-line limitation.
- ALWAYS use `@contextlib.contextmanager` to create simple context managers instead of writing full classes with `__enter__` and `__exit__`.
- ALWAYS use `None` and docstrings to specify dynamic default arguments.
- ALWAYS consider `itertools` for working with iterators and generators.
- ALWAYS prefer public attributes over private ones unless you strictly need to avoid naming conflicts with subclasses.
- ALWAYS use `try/except/else/finally` blocks appropriately: `else` for success paths, `finally` for guaranteed cleanup.
- ALWAYS use `for/else` and `while/else` constructs to handle loop exhaustion without using boolean flags.
- ALWAYS group imports in three alphabetical sections: standard library, third-party, and local modules.
- ALWAYS design sequence constructors to take data as an iterable argument, matching the behavior of built-in sequence types.

#### 📝 Examples

##### ✅ DO
```python
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} has {calories} calories')

if (count := fresh_fruit.get('banana', 0)) >= 2:
    make_smoothies(count)
```

##### ❌ DON'T
```python
for i in range(len(snacks)):
    item = snacks[i]
    print('#%d: %s has %d calories' % (i + 1, item[0], item[1]))

count = fresh_fruit.get('banana', 0)
if count >= 2:
    make_smoothies(count)
```

### Configuration and Environment Standards

#### 🎯 Directives
- ALWAYS follow the 12-Factor App methodology: store configuration that varies between environments in environment variables.
- ALWAYS implement "fail hard" logic for secrets in production. Raise `KeyError` if a required secret is missing when `DEBUG=False`.
- ALWAYS use a `requirements.txt` (or `pyproject.toml`/`uv.lock`) to explicitly declare production dependencies.
- ALWAYS separate development/testing dependencies from production dependencies.
- ALWAYS use Docker for containerization to ensure reproducible environments.
- ALWAYS use lightweight base images (e.g., `python:3.12-slim`).
- ALWAYS run applications as a nonroot user inside Docker containers.
- ALWAYS use bind mounts (`--mount type=bind`) for stateful data (like SQLite databases) and ensure host file permissions match the container's nonroot UID.
- ALWAYS use a production-ready WSGI/ASGI server (e.g., Gunicorn, Uvicorn) in Docker. NEVER use development servers (e.g., Django's `runserver`) in production.
- ALWAYS configure logging to output to the console (`StreamHandler`) so Docker can capture tracebacks.
- ALWAYS use `WhiteNoise` or a reverse proxy (Nginx) to serve static files in production.
- ALWAYS use declarative Infrastructure as Code (IaC) tools like Ansible for server provisioning and deployment.

#### 📝 Examples

##### ✅ DO
```python
import os

if "DJANGO_DEBUG_FALSE" in os.environ:
    DEBUG = False
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
    ALLOWED_HOSTS = [os.environ["DJANGO_ALLOWED_HOST"]]
else:
    DEBUG = True
    SECRET_KEY = "dev-secret-key"
    ALLOWED_HOSTS = []
```

##### ❌ DON'T
```python
### Fails silently and runs insecurely in production
DEBUG = os.environ.get("DEBUG", False)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
```

### Dependency Management Standards

#### 🎯 Directives
- ALWAYS pin external package dependencies to specific versions to ensure reproducibility.
- ALWAYS use isolated virtual environments (`venv`, `poetry`, `uv`) to prevent dependency conflicts.
- ALWAYS use `pdm config use_uv true` when using PDM to leverage uv for faster dependency resolution and installation.
- ALWAYS actively prevent circular physical dependencies. If A imports B and B imports A, extract shared logic to a lower-level module or use Dependency Inversion.
- ALWAYS use dynamic imports (importing inside a function) ONLY as a last resort to break unavoidable circular dependencies.
- ALWAYS encapsulate external libraries with proprietary API wrappers. Do not let third-party library objects leak deep into the core domain logic.
- ALWAYS evaluate external dependencies against safety criteria: Python 3 compatibility, active maintenance, license compatibility.
- ALWAYS prefer the Python Standard Library over external dependencies for basic utilities (`itertools`, `collections`, `datetime`, `argparse`).
- ALWAYS use `stevedore` or `setuptools` entry points when building plug-in architectures to dynamically load extensions.
- ALWAYS use PEP 440 compliant version numbering (e.g., `1.2.0`, `2.3.1b2`).
- ALWAYS use declarative configuration (`setup.cfg` or `pyproject.toml`) for package metadata instead of complex `setup.py` scripts.

#### 📝 Examples

##### ✅ DO
```python
### db_wrapper.py
import external_orm_library

class DatabaseAPI:
    def get_user(self, user_id: int) -> dict:
        return external_orm_library.fetch(user_id)
```

##### ❌ DON'T
```python
### business_logic.py
import external_orm_library # Leaking external dependency into core logic

def process_user(user_id: int):
    user = external_orm_library.fetch(user_id)
```

### Documentation and Comments Standards

#### 🎯 Directives
- ALWAYS write PEP 257 compliant docstrings for EVERY module, class, and public function/method.
- ALWAYS ensure the first line of a docstring is a concise summary. Subsequent paragraphs MUST detail arguments, return values, and raised exceptions.
- ALWAYS document class invariants explicitly in the class-level docstring.
- ALWAYS use Sphinx, `autodoc`, and `autosummary` for generating project documentation from reST (`.rst`) files.
- ALWAYS embed interactive Python examples starting with `>>>` in docstrings to utilize the `doctest` module.
- ALWAYS use the `warnings` module (`warnings.warn`) with `DeprecationWarning` and an appropriate `stacklevel` (e.g., 2 or 3) when deprecating APIs.
- ALWAYS use the `.. deprecated:: <version>` Sphinx directive in docstrings for deprecated elements.
- ALWAYS document API changes thoroughly, including new elements, deprecated elements, and explicit migration instructions.
- ALWAYS consider using libraries like `debtcollector` to automate deprecation warnings and docstring updates.
- NEVER duplicate type information in the docstring if it is already provided via `typing` annotations in the function signature.
- NEVER write comments that merely repeat what the code is doing. Comments MUST explain the *why* or the business context.

#### 📝 Examples

##### ✅ DO
```python
import warnings

def calculate_velocity(distance: float, time: float) -> float:
    """Calculate velocity given distance and time.
    
    >>> calculate_velocity(100.0, 2.0)
    50.0
    """
    if time <= 0:
        raise ValueError("Time must be positive")
    return distance / time

def old_calculate(d: float, t: float) -> float:
    """
    .. deprecated:: 2.0
       Use :func:`calculate_velocity` instead.
    """
    warnings.warn("old_calculate is deprecated", DeprecationWarning, stacklevel=2)
    return calculate_velocity(d, t)
```

##### ❌ DON'T
```python
def calc(d, t):
    # divide d by t
    return d / t
```

### Error Handling Standards

#### 🎯 Directives
- ALWAYS use `Optional[T]` or `Union[T, ErrorType]` for expected failure modes (e.g., not finding an element) because return types can be statically checked, whereas exceptions cannot.
- ALWAYS use exceptions for truly exceptional, unexpected use cases (e.g., network failures, database down) that you wish to guard against.
- NEVER use exceptions for normal control flow or expected business logic failures.
- ALWAYS raise specific, documented exceptions (e.g., `ValueError`, `KeyError`, or custom domain exceptions) for failure states.
- ALWAYS use custom exceptions to express domain concepts (e.g., `OutOfStock`, `AllocationError`) rather than generic exceptions. These should be part of the ubiquitous language.
- NEVER return implicit `None` or magic numbers (like `-1`) to indicate an error. ALWAYS use explicit `Optional` or `Union` types so the typechecker can enforce handling.
- ALWAYS define a root exception (`class Error(Exception): pass`) for every module/package, and have all custom exceptions inherit from it.
- ALWAYS catch specific exceptions. NEVER use bare `except:` or `except Exception:` unless at the absolute top-level boundary for logging/crash reporting.
- ALWAYS use `contextlib.suppress(ExceptionType)` to explicitly ignore specific exceptions instead of `try: ... except: pass`.
- ALWAYS use the `tenacity` library (`@retry`, `Retrying`) to implement synchronous error recovery and exponential backoff for transient failures (e.g., network requests, database deadlocks).
- ALWAYS use `finally` blocks or context managers (`with`) to guarantee resource cleanup (e.g., closing files, releasing locks) regardless of success or failure.
- ALWAYS take advantage of each block in `try/except/else/finally`.
- ALWAYS consider `contextlib` and `with` statements for reusable `try/finally` behavior.
- ALWAYS use `else` blocks in `try/except` constructs to isolate the code that should only run if no exception occurred, keeping the `try` block as small as possible.

#### 📝 Examples

##### ✅ DO
```python
class MyModuleError(Exception):
    pass

class InvalidInputError(MyModuleError):
    pass

class OutOfStock(MyModuleError):
    pass

def process_data(data: str) -> dict:
    try:
        parsed = parse_json(data)
    except JSONDecodeError as e:
        raise InvalidInputError("Data is not valid JSON") from e
    else:
        return enrich_data(parsed)
```

##### ❌ DON'T
```python
def process_data(data: str):
    try:
        parsed = parse_json(data)
        return enrich_data(parsed)
    except Exception:
        return None # Silent failure, returns None
```

### Logging and Observability Standards

#### 🎯 Directives
- ALWAYS use the standard `logging` module. NEVER use `print()` for application logs in production code.
- ALWAYS use `logging.exception("message")` inside `except` blocks to automatically log the full stack trace of the caught exception.
- ALWAYS configure a `StreamHandler` outputting to the console (stdout/stderr) in containerized environments (Docker) so logs are captured by the container runtime.
- ALWAYS inject debug log statements immediately before invoking handlers in a Message Bus or Event-Driven Architecture (e.g., `logger.debug('handling event %s', event)`).
- ALWAYS use structured logging or include contextual identifiers (e.g., `order_id`, `user_id`) in log messages to facilitate tracing across distributed systems.
- ALWAYS configure appropriate log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Use `INFO` for normal operational milestones and `DEBUG` for detailed tracing.
- ALWAYS capture warnings in the logging system using `logging.captureWarnings(True)` in production configurations.

#### 📝 Examples

##### ✅ DO
```python
import logging

logger = logging.getLogger(__name__)

def process_payment(order_id: str, amount: float) -> None:
    logger.info("Processing payment for order %s: $%.2f", order_id, amount)
    try:
        charge_card(amount)
    except PaymentGatewayError:
        logger.exception("Payment failed for order %s", order_id)
        raise
```

##### ❌ DON'T
```python
def process_payment(order_id: str, amount: float) -> None:
    print(f"Processing payment for {order_id}")
    try:
        charge_card(amount)
    except PaymentGatewayError as e:
        print(f"Error: {e}") # Loses the stack trace
```

### Naming Conventions Standards

#### 🎯 Directives
- ALWAYS use `lowercase_underscore` (snake_case) for functions, variables, methods, and module names.
- ALWAYS use `CapitalizedWord` (PascalCase) for classes and exception names.
- ALWAYS use `ALL_CAPS_WITH_UNDERSCORES` for module-level constants.
- ALWAYS use a single leading underscore (`_protected`) for protected instance attributes and internal module functions.
- ALWAYS use a double leading underscore (`__private`) ONLY for private instance attributes to invoke name mangling and prevent subclass collisions.
- ALWAYS name the first parameter of instance methods `self`.
- ALWAYS name the first parameter of class methods `cls`.
- ALWAYS name Commands using the imperative mood (verb phrases, e.g., `Allocate`, `CreateBatch`).
- ALWAYS name Events using past-tense verb phrases (e.g., `Allocated`, `BatchCreated`).
- ALWAYS suffix exception classes with `Error` (e.g., `OutOfStockError`).
- ALWAYS suffix mixin classes with `Mixin` (e.g., `JSONSerializableMixin`).
- ALWAYS use language-agnostic, kebab-case, lowercase filenames for markdown/documentation files (e.g., `naming-conventions.md`).

#### 📝 Examples

##### ✅ DO
```python
MAX_RETRIES = 3

class OrderProcessor:
    def __init__(self):
        self._internal_cache = {}
        
    def process_order(self, order_id: str) -> None:
        pass

@dataclass
class OrderCreated(Event):
    order_id: str
```

##### ❌ DON'T
```python
MaxRetries = 3

class order_processor:
    def ProcessOrder(self, OrderId: str):
        pass

@dataclass
class CreateOrderEvent(Event): # Imperative mood for an event
    order_id: str
```

### Performance and Optimization Standards

#### 🎯 Directives
- NEVER optimize prematurely. ALWAYS profile first using `cProfile`, `memory_profiler`, or `Scalene` to identify actual bottlenecks.
- ALWAYS use `__slots__` for classes that will have millions of instances to prevent `__dict__` memory overhead.
- ALWAYS use `collections.deque` for FIFO queues to achieve O(1) appends and pops. NEVER use `list.pop(0)`.
- ALWAYS use `bisect` for O(log N) searches in sorted lists. NEVER use `list.index()`.
- ALWAYS use `heapq` for priority queues. NEVER use a `list` with continuous `.sort()` calls.
- ALWAYS use `memoryview` and `bytearray` for zero-copy I/O operations. NEVER slice large `bytes` objects.
- ALWAYS use `numpy` arrays and `numexpr` for heavy vectorized math. Avoid creating large temporary arrays in memory.
- ALWAYS use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` for CPU-bound tasks to bypass the GIL.
- ALWAYS use `asyncio` or `concurrent.futures.ThreadPoolExecutor` for I/O-bound tasks.
- ALWAYS use `subprocess` to manage child processes for parallel execution.
- ALWAYS use threads for blocking I/O, but avoid them for parallelism due to the GIL.
- ALWAYS use `Lock` to prevent data races in threads.
- ALWAYS use `Queue` to coordinate work between threads.
- ALWAYS achieve highly concurrent I/O with coroutines (`asyncio`).
- ALWAYS consider `concurrent.futures` for true parallelism.
- ALWAYS use `tracemalloc` to understand memory usage and leaks.
- ALWAYS use Numba (`@njit`) or Cython to compile tight, CPU-bound mathematical loops to machine code.
- ALWAYS use probabilistic data structures (e.g., HyperLogLog, Bloom Filters) when exact counts/membership are not required but memory is strictly constrained.
- ALWAYS use generators (`yield`) to stream large datasets instead of loading everything into RAM.
- NEVER optimize prematurely. ALWAYS profile first using `cProfile`, `line_profiler`, `memory_profiler`, `Scalene`, or `py-spy` to identify actual bottlenecks.
- ALWAYS encapsulate performance-critical code inside functions rather than running it at the module level to benefit from faster local variable lookups (`LOAD_FAST` vs `LOAD_GLOBAL`).
- ALWAYS initialize all instance attributes inside `__init__` to leverage the PEP 412 Key-Sharing Dictionary optimization. NEVER create new instance attributes after `__init__`.
- ALWAYS use `functools.lru_cache(maxsize=2**N)` with a power of 2 for optimal performance, or `functools.cache` if memory is not a concern.
- ALWAYS use `all()` and `any()` for short-circuiting boolean evaluations on iterables instead of `functools.reduce()`.
- ALWAYS use `run_in_executor` to offload CPU-bound or blocking I/O functions to a separate thread or process when using `asyncio`, to avoid blocking the event loop.
- ALWAYS use `set` or `frozenset` for membership testing (`in` operator) on large collections. NEVER use `list` or `tuple` for O(N) lookups.
- ALWAYS use `set` operations (e.g., `set(a) - set(b)`) instead of iterating over lists to find differences or invalid fields.
- ALWAYS use `collections.defaultdict` and `collections.Counter` instead of manual dictionary manipulation for grouping and counting.
- ALWAYS use `"".join()` to concatenate strings in a loop. NEVER use the `+=` operator for string concatenation in loops due to quadratic memory reallocation costs.
- ALWAYS consider tuning the garbage collector (`gc.set_threshold()`) or temporarily disabling it (`gc.disable()`) during massive object creation phases to prevent GC pauses.
- ALWAYS use `Polars`, `Dask`, or `Ray` for data processing tasks that exceed single-machine memory limits or require distributed cluster computing.
- ALWAYS avoid defining functions within functions (unless creating a closure) to prevent needless `MAKE_FUNCTION` bytecode overhead on every call.
- ALWAYS consider using the `dis` module to disassemble and understand Python bytecode for micro-optimizations.
- NEVER run performance-critical loops at the global module scope; ALWAYS wrap them in a function to avoid `LOAD_GLOBAL` overhead.

#### 📝 Examples

##### ✅ DO
```python
import collections

queue = collections.deque()
queue.append(item)
processed = queue.popleft() # O(1)
```

##### ❌ DON'T
```python
queue = []
queue.append(item)
processed = queue.pop(0) # O(N)
```

##### ✅ DO
```python
import functools

@functools.lru_cache(maxsize=128)
def expensive_computation(x: int) -> int:
    return x * x

def process_items(items: list[str]) -> str:
    # Fast local variable lookup and efficient string concatenation
    valid_items = {"apple", "banana", "orange"} # O(1) lookup
    return "".join(item for item in items if item in valid_items)
```

##### ❌ DON'T
```python
### Global scope loop is slow due to LOAD_GLOBAL
result = ""
valid_items = ["apple", "banana", "orange"] # O(N) lookup

for item in items:
    if item in valid_items:
        result += item # Quadratic memory reallocation
```

### Security and Validation Standards

#### 🎯 Directives
- ALWAYS use `pydantic` for runtime validation of external or dynamic data (e.g., JSON, YAML, API payloads).
- ALWAYS use `pandera` to validate Pandas/Polars dataframe schemas at runtime.
- ALWAYS enforce data integrity constraints at the lowest possible level (e.g., database `UNIQUE`, `NOT NULL`, `CHECK` constraints).
- ALWAYS use `ast.literal_eval()` instead of `eval()` for evaluating strings containing Python literals.
- ALWAYS use `yaml.safe_load()` instead of `yaml.load()` to prevent arbitrary code execution.
- ALWAYS use parameterized queries or ORMs to prevent SQL injection. NEVER use f-strings or string concatenation for SQL queries.
- ALWAYS include CSRF tokens (`{% csrf_token %}`) in Django POST forms.
- ALWAYS use `bandit` in CI/CD pipelines to scan for common security vulnerabilities.
- ALWAYS use `dodgy` or similar tools to scan for hardcoded secrets or credentials.
- ALWAYS escape HTML characters in tests when asserting against rendered templates (e.g., `django.utils.html.escape`).

#### 📝 Examples

##### ✅ DO
```python
from pydantic.dataclasses import dataclass
from pydantic import PositiveInt, constr

@dataclass
class UserProfile:
    username: constr(min_length=3, max_length=30)
    age: PositiveInt

### Safe SQL execution
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

##### ❌ DON'T
```python
class UserProfile:
    def __init__(self, username: str, age: int):
        self.username = username
        self.age = age # No runtime validation

### SQL Injection vulnerability
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

### Testing Standards

#### 🎯 Directives
- ALWAYS follow Double-Loop Test-Driven Development (TDD): Use an outer loop of Functional Tests (FTs) to drive high-level requirements, and an inner loop of Unit Tests (Red, Green, Refactor) to drive implementation details.
- ALWAYS use High Gear vs Low Gear TDD: Write the bulk of your tests against the Service Layer (edge-to-edge) using primitives and fakes to decouple tests from domain implementation details. Maintain a small core of tests against the Domain Model for complex logic.
- ALWAYS structure tests using the AAA pattern (Arrange, Act, Assert) or Given-When-Then. Keep the Act phase to 1-2 lines.
- ALWAYS ensure each test tests exactly one thing (single concept or behavior per test) to isolate failures.
- ALWAYS test behavior, not implementation. NEVER test constants (e.g., exact HTML strings); use structural checks (e.g., `assertTemplateUsed`) instead.
- ALWAYS use Triangulation to drive out generic implementations: if a test allows a "cheating" hardcoded implementation, write another test to force the correct logic.
- ALWAYS apply the "Three Strikes and Refactor" rule to eliminate duplication in test code.
- ALWAYS use `pytest` as the primary test runner and `pytest-cov` for coverage.
- ALWAYS use `pytest` fixtures with `yield` for setup and guaranteed teardown (Annihilate).
- ALWAYS use parameterized fixtures (`@pytest.fixture(params=[...])`) to run the same test scenarios against different drivers or configurations.
- ALWAYS run tests in parallel using `pytest-xdist` (e.g., `pytest -n auto`) to speed up large test suites.
- ALWAYS isolate tests. Tests MUST NOT depend on the state of other tests.
- ALWAYS use `@mock.patch` on the *target namespace* (where the dependency is used), not where it is defined.
- ALWAYS pass `spec=True` or the target class to `mock.patch` to prevent silent typos in mock assertions.
- NEVER mock internal application dependencies or ORM sessions; ALWAYS use Dependency Injection and in-memory Fakes (e.g., `FakeRepository`, `FakeUnitOfWork`). Follow the "Don't mock what you don't own" principle.
- ALWAYS use `django.test.LiveServerTestCase` for Functional Tests. NEVER use `time.sleep()`; ALWAYS implement explicit polling/wait loops.
- ALWAYS use `hypothesis` for Property-Based Testing to generate edge cases and test invariants.
- ALWAYS use `mutmut` for Mutation Testing to verify the actual robustness of the test suite, not just line coverage.
- ALWAYS use `behave` and Gherkin (`.feature` files) for Acceptance Testing and BDD.
- ALWAYS use `repr` strings for debugging output.
- ALWAYS verify related behaviors in `TestCase` subclasses.
- ALWAYS isolate tests from each other with `setUp`, `tearDown`, `setUpModule`, and `tearDownModule`.
- ALWAYS encapsulate dependencies to facilitate mocking and testing.
- ALWAYS consider interactive debugging with `pdb`.
- ALWAYS structure the `tests/` directory to separate unit, integration, e2e, and performance tests, mirroring the `src/` directory for unit tests.
- ALWAYS mirror the structure of the rest of the source tree within the `tests` directory (e.g., code in `src/app/services/auth.py` MUST be tested in `tests/unit/app/services/test_auth.py`).
- ALWAYS ensure tests are stored inside a `tests` subpackage of your application/library so they can be shipped and reused, and to prevent them from being accidentally installed as a top-level `tests` module.

#### 📁 Test Directory Structure
```text
my-python-project/
├── src/                        # Source code
│   └── app/
│       ├── services/
│       │   └── auth.py
│       └── utils/
│           └── logger.py
├── tests/
│   ├── conftest.py             # Root fixtures (Shared API clients, DB engine)
│   ├── unit/                   # 1-to-1 Mirror of src/
│   │   └── app/
│   │       ├── services/
│   │       │   ├── test_auth.py
│   │       │   └── mocks.py        # Complex mock objects for unit level
│   │       └── utils/
│   │           └── test_logger.py
│   ├── integration/
│   │   ├── internal/           # Testing logic + DB (Postgres/Redis)
│   │   │   ├── conftest.py     # DB-specific fixtures (Transaction rollback)
│   │   │   └── test_user_db.py
│   │   └── external/           # External API (Sandbox/Live)
│   │       ├── cassettes/      # VCR.py YAML recordings
│   │       │   └── test_stripe_pay.yaml
│   │       ├── conftest.py     # External auth / VCR config
│   │       └── test_stripe.py
│   ├── e2e/                    # Playwright (Python version)
│   │   ├── test_ui_flow.py
│   │   └── pom/                # Page Object Models
│   │       └── dashboard_page.py
│   ├── performance/            # Locust testing
│   │   └── locustfile.py
│   └── data/                   # GLOBAL STATIC FIXTURES (The Python way)
│       ├── sample_payload.json
│       └── test_avatar.png
├── pytest.ini                  # Defines markers like [external, smoke]
└── pyproject.toml
```

####  Examples

##### ✅ DO
```python
import pytest
from unittest.mock import patch, call

@pytest.fixture
def db_session():
    db = setup_db()
    yield db
    db.teardown()

@patch("app.services.send_email", spec=True)
def test_user_registration_sends_email(mock_send_email, db_session):
    # Arrange
    user_data = {"email": "test@example.com"}
    
    # Act
    register_user(user_data, db_session)
    
    # Assert
    assert mock_send_email.call_args == call("test@example.com", "Welcome!")
```

##### ❌ DON'T
```python
def test_user_registration():
    # Missing isolation, manual teardown, no spec on mock
    db = setup_db()
    with patch("app.email_module.send_email") as mock_send:
        register_user({"email": "test@example.com"}, db)
        mock_send.assert_called_with("test@example.com", "Welcome!")
    db.teardown() # Skipped if assert fails
```

### Type Safety Standards

#### 🎯 Directives
- ALWAYS annotate function parameters and return types for all public APIs and cross-module interfaces.
- ALWAYS use `Optional[T]` (or `T | None` in Python 3.10+) when a value can be `None`. NEVER rely on implicit optionals.
- ALWAYS use `Union[A, B]` (or `A | B`) to define Sum Types, restricting state spaces and making illegal states unrepresentable.
- ALWAYS use `typing.Literal` to restrict variables to a specific set of raw values.
- ALWAYS use `typing.NewType` to enforce context-specific boundaries (e.g., `SanitizedString = NewType('SanitizedString', str)`).
- ALWAYS use `typing.Annotated` to attach context-specific metadata or constraints to types (e.g., `Annotated[int, ValueRange(3, 5)]`) to communicate intent, even if not statically checked.
- ALWAYS use `typing.Final` for constants and immutable class variables.
- ALWAYS use `typing.Protocol` for structural subtyping (duck typing). NEVER use `Union` of concrete classes for shared behavior.
- ALWAYS use `@typing.overload` when a function's return type depends dynamically on the input types.
- ALWAYS configure `mypy` strictly: enable `--strict-optional`, `--disallow-untyped-defs`, and `--disallow-any-generics`.
- NEVER use `Any` unless absolutely unavoidable. It neutralizes static analysis.
- NEVER use `typing.cast()` except as an absolute last resort to silence false positives from external stubs.
- NEVER use `TypedDict` for runtime validation; it is strictly for static analysis. Use `pydantic` for runtime checks.

#### 📝 Examples

##### ✅ DO
```python
from typing import Optional, Protocol

class EmailSender(Protocol):
    def send(self, address: str, body: str) -> bool: ...

def notify_user(user_id: int, sender: EmailSender) -> Optional[str]:
    if user_id < 0:
        return None
    sender.send("user@example.com", "Hello")
    return "Success"
```

##### ❌ DON'T
```python
from typing import Any

### Missing return type, implicit None, uses Any, tightly coupled to concrete class
def notify_user(user_id, sender: Any):
    if user_id < 0:
        return None
    sender.send("user@example.com", "Hello")
    return "Success"
```

## Logging and Observability Standards

### 🎯 Directives
- ALWAYS use `packages/koda/src/koda/config/logging.py` for all the logging.

### 📝 Examples

#### ✅ DO
```python
from koda.config.logging import get_logger

logger = get_logger(__name__)

def process_data():
    logger.info("Processing data started")
```

#### ❌ DON'T
```python
import logging

logger = logging.getLogger(__name__)

def process_data():
    logger.info("Processing data started")
```
# Repository Map

```python

apps\koda-api\f\koda\batch_scrape.py:
⋮
│def main(
│    urls: List[str] = [],
│    requests: List[ScrapeRequest] = [],
│    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
│    onlyMainContent: bool = True,
│    actions: List[Action] = [],
│    timeout: int = 60000,
│    s3_resource: Optional[str] = "f/koda/default_s3",
│    webhook: Optional[Webhook] = None,
│    maxConcurrency: int = 10,
⋮

apps\koda-api\f\koda\crawl.py:
⋮
│def main(
│    url: str,
│    prompt: Optional[str] = None,
│    excludePaths: Optional[List[str]] = None,
│    includePaths: Optional[List[str]] = None,
│    maxDiscoveryDepth: int = 0,
│    sitemap: str = "include",
│    ignoreQueryParameters: bool = False,
│    regexOnFullURL: bool = False,
│    limit: int = 10000,
⋮

apps\koda-api\f\koda\scouts\scrape_youtube_profile.py:
⋮
│def main(
│    url: str,
│    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
│    timeout: int = 300000,
│    s3_resource: Optional[str] = "f/koda/default_s3",
│    webhook: Optional[Webhook] = None,
│    max_concurrency: int = 10,
│    tabs: Optional[List[str]] = None,
⋮

apps\koda-api\f\koda\scrape.py:
⋮
│def main(
│    url: str,
│    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
│    onlyMainContent: bool = True,
│    actions: List[Action] = [],
│    timeout: int = 60000,
│    s3_resource: Optional[str] = "f/koda/default_s3",
│    webhook: Optional[Webhook] = None,
⋮

apps\koda-api\rt.d.ts:
⋮
│  type Abstractapi = {
│    apiKey: string
⋮
│  type Acumbamail = {
│    authToken: string
⋮
│  type AeroWorkflow = {
│    apiKey: string
⋮
│  type AgentInstructions = any
│
⋮
│  type Airtable = {
│    apiKey: string
⋮
│  type AirtableTable = {
│    baseId: string,
│    tableName: string
⋮
│  type AnsibleInventory = {
│    content: string
⋮
│  type Anthropic = {
│    apiKey: string,
│    base_url: string,
│    platform: string,
│    enable_1M_context: boolean
⋮
│  type ApifyApiKey = {
│    api_key: string
⋮
│  type ApifyWebhookConfig = {
│    url: string,
│    token: string
⋮
│  type ApiKeyAuth = {
│    api_key_header: string,
│    api_key_secret: string
⋮
│  type Appwrite = {
│    key: string,
│    project: string,
│    endpoint: string,
│    self_signed: boolean
⋮
│  type ArcgisAccount = {
│    password: string,
│    username: string
⋮
│  type Assemblyai = {
│    apiKey: string
⋮
│  type AwsBedrock = {
│    apiKey: string,
│    region: string,
│    awsAccessKeyId: string,
│    awsSessionToken: string,
│    awsSecretAccessKey: string
⋮
│  type AzureBlob = {
│    useSSL: boolean,
│    endpoint: string,
│    accessKey: string,
│    accountName: string,
│    containerName: string
⋮
│  type AzureOauth = {
│    token: string
⋮
│  type AzureOpenai = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type AzureWorkloadIdentity = {
│    useSSL: boolean,
│    accountName: string,
│    containerName: string
⋮
│  type BambooHr = {
│    apiKey: string,
│    companyDomain: string
⋮
│  type Baremetrics = {
│    apiKey: string
⋮
│  type BaserowTable = {
│    table_id: number,
│    database_id: number
⋮
│  type BasicHttpAuth = {
│    password: string,
│    username: string
⋮
│  type BasisTheory = {
│    apiKey: string
⋮
│  type Bigquery = {
│    type: string,
│    auth_uri: string,
│    client_id: string,
│    token_uri: string,
│    project_id: string,
│    private_key: string,
│    client_email: string,
│    private_key_id: string,
│    client_x509_cert_url: string,
⋮
│  type Bitbucket = {
│    password: string,
│    username: string
⋮
│  type Buttondown = {
│    token: string
⋮
│  type Cacertificate = {
│    certificate: string
⋮
│  type Calendly = {
│    token: string
⋮
│  type Certopus = {
│    apiKey: string
⋮
│  type Chromadb = {
│    ssl: boolean,
│    host: string,
│    port: number,
│    tenant: string,
│    database: string
⋮
│  type Circleci = {
│    token: string
⋮
│  type Clickhouse = {
│    host: string,
│    password: string,
│    username: string
⋮
│  type Cloudflare = {
│    key: string,
│    email: string,
│    token: string
⋮
│  type Cockroachdb = {
│    token: string
⋮
│  type ComapeoServer = {
│    server_url: string,
│    access_token: string
⋮
│  type Confluence = {
│    email: string,
│    baseUrl: string,
│    apiToken: string
⋮
│  type Contentful = {
│    spaceId: string,
│    accessToken: string,
│    environment: string
⋮
│  type Contiguity = {
│    token: string
⋮
│  type Convertkit = {
│    apiSecret: string
⋮
│  type Currencyapi = {
│    apiKey: string
⋮
│  type Customai = {
│    api_key: string,
│    base_url: string
⋮
│  type DeepInfra = {
│    token: string
⋮
│  type Deepseek = {
│    api_key: string,
│    base_url: string
⋮
│  type Digitalocean = {
│    token: string
⋮
│  type DiscordBotConfiguration = {
│    public_key: string,
│    application_id: string
⋮
│  type DiscordWebhook = {
│    webhook_url: string
⋮
│  type Discourse = {
│    apiKey: string,
│    apiUsername: string,
│    defaultHost: string
⋮
│  type Docspring = {
│    tokenId: string,
│    tokenSecret: string
⋮
│  type Dynatrace = {
│    accessToken: string,
│    environmentId: string,
│    environmentUrl: string
⋮
│  type Firebase = {
│    appId: string,
│    apiKey: string,
│    projectId: string,
│    authDomain: string,
│    measurementId: string,
│    storageBucket: string,
│    messagingSenderId: string
⋮
│  type Formstack = {
│    token: string
⋮
│  type Foxentry = {
│    apiKey: string
⋮
│  type Freshdesk = {
│    apiKey: string,
│    baseUrl: string
⋮
│  type Funkwhale = {
│    token: string,
│    baseUrl: string
⋮
│  type GcloudStorage = {
│    bucket: string,
│    serviceAccountKey: any
⋮
│  type GcpServiceAccount = {
│    type: string,
│    auth_uri: string,
│    client_id: string,
│    token_uri: string,
│    project_id: string,
│    private_key: string,
│    client_email: string,
│    private_key_id: string,
│    client_x509_cert_url: string,
⋮
│  type Ghostcms = {
│    apiKey: string,
│    apiUrl: string
⋮
│  type GitRepository = {
│    url: string,
│    branch: string,
│    folder: string,
│    gpg_key: any,
│    is_github_app: boolean
⋮
│  type Googleai = {
│    api_key: string,
│    base_url: string
⋮
│  type Gworkspace = {
│    token: string
⋮
│  type IfsCloudOidc = {
│    server: string,
│    clientId: string,
│    oidcPath: string,
│    clientSecret: string
⋮
│  type Intercom = {
│    token: string,
│    apiVersion: string
⋮
│  type JsonSchema = {
│    schema: any
⋮
│  type Kobotoolbox = {
│    api_key: string,
│    server_url: string
⋮
│  type Kustomer = {
│    apiKey: string
⋮
│  type Langfuse = {
│    base_url: string,
│    public_key: string,
│    secret_key: string
⋮
│  type Leonardoai = {
│    apiKey: string
⋮
│  type Linkding = {
│    token: string,
│    baseUrl: string
⋮
│  type Linkedin = {
│    token: string
⋮
│  type Localcontexts = {
│    api_key: string,
│    project_id: string,
│    server_url: string
⋮
│  type Mailchimp = {
│    server: string,
│    api_key: string
⋮
│  type Mailerlite = {
│    apiToken: string
⋮
│  type Mastodon = {
│    token: string,
│    baseUrl: string
⋮
│  type Matteroom = {
│    base_url: string,
│    password: string,
│    username: string
⋮
│  type Meteosource = {
│    tier: string,
│    apiKey: string
⋮
│  type MongodbRest = {
│    api_key: string,
│    endpoint: string
⋮
│  type Motimate = {
│    token: string
⋮
│  type MsSqlServer = {
│    host: string,
│    port: number,
│    user: string,
│    dbname: string,
│    ca_cert: string,
│    encrypt: boolean,
│    password: string,
│    aad_token: any,
│    trust_cert: boolean,
⋮
│  type MsTeamsWebhook = {
│    webhook_url: string
⋮
│  type Nextcloud = {
│    token: string,
│    userId: string,
│    baseUrl: string,
│    password: string,
│    username: string
⋮
│  type OauthClientCredentials = {
│    domain: string,
│    client_id: string,
│    client_secret: string
⋮
│  type Openrouter = {
│    api_key: string,
│    base_url: string
⋮
│  type Oracledb = {
│    user: string,
│    database: string,
│    password: string
⋮
│  type Pandadoc = {
│    apiKey: string
⋮
│  type Paylocity = {
│    token: string
⋮
│  type Personio = {
│    clientId: string,
│    clientSecret: string
⋮
│  type Pinecone = {
│    apiKey: string,
│    environment: string
⋮
│  type Pinterest = {
│    token: string
⋮
│  type Pipedrive = {
│    apiToken: string
⋮
│  type Planetscale = {
│    serviceToken: string,
│    serviceTokenId: string
⋮
│  type Postgresql = {
│    host: string,
│    port: number,
│    user: string,
│    dbname: string,
│    sslmode: string,
│    password: string,
│    root_certificate_pem: string
⋮
│  type Pushover = {
│    user: string,
│    token: string
⋮
│  type Quickbooks = {
│    token: string,
│    realmId: string,
│    isSandBox: boolean
⋮
│  type Replicate = {
│    token: string
⋮
│  type S3AwsOidc = {
│    bucket: string,
│    region: string,
│    roleArn: string
⋮
│  type SageIntacct = {
│    token: string
⋮
│  type Salesflare = {
│    apiKey: string
⋮
│  type Sendgrid = {
│    token: string
⋮
│  type Sensortower = {
│    base_url: string,
│    auth_token: string
⋮
│  type Shutterstock = {
│    token: string
⋮
│  type SignatureAuth = {
│    secret_key: string,
│    signature_provider: string,
│    authentication_config: {
│    encoding: string,
│    algorithm: string,
│    signature_prefix: string,
│    signature_header_name: string
│  }
⋮
│  type Smartsheet = {
│    token: string,
│    baseUrl: string
⋮
│  type Snowflake = {
│    role: string,
│    schema: string,
│    database: string,
│    username: string,
│    warehouse: string,
│    public_key: string,
│    private_key: string,
│    account_identifier: string
⋮
│  type Speechify = {
│    token: string
⋮
│  type Supabase = {
│    key: string,
│    url: string
⋮
│  type Surrealdb = {
│    url: string,
│    token: string
⋮
│  type Telegram = {
│    token: string
⋮
│  type TheirStack = {
│    apiKey: string
⋮
│  type Togetherai = {
│    api_key: string,
│    base_url: string
⋮
│  type Tomorrow = {
│    apiKey: string
⋮
│  type Tripadvisor = {
│    apiKey: string
⋮
│  type TwilioMessageTemplate = {
│    auth_token: string,
│    recipients: string[],
│    account_sid: string,
│    content_sid: string,
│    origin_number: string,
│    message_service_sid: string
⋮
│  type Typeform = {
│    token: string,
│    baseUrl: string
⋮
│  type Ultravox = {
│    apiKey: string
⋮
│  type Weatherapi = {
│    apiKey: string
⋮
│  type Webscrapingai = {
│    apiKey: string
⋮
│  type Woocommerce = {
│    url: string,
│    version: string,
│    consumerKey: string,
│    consumerSecret: string,
│    queryStringAuth: boolean
⋮

packages\koda\src\koda\assets\posthog-monolith.js:
│!function(){"use strict";function t(t,e,i,r,n,s,o){try{var a=t[s](o),l=a.value}catch(t){return void
⋮

packages\koda\src\koda\client.py:
⋮
│class KodaClient:
│    """Primary interface for the Koda extraction infrastructure."""
│    
│    def __init__(self, s3_resource: dict | Any | None = None, **kwargs: Any) -> None:
⋮
│    async def __aenter__(self) -> KodaClient:
⋮
│    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
⋮

packages\koda\src\koda\config\main.py:
⋮
│class S3(BaseModel):
│    endpoint_url: Optional[str] = Field(default=None, validation_alias=AliasChoices("endpoint_url",
⋮
│    @classmethod
│    def from_dict(cls, data: dict) -> Optional["S3"]:
⋮
│class Settings(LoggingSettings, BaseSettings):
│    """
│    Centralized configuration for Koda.
│    Loads values from environment variables with sensible defaults.
⋮
│    @model_validator(mode="after")
│    def validate_browser(self) -> "Settings":
⋮

packages\koda\src\koda\exceptions.py:
⋮
│class Error(Exception):
⋮
│class ScrapeError(Error):
⋮
│class SessionExhaustedError(Error):
⋮
│class TimeoutError(Error):
⋮
│class BrowserLaunchError(Error):
⋮

packages\koda\src\koda\infrastructure\invisible_playwright.py:
⋮
│class BrowserLaunchError(Exception):
⋮
│async def launch_stealth_browser(headless: bool = True, **kwargs: Any) -> BrowserContext:
⋮
│async def stop_stealth_browser() -> None:
⋮

packages\koda\src\koda\infrastructure\pytest.py:
⋮
│def main():
│    """
│    Wrapper around pytest to run tests sequentially in completely isolated processes.
│    This prevents memory leaks and orphaned browser processes from accumulating.
│    It perfectly mimics the original pytest stdout.
⋮
│    def run_and_stream_test(cmd, test_id, current_idx):
⋮

packages\koda\src\koda\integrations\crawl4ai.py:
⋮
│class KodaBrowserManager(BrowserManager):
│    """
│    A custom BrowserManager for crawl4ai that bypasses its internal lifecycle management.
│    It creates new pages from the Playwright BrowserContext provided by Koda.
│    """
│    def __init__(self, context: BrowserContext, *args, **kwargs):
⋮
│    async def start(self):
⋮
│    async def close(self):
⋮
│    async def get_page(self, crawlerRunConfig: CrawlerRunConfig):
⋮
│class KodaAsyncWebCrawler(AsyncWebCrawler):
│    """
│    A custom AsyncWebCrawler that intercepts initialization to route browser
│    management through Koda's infrastructure if a `client` is provided.
│    """
│    def __init__(self, **kwargs):
⋮
│    async def start(self) -> "KodaAsyncWebCrawler":
⋮
│    async def close(self):
⋮
│    async def __aenter__(self):
⋮
│    async def __aexit__(self, exc_type, exc_val, exc_tb):
⋮
│class Crawl4AiTool(BrowserTool):
│    """
│    Adapter for crawl4ai that implements the BrowserTool protocol.
│    DEPRECATED: Use the native KodaAsyncWebCrawler wrapper instead.
│    """
│    def __init__(self, browser_config: Optional[BrowserConfig] = None):
⋮
│    async def execute(self, context_or_page: Any, request: Any) -> Any:
⋮

packages\koda\src\koda\integrations\crawlee.py:
⋮
│class KodaBrowserController(BrowserController):
│    """A browser controller that simply yields pages from a pre-existing Koda BrowserContext."""
│    
⋮
│    def __init__(self, context: BrowserContext):
⋮
│    async def new_page(
│        self,
│        browser_new_context_options: Mapping[str, Any] | None = None,
│        proxy_info: ProxyInfo | None = None,
⋮
│    async def close(self, *, force: bool = False) -> None:
⋮
│class KodaBrowserPlugin(BrowserPlugin):
│    """A browser plugin that returns a KodaBrowserController wrapped around a pre-existing Koda con
│    
⋮
│    def __init__(self, context: BrowserContext):
⋮
│    @property
│    def active(self) -> bool:
⋮
│    async def __aenter__(self) -> 'KodaBrowserPlugin':
⋮
│    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None
⋮
│    async def new_browser(self) -> BrowserController:
⋮
│class KodaPlaywrightCrawler(PlaywrightCrawler):
│    """
│    A Koda-integrated PlaywrightCrawler that injects the KodaClient and
│    wraps the entire crawl execution within Koda's BrowserSession.
│    """
│    def __init__(self, *args, **kwargs):
⋮
│    async def run(self, *args, **kwargs) -> None:  # type: ignore[override]
⋮

packages\koda\src\koda\integrations\posthog.py:
⋮
│def _get_otel_trace_id() -> str:
⋮
│async def flush_telemetry() -> None:
⋮
│async def _send_posthog_request(url: str, method: str, data: str, content_type: Optional[str] = Non
⋮
│async def setup_playwright_transport(context: BrowserContext) -> None:
⋮
│async def setup_network_capture(page: Page, posthog_api_key: str) -> None:
⋮
│async def inject_posthog_monolith(page: Page, api_key: str, host: str) -> None:
⋮

packages\koda\src\koda\integrations\stagehand.py:
⋮
│class KodaStagehand(BaseStagehand):  # type: ignore[misc]
│    """
│    A custom Stagehand wrapper that routes browser management through Koda's
│    infrastructure if a `client` is provided.
│    """
│    def __init__(self, **kwargs):
⋮
│    async def init(self, *args, **kwargs):
⋮
│    async def close(self, *args, **kwargs):
⋮
│class StagehandTool(BrowserTool):
│    """
│    Adapter for stagehand that implements the BrowserTool protocol.
│    DEPRECATED: Use the native KodaStagehand wrapper instead.
│    """
│    def __init__(self, **kwargs):
⋮
│    async def execute(self, context_or_page: Any, request: Any) -> Any:
⋮

packages\koda\src\koda\modules\browser\repositories\cloakbrowser.py:
⋮
│@asynccontextmanager
│async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
⋮

packages\koda\src\koda\modules\browser\repositories\invisible_playwright.py:
⋮
│if InvisiblePlaywright is not None:
│    class KodaInvisiblePlaywright(InvisiblePlaywright):
│        def _default_context_kwargs(self) -> Dict[str, Any]:
│            kwargs = super()._default_context_kwargs()
│            # Force Playwright's native CSP bypass on the persistent context
│            kwargs["bypass_csp"] = True
⋮
│@asynccontextmanager
│async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
⋮

packages\koda\src\koda\modules\browser\service.py:
⋮
│class BrowserTool(Protocol):
│    """Protocol for tools that operate on a Playwright Page or Context."""
│    async def execute(self, context_or_page: Any, request: Any) -> Any:
⋮
│async def _strip_csp_headers(route: Route):
⋮
│@dataclass(frozen=True)
│class CSPStrategy:
⋮
│async def _native_playwright_interceptor(context: BrowserContext) -> None:
⋮
│def _invisible_playwright_modifier(config: dict) -> dict:
⋮
│@asynccontextmanager
│async def BrowserSession(config: Optional[Dict[str, Any]] = None, user_data_dir: str = "") -> Async
│    """
│    Context manager that owns the browser lifecycle.
│    Launches the browser, injects telemetry into all pages, and ensures safe teardown.
⋮
│    async with launcher(user_data_dir, config) as browser_or_context:
│            # Handle both Browser and persistent BrowserContext yields
│            if hasattr(browser_or_context, 'new_context'):
│                kwargs = {"permissions": ["geolocation", "notifications"]}
│                kwargs.update(strategy.context_kwargs)
│                context = await browser_or_context.new_context(**kwargs)
│            else:
│                context = browser_or_context
│                await context.grant_permissions(["geolocation", "notifications"])
│                # Note: strategy.context_kwargs cannot be passed to a persistent context natively.
│                # CSP bypassing relies on extra_prefs (e.g. security.csp.enable=False)
⋮
│            if settings.posthog_api_key and settings.posthog_host:
│                await setup_playwright_transport(context)
│                
│                async def on_page(page: Page):
⋮

packages\koda\src\koda\modules\cache\repositories\windmill.py:
⋮
│def _get_state_path() -> str:
⋮
│async def _fetch_state() -> Dict[str, Any]:
⋮
│async def get(key: str) -> Optional[CacheEntry]:
⋮
│async def set(entry: CacheEntry) -> None:
⋮

packages\koda\src\koda\modules\cache\schema.py:
⋮
│class CacheEntry(BaseModel):
⋮

packages\koda\src\koda\modules\cache\service.py:
⋮
│class CacheService:
│    """Service for managing cache operations."""
│
│    def __init__(self, cache_repo: Any):
⋮
│    async def get(self, key: str) -> Optional[Any]:
⋮
│    async def set(self, key: str, value: Any) -> None:
⋮

packages\koda\src\koda\modules\session\repositories\email\imap.py:
⋮
│async def get_latest_email(address: str) -> Optional[str]:
⋮

packages\koda\src\koda\modules\session\repositories\email\jmap.py:
⋮
│async def get_latest_email(address: str) -> Optional[str]:
⋮

packages\koda\src\koda\modules\session\repositories\lock\consul.py:
⋮
│async def acquire_lock(
│    lock_name: str,
│    ttl_seconds: int = 30,
│    timeout_seconds: int = 10,
⋮
│async def release_lock(lock_name: str, session_id: str) -> bool:
⋮
│def start_heartbeat(session_id: str, interval_seconds: int = 15) -> asyncio.Task:
⋮
│async def _renew_session_loop(session_id: str, interval_seconds: int) -> None:
⋮

packages\koda\src\koda\modules\session\repositories\lock\redis.py:
⋮
│def _get_client() -> Redis:
⋮
│async def acquire_lock(
│    lock_name: str,
│    ttl_seconds: int = 30,
│    timeout_seconds: int = 10,
⋮
│async def release_lock(lock_name: str, token: str) -> bool:
⋮
│def start_heartbeat(lock_name: str, token: str, ttl_seconds: int = 30) -> asyncio.Task:
⋮
│async def _renew_lock_loop(lock_name: str, token: str, ttl_seconds: int) -> None:
⋮

packages\koda\src\koda\modules\session\schema.py:
⋮
│class BrowserParam(BaseModel):
⋮
│class MFAParam(BaseModel):
⋮
│class UserDataParam(BaseModel):
⋮
│class SessionModel(BaseModel):
⋮
│@dataclass
│class Session:
│    """
│    A lightweight wrapper around SessionModel providing an Apify-style API.
│    Delegates I/O and orchestration to service functions.
⋮
│    @property
│    def id(self) -> str:
⋮
│    @property
│    def user_data(self) -> UserDataParam:
⋮
│    @property
│    def error_score(self) -> float:
⋮
│    @property
│    def usage_count(self) -> int:
⋮
│    @property
│    def expires_at(self) -> datetime:
⋮
│    @property
│    def is_blocked(self) -> bool:
⋮
│    @property
│    def is_expired(self) -> bool:
⋮
│    @property
│    def is_max_usage_count_reached(self) -> bool:
⋮
│    @property
│    def is_usable(self) -> bool:
⋮
│    def mark_good(self) -> None:
⋮
│    def mark_bad(self) -> None:
⋮
│    def retire(self) -> None:
⋮
│    def is_blocked_status_code(self, status_code: int) -> bool:
⋮
│    def get_state(self, as_dict: bool = False) -> SessionModel | dict:
⋮
│    @classmethod
│    def from_model(cls, model: SessionModel) -> Session:
⋮

packages\koda\src\koda\modules\session\service.py:
⋮
│class SessionService:
│    """Service for managing browser sessions, including locking, storage, and MFA resolution."""
│
│    def __init__(
│        self,
│        storage_repo: Any,
│        lock_repo: Any,
│        email_repo_imap: Any,
│        email_repo_jmap: Any,
│        s3_repo: Any,
⋮
│    async def get_session(self, metadata: dict[str, Any]) -> Tuple[Session, str]:
⋮
│    async def release_session(self, session: Session, lock_token: str) -> None:
⋮
│    @asynccontextmanager
│    async def browser_session_scope(self, metadata: dict[str, Any]) -> AsyncGenerator[Tuple[Session
⋮
│    async def resolve_mfa(self, session: Session) -> str:
⋮

packages\koda\src\koda\use_cases\batch_scrape\schema.py:
⋮
│class BatchScrapeRequest(BaseModel):
⋮
│class BatchScrapeResponse(BaseModel):
⋮

packages\koda\src\koda\use_cases\batch_scrape\service.py:
⋮
│class BatchScrapeJob:
│    def __init__(self, request: BatchScrapeRequest):
│        self.request = request
│        self.action_results: Dict[str, Dict[str, list]] = {}
│        self.target_requests: Dict[str, ScrapeRequest] = {}
│        if self.request.requests:
│            for req in self.request.requests:
⋮
│    def _init_url_action_results(self, url: str):
⋮
│    async def execute_actions_hook(self, page, context, **kwargs):
⋮
│    async def run(self) -> BatchScrapeResponse:
⋮
│@webhook_dispatch
│async def batch_scrape(request: BatchScrapeRequest) -> BatchScrapeResponse:
⋮

packages\koda\src\koda\use_cases\crawl\schema.py:
⋮
│class ScrapeOptions(BaseModel):
⋮
│class CrawlRequest(BaseModel):
⋮
│class CrawlResponse(BaseModel):
⋮

packages\koda\src\koda\use_cases\crawl\service.py:
⋮
│class CrawlJob:
│    def __init__(self, request: CrawlRequest):
│        self.request = request
│        self.base_url = str(request.url)
⋮
│    async def execute_actions_hook(self, page, context, **kwargs):
⋮
│    async def run(self) -> CrawlResponse:
⋮
│@webhook_dispatch
│async def crawl(request: CrawlRequest) -> CrawlResponse:
⋮

packages\koda\src\koda\use_cases\schema.py:
⋮
│class Action(BaseModel):
⋮

packages\koda\src\koda\use_cases\scrape\schema.py:
⋮
│class ScrapeRequest(BaseModel):
⋮
│class ScrapeResponse(BaseModel):
⋮
│class ScrapeResult(BaseModel):
⋮

packages\koda\src\koda\use_cases\scrape\service.py:
⋮
│class ScrapeJob:
│    def __init__(self, request: ScrapeRequest):
│        self.request = request
│        self.action_results: Dict[str, list] = {
│            "screenshots": [],
│            "scrapes": [],
│            "javascriptReturns": [],
│            "pdfs": [],
│            "errors": []
⋮
│    async def execute_actions_hook(self, page, context, **kwargs):
⋮
│    async def run(self) -> ScrapeResponse:
⋮
│@webhook_dispatch
│async def scrape(request: ScrapeRequest) -> ScrapeResult:
⋮

packages\koda\src\koda\use_cases\scrape_youtube_profile\recording.py:
⋮
│def run(playwright: Playwright) -> None:
│    browser = playwright.chromium.launch(headless=False)
⋮
│    def _wait_for_network():
⋮

packages\koda\src\koda\use_cases\scrape_youtube_profile\schema.py:
⋮
│class ScrapeYoutubeProfileRequest(BaseModel):
⋮
│class ScrapeYoutubeProfileResponse(BaseModel):
⋮

packages\koda\src\koda\use_cases\scrape_youtube_profile\service.py:
⋮
│@router.default_handler
│async def default_handler(context: PlaywrightCrawlingContext) -> None:
⋮
│async def _validate_redirect(page: Page, expected_tab: str) -> bool:
⋮
│@router.handler('VIDEOS')
│async def videos_handler(context: PlaywrightCrawlingContext) -> None:
⋮
│@webhook_dispatch
│async def scrape_youtube_profile(request: ScrapeYoutubeProfileRequest) -> ScrapeYoutubeProfileRespo
⋮

packages\koda\src\koda\use_cases\service.py:
⋮
│async def wait_for_networkidle(page: Page, wait_for_timeout: int = 1000, timeout_ms: int = 10000) -
⋮
│async def scroll_to(page: Page, y: Optional[int] = None, viewport_height: int = 768, wait_callback:
⋮
│async def screenshot(page: Page, max_height: int = 3072) -> bytes:
⋮
│async def execute_actions(page, actions: List[Action], action_results: Dict[str, list]) -> None:
⋮

packages\koda\src\koda\utils\__init__.py:
⋮
│def images_are_identical(img1: Image.Image, img2: Image.Image) -> bool:
⋮
│def sanitize_filename(url: str) -> str:
⋮

packages\koda\src\koda\utils\file\main.py:
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
│    def from_base64(cls, b64_string: str, filename: str, mimetype: Optional[str] = None) -> "File":
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

packages\koda\src\koda\utils\file\service.py:
⋮
│def upload(data: Union[bytes, str], object_name: str, mimetype: str) -> None:
⋮
│def generate_presigned_url(object_name: str, expires_in: int = 3600) -> str:
⋮
│def _get_client():
⋮

packages\koda\src\koda\utils\webhook\schema.py:
⋮
│class WebhookEvent(str, Enum):
⋮
│class Webhook(BaseModel):
⋮

packages\koda\src\koda\utils\webhook\service.py:
⋮
│async def dispatch_webhook(
│    webhook: Optional[Webhook], event: WebhookEvent, payload: Dict[str, Any]
⋮

packages\koda\tests\conftest.py:
⋮
│class AsyncioFilter(logging.Filter):
│    def filter(self, record):
│        if record.levelno >= logging.ERROR and "TargetClosedError" in record.getMessage():
│            return False
⋮
│def get_child_processes():
⋮
│class TestServerThread(threading.Thread):
│    def __init__(self, directory):
│        super().__init__()
│        self.directory = directory
│        self.server = None
│        self.port = None
⋮
│    def run(self):
│        # Capture directory in closure
│        directory = self.directory
│        
│        class Handler(SimpleHTTPRequestHandler):
│            def __init__(self, *args, **kwargs):
⋮
│    def stop(self):
⋮

packages\koda\tests\integration\test_crawlee.py:
⋮
│@pytest.mark.asyncio
│async def test_crawlee_headed_propagation(monkeypatch, local_test_server):
│    """Test that KODA_HEADLESS=false propagates successfully to the browser config."""
⋮
│    class MockContext:
│        async def grant_permissions(self, *args, **kwargs):
│            pass
│        async def close(self):
│            pass
│        def on(self, *args, **kwargs):
│            pass
│        async def route(self, *args, **kwargs):
⋮

packages\koda\tests\integration\test_crawlee_timeout_and_crash.py:
⋮
│@pytest.mark.asyncio
│async def test_koda_browser_controller_crash():
│    """Test that KodaBrowserController catches TargetClosedError and marks _is_closed."""
│    
⋮
│    class PlaywrightError(Exception):
⋮
│@pytest.mark.asyncio
│async def test_koda_browser_controller_protocol_error():
│    """Test that KodaBrowserController catches protocol errors and marks _is_closed."""
│    
⋮
│    class PlaywrightError(Exception):
⋮

packages\koda\tests\integration\test_csp_bypass.py:
⋮
│async def start_local_server(port=8081):
⋮

packages\koda\tests\integration\test_s3_storage.py:
⋮
│@pytest.fixture(autouse=True)
│def setup_s3_settings():
⋮
│@pytest.fixture
│def dummy_profile_dir(tmp_path):
⋮
│@pytest.mark.asyncio
│async def test_s3_upload_download_flow(dummy_profile_dir, tmp_path):
⋮

packages\koda\tests\integration\test_stagehand.py:
⋮
│@pytest.mark.asyncio
│async def test_stagehand_integration(local_test_server):
│    """Test that Stagehand can successfully use a BrowserSession to extract elements via KodaClient
⋮
│    class StagehandMock:
│        def __init__(self, **kwargs):
│            self.client = kwargs.get("client")
│        async def init(self, *args, **kwargs):
│            pass
│        async def close(self, *args, **kwargs):
⋮

packages\koda\tests\manual\use_cases\scrape_youtube_profile\test_scrape_youtube_profile.py:
⋮
│def save_base64_image(b64_string: str, filename: str, output_dir: str = "output") -> str:
⋮
│async def main():
⋮

packages\koda\tests\unit\conftest.py:
⋮
│@pytest.fixture(autouse=True)
│def mock_launch_browser():
⋮

packages\koda\tests\unit\modules\session\test_service.py:
⋮
│def create_mock_session_model(
│    id: str,
│    provider: str = "test_provider",
│    usage_count: int = 0,
│    error_score: float = 0.0,
│    is_blocked: bool = False,
│    mfa: Optional[MFAParam] = None,
│    browser: Optional[BrowserParam] = None
⋮

packages\koda\tests\unit\use_cases\test_crawl_service.py:
⋮
│@pytest.mark.asyncio
│async def test_crawl_success_stream(mock_crawl4ai, mock_koda_client):
│    client_instance = AsyncMock()
⋮
│    async def mock_stream():
⋮

packages\koda\tests\unit\utils\webhook\test_service.py:
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

```