---
name: concurrency-safety-checker
description: Detects race conditions, data races, and concurrency bugs in Go and Rust code by analyzing shared state, locks, goroutines/channels, and ownership patterns.
tags: [concurrency, race-conditions, go, rust, safety, debugging]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Concurrency Safety Checker

This skill detects **race conditions**, **data races**, and **concurrency bugs** in Go and Rust code by analyzing shared state access patterns, synchronization mechanisms (mutexes, channels, Arc/RwLock), and ownership rules. It identifies common anti-patterns like goroutine leaks, unclosed channels, unsafe blocks without proper safety measures, and unprotected shared data access.

## Instructions

When activated, follow this step-by-step process:

### Step 1: Identify Code Language
- **Determine language**: Check for Go patterns (`package main`, `go func()`, `<- channel`) or Rust patterns (`fn`, `async`, `Arc<Mutex<T>>`, `Send/Sync` traits)
- **Load appropriate rules**: Use Go-specific checks (goroutines, channels, mutexes) or Rust-specific checks (ownership, Arc, RwLock, Unsafe blocks)

### Step 2: Build Shared State Map
- **Identify shared variables**: Find global variables, package-level state, struct fields accessed across function boundaries
- **Track mutation sites**: Note where variables are written/modified
- **Map access patterns**: Document all read and write operations on each variable
- **Check function parameters**: Identify mutable references (`*T` in Go, `&mut T` in Rust)

### Step 3: Check Synchronization Mechanisms

**For Go code:**
- **Mutex checks**: Verify `sync.Mutex`, `sync.RWMutex` used before accessing shared data
- **Channel usage**: Ensure channels properly used for communication between goroutines (`<-` operator)
- **WaitGroup patterns**: Confirm `sync.WaitGroup` used to coordinate goroutine completion
- **Once patterns**: Check `sync.Once` for one-time initialization

**For Rust code:**
- **Mutex checks**: Verify `std::sync::Mutex`, `RwLock` wraps shared data
- **Arc ownership**: Ensure `Arc<T>` or `Arc<Mutex<T>>` used for shared state across threads
- **Send/Sync traits**: Check if types properly implement required traits for thread transfer
- **Unsafe blocks**: Identify unsafe code and verify safety invariants are maintained

### Step 4: Detect Common Anti-Patterns

**Go anti-patterns:**
- Goroutine started without synchronization (no WaitGroup, no channel close)
- Channel sent to but never closed, causing goroutine leaks
- Shared mutable state accessed without mutex protection
- Multiple mutex locks in different orders (potential deadlock)
- Blocking operations inside critical sections

**Rust anti-patterns:**
- `Arc` used without proper interior mutability (`Mutex`, `RwLock`)
- References to borrowed data passed across thread boundaries
- `Unsafe` blocks with undefined behavior risks
- Missing `Send`/`Sync` bounds on generic types
- Deadlock potential from lock ordering violations

### Step 5: Verify Ownership Rules (Rust)
- **Move semantics**: Ensure moved values not used after move
- **Borrow checker**: Check for conflicting borrows (`&T` and `&mut T`)
- **Lifetime issues**: Identify references that may outlive their data
- **Thread transfer safety**: Confirm types implementing `Send` when crossed to threads

### Step 6: Generate Report with Severity Levels

**CRITICAL (🔴):**
- Data race causing undefined behavior or memory corruption
- Potential deadlock that will freeze the application
- Unsafe block with clear memory safety violation

**HIGH (🟠):**
- Unprotected shared mutable state access
- Possible goroutine/async task leak
- Channel communication without proper close/handshake

**MEDIUM (🟡):**
- Suboptimal locking strategy (e.g., mutex where rwlock would suffice)
- Potential deadlock under specific timing conditions
- Missing documentation for concurrent access patterns

**LOW (🟢):**
- Code style inconsistency in synchronization usage
- Suggestion to prefer channels over shared memory (Go)
- Recommendation for better lock granularity

### Step 7: Provide Line Numbers and Evidence
For each issue found:
- **Line number**: Exact location of the problematic code
- **Evidence excerpt**: Show 3-5 lines of relevant code context
- **Issue type**: Clear categorization (Data Race, Deadlock Risk, Goroutine Leak, etc.)

### Step 8: Suggest Minimal Fixes
For each issue, provide actionable fix suggestions:
- **Go**: Add `sync.Mutex.Lock()/Unlock()`, use channel for communication, add `WaitGroup.Done()`
- **Rust**: Wrap in `Arc<Mutex<T>>` or `Arc<RwLock<T>>`, ensure proper `Send` bounds, remove unsafe block

## Activation Phrases / When to Use

Use this skill whenever you need to audit concurrent code:

- "Check for race conditions in this Go code"
- "Detect concurrency bugs in this Rust module"
- "Audit shared state safety in this function"
- "Verify thread-safety in this backend code"
- "Find data races in this concurrent code"
- "Analyze goroutine patterns in this server handler"
- "Check Rust async/await safety for this function"

## Usage Examples

| User Input | Expected Skill Behavior |
|------------|------------------------|
| "Check for race conditions in this Go server handler" | Analyze Go handler code, identify shared variables accessed by multiple goroutines without mutex protection, report data race with line numbers and suggest sync.Mutex wrapping. |
| "Detect concurrency bugs in this Rust async function" | Parse Rust async code, check Arc/RwLock usage, verify Send/Sync bounds on futures, identify potential deadlocks or unsafe blocks needing review. |
| "Audit shared cache access in this Go app" | Review Go application's shared cache implementation, detect unprotected map accesses across goroutines, suggest sync.RWMutex for read-heavy workloads. |
| "Verify thread-safety in this Rust web service" | Examine Rust web server code, verify Arc<Mutex<T>> patterns for shared state, check channel communication between threads, ensure no data races in async handlers. |

