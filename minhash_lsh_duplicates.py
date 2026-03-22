
import sys, re, math, numpy as np
from time import time


def normalize_keep_alpha_space(s: str) -> str:
    return re.sub(r'[^a-z ]', '', s.lower())

def shingles_k3(s: str) -> set[str]:
    
    return {s[i:i+3] for i in range(len(s)-2)} if len(s) >= 3 else set()

def next_prime_ge(n: int) -> int:
  
    def is_prime(x):
        if x < 2: return False
        if x % 2 == 0: return x == 2
        r = int(math.sqrt(x))
        for d in range(3, r+1, 2):
            if x % d == 0: return False
        return True
    p = n
    while not is_prime(p):
        p += 1
    return p


def main():
    if len(sys.argv) != 2:
        print("Usage: python hw1_3b.py <path_to_articles.txt>")
        sys.exit(1)

    path = sys.argv[1]
    start = time()

    np.random.seed(0)  

    doc_ids = []
    doc_shingles = []

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            toks = line.split(None, 1)  
            if len(toks) == 1:
                doc_id, text = toks[0], ""
            else:
                doc_id, text = toks[0], toks[1]

            text = normalize_keep_alpha_space(text)
            sh = shingles_k3(text)
            if not sh : 
                continue 
            doc_ids.append(doc_id)
            doc_shingles.append(sh)

   
    all_shingles = sorted(set().union(*doc_shingles))   
    shingle_to_idx = {s: i for i, s in enumerate(all_shingles)}
    n = len(all_shingles)
    c = next_prime_ge(n)

 
    b, r = 6, 20
    K = b * r 
    A = np.random.randint(1, c, size=K)
    B = np.random.randint(0, c, size=K)
    D = len(doc_ids)
    signatures = np.full((D, K), fill_value=np.inf)
    
    for d, shingles in enumerate(doc_shingles):
      
        idxs = [shingle_to_idx[s] for s in shingles if s in shingle_to_idx]
        for k in range(K):
            hvals = (A[k] * np.array(idxs) + B[k]) % c 
            signatures[d, k] = np.min(hvals) if len(hvals) > 0 else np.inf

    bands = []
    for band in range(b):
        start_col = band * r
        end_col = (band + 1) * r
        buckets = {}
        for i in range(D):
            key = tuple(signatures[i, start_col:end_col])
            buckets.setdefault(key, []).append(i)
        bands.append(buckets)

    candidate_pairs = set()
    for band_dict in bands:
        for bucket in band_dict.values():
            if len(bucket) > 1:
                for i in range(len(bucket)):
                    for j in range(i+1, len(bucket)):
                        candidate_pairs.add((min(bucket[i], bucket[j]),
                                             max(bucket[i], bucket[j])))


    for i, j in sorted(candidate_pairs):
        agree = np.sum(signatures[i] == signatures[j])
        sim = agree / K
        if sim >= 0.9:
            print(f"{doc_ids[i]}\t{doc_ids[j]}\t{sim:.6f}")

    #print(f"# Elapsed seconds: {time() - start:.3f}")

# ============================================================
if __name__ == "__main__":
    main()
