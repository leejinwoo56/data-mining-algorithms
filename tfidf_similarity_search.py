
import sys, re, math, numpy as np
from time import time

def normalize_keep_alpha_space(s: str) -> str:
    """소문자화 + 알파벳과 공백만 유지"""
    return re.sub(r'[^a-z ]', '', s.lower())

def main():
    if len(sys.argv) != 2:
        print("Usage: python hw1_3_c.py <path_to_articles.txt>")
        sys.exit(1)

    path = sys.argv[1]
    start = time()
    np.random.seed(0)   # 랜덤 시드 고정

    doc_ids, docs_tokens = [], []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            toks = line.split(None, 1)
            doc_id, text = toks[0], toks[1] if len(toks) > 1 else ""
            text = normalize_keep_alpha_space(text)
            tokens = [t for t in text.split(' ') if t]
            if not tokens: 
                continue
            doc_ids.append(doc_id)
            docs_tokens.append(tokens)

    D = len(doc_ids)
    if D == 0:
        print("# No valid documents after preprocessing.")
        return
    all_terms = sorted(set(t for toks in docs_tokens for t in toks))
    term_to_idx = {t: i for i, t in enumerate(all_terms)}
    V = len(all_terms)

    df = np.zeros(V, dtype=np.int32)
    tf_list = []
    for toks in docs_tokens:
        tf = {}
        seen = set()
        for w in toks:
            j = term_to_idx[w]
            tf[j] = tf.get(j, 0) + 1
            if j not in seen:
                df[j] += 1
                seen.add(j)
        tf_list.append(tf)

    idf = np.log(D / df)
    tfidf_list, norms = [], np.zeros(D)
    for i, tf in enumerate(tf_list):
        vec, ssum = {}, 0.0
        for j, tf_ij in tf.items():
            w = tf_ij * idf[j]
            vec[j] = w
            ssum += w * w
        tfidf_list.append(vec)
        norms[i] = math.sqrt(ssum) if ssum > 0 else 0.0
    K = 10
    R = np.random.randn(K, V)
    signatures = np.zeros((D, K), dtype=int)
    for d in range(D):
        accum = np.zeros(K)
        vec = tfidf_list[d]
        if vec and norms[d] > 0:
            for j, w in vec.items():
                accum += R[:, j] * w #R[:,j]는 그냥 10개의 값이 있는 ( 1차원 리스트) 
        signatures[d, :] = (accum >= 0).astype(int)

    buckets, candidate_pairs = {}, set()
    for i in range(D):
        key = tuple(signatures[i])
        buckets.setdefault(key, []).append(i)
    for bucket in buckets.values():
        if len(bucket) > 1:
            for i in range(len(bucket)):
                for j in range(i + 1, len(bucket)):
                    a, b = bucket[i], bucket[j]
                    candidate_pairs.add((min(a, b), max(a, b)))


    def cosine_sim(i, j):
        ni, nj = norms[i], norms[j]
        if ni == 0 or nj == 0: return 0.0
        vi, vj = tfidf_list[i], tfidf_list[j]
        if len(vi) < len(vj): small, large = vi, vj
        else: small, large = vj, vi
        dot = sum(w * large[k] for k, w in small.items() if k in large)
        return dot / (ni * nj)

    for i, j in sorted(candidate_pairs):
        sim = cosine_sim(i, j)
        if 1.0 - sim < 0.1:
            print(f"{doc_ids[i]}\t{doc_ids[j]}\t{sim:.6f}")

    #print(f"# Elapsed seconds: {time() - start:.3f}")

if __name__ == "__main__":
    main()
