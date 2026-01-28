from __future__ import annotations
import re
from typing import Optional

"""
Email validation utilities.

This module provides lightweight validation without external dependencies.
It is intentionally conservative (may reject some rare valid RFC addresses).
"""



_MAX_EMAIL_LENGTH = 254
_MAX_LOCAL_LENGTH = 64

# Local-part: dot-atom only (no quoted strings)
_LOCAL_PART_RE = re.compile(r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*$")

# Domain labels: letters/digits/hyphen, no leading/trailing hyphen, 1..63 chars
_DOMAIN_LABEL_RE = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")


def normalize_email(email: str) -> Optional[str]:
    """
    Normalize an email address for storage/comparison.

    - Strips surrounding whitespace
    - Lowercases the domain part
    - Returns None if the email is invalid
    """
    if not isinstance(email, str):
        return None

    candidate = email.strip()
    if not is_valid_email(candidate):
        return None

    local, domain = candidate.rsplit("@", 1)
    return f"{local}@{domain.lower()}"


def is_valid_email(email: str) -> bool:
    """
    Return True if `email` looks like a valid email address.

    Notes:
    - Supports common dot-atom local parts (no quoted local parts)
    - Supports ASCII domains and punycode (xn--...) domains
    """
    if not isinstance(email, str):
        return False

    email = email.strip()
    if not email or len(email) > _MAX_EMAIL_LENGTH:
        return False

    if " " in email or "\t" in email or "\n" in email or "\r" in email:
        return False

    if email.count("@") != 1:
        return False

    local, domain = email.rsplit("@", 1)
    if not local or not domain:
        return False

    if len(local) > _MAX_LOCAL_LENGTH:
        return False

    # Local-part checks
    if local[0] == "." or local[-1] == "." or ".." in local:
        return False
    if not _LOCAL_PART_RE.match(local):
        return False

    # Domain checks
    if domain.endswith(".") or domain.startswith(".") or ".." in domain:
        return False

    # Require at least one dot (e.g., example.com)
    if "." not in domain:
        return False

    labels = domain.split(".")
    if any(not lbl for lbl in labels):
        return False

    if not all(_DOMAIN_LABEL_RE.match(lbl) for lbl in labels):
        return False

    tld = labels[-1]
    if len(tld) < 2:
        return False

    return True


__all__ = ["is_valid_email", "normalize_email"]