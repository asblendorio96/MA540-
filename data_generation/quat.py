# -*- coding: utf-8 -*-
"""
TITLE:      quat.py
DATE:       02-03-2022
AUTHOR:     MA540 Team 4
    
DESCRIPTION:
    
A quaternion object class.
Operators have been overriden for quaternion arithmetic.
    
"""

import numpy as np

class Quat:
    
    # Class Variables
    q0 = 0;             # Scalar Component
    q1 = 0;             # i Component
    q2 = 0;             # j Component
    q3 = 0;             # k Component
    
    # Constructor
    def __init__(self, q0=0, q1=0, q2=0, q3=0):
        self.q0 = q0;
        self.q1 = q1;
        self.q2 = q2;
        self.q3 = q3;
        
    # Set Quaternion Values    
    def setValues(self, q0, q1, q2, q3):
        self.q0 = q0;
        self.q1 = q1;
        self.q2 = q2;
        self.q3 = q3;
        
    # Set With Axis and Angle
    def setAngleAxis(self, angle, axis):
        # axis : numpy array with 3 elements
        # Normalize
        normAxis = axis / np.sqrt(np.sum(axis**2))
        
        # Vector Component
        v = np.sin(angle/2)*normAxis
        
        # Scalar Component
        q0 = np.cos(angle/2);
        
        # Assign Quaternion Values
        self.q0 = q0;
        self.q1 = v[0]
        self.q2 = v[1]
        self.q3 = v[2] 
        
    # Normalize this quaternion
    def normalize(self):
        mag = self.getMagnitude()
        if mag == 0:
            raise Exception("Cannot normalize quaternion with magnitude of 0");
        else:
            self.q0 /= mag;
            self.q1 /= mag;
            self.q2 /= mag;
            self.q3 /= mag;
            
    # Return Rotation Angle
    def getAngle(self):
        return np.arccos(self.q0)*2
    
    # Return Rotation Axis
    def getAxis(self):
        halfSin = np.sin(self.getAngle()/2);
        return np.array([self.q1,self.q2,self.q3])/halfSin;
    
    # Return Magnitude of Quaternion
    def getMagnitude(self):
        return np.sqrt(self.q0**2 + self.q1**2 + self.q2**2 + self.q3**2);
    
    # Conjugate
    def conj(self):
        return Quat(self.q0,-self.q1,-self.q2,-self.q3)
    
    # Inverse
    def inv(self):
        qconj = self.conj();
        mag2  = self.getMagnitude()**2;
        return Quat(qconj.q0/mag2,qconj.q1/mag2,qconj.q2/mag2,qconj.q3/mag2)
        
    ## OPERATORS ##
        
    # Quaternion Multiplication
    def __mul__(self,other):
        q0 = self.q0*other.q0-self.q1*other.q1-self.q2*other.q2-self.q3*other.q3
        q1 = self.q0*other.q1+self.q1*other.q0+self.q2*other.q3-self.q3*other.q2
        q2 = self.q0*other.q2-self.q1*other.q3+self.q2*other.q0+self.q3*other.q1
        q3 = self.q0*other.q3+self.q1*other.q2-self.q2*other.q1+self.q3*other.q0
        return Quat(q0,q1,q2,q3)
    
    # Quaternion Addition
    def __add__(self,other):
        return Quat(self.q0+other.q0,self.q1+other.q1,self.q2+other.q2,self.q3+other.q3)
    
    # Quaternion Subtraction
    def __sub__(self,other):
        return Quat(self.q0-other.q0,self.q1-other.q1,self.q2-other.q2,self.q3-other.q3)
    
    # Quaternion Division
    def __truediv__(self,other):
        return self*other.inv()
    