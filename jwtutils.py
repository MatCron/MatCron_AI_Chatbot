import jwt


def validate_token(token: str, JWT_SECRET: str, JWT_ISSUER: str):
    try:
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer=JWT_ISSUER,
            options={"require": ["exp", "iss"]}  # Ensure 'exp' and 'iss' claims exist
        )
        return decoded_token, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired."
    except jwt.InvalidTokenError as ex:
        return None, f"Token validation failed: {str(ex)}"
    except Exception as ex:
        return None, f"Unexpected error: {str(ex)}"
