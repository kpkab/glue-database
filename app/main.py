from fastapi import FastAPI, HTTPException, Request
from dotenv import dotenv_values
from fastapi.responses import JSONResponse
import boto3
from pydantic import BaseModel

config = dotenv_values(".env")
ACCESS_ID = config.get("aws_access_key_id")
ACCESS_KEY = config.get("aws_secret_access_key")
REGION = config.get("aws_region")


client = boto3.client('glue', aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=ACCESS_KEY, region_name=REGION)


app = FastAPI(openapi_url="/app/openapi.json",docs_url="/app/docs")


class Glue_database(BaseModel):
    Name: str
    Description: str

@app.post('/app/create_database')
async def create_database(glue_database:Glue_database, request: Request):
    """CREATE API TO CREATE DATABASE IN AWS GLUE
    
    Returns:
        _type_: _description_
    """
    body=await request.json()
    try:
        response = client.create_database(
            DatabaseInput=body
        )
        return JSONResponse({'status': response['ResponseMetadata']['HTTPStatusCode']}, media_type="application/custom+json")
    except Exception as e:
        return {"Error in creating Database": str(e)}


@app.delete('/app/delete_database/{database_name}')
async def delete_database(database_name: str):
    """API TO DELETE DATABASE USING DATABASE NAME

    Args:
        database_name (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        response = client.delete_database(
            CatalogId='string',
            Name=database_name
        )
        return {'status': response['ResponseMetadata']['HTTPStatusCode']}
    except Exception as e:
        return {"Error in deleting Database": str(e)}


@app.get('/app/get_database/{database_name}')
async def get_database(database_name: str):
    """API TO FETCH DATABASE USING DATABASE NAME IN THE URL

    Args:
        database_name (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        database = client.get_database(
            Name=database_name)
        return database
    except Exception as e:
        return {"Error in Fetching Database": str(e)}


@app.get('/app/get_all_database')
async def get_all_database():
    """API TO FETCH ALL DATABASE PRESENT 

    Returns:
        _type_: _description_
    """
    try:
        databases = client.get_databases()
        return {"databases": databases['DatabaseList']}
    except Exception as e:
        return {"error": str(e)}


@app.put("/app/update")
async def update_database(glue_database:Glue_database, request : Request):
    """API TO UPDATE THE DATABASE

    Returns:
        _type_: _description_
    """
    body = await request.json()
    try:
        database = client.get_database(
            Name=body.get('Name'))
    except client.exceptions.EntityNotFoundException:
        raise HTTPException(status_code=404, detail="Database not found")
    # database['Database']['Name'] = database_name
    # database['Database']['Description'] = description
    client.update_database(Name=body.get('Name'), DatabaseInput=body)

    return {"message": f"Database '{body.get('Name')}' updated successfully"}