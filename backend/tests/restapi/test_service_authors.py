import pytest


@pytest.fixture
def post_paths(all_content, filter_items):
    paths = []
    posts = filter_items(all_content, "Post", False)
    for post in posts:
        parent = post["_container"]
        post_id = post["id"]
        paths.append(f"{parent}/{post_id}")
    return paths


class TestServiceAuthors:
    expander: str = "authors"
    endpoint: str = "/@authors"

    @pytest.fixture(autouse=True)
    def _init(self, portal, post_paths):
        self.portal = portal
        self.posts = post_paths

    def test_author_only_in_post(self, manager_request):
        url = f"{self.endpoint}"
        response = manager_request.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["@id"].endswith(self.endpoint)
        assert "items" not in data

    def test_author_information(self, manager_request):
        url = f"{self.posts[0]}{self.endpoint}"
        response = manager_request.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["@id"].endswith(self.endpoint)
        assert len(data["items"]) == 1
        author_info = data["items"][0]
        assert author_info["fullname"] == "Douglas Adams"
        scales = author_info["image_scales"]
        assert isinstance(scales, dict)
        assert "preview_image_link" in scales

    def test_author_expander(self, manager_request):
        url = f"{self.posts[0]}?expand={self.expander}"
        response = manager_request.get(url)
        assert response.status_code == 200
        data = response.json()
        authors = data["@components"]["authors"]
        assert isinstance(authors, dict)
        author_info = authors["items"][0]
        assert author_info["fullname"] == "Douglas Adams"
