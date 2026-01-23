# SEMANTIC EQUIVALENCE ANALYSIS: LLM vs Ground-Truth SPARQL Queries

## Query Comparison

### Ground-Truth Query
```sparql
PREFIX schema: <http://schema.org/>
PREFIX sc: <https://w3id.org/secure-chain/>
SELECT ?version ?cve
WHERE {
  ?lib schema:name "ffmpeg" .
  ?lib sc:hasSoftwareVersion ?version .
  ?version a sc:SoftwareVersion .
  ?version sc:vulnerableTo ?cve .
}
```

### LLM-Generated Query
```sparql
PREFIX sc: <https://w3id.org/secure-chain/>
PREFIX schema: <http://schema.org/>

SELECT DISTINCT ?version ?vulnerability
WHERE {
  ?software a sc:Software ;
            schema:name ?name .
  
  FILTER(LCASE(?name) = "ffmpeg")
  
  ?software sc:hasSoftwareVersion ?softwareVersion .
  ?softwareVersion sc:versionName ?version .
  ?softwareVersion sc:vulnerableTo ?vuln .
  ?vuln schema:identifier ?vulnerability .
}
ORDER BY ?version ?vulnerability
```

---

## SEMANTIC EQUIVALENCE ASSESSMENT

**VERDICT: NOT SEMANTICALLY EQUIVALENT**

While the queries return the same results on the current dataset, they are **structurally different** and could diverge under certain conditions.

---

## DETAILED STRUCTURAL DIFFERENCES

### 1. Variable Binding Strategy

**Ground-Truth:**
- Returns URIs directly: `?version` and `?cve` are bound to resources
- Output: URIs (e.g., `https://conan.io/center/recipes/ffmpeg?version=4.2.1`)

**LLM Query:**
- Returns literal properties: `?version` and `?vulnerability` are bound to string literals
- Navigates through additional properties: `sc:versionName` and `schema:identifier`
- Output: String literals (e.g., `"4.2.1"`, `"CVE-2020-20891"`)

**Semantic Impact:** These are **fundamentally different query patterns**. One returns resources, the other returns literals extracted from those resources.

---

### 2. Name Matching Strategy

**Ground-Truth:**
```sparql
?lib schema:name "ffmpeg" .
```
- Exact string match (case-sensitive)
- Matches only `"ffmpeg"` (lowercase)

**LLM Query:**
```sparql
?software a sc:Software ;
          schema:name ?name .
FILTER(LCASE(?name) = "ffmpeg")
```
- Case-insensitive matching via `LCASE()` function
- Matches `"ffmpeg"`, `"FFmpeg"`, `"FFMPEG"`, `"FfMpEg"`, etc.

**Semantic Impact:** LLM query is **more permissive**. This could lead to different results if:
- Software names have inconsistent capitalization in the KG
- Multiple software packages exist with case variations

---

### 3. Type Constraint

**Ground-Truth:**
```sparql
?version a sc:SoftwareVersion .
```
- Explicitly requires the version to be typed as `sc:SoftwareVersion`

**LLM Query:**
```sparql
?software a sc:Software ;
```
- Type constraint on the SOFTWARE, not the version
- No explicit type check on `?softwareVersion`

**Semantic Impact:** The LLM query **assumes** that anything returned by `sc:hasSoftwareVersion` is a `SoftwareVersion`, but doesn't verify it. This could cause:
- **False positives** if the KG contains improperly typed nodes
- **False negatives** if some SoftwareVersion nodes lack explicit typing but the ground-truth requires it

---

### 4. Additional Clauses

**LLM Query adds:**
- `DISTINCT` - removes duplicate bindings
- `ORDER BY` - sorts results

**Semantic Impact:** These are **presentation modifiers**, not semantic changes:
- `DISTINCT` only matters if duplicates exist
- `ORDER BY` changes row order, not content

---

## TRIPLE PATTERN COMPARISON

