from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from confirgration import collection
from database.schemas import list_todos
from database.models import Todo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


@router.get('/')
async def get_all_todos():
    data = collection.find({"is_deleted": False})
    return list_todos(data)


@router.post('/')
async def create_task(newtask: Todo):
    try:
        task_dict = dict(newtask)
        task_dict["created_at"] = datetime.timestamp(datetime.now())
        resp = collection.insert_one(task_dict)
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}')
async def update_task(id: str, updated_task: Todo):
    try:
        obj_id = ObjectId(id)
        existing_task = collection.find_one({"_id": obj_id, "is_deleted": False})
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
        task_dict = dict(updated_task)
        task_dict["update_at"] = datetime.timestamp(datetime.now())
        resp = collection.update_one({"_id": obj_id}, {"$set": task_dict})
        return {"status_code": 200, "modified_count": resp.modified_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}')
async def delete_task(id: str):
    try:
        obj_id = ObjectId(id)
        existing_task = collection.find_one({"_id": obj_id, "is_deleted": False})
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
        resp = collection.update_one(
            {"_id": obj_id},
            {"$set": {"is_deleted": True, "update_at": datetime.timestamp(datetime.now())}}
        )
        return {"status_code": 200, "modified_count": resp.modified_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(router)



