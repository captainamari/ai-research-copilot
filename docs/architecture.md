# Architecture

AI Research Copilot starts with a small layered structure:

- `apps/` contains runnable API and web entrypoints.
- `src/research_copilot/core/` contains shared configuration and logging.
- `src/research_copilot/research_os/` contains research-domain models and storage.
- `src/research_copilot/services/` contains application services used by entrypoints.
- `data/` contains local development data and uploaded files.
