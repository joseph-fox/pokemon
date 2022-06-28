from envparse import env


def get_dev_env(path):
    """
    Return the local environments vars.
    """
    env.read_envfile(path)
    return env


def get_env():
    """
    Retrieve and return the production environments vars

    To be implemented.
    """
    # Return a new instance with no scheme.
    raise NotImplemented
