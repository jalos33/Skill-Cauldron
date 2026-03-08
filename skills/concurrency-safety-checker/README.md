# Concurrency Safety Checker Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/jalos33/Skill-Cauldron/tree/main/skills/concurrency-safety-checker)

A Claude Code skill that **detects race conditions**, **data races**, and **concurrency bugs** in Go and Rust code by analyzing shared state access patterns, synchronization mechanisms (mutexes, channels, Arc/RwLock), and ownership rules. Identifies common anti-patterns like goroutine leaks, unclosed channels, unsafe blocks without proper safety measures, and unprotected shared data access.

## Purpose

This skill helps developers write safe concurrent code in Go and Rust by:
- Scanning code for race conditions before runtime execution
- Verifying proper use of synchronization primitives (mutexes, channels, Arc/RwLock)
- Detecting common concurrency anti-patterns (goroutine leaks, deadlocks, unsafe blocks)
- Providing actionable fix suggestions with minimal code changes

Whether you're building a high-performance Go server or a Rust async application, this skill ensures your concurrent code is thread-safe and free from data races.

## Features

- **Multi-Language Support** - Analyzes both Go (goroutines, channels, mutexes) and Rust (Arc, RwLock, Send/Sync traits)
- **Shared State Analysis** - Builds call graphs to track shared variable access across function boundaries
- **Synchronization Verification** - Validates proper use of mutexes, channels, Arc/RwLock patterns
- **Anti-Pattern Detection** - Identifies goroutine leaks, unclosed channels, unsafe blocks, deadlock risks
- **Severity-Based Reporting** - Issues ranked CRITICAL/HIGH/MEDIUM/LOW with clear categorization
- **Actionable Fix Suggestions** - Provides minimal code changes to resolve each issue

## Features Overview

| Feature | Description |
|---------|-------------|
| **Shared State Mapping** | Builds map of global variables and tracks mutation sites |
| **Synchronization Checks** | Verifies mutex, channel, Arc/RwLock usage patterns |
| **Anti-Pattern Detection** | Scans for goroutine leaks, deadlocks, unsafe blocks |
| **Rust Ownership Rules** | Validates Send/Sync traits, move semantics, lifetimes |
| **Severity Classification** | CRITICAL (data races), HIGH (leaks), MEDIUM (deadlock risk), LOW (suggestions) |
| **Fix Suggestions** | Minimal code changes with before/after examples |

## When to Use

Use this skill whenever you're working with concurrent Go or Rust code:

| Scenario | Command |
|----------|---------|
| Check for race conditions | "Check for race conditions in this Go code" |
| Detect concurrency bugs | "Detect concurrency bugs in this Rust module" |
| Audit shared state safety | "Audit shared state safety in this function" |
| Verify thread-safety | "Verify thread-safety in this backend code" |
| Find data races | "Find data races in this concurrent code" |
| Analyze goroutine patterns | "Analyze goroutine patterns in this server handler" |

## How to Use

### Basic Usage

1. **Activate the skill** with any of these phrases:
   - "Check for race conditions in this Go code"
   - "Detect concurrency bugs in this Rust module"
   - "Audit shared state safety in this function"
   - "Verify thread-safety in this backend code"
   - "Find data races in this concurrent code"

2. **Provide the Go or Rust code**:
   ```
   Check for race conditions in this Go server handler:

   package main

   import (
       "fmt"
       "net/http"
       "sync"
   )

   var userCache = make(map[string]*User)
   var cacheMu sync.Mutex

   type User struct {
       ID   string
       Name string
   }

   func getUserHandler(w http.ResponseWriter, r *http.Request) {
       userID := r.URL.Query().Get("id")

       // Race condition: reading without lock
       if user, exists := userCache[userID]; exists {
           w.Write([]byte(user.Name))
           return
       }

       // Race condition: write without lock
       newUser := &User{ID: userID, Name: "New User"}
       userCache[userID] = newUser

       cacheMu.Lock()
       _ = cacheMu // Lock acquired too late!
       cacheMu.Unlock()
   }

   func processUsers(users []string) {
       var wg sync.WaitGroup
       for _, u := range users {
           wg.Add(1)
           go func(name string) {
               fmt.Println("Processing:", name)
               // Missing: defer wg.Done()
               wg.Done() // Called too late, after goroutine might exit
           }(u)
       }
       wg.Wait()
   }
   ```

