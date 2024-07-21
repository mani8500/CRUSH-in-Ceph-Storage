#py3

import hashlib

def crush_hash(name, seed):
   
    hash = hashlib.md5()
    hash.update(name.encode('utf-8'))
    hash.update(seed.encode('utf-8'))
    return int(hash.hexdigest(), 16)

def crush_choose(data, devices, buckets, seed):
    weights = []
    for device in devices:
        hash_value = crush_hash(str(data) + str(device), seed)
        weight = hash_value % 1000000
        weights.append(weight)

    total_weight = sum(weights)
    weights = [float(weight) / total_weight for weight in weights]
    bucket_weights = []
    for bucket in buckets:
        bucket_weight = 0.0
        for device in bucket:
            bucket_weight += weights[device]
        bucket_weights.append(bucket_weight)

    # Choose the bucket with the highest weight
    max_bucket = max(bucket_weights)
    for i in range(len(bucket_weights)):
        if bucket_weights[i] == max_bucket:
            return i

    # If no bucket was chosen, return -1
    return -1

data = "hii helo this is Mani"
devices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11]
buckets = [[0, 1, 2], [3, 4, 5,], [6,7,8, 9,10,11]]
seed = "my_seed"

bucket_index = crush_choose(data, devices, buckets, seed)

if bucket_index != -1:
    print(f"The data {data} was assigned to bucket {bucket_index}.")
else:
    print("Failed to assign data to any bucket.")

