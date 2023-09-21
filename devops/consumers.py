# your_app/consumers.py

import asyncssh
from channels.generic.websocket import AsyncWebsocketConsumer

class SSHTerminalConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        # Retrieve the SSH credentials from the client
        host = '172.21.202.181'
        port = 22
        username = 'cloud'
        password = '1234'

        # Connect to the SSH server and authenticate
        self.conn = await self.connect_ssh(host, port, username, password)

        if self.conn:
            await self.accept()
        else:
            await self.close()

    async def websocket_disconnect(self, event):
        # Close the SSH connection when the WebSocket disconnects
        await self.conn.close()

    async def websocket_receive(self, text_data):
        # Execute the command on the SSH server
        result = await self.conn.run(text_data)

        # Send the command output back to the client
        await self.send(text_data=result.stdout)

    async def connect_ssh(self, host, port, username, password):
        try:
            # Connect to the SSH server
            conn = await asyncssh.connect(
                host, port=port, username=username, password=password, known_hosts=None
            )
            return conn

        except asyncssh.Error as e:
            return None
