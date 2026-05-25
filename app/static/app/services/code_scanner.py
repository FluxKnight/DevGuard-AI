import re
from typing import List, Dict, Any


class CodeScanner:
    def __init__(self):
        self.rules = [
            {
                "title": "Hardcoded password detected",
                "category": "Secrets",
                "severity": "HIGH",
                "pattern": r"(?i)\b(password|passwd|pwd|admin_pass)\b\s*=\s*[\"'][^\"']{3,}[\"']",
                "explanation": "This code appears to contain a password directly inside the source file.",
                "recommendation": "Move passwords into environment variables or a secure secrets manager."
            },
            {
                "title": "Possible API key or token detected",
                "category": "Secrets",
                "severity": "HIGH",
                "pattern": r"(?i)\b(api_key|apikey|token|secret|client_secret)\b\s*=\s*[\"'][^\"']{8,}[\"']",
                "explanation": "This code may contain an API key, token, or secret value.",
                "recommendation": "Do not commit secrets to source code. Use .env files locally and secret storage in production."
            },
            {
                "title": "Weak password value detected",
                "category": "Weak Credentials",
                "severity": "MEDIUM",
                "pattern": r"(?i)(admin123|password123|123456|qwerty|letmein)",
                "explanation": "This code contains a weak or commonly guessed password.",
                "recommendation": "Use strong, randomly generated passwords and never store them directly in code."
            },
            {
                "title": "Possible SQL injection risk",
                "category": "Injection",
                "severity": "CRITICAL",
                "pattern": r"(?i)(select|insert|update|delete).*(\+|%|format\(|f[\"'])",
                "explanation": "This SQL query appears to be built using string concatenation or interpolation.",
                "recommendation": "Use parameterized queries or an ORM query builder instead of directly inserting user input."
            },
            {
                "title": "Debug mode enabled",
                "category": "Configuration",
                "severity": "MEDIUM",
                "pattern": r"(?i)\b(debug|app_debug)\b\s*=\s*(True|true|1)",
                "explanation": "Debug mode appears to be enabled. This can expose sensitive error messages.",
                "recommendation": "Disable debug mode in production environments."
            },
            {
                "title": "Environment file reference detected",
                "category": "Configuration",
                "severity": "LOW",
                "pattern": r"(?i)(\.env|\.env\.local)",
                "explanation": "The code references an environment file. This may be normal, but environment files must not be exposed or committed.",
                "recommendation": "Add .env files to .gitignore and keep example values in .env.example."
            },
            {
                "title": "Unsafe shell execution detected",
                "category": "Command Execution",
                "severity": "HIGH",
                "pattern": r"(?i)(os\.system|subprocess\.call|subprocess\.run).*(shell\s*=\s*True)?",
                "explanation": "This code uses shell execution. If user input reaches this call, it may become command injection.",
                "recommendation": "Avoid shell=True and pass arguments as a list. Validate and sanitize external input."
            },
            {
                "title": "Insecure hash algorithm detected",
                "category": "Cryptography",
                "severity": "MEDIUM",
                "pattern": r"(?i)\b(md5|sha1)\s*\(",
                "explanation": "MD5 and SHA1 are weak for security-sensitive hashing.",
                "recommendation": "Use SHA-256 or stronger algorithms. For passwords, use bcrypt, Argon2, or PBKDF2."
            }
        ]

    def scan(self, code: str) -> List[Dict[str, Any]]:
        findings = []
        lines = code.splitlines()

        for line_number, line in enumerate(lines, start=1):
            for rule in self.rules:
                match = re.search(rule["pattern"], line)
                if match:
                    findings.append({
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "line": line_number,
                        "category": rule["category"],
                        "explanation": rule["explanation"],
                        "recommendation": rule["recommendation"],
                        "matched_text": match.group(0)
                    })

        return findings
