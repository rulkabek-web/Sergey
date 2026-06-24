import requests

login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"

            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )


token = login_admin_response.json().get("token")

delete_all_account_response = requests.delete(
            url="http://localhost:4111/api/admin/users",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )