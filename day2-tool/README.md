# 工具调用中段
        ┌──────────────┐
        │    LLM       │
        └─────┬────────┘
              ↓
     🔒 JSON Schema Guard
              ↓
      Tool Parser (strict)
              ↓
        Tool Router
              ↓
     Structured Tool Result
              ↓
        回填 LLM
