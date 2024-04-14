import json

from pretreatment import start


if __name__ == "__main__":
    # Initialize A Django Environment
    from django.conf import settings
    TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates'}]
    settings.configure(TEMPLATES=TEMPLATES)
    import django
    django.setup()
    file = open("./do/audit/audit_tmp_file.json","w")
    now=dict()
    file.write(json.dumps(now))
    file.close()
    start.main_start()