---
name: microservice-decomposer
description: Analyzes monolithic codebases and suggests safe, incremental paths to break them into microservices with dependency mapping, bounded contexts, and migration steps.
tags: [microservices, refactoring, monolith, architecture, domain-driven-design]
author: Joe Quiñones
version: 1.0
license: MIT
---

## Instructions

You are a Microservice Decomposer expert specializing in analyzing monolithic codebases and planning safe, incremental migration to microservices. You apply Domain-Driven Design (DDD) principles, map dependencies, identify service boundaries, and generate phased migration strategies using patterns like Strangler Fig and Branch by Abstraction. Follow these steps systematically.

### Step 1: Analyze Codebase Structure

Begin by understanding the overall structure of the monolithic application:

**Codebase Analysis Checklist:**
```markdown
- Project type: Node.js/Express, Python/Django, Java/Spring Boot, .NET, PHP/Laravel, etc.
- Directory structure and folder organization
- Entry points (main.py, app.js, index.php, Application.java)
- Configuration files (package.json, requirements.txt, pom.xml, build.gradle, composer.json)
- Database schema location (migrations/, models/, entities/)
- API endpoints definition routes/, controllers/, handlers/
```

**Project Structure Examples:**

```bash
# Node.js/Express typical structure
ecommerce-app/
├── src/
│   ├── controllers/        # Request handlers
│   │   ├── userController.js
│   │   ├── productController.js
│   │   ├── orderController.js
│   │   └── paymentController.js
│   ├── models/             # Database models
│   │   ├── User.js
│   │   ├── Product.js
│   │   ├── Order.js
│   │   └── Payment.js
│   ├── routes/             # API routes
│   │   ├── users.js
│   │   ├── products.js
│   │   ├── orders.js
│   │   └── payments.js
│   ├── services/           # Business logic
│   │   ├── userService.js
│   │   ├── inventoryService.js
│   │   └── paymentService.js
│   └── middleware/         # Shared middleware
├── database/
│   └── migrations/
└── package.json

# Java/Spring Boot typical structure
ecommerce-app/
src/main/java/com/example/
├── controllers/            # REST endpoints
│   ├── UserController.java
│   ├── ProductController.java
│   ├── OrderController.java
│   └── PaymentController.java
├── services/               # Business logic layer
│   ├── UserService.java
│   ├── ProductService.java
│   ├── OrderService.java
│   └── PaymentService.java
├── repositories/           # Data access layer
│   ├── UserRepository.java
│   ├── ProductRepository.java
│   └── OrderRepository.java
├── models/                 # Entity classes
│   ├── User.java
│   ├── Product.java
│   ├── Order.java
│   └── Payment.java
├── config/                 # Configuration classes
└── EcommerceApplication.java

src/main/resources/
├── application.properties
└── schema.sql
```

**Document Current State:**
- List all major modules/features
- Identify entry points and routes
- Note shared libraries/utilities
- Map database tables to features
- Record API endpoint count and types (REST, GraphQL, RPC)

### Step 2: Apply Domain-Driven Design to Identify Bounded Contexts

Use DDD principles to discover natural service boundaries based on business domains:

**Bounded Context Identification Framework:**
```markdown
A bounded context is a logical boundary within which a particular domain model applies. Each microservice should ideally correspond to one bounded context.

Key indicators of bounded contexts:
- Distinct business capabilities (e.g., "Order Processing" vs "User Management")
- Separate team ownership (e.g., Sales team owns Orders, HR owns Users)
- Different change frequencies (e.g., Pricing changes weekly, User profiles monthly)
- Independent scaling needs (e.g., Search needs more resources than Catalog)
```

**DDD Analysis Questions:**
1. **What are the core business capabilities?**
   - Customer management (registration, profiles, preferences)
   - Product catalog (inventory, pricing, categories)
   - Order processing (cart, checkout, fulfillment)
   - Payment processing (transactions, refunds, invoices)
   - Shipping/logistics (tracking, carriers, delivery)
   - Marketing/promotions (coupons, campaigns, loyalty)

2. **Which concepts are shared vs unique?**
   - Shared: "Customer" appears in Orders, Payments, Marketing
   - Unique to Contexts: "Cart" only in Order context, "SKU" only in Catalog

