from django.contrib.auth.models import User, Group
from django.conf import settings
settings.configure(**django_settings)

def sync_users_and_roles():
    # Obtenha todos os usuários do Django
    django_users = User.objeccurl http://localhost:8001
    ts.all()

    for django_user in django_users:
        # Crie ou atualize o usuário no Keycloak
        keycloak_admin.create_user({
            'username': django_user.username,
            'email': django_user.email,
            'enabled': True,
            'credentials': [{'value': django_user.password}],
        })

        # Obtenha ou crie a função (role) correspondente ao grupo do Django
        django_groups = Group.objects.filter(user=django_user)

        for django_group in django_groups:
            try:
                # Tente obter a função (role) no Keycloak
                keycloak_role = keycloak_admin.get_role(django_group.name)
            except:
                # Se a função (role) não existir no Keycloak, crie-a
                keycloak_role = keycloak_admin.create_role({'name': django_group.name})

            # Associe a função (role) ao usuário no Keycloak
            keycloak_admin.assign_user_to_role(django_user.username, keycloak_role['id'])
