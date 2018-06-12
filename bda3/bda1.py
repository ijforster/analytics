# Code for Baysian Data Analysis exercises

# Chapter 1, exercise 9

# Simulation of a queuing problem: a clinic has three doctors. 
# Patients come into the clinic at random from 9 a.m., according to a Poisson process
# with time parameter 10 minutes: that is, the time after opening at which the 
# first patient appears follows an exponential distribution with expectation 10 minutes and then, 
# after each patient arrives the expected waiting time is independently exponentialy distributed,
# also with expectation 10 minutes. When a patient arrives, he or she waits until a doctor is available. 
# The amount of time spent by each doctor on each patient is a random variable, uniformly distributed between
# 5 and 20 minutes. The office stops admitting patients at 4 p.m, and closes when the last patient is 
# through with the doctor.

# (a) Simulate this process once. How many patients came to the office? How many had to wait
# for a doctor? What was their average wait? When did the office close?

# (b) Simulate the process 100 times and estimate the median and 50% interval for each of the
# summaries in (a)


import numpy as np
import math
import matplotlib.pyplot as plt
import uuid

#plt.plot(x, y, "o")
#plt.show()

def RandomAppointmentDuration() :
    return 5.0 + np.random.rand() * 15.0



bins = range(0 , 50)
#plt.hist(poissonDrawings, bins=bins)
#plt.show()

class Doctor:
    def __init__(self): 
        self.nextTimeAvailable = 0
        self.timeDoctorIsWorking = [(0.0,0.0)]
        self.id = uuid.uuid4()

    def NextAvailableTimeToSeePatient(self, time) :
        start, end = zip(*self.timeDoctorIsWorking)
        return max(end)

    def SeePatient(self, time) :
        appointmentDuration = time + RandomAppointmentDuration()
        self.timeDoctorIsWorking.append((time, appointmentDuration))

    def AppointmentFinishTime(self, appointmentTime) :
        for (s, e) in self.timeDoctorIsWorking :
            if s == appointmentTime : return e
        return None

class Patient :
    def __init__(self,arrival): 
        self.arrivalTime = arrival
        self.startTime = None
        self.finishTime = None
        

    def WaitTime(self) :
        return self.startTime - self.arrivalTime
        
    def AppointmentComplete(self) : return self.finishTime != None

class Office:

    doctors = {}
    def __init__(self, numberOfdoctors, openingTime, notionalClosingTime): 
        self.doctors = {}
        for i in range(1,numberOfdoctors):
            d = Doctor()
            self.doctors[d.id] = d
        numberOfDrawings = 100
        poissonDrawings = np.random.poisson(10, numberOfDrawings)
        arrivalTimes = np.cumsum(poissonDrawings)
        arrivalTime_to_patient = lambda x : Patient(x)
        patients = map(arrivalTime_to_patient, arrivalTimes)

        self.patientQueue = my_list = [x for x in patients if x.arrivalTime < notionalClosingTime] # list of patients
        self.openingTime = openingTime
        self.notionalClosingTime = notionalClosingTime

    def Run(self):

        for patient in self.patientQueue :

            # is a doctor available?
            busyDoctors = {}
            for docId in self.doctors :
                doctor = self.doctors[docId]
                nextAvailableTime = doctor.NextAvailableTimeToSeePatient(patient.arrivalTime)
                if (nextAvailableTime <= patient.arrivalTime) :
                    doctor.SeePatient(patient.arrivalTime)
                    patient.startTime = patient.arrivalTime
                    patient.finishTime = doctor.AppointmentFinishTime(patient.arrivalTime)
                    #print("patient seeing doctor " + str(doctor.id) + " start: " + str(patient.arrivalTime) + " finish: " + str(patient.finishTime))
                else : busyDoctors[doctor.id] = nextAvailableTime

            if (patient.AppointmentComplete() == False) :
                dictData = sorted(busyDoctors.items(),key=lambda x: x[1]) 
                id, nextAvailableTime = dictData[0]
                nextAvailableDoctor = self.doctors[id]
                nextAvailableDoctor.SeePatient(nextAvailableTime)
                patient.startTime = nextAvailableTime
                patient.finishTime = nextAvailableDoctor.AppointmentFinishTime(nextAvailableTime)
                del busyDoctors[id]
                #print("patient seeing doctor " + str(nextAvailableDoctor.id) + " start: " + str(patient.arrivalTime) + " finish: " + str(patient.finishTime))

    def NumberOfPatients(self) : return len(self.patientQueue)
    def PaitentsWhoHadToWait(self) : return [x for x in self.patientQueue if x.WaitTime() > 0.0] 
    def AverageWaitTime(self) : return np.mean([x.WaitTime() for x in self.PaitentsWhoHadToWait()])
    def ClosingTime(self) : return max([x.finishTime for x in office.patientQueue]) / 60.0 + office.openingTime


office = Office(3,9,7*60)
office.Run()

#print("Arrival\tStart\tFinish\tWait")
#for p in office.patientQueue :
    #print (str(p.arrivalTime) + "\t" + str(p.startTime) + "\t" + str(p.finishTime) + "\t" + str(p.WaitTime()))

print("Single simulation")
numberOfPatients = office.NumberOfPatients()
print("Number of patients = " + str(numberOfPatients))

patientsWhoHadToWait = office.PaitentsWhoHadToWait()
print("Number of patients who had to wait = " + str(len(patientsWhoHadToWait)))

#waitTime = [x.WaitTime() for x in patientsWhoHadToWait]
print("Average wait time = " + str(office.AverageWaitTime()))

finishTimes = [x.finishTime for x in office.patientQueue]
print("Office close time = " + str(office.ClosingTime()))

simulations = []
for i in range(1, 1000) :
    office = Office(3,9,7*60)
    office.Run()
    simulations.append(office)

numberOfPatients = [x.NumberOfPatients() for x in simulations]
averageWaitTime = [x.AverageWaitTime() for x in simulations]


bins = range(0 , 10)
plt.hist(averageWaitTime, bins=bins)
plt.show()

