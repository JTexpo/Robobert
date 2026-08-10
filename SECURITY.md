# Security Policy

## Reporting a Security Vulnerability

If you discover a security vulnerability in Robobert, please report it
responsibly rather than publicly disclosing the vulnerability before it can be
addressed.

Security issues may include:

* Exposure of Discord bot tokens or other credentials.
* Unauthorized access to systems or services.
* Authentication or authorization bypasses.
* Vulnerabilities that allow arbitrary code execution.
* Vulnerabilities that expose private user or server information.
* Abuse of Robobert's infrastructure or third-party services.
* Other vulnerabilities that could compromise the security of Robobert or its users.

## How to Report

Please report security vulnerabilities through the project's private security
reporting channel or directly to the project maintainer.

If GitHub Security Advisories are enabled for this repository, please use the
repository's **Security → Advisories** section to submit a private report.

When reporting a vulnerability, please include:

1. A description of the vulnerability.
2. Steps required to reproduce the issue.
3. The potential impact.
4. Any relevant logs, screenshots, or proof-of-concept information.
5. A suggested mitigation, if one is known.

Please avoid including passwords, authentication tokens, personal information,
or other sensitive data in your report.

## Responsible Disclosure

Please allow reasonable time for the maintainers to investigate and address
the issue before publicly disclosing the vulnerability.

We appreciate responsible security research and will make a reasonable effort
to acknowledge valid security reports.

## Secrets

Never commit any of the following to the repository:

* Discord bot tokens.
* API keys.
* Passwords.
* OAuth credentials.
* Private keys.
* `.env` files containing secrets.
* Production configuration containing sensitive credentials.

If a secret is accidentally committed, assume that it has been compromised and
rotate or revoke it immediately.

## Scope

This security policy applies to the Robobert source code and infrastructure
controlled by the project.

Vulnerabilities in Discord or other third-party services should be reported
to the appropriate service provider.
