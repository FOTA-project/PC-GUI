import time
import pyrebase

progressInstructionFile = open('progress.txt', 'w')
progressInstructionFile.seek(0, 0)

# upload
firebaseConfig = {
    "apiKey": "AIzaSyBgBFhNa6OnJCLbFTQW3vF_Cyz-rMyN4vU",
    "authDomain": "fota-server-b4148.firebaseapp.com",
    "databaseURL": "https://fota-server-b4148.firebaseio.com",
    "projectId": "fota-server-b4148",
    "storageBucket": "fota-server-b4148.appspot.com",
    "messagingSenderId": "774423425890",
    "appId": "1:774423425890:web:f506832444c3d30b2c323b",
    "measurementId": "G-2DE9D9TN6N"
  };

email = r"fota_project_gp_iti@gmail.com"
password = r"12345@ITI"

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig);
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
user = auth.refresh(user['refreshToken']) # optional

db = firebase.database()
storage = firebase.storage()

user_uid = user['userId']
user_tokenId = user['idToken']

INSTRUCTION_WRITE_MAX_REQUESTS    = -4
INSTRUCTION_COMM_TIMEOUT          = -2
INSTRUCTION_TERMINATE_ON_SUCCESS  = -3

user_db_dir = "users/" + user_uid + "/STM32"
isTerminate = 0

elfProgressMaxRequest = db.child(user_db_dir + "/elfProgressMaxRequest").get(user_tokenId).val()

previousElfProgress = -1
timeoutCtr = 0


progressInstructionFile.write("%d %d\n" %(INSTRUCTION_WRITE_MAX_REQUESTS, elfProgressMaxRequest))
progressInstructionFile.flush()

while isTerminate == 0:
    elfProgress = db.child(user_db_dir + "/elfProgress").get(user_tokenId).val()
    #print("elfProgress = %d, timeoutCtr = %d\n" %(elfProgress, timeoutCtr))
    
    if previousElfProgress != elfProgress:
        timeoutCtr = 0
        previousElfProgress = elfProgress
        progressInstructionFile.write("%d\n" %(elfProgress))
        progressInstructionFile.flush()
    elif elfProgress == elfProgressMaxRequest:
        isTerminate = 1
    else:
        time.sleep(0.000001 * 500) # 500us
        timeoutCtr = timeoutCtr + 1

    if timeoutCtr == 500:
        isTerminate = 1


# end of while
#print("progress-script.py: elfProgress = %d, elfProgressMaxRequest = %d\n" %(elfProgress, elfProgressMaxRequest))
if elfProgress == elfProgressMaxRequest:
    progressInstructionFile.write("%d\n" %(INSTRUCTION_TERMINATE_ON_SUCCESS))
    progressInstructionFile.flush()
    
    # update elfProgress flag in database
    db.child(user_db_dir).update({"elfProgress" : 0}, user_tokenId)
else:
    progressInstructionFile.write("%d\n" %(INSTRUCTION_COMM_TIMEOUT))
    progressInstructionFile.flush()

#### done
print("progress-script.py: done...\n")