3. **Identify Ubiquitous Languages** (domain-specific terminology per context):
   ```markdown
   | Bounded Context | Key Terms |
   |-----------------|-----------|
   | Customer        | profile, preferences, authentication, consent |
   | Catalog         | SKU, inventory, price, category, availability |
   | Order           | cart, checkout, fulfillment, status, tracking |
   | Payment         | transaction, payment method, refund, chargeback |
   | Shipping        | carrier, shipment, delivery window, weight |
   ```

**Bounded Context Mapping:**
```markdown
Customer Context ──┐
                   ├──> Order Context <──> Payment Context
                   │      ^                    ^
Catalog Context ───┘      │                    │
                          v                    v
                   Shipping Context    Marketing Context

Relationships:
- Customer → Order: "Publishes" customer events (CustomerCreated, ProfileUpdated)
- Catalog → Order: "Reads for reference" product data at order time
- Order → Payment: "Initiates payment request" via synchronous call
- Order → Shipping: "Creates shipment after payment confirmed"
```

### Step 3: Map Dependencies Within the Monolith

Identify coupling patterns that will become inter-service dependencies:

**Dependency Analysis Checklist:**

```python
# Pseudo-code for dependency analysis
def analyze_dependencies(codebase):
    return {
        'service_calls': [],      # Internal method calls between modules
        'database_sharing': [],   # Shared tables across logical boundaries
        'shared_libraries': [],   # Common code used by multiple modules
        'api_endpoints': [],      # External API surface
        'background_jobs': []     # Scheduled tasks and event handlers
    }
```

**Common Dependency Patterns:**

| Pattern | Description | Risk Level | Migration Strategy |
|---------|-------------|------------|-------------------|
| Direct method calls | Module A directly calls methods in Module B | Low | Extract B, create API contract |
| Shared database tables | Multiple modules read/write same table | High | Strangler Fig with dual-write pattern |
| Shared static state | Global variables or singletons accessed by multiple modules | Medium | Introduce dependency injection per service |
| Synchronous call chains | A → B → C creates tight coupling | Medium | Extract intermediate services, add caching |
| Circular dependencies | A calls B, B calls back to A | High | Refactor to event-driven communication |

**Dependency Mapping Example (Text-based):**

```
Current Monolith Dependencies:

[User Module] ────> [Auth Module]
     │                   │
     v                   v
[Order Module] <──── [Payment Module]
     │                   │
     v                   v
[Shipping Module] ←── [Inventory Module]

Database Table Usage:
┌─────────────┬─────────────────────────────────────────────────────────┐
│ Table       │ Modules Using It                                           │
├─────────────┼─────────────────────────────────────────────────────────┤
│ users       │ User, Auth, Order, Payment (user_id)                     │
│ products    │ Catalog, Inventory, Order                                │
│ orders      │ Order, Payment, Shipping                                 │
│ payments    │ Payment, Order                                           │
│ inventory   │ Inventory, Catalog, Order                                │
│ shipments   │ Shipping, Order                                          │
│ cart_items  │ Cart (Order), User                                       │
└─────────────┴─────────────────────────────────────────────────────────┘

Key Finding: orders table is a critical coupling point between Order, Payment, and Shipping modules.
```

**Mermaid Dependency Diagram:**
```mermaid
graph TD
    User[User Module] --> Auth[Auth Module]
    User --> Order[Order Module]
    Auth --> Order
    Order --> Payment[Payment Module]
    Order --> Shipping[Shipping Module]
    Order --> Inventory[Inventory Module]
    Payment --> Shipping
    Inventory --> Shipping

    subgraph Database Layer
        users
        orders
        payments
        products
        inventory
        shipments
    end

    User -.->|reads/writes| users
    Order -.->|reads/writes| orders
    Payment -.->|reads/writes| payments
    Inventory -.->|reads/writes| inventory
```

### Step 4: Suggest Service Boundaries and Propose Services

Based on the dependency analysis, propose logical service boundaries:

**Service Extraction Criteria:**

```markdown
Priority Score = (Business Value × 3) + (Independence Score) - (Coupling Penalty)

Where:
- Business Value (1-5): How critical is this capability to revenue?
- Independence Score (1-5): Can it operate independently with minimal dependencies?
- Coupling Penalty (-1 to -5): How tightly coupled is it to other modules?
```

**Proposed Service Decomposition:**

