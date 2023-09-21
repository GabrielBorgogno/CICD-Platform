from django.contrib.auth.models import Permission

permission_download = Permission.objects.create(
    codename='can_download_sftp_file',
    name='Can Download SFTP File',
)

permission_view = Permission.objects.create(
    codename='can_view_sftp_file',
    name='Can View SFTP File',
)
