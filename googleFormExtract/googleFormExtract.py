import sys
import pandas as pd
from multiprocessing import Process
import smtplib
from email.message import EmailMessage 

def sendMail(email, companyName, companyEmail, perMatch):
    EMAIL_ADDRESS = 'vishalnagargoje22@gmail.com'  # enter the user email address here
    EMAIL_PASSWORD = 'magnetferro@227'  # enter the password for the user here
    msg = EmailMessage()
    msg['Subject'] = 'Test Email DoNot reply'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(companyEmail + "has a percentage match of:"+ str(perMatch))  # User can add his message here
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
        
        print("message sent to: ", email)
    except Exception as e:  
        print(e)# if the message fails to send due to some error
        print("Not sent to: ", email)
        


def compareData(CData, exp):
    req_exp= [x.strip() for x in CData.split(",")]
    x=set(req_exp)

    y=set(exp)
  
    z=x.difference(y)
   
    try:
        per= (len(x)-len(z))/len(x)
    except Exception as e:
        print("company data empty")
        per= 0
    return per
    

def extract_experience(experience, email):
    print("Extracting Experience for email:"+str(email))
    exp= [x.strip() for x in experience.split(",")]
    try:
        companyDf= pd.read_csv("sample_data.csv")
    except Exception as e:
        print(e)
        print("error reading company data")
        sys.exit()
        
    for i, row in companyDf.iterrows():
        perc_match= compareData(row["Work_requirement"],exp)
        print("pecentage match="+str(email)+ str(perc_match))
        if (perc_match> 0.3):
            sendMail(email=email,companyName= row["Company"], companyEmail= row["email_id"], perMatch= perc_match)
   

try:
    candidateDS= pd.read_csv("applicant_info.csv")
except Exception as e:
    print(e)
    print("File reading was unsuccessful")
    sys.exit()
    
#with Pool() as pool:
    #pool.starmap(extract_experience,[(row["experience"],row["email_address"],i) for i, row in candidateDS.iterrows()])

#emailRow= candidateDS["email_address"]

if __name__ == '__main__':
   experienceRow= candidateDS[["experience","email_address"]]
   procs=[]
   for i, rows in candidateDS.iterrows():
      proc= Process(target=extract_experience, args=(rows["experience"],rows["email_address"]))
      procs.append(proc)
      proc.start()
       
   for proc in procs:
      proc.join()