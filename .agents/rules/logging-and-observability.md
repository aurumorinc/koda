---
description: Logging practices, tracebacks, and system observability
globs: *
---
# Logging and Observability Standards

## 🎯 Directives
- ALWAYS use `packages/koda/src/koda/config/logging.py` for all the logging.

## 📝 Examples

### ✅ DO
```python
from koda.config.logging import get_logger

logger = get_logger(__name__)

def process_data():
    logger.info("Processing data started")
```

### ❌ DON'T
```python
import logging

logger = logging.getLogger(__name__)

def process_data():
    logger.info("Processing data started")
```
