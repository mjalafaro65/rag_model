# Deployment Process
**Northlane Systems — Engineering**
**Effective Date:** January 2026
**Document ID:** ENG-STD-008

## Purpose
This document describes the standard process for deploying changes to staging and production environments.

## Environments
- **Local:** Developer machines, no shared state
- **Staging:** Mirrors production configuration, used for integration testing and QA sign-off
- **Production:** Live customer-facing environment

Changes must pass through staging before reaching production, except for approved emergency hotfixes (see Emergency Deployment Procedure below).

## Standard Deployment Flow
1. Merge PR to `main` after required approvals (see Code Review Guidelines, ENG-STD-003)
2. Automated CI pipeline builds and runs the full test suite
3. On success, the change is automatically deployed to Staging
4. QA and/or the feature owner verify behavior in Staging
5. A release engineer promotes the build to Production during an approved deployment window

## Deployment Windows
Standard production deployments occur Monday–Thursday, 10:00 AM–4:00 PM in the primary engineering time zone, to ensure adequate staffing for monitoring. Deployments are not scheduled on Fridays, weekends, or the day before major holidays, except for critical security patches.

## Feature Flags
New features affecting customer-facing behavior should be released behind a feature flag, enabling gradual rollout (canary) to a percentage of traffic before full release. Flags should be removed within 90 days of full rollout to avoid flag debt.

## Rollback Procedure
Every deployment must have a documented rollback plan. Automated rollback is triggered if error rates exceed 2x baseline within 10 minutes of deployment, or if key business metrics (checkout success rate, login success rate) drop below defined thresholds. Manual rollback can be triggered by any on-call engineer via the deployment dashboard.

## Emergency Deployment Procedure
Critical security patches or SEV-1 incident fixes (see Security Incident Response Policy, IT-SEC-009) may bypass the standard deployment window with sign-off from an engineering director or the on-call incident commander. Emergency deployments still require passing CI and at least one reviewer approval.

## Post-Deployment Monitoring
Release engineers monitor key dashboards for at least 30 minutes following a production deployment before considering it fully complete.

## Policy Owner
Director of Platform Engineering, Northlane Systems
