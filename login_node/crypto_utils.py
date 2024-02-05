import argon2

# Define parameters
SALT = b"a259812aea3ec74da70f6ecd596ec0d6"  # 16 bytes generated with os.urandom
# Recommendations from argon2-cffi documentation
TIME_COST = 100  # ~50ms - 500ms verification time (depending on hardware)
MEMORY_COST = 1024
PARALLELISM = 4
HASH_LEN = 16 # 16 bytes
TYPE = argon2.low_level.Type.ID


def hash_password(password: bytes) -> bytes:
    """Hash the password using argon2id"""
    return argon2.low_level.hash_secret(
        password, SALT,
        time_cost=TIME_COST, memory_cost=MEMORY_COST, parallelism=PARALLELISM,
        hash_len=HASH_LEN, type=TYPE
    )


def verify_password(hash: bytes, plaintext: bytes) -> bytes:
    """Verify the password using argon2id"""
    try:
        return argon2.low_level.verify_secret(
            hash, plaintext,
            type=TYPE
        )
    except argon2.exceptions.VerificationError:
        return False
    return False
