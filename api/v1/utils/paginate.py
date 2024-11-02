from fastapi import HTTPException
from sqlalchemy.orm import Session, Query
from sqlalchemy import func
from typing import Dict


def paginate_query(db: Session, query: Query, page: int = 1, limit: int = 10) -> Dict:
    """
    Paginate a SQLAlchemy query without explicitly passing a model.

    Parameters:
        - db: The SQLAlchemy session.
        - query: The SQLAlchemy query object.
        - page: Current page number.
        - limit: Number of items per page.

    Returns:
        - A dictionary containing the paginated results, total count, current page, next, and previous page indicators.
    """

    # Validate pagination parameters

    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400, detail="Page and limit must be greater than 0"
        )

    # Get the total count by creating a subquery to count the rows in the query

    total_count = query.with_entities(func.count()).scalar()

    # Calculate the offset

    offset = (page - 1) * limit

    # Fetch results for the current page with the limit and offset

    results = query.offset(offset).limit(limit).all()

    # Calculate next and previous page indicators

    next_page = page * limit < total_count  # True if there are more records
    prev_page = page > 1  # True if the current page is not the first page

    # Construct the paginated response

    return {
        "count": total_count,
        "page": page,
        "next": next_page,
        "prev": prev_page,
        "results": results,
    }
