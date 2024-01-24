# from typing import List
#
# from fastapi import APIRouter, status, Depends, Query, HTTPException
# from sqlalchemy.orm import Session
# from nashafirma_fastapi.database.db import get_db
# from nashafirma_fastapi.repository import profiles as repository_profiles
# from nashafirma_fastapi.schemas.profiles import Inprofile, Outprofile
#
#
# router = APIRouter(prefix="/profiles", tags=["profiles"])
#
#
#
# @router.get("/{profile_id}", response_model=List[Outprofile], status_code=status.HTTP_200_OK)
# async def all_profiles(order_id: int, limit: int = Query(3, ge=0, le=100), offset: int = 0, db: Session = Depends(get_db)):
#     result = await repository_profiles.get_profiles(order_id, limit, offset, db)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profiles not found")
#     return result
#
#
# @router.post("/", response_model=Outprofile, status_code=status.HTTP_201_CREATED)
# async def create_profile(body: Inprofile, db: Session = Depends(get_db)):
#     result = await repository_profiles.create(body, db)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
#     return result
#
# @router.put("/{profile_id}", response_model=Outprofile, status_code=status.HTTP_201_CREATED)
# async def update_profile(profile_id: int, body: Inprofile, db: Session = Depends(get_db)):
#     result = await repository_profiles.update(profile_id, body, db)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
#     return result
#
#
# @router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def remove_profile(profile_id: int, db: Session = Depends(get_db)):
#     result = await repository_profiles.remove(profile_id, db)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
#     return result

