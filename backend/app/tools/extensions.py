from fake_useragent import UserAgent
from .generate_user import GenerateUser
from .generate_pwd import GeneratePassword
from .mailslurp import MailSlurp, new_email_ready


random_user_agent = UserAgent()
random_user = GenerateUser()
random_password = GeneratePassword()
random_mail = MailSlurp()
