from backend.app import app


def test_unauthenticated_customer():
    with app.test_client() as client:
        response = client.get("/main")

        assert response.status_code == 302


def test_unauthenticated_employee():
    with app.test_client() as client:
        response = client.get("/main/employee")

        assert response.status_code == 302


def test_customer_cannot_access_employee():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 4
            session["account_type"] = "customer"

        response = client.get("/main/employee")

        assert response.status_code == 403


def test_employee_cannot_access_customer():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 5
            session["account_type"] = "employee"

        response = client.get("/main")

        assert response.status_code == 403