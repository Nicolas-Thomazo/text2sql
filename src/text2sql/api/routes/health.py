from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(tags=["health"])


@router.post("/", response_model=str)
async def read_root(name_input: str):
    if not name_input:
        raise HTTPException(status_code=404, detail="Name not found")

    try:
        response = "Hello {name}, I'm up and runing!".format(name=name_input)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return response
