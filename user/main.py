from firebase_admin import initialize_app, auth, firestore
from firebase_functions import https_fn

# Initialize Firebase Admin ONCE
initialize_app()

@https_fn.on_request(region="africa-south1")
def create_cashier(req: https_fn.Request) -> https_fn.Response:
    try:
        # Create Firestore client lazily (IMPORTANT)
        db = firestore.client()

        body = req.get_json(silent=True)
        if not body or "data" not in body:
            return https_fn.Response(
                '{"error":"Invalid request"}',
                status=400,
                content_type="application/json"
            )

        data = body["data"]
        email = data.get("email")
        password = data.get("password")
        display_name = data.get("displayName")

        if not email or not password or not display_name:
            return https_fn.Response(
                '{"error":"Missing fields"}',
                status=400,
                content_type="application/json"
            )

        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )

        db.collection("users").document(user.uid).set({
            "email": email,
            "displayName": display_name,
            "role": "cashier",
            "active": True,
            "createdAt": firestore.SERVER_TIMESTAMP
        })

        return https_fn.Response(
            f'''{{
                "success": true,
                "cashier": {{
                    "uid": "{user.uid}",
                    "email": "{email}",
                    "displayName": "{display_name}"
                }}
            }}''',
            status=200,
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            f'{{"error":"{str(e)}"}}',
            status=500,
            content_type="application/json"
        )