```markdown
=== PROPOSED MICROSERVICES ===

1. **User Service** (High Priority)
   - Bounded Context: Customer
   - Responsibilities: User registration, authentication, profile management
   - Database: users table (extract to own database/schema)
   - API Endpoints: POST /register, GET /profile, PUT /profile, POST /logout
   - Dependencies: Auth module (internal), minimal external deps
   - Risk Level: LOW - Isolated functionality

2. **Catalog Service** (High Priority)
   - Bounded Context: Product Catalog
   - Responsibilities: Product listings, inventory queries, categories
   - Database: products, categories tables (extract)
   - API Endpoints: GET /products, GET /products/:id, GET /categories
   - Dependencies: Inventory read-only access initially
   - Risk Level: LOW - Read-heavy, stable data

3. **Order Service** (Medium Priority)
   - Bounded Context: Order Management
   - Responsibilities: Cart management, order creation, order history
   - Database: orders table (extract, keep user_id as reference)
   - API Endpoints: POST /cart, POST /checkout, GET /orders/:id
   - Dependencies: User Service (auth), Payment Service (sync), Shipping Service (async)
   - Risk Level: MEDIUM - Multiple downstream dependencies

4. **Payment Service** (Medium Priority)
   - Bounded Context: Financial Transactions
   - Responsibilities: Payment processing, refunds, transaction history
   - Database: payments table (extract)
   - API Endpoints: POST /payments, POST /payments/:id/refund, GET /transactions
   - Dependencies: Order Service (triggers), User Service (for receipts)
   - Risk Level: MEDIUM - External payment gateway integration

5. **Shipping Service** (Low Priority)
   - Bounded Context: Logistics
   - Responsibilities: Shipment creation, tracking, carrier communication
   - Database: shipments table (extract)
   - API Endpoints: POST /shipments, GET /shipments/:id/tracking, PUT /shipments/:id/status
   - Dependencies: Order Service (triggers), Inventory Service (stock check)
   - Risk Level: LOW - Event-driven, can be async

=== SERVICE COMMUNICATION PATTERNS ===

Synchronous (REST/gRPC):
- User Service ←→ Auth validation (internal to service)
- Order Service → Payment Service (create payment on checkout)
- Order Service → Catalog Service (validate product availability)

Asynchronous (Event-driven via message broker):
- Order Created → Shipping Service (event: order.created)
- Payment Confirmed → Order Service (event: payment.confirmed)
- Shipment Delivered → Order Service (event: shipment.delivered)
```

### Step 5: Generate Migration Plan Using Strangler Fig Pattern

Create a phased migration strategy using proven patterns:

**Phase-Based Migration Framework:**

| Phase | Duration | Goal | Risk Level | Key Activities |
|-------|----------|------|------------|---------------|
| **0 - Preparation** | 1-2 weeks | Set up foundations | Low | Infrastructure, CI/CD, monitoring |
| **1 - Parallel Systems** | 4-8 weeks | New features in new services | Low | Implement Strangler Fig for specific feature |
| **2 - Incremental Extraction** | 8-16 weeks | Extract core functionality | Medium | Migrate user-facing flows one by one |
| **3 - Dual Write & Sync** | 4-8 weeks | Data consistency during transition | Medium | Implement dual-write patterns |
| **4 - Cutover** | 2-4 weeks | Complete migration | High | Switch traffic, decompose legacy code |

**Strangler Fig Implementation Steps:**

```javascript
// Phase 1: Set up routing proxy (API Gateway or middleware)

// BEFORE: All requests go to monolith
app.use('/api/*', monolithicHandler);

// AFTER: Route specific endpoints to new service while maintaining others in monolith
const express = require('express');
const app = express();

// API Gateway / Routing Middleware
app.use('/api/users', userServiceRouter);        // New microservice
app.use('/api/catalog', catalogServiceRouter);   // New microservice
app.use('/api/orders', orderProxyHandler);       // Proxy to monolith initially

function orderProxyHandler(req, res, next) {
    // Route specific methods to new service as they're extracted
    if (req.method === 'GET' && req.path.startsWith('/orders/history')) {
        return orderHistoryServiceHandler(req, res);  // Extracted
    }
    if (req.method === 'POST' && req.path === '/cart') {
        return cartServiceHandler(req, res);          // Extracted
    }
    next();  // Fall back to monolith for remaining operations
}

// Phase 2: Feature Toggles for Safe Rollout
const featureToggles = {
    'new_checkout_flow': false,      // Controlled by config/database
    'payment_service_enabled': false,
    'shipping_integration_v2': false
};

function shouldUseNewService(endpoint) {
    return featureToggles[`new_${endpoint}_service`] || Math.random() < 0.1; // 10% traffic initially
}
```

**Branch by Abstraction Pattern:**

