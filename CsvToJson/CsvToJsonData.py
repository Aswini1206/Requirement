import csv,json, os
from datetime import datetime

class Personnel:
        
    def CalculateAge(self, dob):
        currentDate = datetime.now()
        dateofBirth= datetime.strptime(dob,'%m/%d/%Y')
        daysLeft = currentDate - dateofBirth
        years = ((daysLeft.total_seconds())/(365.242*24*3600))
        yearsInt=int(years)
        months=(years-yearsInt)*12
        monthsInt=int(months)
        return ("{} {} {} {}".format(yearsInt,("years" if yearsInt > 1 else "year"),monthsInt, ("months" if monthsInt > 1 else "month")))

    def FormatDateOfBirth(self, dob):
        dateOfBirth = datetime.strptime(dob,'%m/%d/%Y')
        return dateOfBirth.strftime("%d/%m/%Y")
        
        
        
    def LoadCommonDetails(self, row, commonRec):
        commonRec.update({
            "id" : row["id"],
            "fullName" : row["firstname"].title() + " " + row["lastname"].title(),
            "gender" : "Male" if row["gender"] == "m" else "Female", 
            "dob" : self.FormatDateOfBirth(row["dob"]),
            "age" : self.CalculateAge(row["dob"]),
            "aadhar" : row["aadhar_number"],
            "city" : row["city"],
            "contactNumber" : str(row["contact_number"])
        })

class StudentRecords(Personnel):

    def __init__(self):
        self.__recordCount = 0
        self.__studentList = []

    def PopulateStudentDetails (self, row, studentRec):
        studentRec.update({
                    "rollNo" : int(row["roll_no"]),
                    "className" : row["class"],
                    "totalMarks" : int(row["total_marks"]),
                    "secPercent" : int(row["sec_percent"]),
                    "hsStream" : row["hs_stream"]
                    })
        
    def UpdateStudentRecord(self, studentRec):
        self.__recordCount = self.__recordCount + 1
        self.__studentList.append(studentRec)

    def AddStudentRecord(self,row):
        studentRec = {}
        self.LoadCommonDetails(row, studentRec)
        self.PopulateStudentDetails(row, studentRec)
        self.UpdateStudentRecord(studentRec)

    def CreateStudentsRecordJsonFile(self, jsonPath, fileName):
        studentData = {"studentRecordCount": self.__recordCount, 'data': self.__studentList}
        file = open(os.path.join(jsonPath, fileName), "w")
        file.write(json.dumps(studentData, indent=4))
        file.close()

class TeacherRecords (Personnel):
    
    def __init__(self):
        self.__recordCount = 0
        self.__teachersList = []

    def CalculateServicePeriod(self, doj):
        currentDate   = datetime.now()
        dateofJoining = datetime.strptime(doj,'%m/%d/%Y')
        daysLeft      = currentDate - dateofJoining
        years         = ((daysLeft.total_seconds())/(365.242*24*3600))
        yearsInt      = int(years)
        months        = (years-yearsInt)*12
        monthsInt     = int(months)
        days          = (months-monthsInt)*(365.242/12)
        daysInt       = int(days)
        return ("{} {} {} {} {} {} ".format(yearsInt,("years" if yearsInt > 1 else "year"),monthsInt, ("months" if monthsInt > 1 else "month"), daysInt , ("days" if daysInt > 1 else "day")))
        
        
    def PopulateTeacherDetails(self, row, teacherRec):

        teacherRec.update({
                    "empNo" : row["emp_no"],
                    "classTeacher" : row["class_teacher_of"],
                    "doj" : row["doj"],
                    "servicePeriod" : self.CalculateServicePeriod(row["doj"]),
                    "previousSchool" : row['previous_school'],
                    "post" : row["post"],
                    "salary" : ("{:,.0f}".format(int(row["salary"])))
                    })
        
    def UpdateTeacherRecord(self, teacherRec):
        self.__recordCount=self.__recordCount+1
        self.__teachersList.append(teacherRec)

    def AddTeachersRecord(self, row):
        teacherRec = {}
        self.LoadCommonDetails(row, teacherRec)
        self.PopulateTeacherDetails(row, teacherRec)
        self.UpdateTeacherRecord(teacherRec)

    def CreateTeachersRecordJsonFile(self, jsonPath, fileName):
        teacherData = {"teacherRecordCount": self.__recordCount, 'data': self.__teachersList}
        file = open(os.path.join(jsonPath, fileName), "w")
        file.write(json.dumps(teacherData, indent=4))
        file.close()

## main class routine
class csvToJsonConverter:

    def __init__(self, csvFilepath, jsonPath):
        self.__studentRecObj = StudentRecords()
        self.__teacherRecObj = TeacherRecords()
        self.__csvFilePath   = csvFilepath
        self.__jsonFileStoragePath = jsonPath

    def GetStudentRefObj(self):
        return self.__studentRecObj

    def GetTeacherRefobj(self):
        return self.__teacherRecObj

    def ParseCSVToJSON(self):
        # reads the csv file
        with open(self.__csvFilePath) as csvFile:
            csvReader = csv.DictReader(csvFile)

            for row in csvReader:
                category=row['category']
                if category == 'student':
                    self.GetStudentRefObj().AddStudentRecord(row)
                    
                elif category == 'teacher':
                    self.GetTeacherRefobj().AddTeachersRecord(row)
                else:
                    print("none")

    def CreateJsonRecordFile(self, typeOfRecord):

        jsonPath = self.__jsonFileStoragePath
        if not os.path.exists(jsonPath):
            os.mkdir(jsonPath)

        todaysDate = (datetime.today()).strftime("%Y%m%d")
        
        
        if typeOfRecord == "student":
            fileName = "student_record_" + todaysDate + ".json"
            
            self.GetStudentRefObj().CreateStudentsRecordJsonFile(jsonPath, fileName)
        else:
            fileName = "teacher_record_" + todaysDate + ".json"
            self.GetTeacherRefobj().CreateTeachersRecordJsonFile(jsonPath, fileName)

csvFilePath='D:\Req\Resources\ValidInput.csv'
jsonPath='D:\Req\JsonFilePath'
csvObj = csvToJsonConverter(csvFilePath, jsonPath)
csvObj.ParseCSVToJSON()
csvObj.CreateJsonRecordFile("student")
csvObj.CreateJsonRecordFile("teacher")

        

    