3. **Receive concurrency safety report**:
   - Issues ranked by severity (CRITICAL/HIGH/MEDIUM/LOW)
   - Line numbers and code evidence for each issue
   - Minimal fix suggestions with before/after code

### Example Workflow

```
User: Check for race conditions in this Go server handler

[Go code provided above]

Skill Output:

# Concurrency Safety Report

## Summary
- Language Analyzed: Go
- Total Issues Found: 3 (Critical: 1, High: 2)
- Files Reviewed: main.go

---

## 🔴 CRITICAL Issues

### Data Race on userCache Map Access
**Severity:** CRITICAL | **Type:** Data Race
**File:** `main.go` | **Line:** 20

**Evidence:**
```go
// Race condition: reading without lock
if user, exists := userCache[userID]; exists {
    w.Write([]byte(user.Name))
    return
}

// Race condition: write without lock
newUser := &User{ID: userID, Name: "New User"}
userCache[userID] = newUser
```

**Issue:** The `userCache` map is accessed (both read and write) by multiple handlers potentially running concurrently, without holding the mutex. This can cause panic or data corruption.

**Fix:** Protect all accesses with lock:
```go
func getUserHandler(w http.ResponseWriter, r *http.Request) {
    userID := r.URL.Query().Get("id")

    cacheMu.Lock()
    if user, exists := userCache[userID]; exists {
        name := user.Name // Copy while holding lock
        cacheMu.Unlock()
        w.Write([]byte(name))
        return
    }

    newUser := &User{ID: userID, Name: "New User"}
    userCache[userID] = newUser
    cacheMu.Unlock()

    w.Write([]byte(newUser.Name))
}
```

---

## 🟠 HIGH Issues

### Goroutine Leak: WaitGroup Misuse
**Severity:** HIGH | **Type:** Goroutine Leak / Deadlock Risk
**File:** `main.go` | **Line:** 35

**Evidence:**
```go
func processUsers(users []string) {
    var wg sync.WaitGroup
    for _, u := range users {
        wg.Add(1)
        go func(name string) {
            fmt.Println("Processing:", name)
            // Missing: defer wg.Done() at start of goroutine
            wg.Done() // Called too late, after goroutine might exit
        }(u)
    }
    wg.Wait()
}
```

**Issue:** The `wg.Done()` call is placed at the end of the goroutine body. If any code before it panics or returns early, the WaitGroup counter never decrements, causing `wg.Wait()` to block forever.

**Fix:** Use defer at the start:
```go
for _, u := range users {
    wg.Add(1)
    go func(name string) {
        defer wg.Done() // Always called when goroutine exits
        fmt.Println("Processing:", name)
    }(u)
}
```

---

## Recommended Actions

1. **Fix data race immediately** - Wrap all userCache accesses in mutex lock (CRITICAL)
2. **Add defer for WaitGroup** - Ensure wg.Done() is called even on early return (HIGH)
3. **Consider RWMutex** - If reads dominate writes, use sync.RWMutex for better performance

---
*Generated by Concurrency Safety Checker v1.0*
```

## Installation

### Install from Repository

Download and install the skill directly:

```bash
curl -L https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/concurrency-safety-checker/concurrency-safety-checker.skill \
  -o ~/.claude/skills/concurrency-safety-checker.skill && echo "✅ Concurrency Safety Checker installed!"
```

### Verify Installation

```bash
ls -la ~/.claude/skills/concurrency-safety-checker.skill
```

## Testing the Skill

Run these test cases to verify the skill works correctly:

| Test | Command | Expected Output |
|------|---------|-----------------|
| **Test 1** | "Check for race conditions in this Go server handler" | Report identifying data races on shared map access, WaitGroup misuse with goroutine leak risk |
| **Test 2** | "Detect concurrency bugs in this Rust async function" | Analysis of Arc/RwLock usage, Send/Sync trait bounds, potential deadlocks in async code |
| **Test 3** | "Audit shared cache access in this Go app" | Detection of unprotected map accesses across goroutines, suggestions for sync.RWMutex or channel patterns |