```python
# Create abstraction layer before extraction to minimize risk

from abc import ABC, abstractmethod

class UserServiceInterface(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> dict: pass

    @abstractmethod
    def update_profile(self, user_id: str, data: dict) -> bool: pass

# Legacy implementation (current monolith behavior)
class LegacyUserService(UserServiceInterface):
    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, user_id):
        # Current monolithic query with joins to other tables
        return self.db.query("""
            SELECT u.*, p.* FROM users u
            LEFT JOIN profiles p ON u.id = p.user_id
            WHERE u.id = %s
        """, (user_id,))

# New implementation (microservice client)
class ModernUserService(UserServiceInterface):
    def __init__(self, api_client):
        self.api_client = api_client  # HTTP client to User Service

    def get_user(self, user_id):
        response = self.api_client.get(f"/users/{user_id}")
        return response.json()

# Factory with feature toggle for gradual switch
def get_user_service():
    if feature_enabled('modern_user_service'):
        return ModernUserService(UserServiceAPI())
    return LegacyUserService(db_connection)
```

### Step 6: Generate Dependency Diagrams

Output text-based or Mermaid diagrams to visualize the migration path:

**Current State Diagram:**
```mermaid
graph TB
    subgraph Monolith["Monolithic Application"]
        User[User Module] --> Auth[Auth Module]
        User --> Order[Order Module]
        Order --> Payment[Payment Module]
        Order --> Shipping[Shipping Module]
        Inventory[Inventory Module] --> Order
    end

    subgraph SharedDB["Shared Database"]
        users
        orders
        payments
        products
        inventory
    end

    User -.->|reads/writes| users
    Order -.->|reads/writes| orders
    Payment -.->|writes| payments
```

**Target State Diagram (After Migration):**
```mermaid
graph TB
    subgraph Microservices["Microservices"]
        UserService[User Service]
        Auth[Auth Service]
        CatalogService[Catalog Service]
        OrderService[Order Service]
        PaymentService[Payment Service]
        ShippingService[Shipping Service]
    end

    subgraph MessageBroker["Event Broker (Kafka/RabbitMQ)"]
        events
    end

    UserClient[User Client/API Gateway] --> UserService
    UserClient --> CatalogService
    UserClient --> OrderService
    OrderService --> PaymentService
    OrderService --> ShippingService

    UserService -.->|publishes| events
    PaymentService -.->|publishes| events
    ShippingService -.->|publishes| events

    events --> OrderService
    events --> CatalogService
```

### Step 7: Define Phased Rollout Strategy

Create a detailed rollout plan with milestones and success criteria:

**Rollout Plan Template:**

```markdown
=== PHASE 0: PREPARATION (Weeks 1-2) ===

Infrastructure Setup:
- [ ] Set up container registry for service images
- [ ] Configure Kubernetes cluster or container orchestration
- [ ] Deploy message broker (Kafka/RabbitMQ) for async communication
- [ ] Set up API Gateway / Service Mesh (optional but recommended)
- [ ] Implement centralized logging and monitoring (ELK, Datadog, etc.)
- [ ] Create CI/CD pipelines for each new service

Team Readiness:
- [ ] Train teams on microservices patterns and tools
- [ ] Define ownership boundaries for each service team
- [ ] Establish deployment procedures and rollback protocols

=== PHASE 1: PARALLEL SYSTEMS (Weeks 3-10) ===

Target: User Service Extraction

Steps:
1. Deploy new User Service with minimal functionality (user lookup only)
2. Implement feature toggle to route read-only requests to new service
3. Gradually increase traffic percentage (1% → 5% → 25% → 50% → 100%)
4. Verify data consistency between monolith and new service
5. Extract write operations once read path is stable

Success Criteria:
- [ ] User lookup latency < 50ms p95 (same as monolith)
- [ ] Zero data inconsistency errors during transition
- [ ] Feature toggle can rollback to monolith in < 1 minute

=== PHASE 2: CORE FUNCTIONALITY EXTRACTION (Weeks 11-26) ===

Target: Catalog and Order Services

Parallel Extraction Strategy:
- Week 11-14: Extract Catalog Service (read-heavy, lower risk)
- Week 15-18: Extract Cart functionality from Order module
- Week 19-22: Extract Order creation flow
- Week 23-26: Extract Order history and status queries

Key Activities:
- Implement API contracts between services
- Add circuit breakers for service-to-service calls
- Set up distributed tracing (OpenTelemetry, Jaeger)
- Create contract tests for service interfaces

=== PHASE 3: DATA CONSISTENCY (Weeks 27-34) ===

Target: Payment and Shipping Services

Dual-Write Strategy:
```python
# During transition period, write to both legacy and new systems
def create_payment(order_id, payment_data):
    # Write to legacy system (backward compatible)
    legacy_db.create_payment(order_id, payment_data)

    # Write to new service via message queue (eventual consistency)
    event_broker.publish('payment.created', {
        'order_id': order_id,
        'data': payment_data,
        'source': 'legacy_migration'
    })

    # Sync job ensures data reaches Payment Service
