import hashlib
import bisect

def crush_choose(hash_key, devices, num_replicas):
    
    hash_val = int(hashlib.md5(hash_key.encode('utf-8')).hexdigest(), 16)
    device_weights = [hashlib.md5(d.encode('utf-8')).digest() for d in devices]

    sorted_devices = sorted(zip(device_weights, devices))
    chosen_devices = []
    for i in range(num_replicas):
        
        pos = hash_val % len(sorted_devices)
        chosen_devices.append(sorted_devices[pos][1])
        del sorted_devices[pos]
        sorted_devices = sorted(sorted_devices)

    return chosen_devices
    
devices = ['device5', 'device2', 'device3', 'device4', 'device1']
hash_key = 'my-object-key'
num_replicas = 4

chosen_devices = crush_choose(hash_key, devices, num_replicas)

print(chosen_devices)
