from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from ..models.schemas import DashboardStats, User
from ..services.auth_service import auth_service

router = APIRouter(prefix="/api/v1", tags=["dashboard"])

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(auth_service.get_current_active_user)
):
    """Obtiene estadísticas del dashboard"""
    try:
        # Datos simulados del dashboard
        # En una implementación real, estos datos vendrían de Odoo
        stats = DashboardStats(
            total_products=25,
            total_sales=4699.95,
            total_customers=5,
            pending_orders=1,
            low_stock_products=3,
            monthly_revenue=12500.00,
            top_selling_product="Refrigerador Samsung RT38K5982BS",
            recent_sales=[
                {
                    "id": 1,
                    "customer_name": "Juan Pérez",
                    "product_name": "Refrigerador Samsung RT38K5982BS",
                    "total": 899.99,
                    "date": "2024-01-15"
                },
                {
                    "id": 2,
                    "customer_name": "María García",
                    "product_name": "Lavadora LG F4WV5012S0W",
                    "total": 649.99,
                    "date": "2024-01-14"
                },
                {
                    "id": 3,
                    "customer_name": "Carlos López",
                    "product_name": "Televisor Sony KD-55X80J",
                    "total": 1599.98,
                    "date": "2024-01-13"
                }
            ]
        )
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas del dashboard: {str(e)}")

@router.get("/dashboard/categories")
async def get_categories(
    current_user: User = Depends(auth_service.get_current_active_user)
):
    """Obtiene categorías de productos"""
    try:
        # Datos simulados de categorías
        # En una implementación real, estos datos vendrían de Odoo
        categories = [
            {"id": 1, "name": "Refrigeradores", "count": 8},
            {"id": 2, "name": "Lavadoras", "count": 6},
            {"id": 3, "name": "Televisores", "count": 5},
            {"id": 4, "name": "Microondas", "count": 4},
            {"id": 5, "name": "Lavavajillas", "count": 2}
        ]
        
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo categorías: {str(e)}")
