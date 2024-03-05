def load_plugins():
    import plugins.mfa

    return [plugins.mfa.MFAPlugin()]
