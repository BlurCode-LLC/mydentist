from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}"


reset_password_token = ResetPasswordTokenGenerator()
