from django.db import migrations


def set_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        pk=1,
        defaults={"domain": "aiproof.fastinfer.org", "name": "AIProof"},
    )


def reset_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        pk=1,
        defaults={"domain": "example.com", "name": "example.com"},
    )


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        # idempotent: run unconditionally on every fresh deploy
        migrations.RunPython(set_site_domain, reset_site_domain, elidable=False),
    ]