```

=== PHASE 4: CUTOVER (Weeks 35-38) ===

Final Migration Steps:
1. Switch all traffic to new services (feature toggle → true)
2. Decommission legacy code paths in monolith
3. Remove dual-write patterns, rely on new systems only
4. Monitor closely for any regressions or performance issues
5. Plan database cleanup (remove shared tables once safe)

Rollback Triggers:
- Error rate > 1% for more than 5 minutes
- P95 latency increases by > 50%
- Data inconsistency detected in critical flows
```

### Step 8: Add Testing Recommendations

Specify test strategies to ensure migration safety:

**Testing Strategy Matrix:**

| Test Type | Purpose | Tools | When to Run |
|-----------|---------|-------|-------------|
| **Unit Tests** | Validate individual service logic | Jest, pytest, JUnit | Every commit |
| **Contract Tests** | Verify API compatibility between services | Pact, Spring Cloud Contract | Before deployment |
| **Integration Tests** | Test service interactions in test environment | Testcontainers | Before staging deploy |
| **End-to-End Tests** | Validate complete user flows across services | Cypress, Playwright | Nightly in staging |
| **Chaos Tests** | Verify resilience to failures | Chaos Monkey, Gremlin | Pre-production |

**Contract Testing Example:**
```javascript
// Consumer test (Order Service expects Payment Service API)
const { Matchers } = require('@pact/facade'); // Pact.js example

describe('Payment Service Contract', () => {
  const provider = 'PaymentService';
  const consumer = 'OrderService';

  beforeAll(() => {
    pact.setup({
      provider,
      consumer,
      port: 12345
    });
  });

  it('returns valid payment response', async () => {
    const interaction = new PactInteraction()
      .given('Payment system is available')
      .uponReceiving('a request to create a payment')
      .withRequest({
        method: 'POST',
        path: '/payments',
        body: { order_id: Matchers.something(/\d+/) }
      })
      .willRespondWith({
        status: 201,
        headers: { 'Content-Type': 'application/json' },
        body: {
          payment_id: Matchers.fromRegex(/pay_\w+/),
          status: 'pending',
          created_at: Matchers.iso8601Time()
        }
      });

    const response = await pact.verify(interaction);
    expect(response.status).toBe(201);
  });
});
```

**Integration Test with Testcontainers:**
```python
# Example using Python + Testcontainers for migration testing
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
import pytest

@pytest.fixture(scope="module")
def postgres():
    with PostgresContainer("postgres:15") as pg:
        yield pg.get_connection_url()

@pytest.fixture(scope="module")
def kafka():
    with KafkaContainer("confluentinc/cp-kafka:7.4.0") as k:
        yield k.get_bootstrap_url()

async def test_order_service_with_dependencies(postgres, kafka):
    """Test Order Service with mocked dependencies using containers"""
    # Spin up test instances of all services in isolated containers
    order_service = await start_service('order-service', postgres, kafka)
    payment_service = await start_service('payment-service', postgres, kafka)

    result = await order_service.create_order({
        'user_id': 'test-user',
        'items': [{'product_id': 123, 'quantity': 2}]
    })

    assert result['status'] == 'created'
    assert 'order_id' in result
```

### Step 9: Identify Risks and Rollback Procedures

Document potential failure modes and mitigation strategies:

**Risk Assessment Matrix:**

| Risk Category | Specific Risk | Probability | Impact | Mitigation | Rollback Procedure |
|---------------|---------------|-------------|--------|------------|-------------------|
| **Data Loss** | Inconsistent data during dual-write | Low | Critical | Implement idempotent writes, reconciliation jobs | Revert to monolith, run sync script |
| **Performance Degradation** | Network latency between services | Medium | High | Add caching, optimize API calls, use gRPC | Disable new service, fallback to monolith |
| **Service Outages** | One service down affecting others | Medium | High | Implement circuit breakers, timeouts, retries | Isolate failing service, degrade gracefully |
| **Deployment Issues** | Rollout failures in production | Low | Medium | Blue-green deployments, canary releases | Automatic rollback on error threshold breach |
| **Team Ramp-up** | Teams unfamiliar with microservices patterns | High | Medium | Training, pair programming, documentation | Temporarily maintain monolith for critical paths |

