# PointSite Canary

- Public, static, read-only Canary destination for Builder Issue #70.
- Builder Canary publishes through pointsite-staging-canary into this repository only.
- Content publication and rollback must be initiated by an authenticated Administrator in Builder Canary. Maintainer changes never imply content approval.
- Bootstrap is a one-time deployment of the reviewed public baseline; remove its workflow after verified deployment.
- Never write to pointsite, copy private drafts or credentials, or accept executable files from publication inputs.
- Runtime callers must pin reviewed immutable code from PointCommunity/pointsite-staging. Preserve destination-specific OIDC identity, expected bases, output manifests, and release evidence.
