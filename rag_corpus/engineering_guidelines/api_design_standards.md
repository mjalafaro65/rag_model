# API Design Standards
**Northlane Systems — Engineering**
**Effective Date:** October 2025
**Document ID:** ENG-STD-004

## Purpose
These standards ensure consistency, discoverability, and backward compatibility across Northlane's internal and external APIs.

## Naming Conventions
- Use plural nouns for resource collections: `/customers`, not `/customer`
- Use kebab-case for multi-word path segments: `/billing-accounts`
- Avoid verbs in URLs; represent actions through HTTP methods (GET, POST, PATCH, DELETE)

## Versioning
All public APIs must be versioned via the URL path (e.g., `/v2/customers`). Breaking changes require a new major version. Non-breaking additions (new optional fields, new endpoints) may be introduced within the current version.

## Backward Compatibility
A field may not be removed or have its type changed within a major version. Deprecated fields must remain functional for at least 6 months after a deprecation notice is published, and must be marked with a `deprecated: true` flag in the OpenAPI spec.

## Error Handling
All error responses must follow the standard error envelope:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Human-readable description",
    "request_id": "uuid"
  }
}
```
Error codes must be documented in the API reference and stable across releases; the underlying message text may change without notice.

## Authentication
Internal service-to-service APIs use mutual TLS or signed service tokens. External-facing APIs use OAuth 2.0 with scoped access tokens. API keys alone are not sufficient authentication for any endpoint returning customer data.

## Rate Limiting
Public APIs enforce rate limits per API key, returned via `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers. Default limits are 100 requests/minute for standard tier and 1,000 requests/minute for enterprise tier, unless otherwise negotiated in a customer's contract.

## Pagination
List endpoints must support cursor-based pagination using `page_token` and `page_size` query parameters, rather than offset-based pagination, to ensure stable results under concurrent writes.

## Documentation Requirements
Every public endpoint must have an OpenAPI 3.0 definition, at least one example request/response pair, and a changelog entry for any modification.

## Policy Owner
Principal Engineer, API Platform Team
