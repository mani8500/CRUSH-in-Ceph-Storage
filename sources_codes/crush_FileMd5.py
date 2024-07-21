#returns 128 bit
import hashlib

def crush_hash(key):
    h = hashlib.md5(str(key).encode())
    return h.digest()

def crush_choose(weight_vector, key):
    
    hash_val = crush_hash(key)
    n = len(weight_vector)
    node_weights = [w for (w, _) in weight_vector]
    node_sum = sum(node_weights)
    cum_weights = [sum(node_weights[:i+1])/node_sum for i in range(n)]
    bucket_id = 0
    for i in range(n):
        if cum_weights[i] > (int.from_bytes(hash_val, byteorder='big')/2**128):
            bucket_id = i
            break
    return weight_vector[bucket_id][1]

def main():
    
    weights = [(1, "bucket0"), (2, "bucket1"), (3, "bucket2")]
    files = [("file1", 100), ("file2", 200), ("file3", 150), ("file4", 75), ("file5", 300)]
    for file_id, file_size in files:
        bucket_id = crush_choose(weights, file_size)
        print(f"File {file_id} with size {file_size} assigned to bucket {bucket_id}")

if __name__ == '__main__':
    main()
