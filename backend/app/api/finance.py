from fastapi import APIRouter
from schemas import AssetSchema
from repository import AssetsRepository
from fastapi import HTTPException

router = APIRouter(
    prefix="/assets",
    tags=["assets"]
)


@router.post("/")
async def add_ticker(body: AssetSchema):
    try:
        ticker = await AssetsRepository.add_asset(body)
        return {"ticker": ticker}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[AssetSchema])
async def get_assets():
    assets = await AssetsRepository.all_assets()
    return assets


@router.get("/{asset_ticker}")
async def get_asset(asset_ticker: str) -> AssetSchema:
    asset = await AssetsRepository.get_asset(asset_ticker)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_ticker}")
async def delete_asset(asset_ticker: str):
    success = await AssetsRepository.delete_asset(asset_ticker)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted"}
