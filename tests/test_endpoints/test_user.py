"""
Set of test for the user endpoints.
"""
import pytest


class TestUserView:
    """Group of tests for `/user` endpoint."""

    def test_valid_user(self, client, db_session):
        """Test valid input data."""
        valid_data = {"name": "Valid Name", "email": "valid@email.com"}
        resp = client.post("/user", json=valid_data)

        assert resp.status_code == 201
        assert b"userId" in resp.data

    def test_valid_user_with_amount(self, client, db_session):
        """Test valid input data with an initial amount."""
        valid_data = {"name": "Valid Name", "email": "valid@email.com", "init_balance": "100.00"}
        resp = client.post("/user", json=valid_data)

        assert resp.status_code == 201
        assert b"userId" in resp.data

        user_id = resp.json["userId"]
        resp = client.get(f"/user/{user_id}/balance")

        assert b"100.00" in resp.data

    def test_invalid_request_data(self, client, db_session):
        """Test with invalid input data."""
        invalid_data = {"name": "Valid Name", "email": "invalid_email"}
        resp = client.post("/user", json=invalid_data)

        assert resp.status_code == 400

    def test_duplicate_user(self, client, db_session):
        """Test invalid input data (duplicate user)."""
        input_data = {"name": "Valid Name", "email": "valid@email.com"}
        resp = client.post("/user", json=input_data)

        assert resp.status_code == 201

        resp = client.post("/user", json=input_data)

        assert resp.status_code == 403
        assert b"User already exists" in resp.data


@pytest.mark.usefixtures("user_view_init_data")
class TestUserBalanceView:
    """Group of tests for `/user/<id>/balance` endpoint."""

    def test_existing_user(self, client):
        """Test retrieving balance of existing user."""
        resp = client.get(f"/user/2/balance")

        assert resp.status_code == 200
        assert b"200.0" in resp.data

    def test_inexistent_user(self, client):
        """Test retrieving balance of inexistent user."""
        resp = client.get(f"/user/10/balance")

        assert resp.status_code == 403
        assert b"User not found" in resp.data


@pytest.mark.usefixtures("user_view_init_data")
class TestUserTransferView:
    """Group of tests for `/user/<id>/transfer` endpoint."""

    def test_valid_transfer(self, client):
        """Test valid transfer."""
        data_input = {"toUserId": 1, "amount": "50.00"}
        resp = client.post("/user/2/transfer", json=data_input)

        assert resp.status_code == 200
        assert b"done" in resp.data

        # Check recipient balance
        resp = client.get(f"/user/1/balance")

        assert b"50.00" in resp.data

        # Check sender balance
        resp = client.get(f"/user/2/balance")

        assert b"150.00" in resp.data

    def test_invalid_request_data(self, client):
        """Test with invalid input data (more than 2 decimals)."""
        invalid_data = {"toUserId": 1, "amount": "30.005"}
        resp = client.post("/user/2/transfer", json=invalid_data)

        assert resp.status_code == 400
        assert b" decimal digits allowed" in resp.data

    def test_not_enough_funds(self, client):
        """Test in valid transfer due to insufficient funds."""
        data_input = {"toUserId": 1, "amount": "300.00"}
        resp = client.post("/user/2/transfer", json=data_input)

        assert resp.status_code == 403
        assert b"Insufficient funds" in resp.data

    def test_inexistent_sender(self, client):
        """Test make a tranfer with inexistent sender."""
        data_input = {"toUserId": 1, "amount": "50.00"}
        resp = client.post("/user/5/transfer", json=data_input)

        assert resp.status_code == 403
        assert b"User not found" in resp.data

    def test_inexistent_recipient(self, client):
        """Test make a tranfer with inexistent recipient."""
        data_input = {"toUserId": 10, "amount": "50.00"}
        resp = client.post("/user/2/transfer", json=data_input)

        assert resp.status_code == 403
        assert b"User not found" in resp.data
