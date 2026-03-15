import sys
import time
import numpy as np
import os
import re
import math
import csv


def main():
    if len(sys.argv) != 2:
        print("Usage: python hw1_2_b.py <path_to_browsing.txt>")
        sys.exit(1)

    input_path = sys.argv[1]
    start = time.time()

    item_count = {}
    with open(input_path, "r") as f:
        for line in f:
            
            items = line.strip().split()
            for item in items:
                item_count[item] = item_count.get(item, 0) + 1 # line?—?„œ item ê°œìˆ˜ ?„¸ê¸? ?—†?œ¼ë©? 0 ë°˜í™˜ 

    # support threshold
    support_threshold = 100
    conf_threshold= 0.5
    # keep only frequent items
    frequent_items = [item.strip() for item, cnt in item_count.items() if cnt >= support_threshold]
    frequent_items = sorted(set(frequent_items))
    N = len(frequent_items)
    
   

    # build index map (item -> idx)
    index_map = {item: idx for idx, item in enumerate(frequent_items)}
    # {'A' : 0 , ' B ' : 1 , 'C' :2 }
    # counting pair using triangular method 
    pair_count = np.zeros((N * (N - 1)) // 2, dtype=np.int32) # pair ????ž¥?•  ë°°ì—´ 

    def pair_index(i, j):
        # Convert (i,j) with i<j into linear index in triangular matrix
        # index = i*(N-1) - (i*(i-1))//2 + (j - i - 1)
        return i * (N - 1) - (i * (i - 1)) // 2 + (j - i - 1)

    # count co-occurrences
    with open(input_path, "r") as f:
        for line in f:
            items = line.strip().split()
            # keep only frequent items in this basket
            basket = sorted({index_map[i] for i in items if i in index_map})
            basket.sort()
            L = len(basket)
            for a in range(L):
                for b in range(a + 1, L):
                
                    idx = pair_index(basket[a], basket[b])
                    
                    pair_count[idx] += 1

    frequent_pairs = []
    for i in range(N):
        for j in range(i + 1, N):
            idx = pair_index(i, j)
            if pair_count[idx] >= support_threshold:
                frequent_pairs.append((frequent_items[i], frequent_items[j], pair_count[idx]))
    rules = [] # (confidence, support, A , B) ?˜•?ƒœ?˜ ?Šœ?”Œ ?ƒ?„± 
    for (A, B , supp_AB) in frequent_pairs : 
        supp_A = item_count[A]
        supp_B = item_count[B]
        if supp_A > 0 : 
            conf_AB = supp_AB / supp_A
            if conf_AB >= conf_threshold : 
                rules.append((conf_AB, supp_AB, A, B))
        if supp_B > 0 : 
            conf_BA = supp_AB / supp_B
            if conf_BA >= conf_threshold : 
                rules.append((conf_BA, supp_AB, B, A))
    num_frequent_pairs = len(frequent_pairs)
    num_rules = len(rules)
    rules.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]))
    top10 = rules[:10]
    print(num_frequent_pairs)
    print(num_rules)
    for conf, supp, A, B in top10:
        print(f"Rule: {A}-> {B}, Confidence: {conf:.6f}, Support: {supp}")
    elapsed = time.time() - start
    

if __name__ == "__main__":
    main()
