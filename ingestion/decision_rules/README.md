# Decision Rules System

## Overview

A rule-based engine that determines when to use cached clinical data versus performing live searches. Balances patient safety, performance, and cost by intelligently choosing search strategies.

## Rule Structure

Each rule is a dictionary with:

```python
{
    "name": "rule_identifier",
    "condition": "boolean_expression",
    "decision": "action",
    "priority": 1-6,
    "reasoning": "explanation"
}
```

## Decision Types

| Decision | Description |
|----------|-------------|
| `live_search` | Fresh search from external sources |
| `use_cache` | Use existing cached data |
| `parallel_search` | Use cache immediately, verify with live search |
| `hybrid_search` | Check cache first, then live if needed |
| `cache_immediate_with_live_verification` | Return cache immediately, verify in background |
| `use_cache_with_warning` | Use cache with staleness warning |

## Rule Tiers

### Tier 1: Critical Safety (Priority 1)
- **drug_safety_critical**: Live search for drug interactions or critical queries
- **emergency_override**: Emergency cases get immediate cache with background verification

### Tier 2: Freshness-Critical (Priority 2)
- **rare_condition_live**: Live search for rare conditions
- **trials_freshness**: Live search if clinical trial data > 24 hours old
- **recent_keyword_trigger**: Live search when query mentions "recent" with low confidence
- **literature_freshness**: Live search for literature > 7 days old in critical/treatment cases
- **multiple_medications_safety**: Live search for complex medication regimens (>5 meds)
- **previous_treatment_resistance**: Live search for treatment resistance queries
- **clinical_trial_specific**: Live search for recruiting trial status

### Tier 3: Balanced (Priority 3)
- **guidelines_cache**: Use cache for guidelines ≤30 days old with high confidence
- **drug_labels_cache**: Use cache for drug labels ≤90 days old with high confidence
- **parallel_strategy**: Parallel search for medium confidence treatment queries
- **literature_cache_ok**: Use cache for recent literature in background research

### Tier 4: Confidence-Based (Priority 4)
- **high_confidence_cache**: Use cache for high confidence recent background data
- **low_confidence_live**: Live search for low confidence data (<0.5)
- **medium_confidence_treatment**: Hybrid search for medium confidence treatment queries

### Tier 5: Cost Management (Priority 5)
- **quota_exceeded_fallback**: Use cache with warning when quota exceeded
- **cost_optimization_background**: Use cache for background research to save costs

## Key Variables

- `query_type`: drug_interactions, clinical_trials, literature, guidelines, drug_labels, rare_conditions
- `criticality`: critical, treatment, background
- `confidence_score`: 0.0-1.0 reliability measure
- `data_age_hours/days`: Time since last update
- `case_type`: emergency, routine, follow-up
- `has_rare_condition`: Boolean for rare conditions
- `mentions_recent`: Boolean for "recent" keywords
- `daily_quota_exceeded`: Boolean for API limits
- `medications`: List of patient medications
- `keywords`: Query keywords

## Usage

```python
from ingestion.decision_rules.decision_rules import DECISION_RULES

def evaluate_rules(context):
    for rule in sorted(DECISION_RULES, key=lambda x: x['priority']):
        if eval(rule['condition'], {}, context):
            return rule['decision']
    return 'use_cache'  # Default fallback
```

## Example Context

```python
context = {
    'query_type': 'drug_interactions',
    'criticality': 'critical',
    'confidence_score': 0.7,
    'data_age_hours': 12,
    'case_type': 'routine',
    'has_rare_condition': False,
    'daily_quota_exceeded': False,
    'mentions_recent': False,
    'medications': ['aspirin', 'warfarin'],
    'keywords': ['interaction']
}
```

## Rule Evaluation

1. Rules evaluated in priority order (1=highest)
2. First matching rule determines decision
3. Default to `use_cache` if no rules match
