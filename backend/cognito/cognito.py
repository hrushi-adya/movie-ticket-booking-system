from botocore.exceptions import ClientError
import boto3
import hmac
import hashlib
import base64

client = boto3.client('cognito-idp')


class CognitoIdentityProviderWrapper:
    """Encapsulates Amazon Cognito actions"""

    def get_secret_hash(self, username):
        msg = username + self.client_id
        dig = hmac.new(
            str(self.client_secret).encode('utf-8'),
            msg=str(msg).encode('utf-8'),
            digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    def calculate_secret_hash(self, username):
        message = username + self.client_id
        digest = hmac.new(self.client_secret.encode(), message.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()
    
    def __init__(self, cognito_idp_client, user_pool_id, client_id, client_secret=None):
        """
        :param cognito_idp_client: A Boto3 Amazon Cognito Identity Provider client.
        :param user_pool_id: The ID of an existing Amazon Cognito user pool.
        :param client_id: The ID of a client application registered with the user pool.
        :param client_secret: The client secret, if the client has a secret.
        """
        self.cognito_idp_client = cognito_idp_client
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client_secret = client_secret

    def sign_up_user_ph(self, user_name, profile_type, password, user_email, user_phone_number):
        """
        Signs up a new user with Amazon Cognito. This action prompts Amazon Cognito
        to send an email to the specified email address. The email contains a code that
        can be used to confirm the user.

        When the user already exists, the user status is checked to determine whether
        the user has been confirmed.


        :param profile_type:
        :param user_name: The user name that identifies the new user.
        :param password: The password for the new user.
        :param user_email: The email address for the new user.
        :param user_phone_number:
        :return: True when the user is already confirmed with Amazon Cognito.
                 Otherwise, false.
        """
        try:
            kwargs = {
                'ClientId': self.client_id, 'Username': user_name, 'Password': password,
                'UserAttributes': [{'Name': 'email', 'Value': user_email},
                                   {'Name': 'phone_number', 'Value': user_phone_number},
                                   {'Name': 'custom:profile_type', 'Value': profile_type}],
            }
            if self.client_secret is not None:
                kwargs['SecretHash'] = self.get_secret_hash(user_name)
            response = self.cognito_idp_client.sign_up(**kwargs)
            print(response)
            confirmed = response['UserConfirmed']
        except ClientError as err:
            if err.response['Error']['Code'] == 'UsernameExistsException':
                response = self.cognito_idp_client.admin_get_user(
                    UserPoolId=self.user_pool_id, Username=user_name)
                print("User %s exists and is %s.", user_name, response['UserStatus'])
                confirmed = response['UserStatus'] == 'CONFIRMED'
            else:
                print(
                    "Couldn't sign up %s. Here's why: %s: %s", user_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        return confirmed

    def sign_up_user(self, user_name, password, user_email):
        """
        Signs up a new user with Amazon Cognito. This action prompts Amazon Cognito
        to send an email to the specified email address. The email contains a code that
        can be used to confirm the user.

        When the user already exists, the user status is checked to determine whether
        the user has been confirmed.

        :param user_name: The user name that identifies the new user.
        :param password: The password for the new user.
        :param user_email: The email address for the new user.
        :return: True when the user is already confirmed with Amazon Cognito.
                 Otherwise, false.
        """
        try:
            kwargs = {
                'ClientId': self.client_id, 'Username': user_name, 'Password': password,
                'UserAttributes': [{'Name': 'email', 'Value': user_email}]}
            if self.client_secret is not None:
                kwargs['SecretHash'] = self.get_secret_hash(user_name)
            response = self.cognito_idp_client.sign_up(**kwargs)
            confirmed = response['UserConfirmed']
        except ClientError as err:
            if err.response['Error']['Code'] == 'UsernameExistsException':
                response = self.cognito_idp_client.admin_get_user(
                    UserPoolId=self.user_pool_id, Username=user_name)
                print("User %s exists and is %s.", user_name, response['UserStatus'])
                confirmed = response['UserStatus'] == 'CONFIRMED'
            else:
                print(
                    "Couldn't sign up %s. Here's why: %s: %s", user_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        return confirmed

    def confirm_user_sign_up(self, user_name, confirmation_code):
        """
        Confirms a previously created user. A user must be confirmed before they
        can sign in to Amazon Cognito.

        :param user_name: The name of the user to confirm.
        :param confirmation_code: The confirmation code sent to the user's registered
                                  email address.
        :return: True when the confirmation succeeds.
        """
        try:
            kwargs = {
                'ClientId': self.client_id, 'Username': user_name,
                'ConfirmationCode': confirmation_code}
            if self.client_secret is not None:
                kwargs['SecretHash'] = self.get_secret_hash(user_name)
            self.cognito_idp_client.confirm_sign_up(**kwargs)
        except ClientError as err:
            print(
                "Couldn't confirm sign up for %s. Here's why: %s: %s", user_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return True

    def send_verification_code_phone(self, access_token):
        """
        Prompts Amazon Cognito to resend an SMS with confirmation code.

        :param access_token: The access_token after user signed in.
        :return: Delivery information about where the SMS is sent.
        """
        try:

            res = self.cognito_idp_client.get_user_attribute_verification_code(
                AccessToken=access_token,
                AttributeName='phone_number'
            )
        except ClientError as err:
            print(
                "Couldn't send SMS for this user. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return res

    def send_verification_code_email(self, access_token):
        """
        Prompts Amazon Cognito to resend an EMAIL with confirmation code.

        :param access_token: The access_token after user signed in.
        :return: Delivery information about where the EMAIL is sent.
        """
        try:

            res = self.cognito_idp_client.get_user_attribute_verification_code(
                AccessToken=access_token,
                AttributeName='email'
            )
        except ClientError as err:
            print(
                "Couldn't send EMAIL for this user. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return res

    def verify_user_phone(self, access_token, code):
        """
        Verify the user's phone number with code.

        :param access_token: The access_token after user signed in.
        :param code: verification code.
        :return: Delivery information about where the SMS is sent.
        """
        try:

            res = self.cognito_idp_client.verify_user_attribute(
                AccessToken=access_token,
                AttributeName='phone_number',
                Code=code
            )
        except ClientError as err:
            print(
                "Couldn't verify phone number for this user. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return res

    def verify_user_email(self, access_token, code):
        """
        Verify the user's phone number with code.

        :param access_token: The access_token after user signed in.
        :param code: verification code.
        :return: Delivery information about where the SMS is sent.
        """
        try:

            res = self.cognito_idp_client.verify_user_attribute(
                AccessToken=access_token,
                AttributeName='email',
                Code=code
            )
        except ClientError as err:
            print(
                "Couldn't verify email for this user. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return res

    def resend_confirmation(self, user_name):
        """
        Prompts Amazon Cognito to resend an SMS/EMAIL with a new confirmation code.

        :param user_name: The name of the user who will receive the email.
        :return: Delivery information about where the email is sent.
        """
        try:
            kwargs = {
                'ClientId': self.client_id, 'Username': user_name}
            if self.client_secret is not None:
                kwargs['SecretHash'] = self.get_secret_hash(user_name)
            response = self.cognito_idp_client.resend_confirmation_code(**kwargs)
            delivery = response['CodeDeliveryDetails']
        except ClientError as err:
            print(
                "Couldn't resend confirmation to %s. Here's why: %s: %s", user_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return delivery

    def forgot_password(self, user_name):
        """
        Sends confirmation code to confirm user_id when resetting password

        :param user_name: user_id for which password needs to be reset
        :return: Confirmation code with delivery information
        """
        try:
            secret_hash = self.get_secret_hash(user_name)
            kwargs = {
                "ClientId": self.client_id,
                "SecretHash": secret_hash,
                "Username": user_name
            }
            response = self.cognito_idp_client.forgot_password(**kwargs)

        # except client.exceptions.UserNotFoundException:
        #     return {"error": True,
        #             "data": None,
        #             "success": False,
        #             "message": "Username doesnt exists"}
        #
        # except client.exceptions.InvalidParameterException:
        #     return {"error": True,
        #             "success": False,
        #             "data": None,
        #             "message": f"User <{user_name}> is not confirmed yet"}
        #
        # except client.exceptions.CodeMismatchException:
        #     return {"error": True,
        #             "success": False,
        #             "data": None,
        #             "message": "Invalid Verification code"}
        #
        # except client.exceptions.NotAuthorizedException:
        #     return {"error": True,
        #             "success": False,
        #             "data": None,
        #             "message": "User is already confirmed"}

        except Exception as e:
            # return {"error": True,
            #         "success": False,
            #         "data": None,
            #         "message": f"Unknown    error {e.__str__()} "}
            raise

        return response

    def confirm_forgot_password(self, user_name, confirmation_code, password):
        """
        Reset password with verification code

        :param user_name: User id
        :param confirmation_code: conformation code received in response of forgot_password
        :param password: new password
        :return: HTTP Status Code showing success/failure, empty body
        """
        try:
            kwargs = {
                "ClientId": self.client_id,
                "SecretHash": self.get_secret_hash(user_name),
                "Username": user_name,
                "ConfirmationCode": confirmation_code,
                "Password": password
            }

            response = self.cognito_idp_client.confirm_forgot_password(**kwargs)

        except Exception as e:
            raise

        return response

    def start_sign_in(self, user_name, password):
        """
        Starts the sign-in process for a user by using administrator credentials.
        This method of signing in is appropriate for code running on a secure server.

        If the user pool is configured to require MFA and this is the first sign-in
        for the user, Amazon Cognito returns a challenge response to set up an
        MFA application. When this occurs, this function gets an MFA secret from
        Amazon Cognito and returns it to the caller.

        :param user_name: The name of the user to sign in.
        :param password: The user's password.
        :return: The result of the sign-in attempt. When sign-in is successful, this
                 returns an access token that can be used to get AWS credentials. Otherwise,
                 Amazon Cognito returns a challenge to set up an MFA application,
                 or a challenge to enter an MFA code from a registered MFA application.
        """
        try:
            kwargs = {
                'UserPoolId': self.user_pool_id,
                'ClientId': self.client_id,
                'AuthFlow': 'ADMIN_USER_PASSWORD_AUTH',
                'AuthParameters': {'USERNAME': user_name, 'PASSWORD': password}}
            if self.client_secret is not None:
                kwargs['AuthParameters']['SECRET_HASH'] = self.get_secret_hash(user_name)
            response = self.cognito_idp_client.admin_initiate_auth(**kwargs)
            challenge_name = response.get('ChallengeName', None)
            if challenge_name == 'MFA_SETUP':
                if 'SOFTWARE_TOKEN_MFA' in response['ChallengeParameters']['MFAS_CAN_SETUP']:
                    response.update(self.get_mfa_secret(response['Session']))
                else:
                    raise RuntimeError(
                        "The user pool requires MFA setup, but the user pool is not "
                        "configured for TOTP MFA. This example requires TOTP MFA.")
        except ClientError as err:
            print(
                "Couldn't start sign in for %s. Here's why: %s: %s", user_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            response.pop('ResponseMetadata', None)
            return response

    def initiate_auth(self, username, password):
        secret_hash = self.get_secret_hash(self, username)
        try:
            resp = self.cognito_idp_client.admin_initiate_auth(
                UserPoolId=self.user_pool_id,
                ClientId=self.client_id,
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'SECRET_HASH': secret_hash,
                    'PASSWORD': password,
                },
                ClientMetadata={
                    'username': username,
                    'password': password, })
        except client.exceptions.NotAuthorizedException:
            return None, "The username or password is incorrect"
        except client.exceptions.UserNotConfirmedException:
            return None, "User is not confirmed"
        except Exception as e:
            return None, e.__str__()
        if resp.get("AuthenticationResult"):
            return {'message': "success",
                    "error": False,
                    "success": True,
                    "data": {
                        "id_token": resp["AuthenticationResult"]["IdToken"],
                        "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                        "access_token": resp["AuthenticationResult"]["AccessToken"],
                        "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                        "token_type": resp["AuthenticationResult"]["TokenType"]
                    }}

    def get_user(self, access_token):
        """
        Get the user details with the access_token.

        :param access_token: JWT access_token received after sign in.
        :return: Delivery information about where the email is sent.
        """
        try:
            response = self.cognito_idp_client.get_user(
                AccessToken=access_token
            )
        except ClientError as err:
            print(
                "Couldn't user details for this token. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response

    def delete_user(self, user_id):
        """
        Delete a particular user from pool
        :param user_id:
        :return:
        """
        try:
            response = self.cognito_idp_client.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=user_id
            )
        except ClientError as err:
            print(
                "Couldn't delete user for the id: %s, Here's why: %s: %s", user_id,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response

    def disable_user(self, user_id):
        """
        Disable a user in pool
        :param user_id:
        :return:
        """
        try:
            response = self.cognito_idp_client.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=user_id
            )
        except ClientError as err:
            print(
                "Couldn't disable user for the id: %s, Here's why: %s: %s", user_id,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response

    def enable_user(self, user_id):
        """
        Enable back a user
        :param user_id:
        :return:
        """
        try:
            response = self.cognito_idp_client.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=user_id
            )
        except ClientError as err:
            print(
                "Couldn't enable user for the id: %s, Here's why: %s: %s", user_id,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response

    def update_user_attributes(self, user_id, user_attributes):
        """
        Update user pool attributes
        :param user_attributes:
        :param user_id:
        :return:
        """
        try:
            response = self.cognito_idp_client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=user_id,
                UserAttributes=user_attributes,
            )
        except ClientError as err:
            print(
                "Couldn't update user for the id: %s, Here's why: %s: %s", user_id,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response

    def get_user_id_with_sub(self, profile_id):
        try:
            response = self.cognito_idp_client.list_users(
                UserPoolId=self.user_pool_id,
                AttributesToGet=[
                    'username',
                ],
                Limit=1,
                Filter='sub='+profile_id
            )
        except ClientError as err:
            print(
                "Couldn't update user for the id: %s, Here's why: %s: %s", profile_id,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response
