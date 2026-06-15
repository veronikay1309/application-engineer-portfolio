# Application Engineer Portfolio

A collection of tools and frameworks demonstrating the core competencies of an Application Engineer, specifically focused on data quality validation, ETL pipelines, metadata migration, log analysis, and SLA tracking tools built in Python.

## Projects Included

| # | Project Name | Description | Status |
|---|--------------|-------------|--------|
| 1 | [catalog-data-validator](./catalog-data-validator) | Validates e-commerce catalog data against JSON schemas | ✅ Complete |
| 2 | [etl-pipeline-framework](./etl-pipeline-framework) | Pluggable ETL pipeline for processing customer data | ✅ Complete |
| 3 | [metadata-migration-tool](./metadata-migration-tool) | Extracts and maps legacy system metadata | ✅ Complete |
| 4 | [incident-log-analyzer](./incident-log-analyzer) | Parses server logs to detect anomalies and error spikes | ✅ Complete |
| 5 | [sla-ticket-tracker](./sla-ticket-tracker) | Tracks support tickets and proactively alerts on SLA breaches | ✅ Complete |
| 6 | [product-deduplicator](./product-deduplicator) | Identifies duplicate product listings using Exact and Fuzzy string matching | ✅ Complete |

## Quick Start
Each project is self-contained with its own `Makefile`, `requirements.txt`, and automated tests. Navigate to any project folder to get started.

```bash
cd catalog-data-validator
make install
make run
```

## Technologies
- **Python 3.9+**
- **Pandas** for data manipulation
- **Pytest** for unit and integration testing
- **Jinja2** for HTML dashboard generation
- **TheFuzz** for Levenshtein distance string matching
- **GitHub Actions** for CI/CD pipelines
