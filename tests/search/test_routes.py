from unittest.mock import patch
from config.app import application
from fastapi.testclient import TestClient


client = TestClient(application)


def test_products_by_search_id():
    mock_search_id = "64eb783090d46102583f00bd"
    mock_url = f"/apiv1/search/products/{mock_search_id}"
    mock_products = {
        "data": [
            {
                "products": {
                    "url": "https://articulo.mercadolibre.com.co/MCO-1789174042",
                    "product_id": "64eb783490d46102583f00be",
                    "ecommerce": "mercadolibre"
                }
            },
        ],
        "total_searches": 1,
        "search_id": mock_search_id,
        "msg": "ok"
    }

    with patch("app.search.controller.db_search.get_products_by_search_id", return_value=mock_products):
        response = client.get(mock_url)
        assert response.status_code == 200
        data = response.json()
        assert data == mock_products
