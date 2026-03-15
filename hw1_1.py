#!/usr/bin/env python3
# hw1_1.py  -- EE412 HW1 Problem 1
# Usage: python hw1_1.py /path/to/soc-LiveJournal1Adj.txt

import sys
import time
from pyspark import SparkConf, SparkContext

def parse_line(line):
    """Parse '<u>\\t<comma_sep_friends>' -> (u, set_of_friends)"""
    line = line.strip() # 공백 제거
    if not line: # 빈줄 스킵
        return None 
    if '\t' not in line: # 탭 문자 없어도 스킵 
        return None
    u_str, friends_str = line.split('\t', 1) # tap 기준으로 왼쪽은 user 오른쪽은 친구
    try:
        u = int(u_str) #정수로 바꾸기 
    except:
        return None
    friends = set() # 친구들 집합 생성 ->중복 알아서 제거해주는 집합 사용이 효율적
    for tok in friends_str.split(','): 
        tok = tok.strip() # 문자열 쉼표로 쪼개서 토큰 앞뒤 제거하고 집합으로 만든다 
        if not tok:
            continue
        try:
            v = int(tok) # 친구 토큰도 정수로 ㅇ바꾸고 
            if v != u: # v가 u 자기자신인 경우는 스킵
                friends.add(v)
        except:
            continue
    return (u, friends)

def gen_pairs_sorted(lst):
    """Yield all i<j index pairs for a sorted list (no itertools)"""
    n = len(lst) # 리스트 길이
    for i in range(n - 1): # 마지막 원소는 비교하지 않음 
        vi = lst[i] # 정렬되어 있으므로 그냥 꺼낸 후에 다시 for loop으로 i+1부터 끝까지 
        for j in range(i + 1, n):
            vj = lst[j]
            yield (vi, vj) 

def main():
    if len(sys.argv) != 2: #인자 두 개 정상적을 받았는지 확인
        print("Usage: python hw1_1.py <path_to_soc-LiveJournal1Adj.txt>")
        sys.exit(1)

    input_path = sys.argv[1]
    t0 = time.time()

    conf = (
        SparkConf()
        .setAppName("EE412_HW1_Problem1")
        .setMaster("local[*]")
        .set("spark.driver.memory", "8g")
        .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    )
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")

    # A) Read & parse to directed neighbor sets
    lines = sc.textFile(input_path)
    parsed = lines.map(parse_line).filter(lambda x: x is not None)
    # (u -> set(friends)) but RDD of (u, set)
    # for directed edges RDD:
    directed_edges = parsed.flatMap( # undirected edge  만들기 
        lambda uv: [ (uv[0], v) for v in uv[1] ]
    ).cache()

    # B) Build undirected edges by requiring mutual presence:
    # Map directed (u,v) -> key=(min,max), count 1; reduce; keep those with count>=2
    undirected_keys = (  
        directed_edges
        .map(lambda uv: ( (uv[0], uv[1]) if uv[0] < uv[1] else (uv[1], uv[0]), 1 ))
        # uv와 vu를 똑같이 만들고 숫자를 세서 만약 2개면 undirected가 됨 
        .reduceByKey(lambda a,b: a+b)
        .filter(lambda kv: kv[1] >= 2)
        .keys() # value 필요없으니까 버리고 key만 꺼냄 
        .cache()
    )

    # Broadcast set for O(1) edge existence checks (as sorted tuple pairs)
    edge_set = set(undirected_keys.collect())
    b_edge = sc.broadcast(edge_set)

    # C) Build undirected adjacency N(u)
    # From undirected edges (u,v), add both directions then group
    neighbors_undir = (
        undirected_keys # undirected들을 모아서 []
        .flatMap(lambda e: [(e[0], e[1]), (e[1], e[0])])
        .groupByKey()
        .mapValues(lambda vs: sorted(set(vs)))
        .cache()
    )

    # D) For each node 'a', emit non-edge neighbor pairs (v,w) with 'a' as common neighbor
    # (v,w) must be non-adjacent to avoid diagonal (v,w)
    # Key: (v,w), Value: a
    common_by_nonedge = (
        neighbors_undir.flatMap(
            lambda aw: [
                ((v, w), aw[0])
                for (v, w) in gen_pairs_sorted(aw[1])
                if ( (v, w) if v < w else (w, v) ) not in b_edge.value
            ]
        )
        .groupByKey()
        .mapValues(lambda it: sorted(set(it)))  # A = sorted unique common neighbors
        .cache()
    )

    # E) For each non-edge pair (v,w) with common neighbors A, pick pairs (a,x),
    # require (a,x) to be NON-edge (avoid the other diagonal). If so, yield sorted 4-tuple.
    squares = (
        common_by_nonedge.flatMap(
            lambda vw_A: [
                tuple(sorted((a, vw_A[0][0], x, vw_A[0][1])))
                for idx, a in enumerate(vw_A[1])
                for x in vw_A[1][idx+1:]
                if ( (a, x) if a < x else (x, a) ) not in b_edge.value
            ]
        )
        .distinct()
        .cache()
    )

    
    first10 = squares.takeOrdered(10)
    last10  = squares.top(10)  # top() gives the last 10 in lexicographic order

    # Output format: u<TAB>v<TAB>w<TAB>x
    for t in first10:
        print(f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}")

    for t in sorted(last10):
        print(f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}")


    # (선택) 경과 시간 출력은 콘솔 맨 끝에 참고용으로 찍어두자.
    elapsed = time.time() - t0
    #print(f"# Elapsed seconds: {elapsed:.3f}", file=sys.stderr)
    
    sc.stop()

if __name__ == "__main__":
    main()
