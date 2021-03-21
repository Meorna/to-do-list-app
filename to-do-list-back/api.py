if __name__ == '__main__':
    """
        Create an application instance
    """
    from todolistsapi.__init__ import app
    """
        Runs the dev serveur:
            # Host : Chosse the host IP Address
            # Port : Choose the listening port
    """
    app.run(host= '0.0.0.0', port='5001')