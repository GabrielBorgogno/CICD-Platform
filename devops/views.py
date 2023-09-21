import paramiko
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import permission_required
from dotenv import load_dotenv
import os
from django.shortcuts import render
from django.db import connection, connections
load_dotenv()

host = os.getenv('SSH_TERMINAL_HOST')
port = int(os.getenv('SSH_TERMINAL_PORT'))
username = os.getenv('SSH_TERMINAL_USERNAME')
password = os.getenv('SSH_TERMINAL_PASSWORD')

@permission_required('authentication.can_view_files_scripts', raise_exception=True)
def list_remote_files(request):
   

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)

    _, stdout, _ = ssh.exec_command('ls /home/cloud/devops/scripts')
    files = stdout.read().decode('utf-8').splitlines()

    ssh.close()

    return render(request, 'automate.html', {'files': files})

@permission_required('authentication.can_execute_scripts', raise_exception=True)
def execute_script(request):
    if request.method == 'POST':
        file_name = request.POST.get('file')

        commandt = file_name.split(".")[-1]

        if commandt == "py":
            remote_command = f'python3 /home/cloud/devops/scripts/{file_name}'
        elif commandt == "yml":
            remote_command = f'ansible-playbook -i /home/cloud/devops/scripts/localhost.ini /home/cloud/devops/scripts/{file_name} --extra-vars service=home/cloud/devops/scripts/{file_name}'
        else:
            remote_command = f'bash /home/cloud/devops/scripts/{file_name}'

        def execute_remote_script():
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password)

                stdin, stdout, stderr = client.exec_command(remote_command)

                for line in stdout:
                    yield f"stdout: {line}<br>"
                for line in stderr:
                    yield f"stderr: {line}<br>"

                client.close()
            except Exception as e:
                yield f"An error occurred: {str(e)}<br>"

        return StreamingHttpResponse(execute_remote_script())

    else:
        return JsonResponse({'error': 'Invalid request method'})








def migration_monitor(request):
    # Execute uma consulta SQL para obter todas as informações da tabela django_migrations
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM django_migrations;")
        migrations = cursor.fetchall()

    context = {
        'migrations': migrations,
    }
    return render(request, 'database.html', context)
