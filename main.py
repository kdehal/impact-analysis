import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pydantic import BaseModel

class Item(BaseModel):
    dependants: list

def connectToMongoServer(databasename):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    return myclient

myclient=connectToMongoServer("localhost")

def getDatabase(myclient,databasename):

    mydb = myclient[databasename]
    return mydb

mydb=getDatabase(myclient,"impact")

def getDBCollection(mydb,collectionName):
    mycol = mydb[collectionName]
    return mycol

mycol=getDBCollection(mydb,"objects")

def listDBs(myclient):
    dblist = myclient.list_database_names()
    #if "mydatabase" in dblist:
    #    print("The database exists.")
    return dblist

dblist=listDBs(myclient)


myquery = { 
    "SourceSystem": "Windchill",
    "SourceID":"OID:wt.part.WTPart:12345433"
 }

#mydoc = mycol.find(myquery)

#for x in mydoc:
#  print(x) 



mydict = { 
    "SourceSystem": "Windchill",
    "SourceID": "OID:wt.part.WTPart:12345433",
    "Number":"123-123-1234",
    "Name":"Part Name",
    "Version":"A" 
    }

#x = mycol.insert_one(mydict)

#print(x.inserted_id) 


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def getWindchillAttributes(UniqueID):
    #get Number,Version,Type,View,isLatestReleased
    SourceSystem="Windchill"
    Number=f"{UniqueID}-Unknown Number"
    Version="Unknown Version"
    Type="Unknown Type"
    View="Unknown View"
    Status="Unknown Status"
    response={"Source":SourceSystem,"Number":Number,"Version":Version,"Type":Type,"View":View,"Status":Status}
    return response

def hydrateRecordList(recordList: list):
    output=[]
    for record in recordList:
        Source,UniqueID=record.split("_")
        if Source=="Windchill":
            output.append(getWindchillAttributes(UniqueID))

    return output

def getVR(Number,Version,Type,View):
    #call Windchill API to get VR OID
    VRoid="100"#placeholder
    return VRoid

def get_record_id(Source,Number,Version,Type,View="EBOM"):
    record_id="100"
    #go to source system and get unique ID
    if Source=="Windchill":
        VRoid=getVR(Number,Version,Type,View)
        record_id=f"Windchill_{VRoid}"
    return record_id

def checkRecordStatus(SourceSystem,Number,Version):
    return "unknown"

def queryDatabase(record_id):
    query={"_id":record_id}
    return mycol.find_one(query)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/upstream_impact/{Source}/{Number}/{Version}/{Type}")
async def get_upstream_impact(Source: str,Number: str,Version: str,Type: str):
    record_id=get_record_id(Source,Number,Version,Type)
    record = queryDatabase(record_id)
    upstream_record_list=record['dependants']
    hyrdatedRecords = hydrateRecordList(upstream_record_list)
    return hyrdatedRecords


@app.post("/upstream_impact/{Source}/{Number}/{Version}/{Type}")
async def update_upstream_impact(Source: str,Number: str,Version: str,Type: str, request_body: Item):
    record_id=get_record_id(Source,Number,Version,Type)
    dependantList=[]
    for dependant in request_body.dependants:
        dependant_id=get_record_id(dependant.Source,dependant.Number,dependant.Version,dependant.Type)
        dependantList.append(dependant_id)
    newvalues = { "$set": { "_id":record_id, 'dependants': dependantList } }
    query={"_id":record_id}
    databaseOutput = mycol.update_one(query,newvalues,upsert=True)#update record, or create it if needed
    updatedRecord = queryDatabase(record_id)
    return updatedRecord

@app.get("/record/{record_id}")
async def get_records(record_id: str):
    record = queryDatabase(record_id)
    response=hydrateRecord(record)
    return mydoc

@app.post("/record/{record_id}")
async def update_records(record_id: str, item: Item):
    newvalues = { "$set": { "_id":record_id, 'dependants': item.dependants } } 
    query={"_id":record_id}
    x = mycol.update_one(query,newvalues,upsert=True)#update record, or create it if needed
    #print(x)
    mydoc = mycol.find_one(query)
    return mydoc

@app.get("/upstream-impact/{number}")
def get_impact(number):
    recordList=[]
    #result={}
    myquery = { 
        "SourceSystem": "Windchill",
        "Number":number,
        "Version":"A"
    }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        #print(x)
        #result[x["_id"]]=x
        SourceSystem=x['SourceSystem']
        Number=x['Number']
        Version=x['Version']
        Status=checkRecordStatus(SourceSystem,Number,Version)
        recordList.append({"Source":SourceSystem,"Number":Number,"Version":Version,"Status":Status})
    #recordList.append({"Source":"Windchill","Number":"123-123-1234","Version":"A","Status":"Being Changed"})
    #recordList.append({"Source":"Jules","Number":"123456","Version":"4","Status":"Upto Date"})
    #recordList.append({"Source":"Doors NG","Number":"R001","Version":"A","Status":"Out of Date"})
    return recordList


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)