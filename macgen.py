import random


def generate_mac():
    random_bytes = [random.randint(0, 255) for _ in range(4)]
    random_mac = f"02:00:{random_bytes[0]:02x}:{random_bytes[1]:02x}:{random_bytes[2]:02x}:{random_bytes[3]:02x}"
    return random_mac

def main():
    print(generate_mac())

if __name__ == "__main__":
    main()