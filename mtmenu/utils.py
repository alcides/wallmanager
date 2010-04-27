'''
Created on 2010/04/27

@author: msimoes
'''

from models import *

def getAllCategories():
    return CategoryProxy.objects.all()    
    
def getAllApplications():
    return ApplicationProxy.objects.all()

def getApplicationsOfCategory(cat):
    return ApplicationProxy.objects.filter(category = cat)