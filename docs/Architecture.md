# Architecture

- Bun-powered dev environment
  - ultra-fast installs, test runner, and scripts
  - note: Bun is the runtime and package manager, but SvelteKit still uses Vite internally for bundling, HMR, SSR, and plugin integration
- SvelteKit SPA architecture
  - routing, server endpoints, local-first operations
  - svelte-shadcn component library for consistent UI patterns
  - svelte stores reacting to DB + Tauri backend changes
  - relies on Vite as the build system; Bun does not replace Vite for SvelteKit
- Tauri desktop shell
  - secure Rust backend for Git, filesystem, and process integrations
  - lightweight app bundle with auto-updatable commands
- Local SQLite via SQLocal (WASM)
  - local-first persistence
  - DAG-based conversation + version modeling
- No login required; all data local and user-owned
- Fully open source; contributions welcome

# Other Considerations

- cancelable streams
- retry logic
- token buffers
- role tagging
- svelt virtual scrolling for large histories
- drizzle for typed schema
- zod for schema validation
- web workers to stream and parse recursive sql queries
- backups for exporting to .sqlite files on local computer
- will need some broadcast channel sync, or tab locking rules for if someone opens the UI in two tabs

# Extended System Considerations

- **Tauri Command Layer**

  - Rust commands for: Git operations, file IO, repo scanning, diff generation
  - secure IPC boundary with permission scoping
  - background tasks for long-running operations (commit history, indexing)

- **Git Integration Layer**

  - ability to link a project folder and track histories
  - commit snapshots of conversations, states, and embeddings
  - optional GitHub sync (future feature)

- **Local-First Data Model**

  - SQLite schema built with Drizzle ORM
  - DAG-based message/version graph
  - background compaction + indexing workers
  - export/import `.sqlite` archives

- **OpenRouter Integration**
  - ability to select different models (OpenAI, Anthropic, Gemini, etc.)
  - cached metadata and model lists
  - request routing through local DB + streamed UI responses
