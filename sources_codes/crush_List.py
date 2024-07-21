import hashlib

osd_list = [0, 1, 2, 3, 4, 5, 6, 7]

bucket_list = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9],
    [10, 11],
    [12, 13],
    [14, 15],
    [16, 17],
    [18, 19],
    [20, 21],
    [22, 23],
    [24, 25],
    [26, 27],
    [28, 29],
    [30, 31],
]

def crush(hash_val, num_replicas):
   
    int_val = int(hashlib.md5(str(hash_val).encode('utf-8')).hexdigest(), 16)
    
    osd_set = set()
    for i in range(num_replicas):
        bucket_id = int_val % len(bucket_list)
        bucket = bucket_list[bucket_id]
        if isinstance(bucket[0], list):
            bucket_id = int_val % len(bucket)
            bucket = bucket[bucket_id]
        osd_set.update(bucket)
        int_val >>= 32
   
    return list(osd_set)

hash_val = 'test_key'
num_replicas = 3
osd_set = crush(hash_val, num_replicas)
print(osd_set)