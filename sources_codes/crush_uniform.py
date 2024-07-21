import hashlib


num_osds = 8
num_buckets = 4

def crush(hash_val, num_replicas):
  
    int_val = int(hashlib.md5(str(hash_val).encode('utf-8')).hexdigest(), 16)
    osd_set = set()
    for i in range(num_replicas):
        bucket_id = int_val % num_buckets
        bucket_start = bucket_id * num_osds // num_buckets
        bucket_end = (bucket_id + 1) * num_osds // num_buckets
        osd_set.update(range(bucket_start, bucket_end))
        int_val >>= 32  
    
    return list(osd_set)

hash_val = 'test_key_mani'
num_replicas = 4
osd_set = crush(hash_val, num_replicas)
print(osd_set)