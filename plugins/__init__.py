import rumps


def load_plugins(app: "rumps.App"):
    import plugins.vps
    import plugins.mfa
    import plugins.ip_security

    return [
        plugins.vps.VPSPlugin(app=app),
        plugins.mfa.MFAPlugin(app=app),
        plugins.ip_security.IPSecurityPlugin(app=app),
    ]
