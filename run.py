import os
if os.path.exists('settings.py'):
    from settings import username, password

print(username, password)
