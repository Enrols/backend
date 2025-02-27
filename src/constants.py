from datetime import timedelta


#### Auth consts #### 
FORGOT_PASSWORD_EXP_TIME = timedelta(minutes=30)
VERIFY_EMAIL_EXP_TIME = timedelta(hours=1)

OTP_LENGTH = 6
OTP_EXP_TIME = timedelta(minutes=30)

IMAGE_UPLOAD_PATH = 'images/'
FILE_UPLOAD_PATH = 'docs/'