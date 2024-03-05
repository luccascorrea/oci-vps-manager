def load_plugins():
    import plugins.mfa
    import plugins.ip_security

    return [plugins.mfa.MFAPlugin(), plugins.ip_security.IPSecurityPlugin()]
