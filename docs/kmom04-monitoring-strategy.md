# Kmom04 monitoring strategy

Microblog gets a small but practical monitoring setup that focuses on fast feedback when the app starts failing.

## Goals

- detect server-side errors quickly
- show the errors in a dashboard that is easy to read during debugging
- notify externally when an alert fires
- keep a little extra context around load and latency

## What to monitor

### Errors

The main signal is `flask_http_request_total` filtered to `5xx` status codes. This is used in two places:

- Prometheus alert rule `MicroblogServerErrors`
- Grafana panel showing the total amount of 5xx responses

### Traffic

Request rate split by status code gives context around whether the application is healthy or only partly failing.

### Latency

The `95th percentile` latency panel helps show degraded behavior before or alongside outright failures.

## Alerting flow

1. Flask exposes `/metrics`.
2. Prometheus scrapes the app every five seconds.
3. The alert rule fires when new 5xx responses appear during the last minute.
4. Alertmanager forwards the alert to webhook.site.
5. Grafana reads the same Prometheus data for dashboards.

## AI assistance summary

AI suggested keeping the course-provided 5xx alert as the core signal and adding two supporting views: request rate by status code and p95 latency. That was a good fit for the assignment, so the strategy kept those additions. The only simplification was to avoid adding too many extra alerts and instead focus on one clear alert plus a dashboard that explains what happened.