## Severity Badge Legend

| Badge | Level | Meaning | Action Required |
|-------|-------|---------|-----------------|
| 🔴 | CRITICAL | Data race causing undefined behavior or memory corruption | Fix immediately before deployment |
| 🟠 | HIGH | Possible goroutine/async task leak, unprotected shared state | Fix before production release |
| 🟡 | MEDIUM | Suboptimal locking strategy, potential deadlock under timing conditions | Address in next sprint |
| 🟢 | LOW | Code style inconsistency, design suggestions for improvement | Optional enhancement |

## Best Practices

- **Prefer channels over shared memory in Go**: Follow the principle "Do not communicate by sharing memory; instead, share memory by communicating"
- **Use Arc/RwLock for shared state in Rust**: Wrap shared data in `Arc<Mutex<T>>` or `Arc<RwLock<T>>` for thread-safe access
- **Run with race detector in CI/CD**: Use Go's `-race` flag (`go test -race`) and Rust sanitizers (`RUSTFLAGS="-Z sanitizer=address"`)
- **Avoid unsafe blocks unless necessary**: Unsafe code should be minimized and well-documented with safety proofs
- **Use proper lock ordering**: Prevent deadlocks by establishing a consistent lock acquisition order across the codebase
- **Document concurrent access patterns**: Clearly document which locks protect which shared state
- **Prefer higher-level concurrency primitives**: Use `sync.Once`, channel patterns, or async/await where appropriate
- **Test concurrent code thoroughly**: Write specific race condition tests using `-race` flag

## Go Concurrency Patterns

### Proper Mutex Usage

```go
var (
    counter int
    mu      sync.Mutex
)

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}

func getCount() int {
    mu.Lock()
    defer mu.Unlock()
    return counter
}
```

### Channel-Based Communication (Preferred)

```go
// Instead of shared state with mutex:
taskChan := make(chan Task, 100)

// Launch workers that consume from channel:
for i := 0; i < workerCount; i++ {
    go func() {
        for task := range taskChan {
            process(task)
        }
    }()
}

// Send tasks to channel (no shared state needed):
taskChan <- Task{ID: 1, Data: "work"}
close(taskChan) // Signal no more tasks coming
```

### WaitGroup with Defer

```go
func processTasks(tasks []string) {
    var wg sync.WaitGroup
    for _, task := range tasks {
        wg.Add(1)
        go func(t string) {
            defer wg.Done() // Ensures counter decrements on any exit path
            doWork(t)
        }(task)
    }
    wg.Wait()
}
```

## Rust Concurrency Patterns

### Arc<Mutex<T>> for Shared State

```rust
use std::sync::{Arc, Mutex};

struct SharedCounter {
    count: u64,
}

fn main() {
    let counter = Arc::new(Mutex::new(SharedCounter { count: 0 }));

    // Clone the Arc to share ownership across threads
    let counter1 = Arc::clone(&counter);
    let handle1 = std::thread::spawn(move || {
        let mut num = counter1.lock().unwrap();
        num.count += 1;
    });

    let counter2 = Arc::clone(&counter);
    let handle2 = std::thread::spawn(move || {
        let num = counter2.lock().unwrap();
        println!("Count: {}", num.count);
    });

    handle1.join().unwrap();
    handle2.join().unwrap();
}
```

### RwLock for Read-Heavy Workloads

```rust
use std::sync::{Arc, RwLock};

let data = Arc::new(RwLock::new(DataStore { items: Vec::new() }));

// Multiple readers can access simultaneously
{
    let read_guard = data.read().unwrap();
    // Read-only operations
}

// Exclusive writer blocks all other access
{
    let mut write_guard = data.write().unwrap();
    // Write operations
}
```

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contributing

Found issues or want to improve this skill? Open an issue at:
https://github.com/jalos33/Skill-Cauldron/issues

## See Also

- [Code Reviewer Skill](../code-reviewer/) - Automated code review with competing agents framework
- [CI/CD Pipeline Auditor](../ci-cd-pipeline-auditor/) - Security audit for GitHub Actions workflows
- More skills in the [Skill-Cauldron repository](https://github.com/jalos33/Skill-Cauldron)
