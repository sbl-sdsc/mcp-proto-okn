# OpenSSL CVE-2023-3817 Vulnerability Analysis

👤 **User**  
@securechainkg: Which versions of openssl no longer have the CVE-2023-3817 vulnerability?

---

🧠 **Assistant**  
Based on the SecureChain KG knowledge graph data, here are the OpenSSL versions and their relationship to **CVE-2023-3817**:

## Versions **VULNERABLE** to CVE-2023-3817:

**OpenSSL 1.0.2 series:**
- 1.0.2l-1~bpo8+1
- 1.0.2s, 1.0.2t, 1.0.2u

**OpenSSL 1.1.1 series:**
- 1.1.1c through 1.1.1w (all releases in this series)
- This includes: 1.1.1c, 1.1.1d, 1.1.1e, 1.1.1f, 1.1.1g, 1.1.1h, 1.1.1i, 1.1.1j, 1.1.1k, 1.1.1l, 1.1.1m, 1.1.1n, 1.1.1o, 1.1.1p, 1.1.1q, 1.1.1s, 1.1.1t, 1.1.1u, 1.1.1v, 1.1.1w

## Versions **NOT VULNERABLE** to CVE-2023-3817:

**OpenSSL 3.x series:**
- All OpenSSL 3.0.x versions (3.0.0 through 3.0.14)
- All OpenSSL 3.1.x versions (3.1.0 through 3.1.6)
- All OpenSSL 3.2.x versions (3.2.0 through 3.2.2)
- All OpenSSL 3.3.x versions (3.3.1)

**Earlier versions:**
- All versions prior to 1.0.2l appear to be unaffected according to the data

## Summary:
If you want to avoid CVE-2023-3817, you should upgrade to **OpenSSL 3.0 or later**. The entire OpenSSL 3.x series is not vulnerable to this CVE. The vulnerability primarily affects the 1.1.1 series and some late 1.0.2 versions.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.5.0 on 2026-01-17*

*Model: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)*
