def output_format1(hash: str, pw: str, steps: int):
    """
    Hash: {hash}

    Password: {pw}

    Took {steps} attempts to crack message.
    """
    print(f"Hash: {hash}")
    print(f"Password: {pw}")
    print(f"Took {steps} attempts to crack message.")
    return