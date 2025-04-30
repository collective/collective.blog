import pytest


class TestControlPanel:
    base_endpoint: str = "/@controlpanels"
    configlet_id: str = "blog-controlpanel"

    def test_controlpanel_is_available_anon(self, anon_request):
        response = anon_request.get(self.base_endpoint)
        assert response.status_code == 401
        data = response.json()
        assert isinstance(data, dict)
        assert data["type"] == "Unauthorized"

    def test_controlpanel_is_available_manager(self, manager_request):
        response = manager_request.get(self.base_endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        filtered = [item for item in data if item["@id"].endswith(self.configlet_id)]
        assert len(filtered) == 1
        controlpanel = filtered[0]
        assert controlpanel["title"] == "Blog Settings"

    def test_controlpanel_get(self, manager_request):
        url = f"{self.base_endpoint}/{self.configlet_id}"
        response = manager_request.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "schema" in data

    @pytest.mark.parametrize(
        "attr,type_,expected",
        [
            ("enable_authors_folder", bool, True),
        ],
    )
    def test_controlpanel_default_values(self, manager_request, attr, type_, expected):
        url = f"{self.base_endpoint}/{self.configlet_id}"
        response = manager_request.get(url)
        data = response.json()
        value = data["data"][attr]
        assert isinstance(value, type_)
        if type_ in (bool, None):
            assert value is expected
        else:
            assert value == expected

    @pytest.mark.parametrize(
        "attr,type_,value",
        [
            ("enable_authors_folder", bool, False),
        ],
    )
    def test_controlpanel_update(self, manager_request, attr, type_, value):
        url = f"{self.base_endpoint}/{self.configlet_id}"
        # Update values
        new_values = {attr: value}
        response = manager_request.patch(url, json=new_values)
        assert response.status_code == 204
        # Check values are persisted
        response = manager_request.get(url)
        data = response.json()
        new_value = data["data"][attr]
        assert isinstance(new_value, type_)
        if type_ in (bool, None):
            assert new_value is value
        else:
            assert new_value == value
