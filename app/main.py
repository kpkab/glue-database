import boto3
import botocore
from app.model import (ErrorResponse, ExceptionResponse, Glue_database,
                       SuccessResponse)
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

config = dotenv_values(".env")
ACCESS_ID = config.get("aws_access_key_id")
ACCESS_KEY = config.get("aws_secret_access_key")
REGION = config.get("aws_region")


client = boto3.client('glue', aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=ACCESS_KEY, region_name=REGION)


app = FastAPI(openapi_url="/database/openapi.json", docs_url="/database/docs")


@app.post('/database/create_database')
async def create_database(glue: Glue_database):
    """CREATE API TO CREATE DATABASE IN AWS GLUE

    Returns:
        _type_: _description_
    """
    try:
        response = client.create_database(
            DatabaseInput={
                'Name': glue.Name,
                'Description': glue.Description
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'AlreadyExistsException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ResourceNumberLimitExceededException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InternalServiceException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'GlueEncryptionException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ConcurrentModificationException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'FederatedResourceAlreadyExistsException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.delete('/database/delete_database/{database_name}')
async def delete_database(database_name: str):
    """API TO DELETE DATABASE USING DATABASE NAME

    Args:
        database_name (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        response = client.delete_database(
            Name=database_name
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InternalServiceException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ConcurrentModificationException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/database/get_database/{database_name}')
async def get_database(database_name: str):
    """API TO FETCH DATABASE USING DATABASE NAME IN THE URL

    Args:
        database_name (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        response = client.get_database(
            Name=database_name)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response['Database'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InternalServiceException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'GlueEncryptionException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'FederationSourceException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/database/get_all_database')
async def get_all_database():
    """API TO FETCH ALL DATABASE PRESENT 

    Returns:
        _type_: _description_
    """
    try:
        response = client.get_databases()
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response['DatabaseList'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InternalServiceException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'GlueEncryptionException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.put("/database/update")
async def update_database(glue: Glue_database):
    """API TO UPDATE THE DATABASE

    Returns:
        _type_: _description_
    """
    try:
        response = client.update_database(
            Name=glue.Name,
            DatabaseInput={
                'Name': glue.Name,
                'Description': glue.Description})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'InternalServiceException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'GlueEncryptionException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ConcurrentModificationException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()
