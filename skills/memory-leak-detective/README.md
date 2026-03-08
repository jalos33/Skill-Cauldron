# Memory Leak Detective Skill

A Claude Code skill for analyzing heap dumps and runtime memory patterns in Node.js and Python applications to detect memory leaks and suggest fixes.

## Description

The Memory Leak Detective skill helps developers identify, diagnose, and fix memory leaks in their applications by analyzing heap snapshots and runtime memory usage patterns. It provides actionable recommendations for preventing common leak scenarios.

## Purpose

Memory leaks are notoriously difficult to debug because they manifest gradually over time. This skill provides a systematic approach to:
- Analyze heap dump files (.heapsnapshot) from Node.js applications
- Trace memory allocations in Python using tracemalloc and related tools
- Identify root causes of growing memory usage
- Suggest concrete fixes based on leak patterns

## Features

- **Heap Snapshot Analysis**: Parse and compare .heapsnapshot files to identify retained objects
- **Pattern Detection**: Recognizes common leak patterns (event listeners, unclosed connections, unbounded caches)
- **Cross-Language Support**: Works with both Node.js and Python applications
- **GC Tuning Recommendations**: Suggests optimal garbage collection settings for long-running services
- **Weak Reference Guidance**: Recommends when to use WeakMap/WeakSet or weakref modules
- **Severity Classification**: Categorizes findings by urgency (Critical/High/Medium/Low)

## How to Use

### Activation Phrases

Use these phrases to invoke the Memory Leak Detective skill:
- "Analyze this heap dump for leaks"
- "Find memory leak in this Node.js app"
- "Debug Python memory growth"
- "Suggest fixes for increasing heap size"
- "Review memory usage after adding cache"

### Usage Examples

```bash
# Analyze a Node.js heap snapshot
Analyze heapdump-2026-03-07.heapsnapshot for leaks in Node.js

# Debug Python memory issues
Why is my Python process memory climbing over time?

# Get fix recommendations
Suggest fixes for this Node.js server leaking on every request
```

## Examples

### Node.js Heap Analysis

1. Generate a heap snapshot:
```javascript
const heapdump = require('heapdump');
heapdump.writeSnapshot('/tmp/heap-' + Date.now() + '.heapsnapshot');
```

2. Load in Chrome DevTools and ask the skill to analyze for leaks.

### Python Memory Tracing

1. Enable tracemalloc:
```python
import tracemalloc
tracemalloc.start()
# ... run application ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

2. Share the output with the skill for analysis.

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/memory-leak-detective
