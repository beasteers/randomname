import difflib
import fnmatch



def get_similarity_scores(query, candidates, cutoff, sep='/', skew=0.1):
    result = []
    qparts = query.split(sep)
    sm = [difflib.SequenceMatcher(b=q) for q in qparts]
    for candidate in candidates:
        cparts = candidate.split(sep)
        total = 0
        for s, q in zip(sm, qparts):
            sc = max(
               (1+i*skew) * _get_score(s, q, w, cutoff) 
               for i, w in enumerate(cparts))
            total += sc
        result.append(total)
    return result

def _get_score(sm, a, b, cutoff, start_bias=0.5):
    sm.set_seqs(a, b)
    if '*' in a:
        return 1 if fnmatch.fnmatch(b, a) else -1000
    if a == b:
        return 1
    if b.startswith(a):
        return start_bias + (len(a)/len(b)) * (1 - start_bias)
    if (sm.real_quick_ratio() >= cutoff and 
        sm.quick_ratio() >= cutoff and 
        sm.ratio() >= cutoff):
            return sm.ratio()
    if a in b:
        return len(a) / len(b)
    return 0

def _get_top_similarity_matches(similarity, candidates, n=5, dropoff=0.0, return_scores=False):
    top = sorted(zip(similarity, candidates), reverse=True, key=lambda x: x[0])[:n]
    score_cutoff = (top[0][0] if top else 0) * dropoff
    return [
        (score, w)  if return_scores else w
        for score, w in top
        if score and score >= score_cutoff
    ]

def close_matches(query, candidates, cutoff=0.55, n=5, dropoff=0.5, return_scores=False):
    similarity = get_similarity_scores(query, candidates, cutoff)
    # print(similarity)
    return _get_top_similarity_matches(similarity, candidates, n, dropoff, return_scores)
