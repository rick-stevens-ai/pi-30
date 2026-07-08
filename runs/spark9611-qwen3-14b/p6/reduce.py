import math

def parallel_sum(xs, nchunks):
    chunks = []
    chunk_size = len(xs) // nchunks
    remainder = len(xs) % nchunks
    index = 0
    for i in range(nchunks):
        size = chunk_size + (1 if i < remainder else 0)
        chunks.append(xs[index:index+size])
        index += size
    return math.fsum(xs)