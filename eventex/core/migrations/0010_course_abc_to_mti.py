from django.db import migrations


def copy_src_to_dst(Source, Destination):
    for abc in Source.objects.all():
        mti = Destination(
            title=abc.title,
            start=abc.start,
            description=abc.description,
            slots=abc.slots
        )
        mti.save()
        mti.speakers.set(abc.speakers.all())
        abc.delete()


def forward_course_abc_to_mti(apps, scheme_editor):
    """Instatiates a MTI with all attributes for each ABC
    Associates speaker from ABC to MTI
    Deletes ABC"""
    CourseAbc = apps.get_model('core', 'CourseOld')
    CourseMti = apps.get_model('core', 'Course')

    copy_src_to_dst(CourseAbc, CourseMti)


def backward_course_abc_to_mti(apps, scheme_editor):
    """Instatiates a ABC with all attributes for each MTI
    Associates speaker from MTI to ABC
    Deletes MTI"""
    CourseAbc = apps.get_model('core', 'CourseOld')
    CourseMti = apps.get_model('core', 'Course')

    copy_src_to_dst(CourseMti, CourseAbc)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_course'),
    ]

    operations = [
        migrations.RunPython(forward_course_abc_to_mti)
    ]
