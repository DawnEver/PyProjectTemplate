# PyProjectTemplate

Extensible Python 3.12+ starter kit that ships with typed configuration, pint-backed physical quantities, structured logging, docs generation, and a fully wired test + lint stack. Use it as-is for simulation/analysis tooling or clone it as a baseline for new services.

> **Quick start**
> 1. `uv pip install -e ".[dev]"` (or `pip install -e ".[dev]"`)
> 2. `python -m pre-commit install`
> 3. `make all` to format, lint, and run pytest with coverage

## Highlights

- **Typed config loader** (`app.utils.config`) powered by `pydantic` + `pint`, ensuring every numeric field carries validated units.
- **Safety rails for I/O** (`app.utils.file_io`) that clone default TOML configs into `usr/local/` and keep reports/logs under `output/`.
- **Logging-first runtime** with rotating folders (`output/logs/<YYYY-MM-DD>/<HH>.log`) and consistent console/file formats configurable from TOML.
- **Quantity toolbox** (`app.utils.quantities`) offering reusable electromagnetic & mechanical units, conversions to/from numpy arrays, and helpers for geometry points.
- **Production-ready packaging**: `setuptools-scm` for versioning, console entry point (`app`), Ruff formatting, pytest + coverage, and optional dev extras.
- **Docs on tap**: `scripts/pdoc.py` regenerates the searchable API site in `docs/` (already built for offline browsing), complete with Mermaid + MathJax.

## Project Layout

```
├─ src/app/                 # Library code & CLI entry point (python -m app)
│   └─ utils/               # Config, logging, file IO, quantities, visualization helpers
├─ tests/                   # Unit / integration / e2e pytest suites (+ doctests)
├─ scripts/pdoc.py          # API doc generator and asset synchronizer
├─ usr/                     # User-level configs (local overrides vs defaults)
├─ output/                  # Auto-created logs and reports
├─ docs/                    # Rendered API documentation (pdoc output)
├─ htmlcov/                 # Coverage HTML artifacts from pytest --cov
├─ Makefile                 # install / lint / test / clean shortcuts
└─ pyproject.toml           # Metadata, deps, Ruff, pytest, commitizen config
```

## Requirements

- Python **3.12** or newer (Ruff + pytest settings target 3.12/3.13)
- Optional but recommended: [uv](https://github.com/astral-sh/uv) for ultra-fast installs
- `make` for the convenience targets (Windows users can run the underlying `python -m ...` commands directly)

## Setup & Installation

```bash
git clone https://github.com/DawnEver/PyProjectTemplate.git
cd PyProjectTemplate

# Create & activate a virtual environment (uv auto-manages .venv)
uv venv

# Install runtime + dev extras (pytest, coverage, ruff, pdoc, commitizen, pre-commit)
uv pip install -e ".[dev]"

# Enable git hooks and sanity-check the repo
python -m pre-commit install
make all
```

Prefer pip? Substitute `uv pip ...` with `pip ...`; everything else is unchanged.

## Running the Application

- **CLI entry**: `python -m app` (or just `app` thanks to `[project.scripts]` in `pyproject.toml`). The default `main()` is a stub—drop in orchestration logic and the logger/config stack is ready.
- **Logging**: `app.utils.logger.add_handle()` wires file + console handlers using formats stored in `CONF.utils`. Each run creates `output/logs/<YYYY-MM-DD>/<HH>.log`, plus timestamped figure/report paths.
- **Outputs**: Reports land under `output/reports/`; figures default to `<timestamp>.png` inside the run-specific log folder.

## Configuration

- User-editable settings live in `usr/local/config.toml`. If missing, it is cloned from `usr/default/default.config.toml` the first time `app.utils.config` loads.
- Schemas are defined via `Config(BaseModel_with_q)` ensuring:
	- automatic conversion of scalar inputs into pint quantities (e.g., `"10 mm"` → `Quantity`)
	- serialization back to TOML/JSON with units intact
	- numpy arrays emitted as vanilla lists when dumping configs or reports
- `PathData` centralizes canonical directories (logs, reports, default figs) so utility modules never hard-code paths.

To introduce new settings, extend `Core` or `Utils`, regenerate docs (`python scripts/pdoc.py`), and document defaults in `usr/default/default.config.toml`.

## Tooling & Commands

| Task            | Preferred Command                  | Notes |
|-----------------|------------------------------------|-------|
| Install runtime | `uv pip install -e .`              | Minimal dependencies only |
| Install dev set | `uv pip install -e ".[dev]"`      | Adds pytest/ruff/pdoc/etc. |
| Format & lint   | `make fmt`                         | Runs Ruff check + format with `--fix` |
| Lint only       | `make lint`                        | Ruff check + format --check |
| Run tests       | `make test` or `python -m pytest`  | Includes doctests, coverage, HTML report |
| Parallel tests  | `make test-parallel`               | Auto-detects CPU count via pytest-xdist |
| Longest tests   | `make test-duration`               | Shows slowest 10 tests |
| Clean artifacts | `make clean`                       | Removes build, cache, htmlcov, output, etc. |

## Testing & Coverage

- `python -m pytest` collects tests under `tests/` **and** `src/` (thanks to `pyproject.toml` → `tool.pytest.ini_options.testpaths`).
- Coverage is stored in `htmlcov/`; open `htmlcov/index.html` to inspect per-file detail.
- CI-style flags (`-q`, `-s`, doctest options, `--cov-append`, `--no-cov-on-fail`) are preconfigured—no need to memorize them.

## Documentation

- Generate/refresh API docs locally:

```bash
python scripts/pdoc.py               # Writes to docs/ and serves at http://localhost:8080
python scripts/pdoc.py -- open_webpage True  # auto-open browser (see script for flag)
```

- Static HTML lives under `docs/` (checked in so you can publish via GitHub Pages or any static host).
- The script also copies `.svg/.png/.jpg` assets from `src/app/**` into matching doc folders, keeping diagrams in sync.

## Working With Upstream Templates

If you forked this template and want to keep pulling upstream improvements, add the canonical remote once:

```bash
git remote add template https://github.com/DawnEver/PyProjectTemplate.git
git remote set-url --push template no_push_allowed
```

Then periodically `git fetch template` and rebase/merge as needed.

## Contributing & Release Hygiene

1. Create a feature branch, run `make fmt` + `python -m pytest` before pushing.
2. Keep commits conventional (`cz commit` or follow Conventional Commits manually); version bumps are handled via `setuptools-scm` and `commitizen`.
3. Run `python -m pre-commit run --all-files` for consistent formatting/metadata.
4. Update `README.md`, docs, and default configs when introducing user-visible options.

## Troubleshooting

- **Missing config**: Delete `usr/local/config.toml` to force regeneration from defaults.
- **Stale docs/coverage**: `make clean` removes `docs/`, `htmlcov/`, caches, and build artifacts so you can rebuild from scratch.
- **Windows without `make`**: invoke the commands directly (e.g., `python -m ruff check src`).

Ready to tailor the template? Start editing `src/app/__main__.py`, grow the typed config models, add tests under `tests/`, and regenerate docs—everything else is already wired up.
