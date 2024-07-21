import hashlib

def crush_hash(name, seed):
    hash = hashlib.md5()
    hash.update(name.encode('utf-8'))
    hash.update(seed.encode('utf-8'))
    return int(hash.hexdigest(), 16)

def crush_choose(file_size, devices, buckets, seed):
    weights = [crush_hash(str(file_size) + str(device), seed) % 1000000 for device in devices]
    total_weight = sum(weights)
    weights = [float(weight) / total_weight for weight in weights]
    bucket_weights = []
    for bucket in buckets:
        bucket_weight = 0.0
        for device in bucket:
            bucket_weight += weights[device]
        bucket_weights.append(bucket_weight)
    max_bucket = max(bucket_weights)
    for i in range(len(bucket_weights)):
        if bucket_weights[i] == max_bucket:
            return i
    return -1
file_size =  1024
devices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
buckets = [[0, 1, 7], [3, 2, 5, 6], [6, 8, 9]]
seed = "my_seed"

bucket_index = crush_choose(file_size, devices, buckets, seed)

if bucket_index != -1:
    print(f"The file of size {file_size} was assigned to bucket {bucket_index}.")
else:
    print("Failed to assign file to any bucket.")