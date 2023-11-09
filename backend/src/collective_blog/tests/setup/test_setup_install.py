from collective_blog import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if collective_blog is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that ICollectiveBlogLayer is registered."""
        from collective_blog.interfaces import ICollectiveBlogLayer

        assert ICollectiveBlogLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "20231109001"
