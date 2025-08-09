DECISION_RULES = [
    # === TIER 1: CRITICAL SAFETY RULES (Priority 1) ===    
    {
        "name": "drug_safety_critical",
        "condition": "query_type == 'drug_interactions' or criticality == 'critical'",
        "decision": "live_search",
        "priority": 1,
        "reasoning": "Safety-critical queries require latest information"
    },
    
    {
        "name": "emergency_override", 
        "condition": "case_type == 'emergency'",
        "decision": "cache_immediate_with_live_verification",
        "priority": 1,
        "reasoning": "Emergency: return cache immediately, verify in background"
    },
    
    # === TIER 2: FRESHNESS-CRITICAL RULES (Priority 2) ===
    {
        "name": "rare_condition_live",
        "condition": "has_rare_condition or query_type == 'rare_conditions'",
        "decision": "live_search", 
        "priority": 2,
        "reasoning": "Rare conditions not well-represented in cache"
    },
    
    {
        "name": "trials_freshness",
        "condition": "query_type == 'clinical_trials' and data_age_hours > 24",
        "decision": "live_search",
        "priority": 2,
        "reasoning": "Clinical trial enrollment changes daily"
    },
    
    {
        "name": "recent_keyword_trigger",
        "condition": "mentions_recent and confidence_score < 0.8",
        "decision": "live_search",
        "priority": 2,
        "reasoning": "Query explicitly requests recent information"
    },
    
    {
        "name": "literature_freshness", 
        "condition": "query_type == 'literature' and data_age_days > 7 and criticality in ['critical', 'treatment']",
        "decision": "live_search",
        "priority": 2,
        "reasoning": "Treatment decisions need recent literature"
    },
    
    # === TIER 3: BALANCED RULES (Priority 3) ===
    {
        "name": "guidelines_cache",
        "condition": "query_type == 'guidelines' and data_age_days <= 30 and confidence_score >= 0.7",
        "decision": "use_cache",
        "priority": 3,
        "reasoning": "Guidelines updated monthly/quarterly, cache acceptable"
    },
    
    {
        "name": "drug_labels_cache",
        "condition": "query_type == 'drug_labels' and data_age_days <= 90 and confidence_score >= 0.8",
        "decision": "use_cache",
        "priority": 3,
        "reasoning": "Drug labels change rarely, cache acceptable for 90 days"
    },
    
    {
        "name": "parallel_strategy",
        "condition": "confidence_score >= 0.6 and confidence_score < 0.8 and criticality == 'treatment'", 
        "decision": "parallel_search",
        "priority": 3,
        "reasoning": "Medium confidence - use cache immediately, verify with live search"
    },
    
    {
        "name": "literature_cache_ok",
        "condition": "query_type == 'literature' and data_age_days <= 7 and confidence_score >= 0.8 and criticality == 'background'",
        "decision": "use_cache",
        "priority": 3,
        "reasoning": "Recent literature cache acceptable for background research"
    },
    
    # === TIER 4: CONFIDENCE-BASED RULES (Priority 4) ===
    {
        "name": "high_confidence_cache",
        "condition": "confidence_score >= 0.8 and data_age_days <= 7 and criticality == 'background'",
        "decision": "use_cache",
        "priority": 4,
        "reasoning": "High confidence recent data for background research"
    },
    
    {
        "name": "low_confidence_live",
        "condition": "confidence_score < 0.5",
        "decision": "live_search", 
        "priority": 4,
        "reasoning": "Low confidence cached data, need verification"
    },
    
    {
        "name": "medium_confidence_treatment",
        "condition": "confidence_score >= 0.5 and confidence_score < 0.7 and criticality == 'treatment'",
        "decision": "hybrid_search",
        "priority": 4,
        "reasoning": "Medium confidence for treatment - check cache then live if needed"
    },
    
    # === TIER 5: COST MANAGEMENT RULES (Priority 5) ===
    {
        "name": "quota_exceeded_fallback",
        "condition": "daily_quota_exceeded and confidence_score >= 0.6",
        "decision": "use_cache_with_warning",
        "priority": 5,
        "reasoning": "API quota exceeded, using cached data with confidence warning"
    },
    
    {
        "name": "cost_optimization_background",
        "condition": "criticality == 'background' and confidence_score >= 0.6 and data_age_days <= 14",
        "decision": "use_cache",
        "priority": 5,
        "reasoning": "Cost optimization: cached data sufficient for background research"
    },
    
    # === TIER 6: SPECIAL CASE RULES (Priority 6) ===
    {
        "name": "multiple_medications_safety",
        "condition": "len(medications) > 5 and query_type in ['drug_interactions', 'drug_labels']",
        "decision": "live_search",
        "priority": 2,  # High priority for safety
        "reasoning": "Complex medication regimen requires current interaction data"
    },
    
    {
        "name": "previous_treatment_resistance",
        "condition": "'resistance' in keywords and criticality == 'treatment'",
        "decision": "live_search",
        "priority": 2,
        "reasoning": "Treatment resistance requires latest research and protocols"
    },
    
    {
        "name": "clinical_trial_specific",
        "condition": "query_type == 'clinical_trials' and 'recruiting' in keywords",
        "decision": "live_search",
        "priority": 2,
        "reasoning": "Active trial recruitment status changes frequently"
    }
]
