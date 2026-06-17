---
description: Environment variables, Docker, and deployment configuration
globs: *
---
# Configuration and Environment Standards

## 🎯 Directives
- ALWAYS use the setting module in `packages/koda/src/koda/config/main.py` for all the config.
- ALL modules or any part of the system MUST update the setting module and get config from the setting module.

## 📝 Examples

### ✅ DO
```python
from koda.config.main import settings

def connect_to_db():
    db_url = settings.consul_base_url
    # use db_url
```

### ❌ DON'T
```python
import os

def connect_to_db():
    # DON'T use os.getenv directly in modules
    db_url = os.getenv("CONSUL_BASE_URL", "http://localhost:8500")
```
