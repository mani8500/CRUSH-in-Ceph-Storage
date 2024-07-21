#py3
import random

class StorageDevice:
    def __init__(self, id):
        self.id = id
        self.weight = random.randint(1, 10)

class CRUSH:
    def __init__(self, devices):
        self.devices = devices
        self.num_buckets = 4
        self.buckets = [self.create_bucket() for i in range(self.num_buckets)]
    
    def create_bucket(self):
        bucket = []
        for i in range(random.randint(1, 10)):
            if random.random() < 1:
                bucket.append(self.devices[random.randint(0, len(self.devices)-1)])
            else:
                bucket.append(self.create_bucket())
        return bucket

    def choose_device(self, data):
        _hash = hash(data)
        bucket_index = _hash % self.num_buckets
        bucket = self.buckets[bucket_index]
        return self.choose_device_from_bucket(bucket, _hash)
    
    def choose_device_from_bucket(self, bucket, _hash):
        if isinstance(bucket,StorageDevice):
            return bucket
        if len(bucket) == 0:
            return None
        if len(bucket) == 1:
            return bucket[0]
        
        # Device selection logic inside bucket
        bucket_weights = [self.get_bucket_weight(sub_bucket) for sub_bucket in bucket]
        
        target = _hash % sum(bucket_weights)
        for i in range(len(bucket)):
            target -= bucket_weights[i]
            if target < 0:
                return self.choose_device_from_bucket(bucket[i], _hash)
        return None
    
    def get_bucket_weight(self, bucket):
        if isinstance(bucket, StorageDevice):
            return bucket.weight
        else:
            return sum(self.get_bucket_weight(sub_bucket) for sub_bucket in bucket)

devices = [StorageDevice(i) for i in range(10)]
crush = CRUSH(devices)

for i in range(10000):
    data = "data{}".format(i)
    device = crush.choose_device(data)
    
    if(device==None):
        print('not found')
    else:
        print("Finally {} stored on device {}".format(data, device.id))