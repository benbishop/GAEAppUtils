__author__ = 'Ben'

from google.appengine.ext import webapp
from appmodels import Species
from appexceptions import PropertyDoesNotExistOnModelException


def createRequestModelFromWebRequest(request, fields):
    requestModel = {}
    for fieldName in fields:
        if request.get(fieldName).lower() == 'true':
            requestModel[fieldName] = True
        elif request.get(fieldName).lower() == 'false':
            requestModel[fieldName] = False
        elif str(request.get(fieldName)).strip('-').isdigit():
            requestModel[fieldName] = int(request.get(fieldName))
        elif str(request.get(fieldName)).replace('.', '').isdigit():
            requestModel[fieldName] = float(request.get(fieldName))
        else:
            requestModel[fieldName] = request.get(fieldName)

    if request.get('key'):
        requestModel['key'] = request.get('key')
        
    return requestModel


def updateModelFromRequestModel(model, requestModel):
    for fieldKey in requestModel:
        if fieldKey in model.fields():
            model.__setattr__(fieldKey, requestModel[fieldKey])
        elif fieldKey != 'key':
            raise PropertyDoesNotExistOnModelException(PropertyDoesNotExistOnModelException.TITLE,
                                                       PropertyDoesNotExistOnModelException.MESSAGE)


def createHashFromModel(model):
    simpleObject = {}
    for fieldKey in model.fields():
        if fieldKey != 'key':
            simpleObject[fieldKey] = model.__getattribute__(fieldKey)
    simpleObject['key'] = str(model.key())
    return simpleObject