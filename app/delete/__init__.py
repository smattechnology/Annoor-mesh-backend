from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.products.models import Product
from app.database import get_db

router = APIRouter(prefix="/product", tags=["Products"])

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """
    Delete a product by ID.
    Returns 204 No Content if successful.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    try:
        db.delete(product)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )
    return None
