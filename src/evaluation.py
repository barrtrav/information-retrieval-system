def precision_score(relevant, recovered) -> float:
    rr = [doc for doc in recovered if doc in relevant]
    return len(rr) / len(recovered)

def recall_score(relevant, recovered) -> float:
    rr = [doc for doc in recovered if doc in relevant]
    return len(rr) / len(relevant)

def fbeta_score(relevant, recovered, beta: float) -> float:
    p = precision_score(relevant, recovered)
    r = recall_score(relevant, recovered)
    try:
        return (1 + beta ** 2) / (1 / p + (beta ** 2) / r)
    except ZeroDivisionError:
        return 0

def f1_score(relevant, recovered) -> float:
    return fbeta_score(relevant, recovered, 1)

def fallout(relevant, recovered, total: int) -> float:
    ri = [d for d in recovered if d not in relevant]
    irrelevant = total - len(relevant)
    return len(ri) / irrelevant

def r_precision_score(r: int, relevant, recovered) -> float:
    return precision_score(relevant, recovered[:r])

def r_recall_score(r: int, relevant, recovered) -> float:
    return recall_score(relevant, recovered[:r])

def r_f1_score(r: int, relevant, recovered) -> float:
    return f1_score(relevant, recovered[:r])

def r_fallout_score(r: int, relevant, recovered, total: int) -> float:
    return fallout(relevant, recovered[:r], total)