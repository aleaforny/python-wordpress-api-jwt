def validate_protocol(proto):
    """
    Validating that passed protocol is either http or https
    """
    if "http" not in proto and "https" not in proto:
        raise ValueError(f"The protocol {proto} is unknown. Can only be either http or https.")
    return proto