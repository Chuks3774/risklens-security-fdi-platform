ADR-001: Project scope and production standards

Problem: Businesses and researchers need reproducible, auditable insight into how security risks and governance quality correlate with foreign investment outcomes.

Decision: Build a Lakehouse-style data platform (Bronze/Silver/Gold) that:

ingests public datasets (security risk, governance/corruption proxies, macro indicators, FDI)

models into a star schema for analytics performance

enforces data quality rules and a basic SLA

publishes a Power BI-ready serving layer

Production standards included:

config-driven pipelines

data validation (Great Expectations)

documented architecture + decision records

versioned releases (v0.1+)

Time window: 2013–2023