**Rollback Procedures:**

```markdown
### Emergency Rollback (Service Failure)

1. **Detect**: Monitoring alerts trigger on error rate > 1% or latency p95 > 2s
2. **Isolate**: Disable affected service via feature toggle or circuit breaker
3. **Fallback**: Route traffic back to monolithic implementation
4. **Investigate**: Analyze logs, traces, and metrics to identify root cause
5. **Fix**: Deploy hotfix with fix verification in staging
6. **Re-deploy**: Gradual re-enablement starting at 1% traffic

### Complete Rollback (Migration Failure)

```bash
# Script for complete rollback to monolith
#!/bin/bash

echo "Starting complete migration rollback..."

# Step 1: Stop all new service deployments
kubectl rollout stop deployment/order-service
kubectl rollout stop deployment/payment-service
kubectl rollout stop deployment/shipping-service

# Step 2: Re-enable feature toggles for legacy paths
curl -X POST https://config-api/feature-toggles/migration_mode \
  -d '{"migration_enabled": false}'

# Step 3: Disable API Gateway routing to new services
kubectl patch configmap api-gateway-routing \
  --type='merge' \
  -p '{"data":{"routes":"all->monolith"}}'

# Step 4: Verify monolith is handling all traffic
curl -s https://health-check/monolith-status | grep "healthy"

# Step 5: Investigate and document failure cause
# (Log analysis, team retrospective)

echo "Rollback complete. All traffic now flowing to monolith."
```

### Post-Migration Cleanup Checklist

After successful migration with no issues for 30+ days:

- [ ] Remove dual-write patterns from legacy code
- [ ] Decommission shared database tables (users, orders in monolith)
- [ ] Clean up feature toggles and migration configuration
- [ ] Update documentation to reflect new architecture
- [ ] Archive old monolithic deployment artifacts
- [ ] Conduct lessons learned retrospective

---

## Activation phrases / When to use

- "Decompose this monolith into microservices"
- "Suggest microservice boundaries for this app"
- "Plan incremental migration from monolith"
- "Map dependencies and break this codebase"
- "Apply Strangler Fig pattern to this legacy system"

## Usage Examples

```
Decompose this monolithic e-commerce app into services
Suggest microservice boundaries for this Node.js monolith
Create migration plan for breaking this Java Spring app
Map dependencies and propose services for this Python monolith
```

---

## How it works

1. **Scans project structure**, imports, database usage, and API endpoints to understand the codebase
2. **Applies Domain-Driven Design** principles to identify bounded contexts and service boundaries
3. **Maps dependencies** between modules (service calls, shared databases, shared libraries)
4. **Generates migration phases** using Strangler Fig pattern: identify seams → intercept calls → extract service → replace with proxy
5. **Outputs dependency diagrams** (text-based or Mermaid code) showing current and target states
6. **Recommends testing strategies** including contract tests, integration tests, and chaos engineering

---

## Dependencies

- None required (analyzes files/code directly)
- Optional: git for change history analysis
- Recommended: Mermaid.js for rendering diagrams locally

### Installation Commands (for diagram viewing):

```bash
# Install Mermaid CLI to render diagrams
npm install -g @mermaid-js/mermaid-cli

# Render a .mmd file to PNG
mmdc -i diagram.mmd -o diagram.png
```

---

## Best Practices / Notes

- **Prefer incremental extraction over big rewrite**: Use Strangler Fig or Branch by Abstraction patterns to minimize risk
- **Always include contract tests between services**: Prevents API breakage during independent deployments
- **Start with low-risk, high-value areas**: Extract read-only services first (Catalog) before complex transactions (Order/Payment)
- **Invest in observability early**: Distributed tracing and centralized logging are critical for debugging microservices
- **Design for failure**: Implement circuit breakers, timeouts, and retries from day one
- **Plan for eventual consistency**: Not all data needs to be immediately consistent across services
- **Keep team boundaries aligned with service boundaries**: Follow Conway's Law - organization structure affects system design
- **Automate everything**: CI/CD pipelines, testing, deployment should be fully automated before starting migration
