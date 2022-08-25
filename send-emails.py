import time
import pandas as pd
import numpy as np

haveRecievedEmail = []
df = pd.read_csv('linkedinbot/linkedin_cleaned.csv')

allStudents = df.to_dict('records')
def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

#TODO
def filterByMajorAndYear(students, major, year):
    result = []
    for s in students:
        if (((not pd.isnull(s["Department"])) and major[0] in s["Department"]) or ((not pd.isnull(s["Major"])) and major[1] in s["Major"])):
            if s["Year"] == year or (year == 3 and not pd.isnull(s["Department"])):
                result.append(s)
    return result
def sendEmailsTo(students): 
    for student in students:
        if student not in haveRecievedEmail:
            #TODO actually send email
            print("YOU NEED TO IMPLEMENT THE SEND EMAIL FUNCTION")
            haveRecievedEmail.append(student)

#listed in order of priority
majors = [("Philosophy", "Philosophy"), ("Mathematics", "Mathematics"), ("Political Science", "Political Science"), ("ZZZZZZZZZZZZZ", "Neuroscience"), ("Computer Science", "Computer Science"), ("EARTH INSTITUTE", "Sustainable Development")]
# 3 refers to juniors or seniors
years = [1,2,3]

# prioritize major and then year within major this will send emails to all students who I know have one of majors we are targeting
for major in majors:
    for year in years:
        matchingStudents = filterByMajorAndYear(allStudents, major, year)
        sendEmailsTo(matchingStudents)
                
# send to everyone with high gpa
highGPAPeeps = [s for s in allStudents if s["GPA"] != np.nan and s["GPA"] > 3.9]
sendEmailsTo(highGPAPeeps)

# then send emails to the rest of lowerclassmen who have linkedin profiles.
linkedInLowerClassmen = [s for s in allStudents if s["Year"] != np.nan and s["Year"] <=2]
sendEmailsTo(linkedInLowerClassmen)

# print(len(haveRecievedEmail))
# emails = [s["Email"] for s in haveRecievedEmail]
# for e in emails:
#     if (emails.count(e) > 1):
#         print(e)
#         print("DUPLICATE")
#         break
# pd.DataFrame.from_dict(haveRecievedEmail).to_csv(r"./email_order.csv", encoding='utf-8', index=False)