## How It Works

```
User provides Go or Rust concurrent code
          │
          ▼
┌───────────────────────┐
│  Step 1: IDENTIFY    │ → Detect language (Go/Rust)
│  (Language Detection)│ → Load appropriate ruleset
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 2: MAP STATE   │ → Build shared variable map
│  (Shared State Map)  │ → Track mutations and accesses
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 3: CHECK SYNC  │ → Verify mutex/lock usage
│  (Synchronization)   │ → Validate channels/Arc patterns
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 4: DETECT      │ → Identify anti-patterns
│  (Anti-Pattern Scan) │ → Check for leaks, deadlocks
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 5: VERIFY      │ → Rust ownership rules
│  (Ownership/Rules)   │ → Send/Sync trait checks
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 6: REPORT      │ → Generate severity report
│  (Severity Report)   │ → Line numbers, evidence
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 7: SUGGEST     │ → Provide fix suggestions
│  (Fix Recommendations)│ → Minimal code changes
└───────────────────────┘
          │
          ▼
    Output: Concurrency safety report with fixes
```

## Dependencies

- **No external dependencies required** - performs static analysis via pattern matching on source code
- Optional: `go test -race` for Go runtime race detection (recommended for CI/CD)
- Optional: `cargo test -- --test-threads=1` or `RUSTFLAGS="-Z sanitizer=address"` for Rust

## Best Practices / Notes

- **Prefer channels over shared memory in Go**: Follow the "Do not communicate by sharing memory; instead, share memory by communicating" principle
- **Use Arc/RwLock for shared state in Rust**: Wrap shared data in `Arc<Mutex<T>>` or `Arc<RwLock<T>>` for thread-safe access
- **Run with race detector in CI/CD**: Use Go's `-race` flag and Rust sanitizers for comprehensive detection
- **Avoid unsafe blocks unless necessary**: Unsafe code should be minimized and well-documented
- **Use proper lock ordering**: Prevent deadlocks by establishing a consistent lock acquisition order across the codebase
- **Document concurrent access patterns**: Clearly document which locks protect which shared state
- **Prefer higher-level concurrency primitives**: Use `sync.Once`, `channel` patterns, or async/await where appropriate
- **Test concurrent code thoroughly**: Write specific race condition tests using `-race` flag

## Output Format

The skill outputs a structured concurrency safety report:

```markdown
# Concurrency Safety Report

## Summary
- Language Analyzed: Go / Rust
- Total Issues Found: 5 (Critical: 1, High: 2, Medium: 1, Low: 1)
- Files Reviewed: main.go, cache.go

---

## 🔴 CRITICAL Issues

### Data Race on sharedCounter
**Severity:** CRITICAL | **Type:** Data Race
**File:** `main.go` | **Line:** 45

**Evidence:**
```go
var sharedCounter int // Global variable

func handler1() {
    sharedCounter++ // Write without lock!
}

func handler2() {
    fmt.Println(sharedCounter) // Read from different goroutine!
}
```

**Issue:** `sharedCounter` is accessed by multiple goroutines without synchronization, leading to undefined behavior.

**Fix:** Protect with mutex:
```go
var (
    sharedCounter int
    counterMu     sync.Mutex
)

func handler1() {
    counterMu.Lock()
    sharedCounter++
    counterMu.Unlock()
}

func handler2() {
    counterMu.Lock()
    fmt.Println(sharedCounter)
    counterMu.Unlock()
}
```

---

## 🟠 HIGH Issues

### Goroutine Leak: WaitGroup Not Called
**Severity:** HIGH | **Type:** Goroutine Leak
**File:** `main.go` | **Line:** 78

**Evidence:**
```go
func processTasks(tasks []string) {
    var wg sync.WaitGroup
    for _, task := range tasks {
        wg.Add(1)
        go func(t string) {
            doWork(t)
            // Missing: defer wg.Done()
        }(task)
    }
}
```

**Issue:** WaitGroup's `Done()` is never called, causing the goroutine to block forever waiting for completion.

**Fix:** Add deferred call:
```go
for _, task := range tasks {
    wg.Add(1)
    go func(t string) {
        defer wg.Done() // Add this line
        doWork(t)
    }(task)
}
```

---

## 🟡 MEDIUM Issues

### Lock Ordering Violation Risk
**Severity:** MEDIUM | **Type:** Potential Deadlock
**File:** `cache.go` | **Line:** 23

**Issue:** Different lock acquisition orders in `updateCache()` and `readCache()` could cause deadlock under contention.

**Recommendation:** Establish consistent lock ordering: always acquire `fileMu` before `dataMu`.

---

## 🟢 LOW Issues

### Prefer Channels Over Shared Memory
**Severity:** LOW | **Type:** Design Suggestion
**File:** `worker.go` | **Line:** 12

**Suggestion:** Consider using a channel for task distribution instead of shared queue with mutex protection.

```go
// Instead of:
var taskQueue []Task
var mu sync.Mutex

// Use:
taskChan := make(chan Task, bufferSize)
```

---

*Generated by Concurrency Safety Checker v1.0*
```
