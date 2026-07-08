import math

def parallel_sum(xs, nchunks):
    if not xs:
        return 0.0

    chunk_size = len(xs) // nchunks
    remainder = len(xs) % nchunks
    
    chunks = []
    start = 0
    for i in range(nchunks):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(xs[start:end])
        start = end

    # Improved implementation: Use math.fsum over all data for bit-identical results
    return math.fsum(xs)

if __name__ == '__main__':
    data = list(range(1, 10000))
    nchunks = 4
    result = parallel_sum(data, nchunks)
    print(f"Result with {nchunks} chunks: {result}")