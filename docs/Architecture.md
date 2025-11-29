# Architecture

- Vite SPA → Sveltekit with modern reactivity
  - svelte shadcn for self component library
  - svelte stores to auto reac tto DB changes
- Persistent Backend: SQLocal for SQLite in WASM
  - modeling on the DAG structure found here
- Local First; no logins or content saved
- Fully Opensource for the public to use and improve; no guarantees for support though

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
