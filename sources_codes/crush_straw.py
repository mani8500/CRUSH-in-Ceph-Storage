import hashlib


osd_list = [0, 1, 2, 3, 4, 5, 6, 7]
bucket_list = [
    {'id': 0, 'weight': 1.0, 'items': [0, 1, 2]},
    {'id': 1, 'weight': 2.0, 'items': [3, 4, 5]},
    {'id': 2, 'weight': 1.0, 'items': [6, 7]},
]
def crush(hash_val, num_replicas):
    int_val = int(hashlib.md5(str(hash_val).encode('utf-8')).hexdigest(), 16)
    osd_set = set()
    for i in range(num_replicas):
        straw_vals = []
        for bucket in bucket_list:
            straw_val = 0
            for item in bucket['items']:
                hash_val = int(hashlib.md5(str(item).encode('utf-8')).hexdigest(), 16)
                straw_val += hash_val
            straw_vals.append((bucket['id'], straw_val))
        
        sorted_buckets = sorted(straw_vals, key=lambda x: x[1])
        
        bucket_id = None
        r = int_val / float(2**32)
        weight_sum = 0.0
        for bucket in sorted_buckets:
            weight_sum += bucket_list[bucket[0]]['weight']
            if r < weight_sum:
                bucket_id = bucket[0]
                break
        if bucket_id is None:
            bucket_id = sorted_buckets[-1][0]
        
        bucket = bucket_list[bucket_id]
        osd_id = bucket['items'][int_val % len(bucket['items'])]
        osd_set.add(osd_id)
        int_val >>= 32
   
    return list(osd_set)


hash_val = 'test_key_mani'
num_replicas = 2
osd_set = crush(hash_val, num_replicas)
print(osd_set)