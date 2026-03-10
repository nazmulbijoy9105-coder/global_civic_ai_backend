from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models

# Reuse get_current_user and require_roles from earlier

def require_owner_or_roles(allowed_roles: list[str], resource_owner_id: int, current_user: models.User):
    """
    Allow access if the current user is the resource owner OR has one of the allowed roles.
    """
    if current_user.id != resource_owner_id and current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )
    return True

# --- Example Protected Route with Ownership Check ---

@router.get("/users/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Allow users to view their own profile, or admins to view any profile.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Ownership or role check
    require_owner_or_roles(["admin"], resource_owner_id=user.id, current_user=current_user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }