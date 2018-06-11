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
# for a doctor? WHat was their average wait? When did the office close?

# (b) Simulate the process 100 times and estimate the median and 50% intervalfor each of the
# summaries in (a)


import numpy as np


def Poisson(x, lamda) :
    return np.exp(-lamda * x)

x = Poisson(1.0,1.0)
print(x)

def RandomAppointmentDuration() :
    return 5.0 + np.random() * 15.0

class Doctor:
    nextTimeAvailable = 0
    def AvailableToSeePatient(self, time) :
        if time > nextTimeAvailable :
            nextTimeAvailable = time + RandomAppointmentDuration()
            return True
        else : return false



class Office:
    patientQueue = [] # list of patients
    doctors = [Doctor] # list of doctors
    openingTime = 0
    notionalClosingTime = 7.0