| Pattern | Ground-Truth | LLM Query | Equivalent? |
|---------|--------------|-----------|-------------|
| Software matching | `?lib schema:name "ffmpeg"` | `?software schema:name ?name` + `FILTER(LCASE(?name) = "ffmpeg")` | ❌ No (case sensitivity) |
| Software type | Implicit (via schema:name) | `?software a sc:Software` | ❌ Different (explicit vs implicit) |
| Has version | `?lib sc:hasSoftwareVersion ?version` | `?software sc:hasSoftwareVersion ?softwareVersion` | ✓ Yes (same pattern) |
| Version type | `?version a sc:SoftwareVersion` | None | ❌ No (missing constraint) |
| Version name | None | `?softwareVersion sc:versionName ?version` | ❌ No (additional navigation) |
| Vulnerable to | `?version sc:vulnerableTo ?cve` | `?softwareVersion sc:vulnerableTo ?vuln` | ✓ Yes (same pattern) |
| CVE identifier | None | `?vuln schema:identifier ?vulnerability` | ❌ No (additional navigation) |

---

## POTENTIAL EDGE CASES WHERE RESULTS COULD DIVERGE

### 1. Case Sensitivity in Software Names
**Scenario:** KG contains both `"ffmpeg"` and `"FFmpeg"` as separate software entries

- **Ground-Truth:** Returns only `"ffmpeg"` matches
- **LLM Query:** Returns both `"ffmpeg"` AND `"FFmpeg"` matches
- **Result:** LLM could have **false positives**

### 2. Missing Type Assertions
**Scenario:** Some version nodes lack `rdf:type sc:SoftwareVersion` triple

- **Ground-Truth:** Filters out untyped versions
- **LLM Query:** Includes untyped versions (no type check)
- **Result:** LLM could have **false positives**

### 3. Missing Literal Properties
**Scenario:** A SoftwareVersion exists but lacks `sc:versionName` property

- **Ground-Truth:** Returns the version URI
- **LLM Query:** Filters out the version (no binding for `?version`)
- **Result:** LLM could have **false negatives**

### 4. Missing CVE Identifiers
**Scenario:** A Vulnerability node exists but lacks `schema:identifier` property

- **Ground-Truth:** Returns the vulnerability URI
- **LLM Query:** Filters out the vulnerability (no binding for `?vulnerability`)
- **Result:** LLM could have **false negatives**

### 5. Multiple Version Names or Identifiers
**Scenario:** A SoftwareVersion has multiple `sc:versionName` values (e.g., `"4.2.1"` and `"4.2.1-stable"`)

- **Ground-Truth:** Returns 1 row per vulnerability
- **LLM Query:** Returns 2 rows per vulnerability (Cartesian product)
- **Result:** LLM could have **duplicate rows** (mitigated by `DISTINCT`)

### 6. Non-Software Entities Named "ffmpeg"
**Scenario:** KG contains a Hardware component named "ffmpeg"

- **Ground-Truth:** Could potentially match (no type constraint on `?lib`)
- **LLM Query:** Filters out non-Software (requires `?software a sc:Software`)
- **Result:** Ground-truth could have **false positives**

---

## SUMMARY OF RISKS

### False Positive Risks (LLM returns extra results)
1. ✓ **Case variations** in software names (`"FFmpeg"` vs `"ffmpeg"`)
2. ✓ **Untyped version nodes** missing `rdf:type sc:SoftwareVersion`
3. ✓ **Multiple literal values** for versionName or identifier (mitigated by DISTINCT)

### False Negative Risks (LLM misses valid results)
1. ✓ **Missing versionName property** on SoftwareVersion nodes
2. ✓ **Missing identifier property** on Vulnerability nodes
3. ⚠️ **Case-sensitive "ffmpeg"** in ground-truth could miss legitimate matches

### Data Quality Assumptions
- LLM query assumes **all relevant data exists as literal properties**
- Ground-truth assumes **all version nodes are properly typed**
- Both assume **consistent property usage** across the KG

---

## CONCLUSION

**Semantic Equivalence: NO**

The queries are **NOT semantically equivalent** because:

1. **Different output types**: URIs vs literals
2. **Different matching strategies**: Case-sensitive vs case-insensitive
3. **Different constraints**: Explicit type checking vs property navigation
4. **Different failure modes**: Missing types vs missing literals

**Why they return identical results on THIS dataset:**
- The SecureChainKG appears to be well-structured with:
  - Consistent lowercase "ffmpeg" naming
  - Proper type assertions on all version nodes
  - Complete literal properties (versionName, identifier) on all relevant nodes
  
**Critical difference:**
The ground-truth query is more **robust to missing literal properties** (can return URIs even if identifiers are missing), while the LLM query is more **robust to missing type assertions** and **case inconsistencies**.

The LLM query makes stronger assumptions about data completeness but provides more user-friendly output.
