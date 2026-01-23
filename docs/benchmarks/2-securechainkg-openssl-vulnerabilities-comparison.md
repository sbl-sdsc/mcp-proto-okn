# Systematic Comparison: LLM Query vs Ground-Truth Query

## Executive Summary

The LLM-generated query achieved **98.52% F1 score** compared to the ground-truth query, demonstrating high accuracy with minor discrepancies primarily due to URI encoding differences and a small number of incorrectly included vulnerable versions.

---

## 1. Summary Table

| Metric | Count | Percentage |
|--------|-------|------------|
| **Ground-truth records** | 235 | 100% |
| **LLM records** | 238 | - |
| **Intersection size** | 233 | - |
| **False positives** | 5 | 2.10% |
| **False negatives** | 2 | 0.85% |
| **Precision** | - | 97.90% |
| **Recall** | - | 99.15% |
| **F1 Score** | - | **98.52%** |

**Result Classification:** Partially Overlapping (High Overlap)

---

## 2. Discrepancy Details

### False Positives (5 records)
Versions in LLM results but NOT in ground truth:

1. **`1.0.2o`** - Status: Unknown (not in vulnerable list check)
2. **`1.1.1g`** - Status: **VULNERABLE** (confirmed via query)
3. **`1.1.1k",override=True`** - Status: URL encoding difference
4. **`1.1.1l`** - Status: **VULNERABLE** (confirmed via query)
5. **`1.1.1s",override=True`** - Status: URL encoding difference

### False Negatives (2 records)
Versions in ground truth but NOT in LLM results:

1. **`1.1.1k",override%3DTrue`** - URL-encoded version of `1.1.1k",override=True`
2. **`1.1.1s",override%3DTrue`** - URL-encoded version of `1.1.1s",override=True`

---

## 3. Root Cause Analysis

### Issue 1: URI vs Literal Value Handling ⚠️

**Description:** The ground-truth query returns URI resources directly, while the LLM query extracted literal values from the `versionName` property.

**Impact:** 
- Creates string representation differences
- URL-encoded strings (`%3D`) vs decoded strings (`=`)
- Affects 2 versions: `1.1.1k",override=True` and `1.1.1s",override=True`

**Technical Detail:**
```sparql
# Ground truth returns:
?version  # URI like https://www.google.com/search?q=openssl+1.1.1k%22%2Coverride%3DTrue

# LLM query returns:
?sv secchain:versionName ?version  # Literal: "1.1.1k",override=True"
```

### Issue 2: Incorrect Inclusion of Vulnerable Versions ❌

**Description:** The LLM query incorrectly included 2 versions that ARE vulnerable to CVE-2023-3817.

**Affected Versions:**
- `1.1.1g` - Confirmed VULNERABLE
- `1.1.1l` - Confirmed VULNERABLE

**Root Cause:** The LLM query used different namespace prefixes and property paths:
```sparql
# LLM approach:
?software sc:name ?softwareName .
FILTER(?softwareName = "openssl" || ?softwareName = "OpenSSL")
?software secchain:hasSoftwareVersion ?sv .
?sv secchain:versionName ?version .

# Ground truth approach:
?lib schema:name "openssl" .
?lib sc:hasSoftwareVersion ?version .
?version a sc:SoftwareVersion .  # Type constraint
```

**Key Difference:** The ground truth query includes an explicit type constraint (`?version a sc:SoftwareVersion`), which may filter results differently based on the RDF graph structure.

### Issue 3: Software Name Matching Breadth 📊

**Description:** The LLM query matched both "openssl" and "OpenSSL" (case-insensitive matching), while the ground truth matched only lowercase "openssl".

**Impact:** Potentially included versions from different software entities that happen to be named "OpenSSL" with capital letters.

---

## 4. Corrected Analysis

### Actual Discrepancies When Accounting for URL Encoding:

If we normalize URL encoding, the true false positives are:
1. `1.0.2o` (possibly vulnerable, unverified)
2. `1.1.1g` (CONFIRMED vulnerable)
3. `1.1.1l` (CONFIRMED vulnerable)

The URL encoding differences for `1.1.1k` and `1.1.1s` variants are **not semantic differences** but rather string representation artifacts.

### Corrected Metrics (Semantic Comparison):

| Metric | Count | Percentage |
|--------|-------|------------|
| **Semantic false positives** | 3 | 1.26% |
| **Semantic false negatives** | 0 | 0.00% |
| **Effective Precision** | - | 98.74% |
| **Effective Recall** | - | 100.00% |
| **Effective F1 Score** | - | **99.36%** |

---

## 5. Query Comparison

### Ground-Truth Query Approach:
✅ Returns URI resources directly  
✅ Uses explicit type constraints (`a sc:SoftwareVersion`)  
✅ Exact string matching for software name  
✅ More precise filtering  

### LLM-Generated Query Approach:
⚠️ Extracts literal property values  
⚠️ Uses property path to version name  
⚠️ Case-flexible matching (openssl OR OpenSSL)  
❌ Missing some implicit constraints  

---

## 6. Final Verdict

### PARTIAL PASS ⚠️

**Justification:**
- The LLM query achieved excellent coverage (99.15% recall)
- High precision (97.90%) with only minor errors
- The main issues are:
  1. **Critical:** Incorrectly included 2 confirmed vulnerable versions (1.1.1g, 1.1.1l)
  2. **Minor:** URL encoding representation differences (semantically equivalent)
  3. **Unverified:** One version (1.0.2o) needs verification

**Why Not PASS:**
- Including vulnerable versions in a "non-vulnerable" list is a **security-critical error**
- Even though the error rate is small (2 out of 238), the nature of the error is significant

**Why Not FAIL:**
- 98.52% F1 score indicates very high overall accuracy
- The query successfully identified 233 out of 235 correct versions
- The logic was sound, with only minor implementation differences

### Recommendations for Improvement:

1. **Add explicit type constraint:** `?version a sc:SoftwareVersion`
2. **Use exact software name matching:** Use only lowercase "openssl"
3. **Return URIs instead of literals** if consistency with ground truth is required
4. **Validate results** against known vulnerable versions before finalizing

---

## 7. Conclusion

The LLM-generated query demonstrated strong capability in querying the knowledge graph, achieving near-perfect recall and high precision. The discrepancies were primarily due to:
- URI vs literal value extraction methodology
- Minor differences in filtering constraints
- String encoding representation differences

With minor adjustments to match the ground-truth query structure more closely, the LLM approach could achieve 100% accuracy.
