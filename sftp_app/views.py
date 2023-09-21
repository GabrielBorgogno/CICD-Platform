import paramiko
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from authentication.models import CustomUser
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv('SSH_TERMINAL_HOST')
port = int(os.getenv('SSH_TERMINAL_PORT'))
username = os.getenv('SSH_TERMINAL_USERNAME')
password = os.getenv('SSH_TERMINAL_PASSWORD')

@permission_required('authentication.candownloadfiles', raise_exception=True)
def download_file(request, file_name):
    try:
        # Connect to the SFTP server
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)

        # Open the requested file on the SFTP server
        sftp = client.open_sftp()
        file_path = f'sftp/{file_name}'  # Update with the actual path
        remote_file = sftp.open(file_path, 'r')

        # Read the content of the file
        file_content = remote_file.read()

        # Close the SFTP connection and SSH client
        remote_file.close()
        sftp.close()
        client.close()

        # Serve the file as a downloadable response
        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

    except Exception as e:
        return HttpResponse("An error occurred: " + str(e))


@permission_required('authentication.can_view_files', raise_exception=True)
def sftp_client(request):
    try:
        # Connect to the SSH server
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)

        # Execute the "ls" command to list files and directories
        stdin, stdout, stderr = client.exec_command("ls -th sftp ")

        file_list = stdout.read().decode("utf-8").strip().split('\n')

        # Close the SSH client
        client.close()

        return render(request, 'sftp.html', {'file_list': file_list})

    except paramiko.AuthenticationException as auth_exc:
        return render(request, 'sftp.html', {'error_message': "Authentication failed: " + str(auth_exc)})

    except paramiko.SSHException as ssh_exc:
        return render(request, 'sftp.html', {'error_message': "SSH connection failed: " + str(ssh_exc)})

    except Exception as e:
        return render(request, 'sftp.html', {'error_message': "An error occurred: " + str(e)})
