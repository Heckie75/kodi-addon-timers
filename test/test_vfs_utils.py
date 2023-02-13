import os
import unittest

from resources.lib.utils import vfs_utils


class TestVfsUtils(unittest.TestCase):

    def test_is_playlist(self):

        self.assertEqual(vfs_utils.is_playlist("/a/b/c/file.mp3"), False)
        self.assertEqual(vfs_utils.is_playlist("/a/b/c/file.pls"), True)
        self.assertEqual(vfs_utils.is_playlist("/a/b/c/file.m3u"), True)
        self.assertEqual(vfs_utils.is_playlist("/a/b/c/file.m3u8"), True)
        self.assertEqual(vfs_utils.is_playlist("/a/b/c/"), False)

    def test_is_musicdb(self):

        self.assertEqual(vfs_utils.is_musicdb("musicdb://a/b/c.mp3"), True)
        self.assertEqual(vfs_utils.is_musicdb("videodb://a/b/c.mp3"), False)

    def test_is_videodb(self):

        self.assertEqual(vfs_utils.is_videodb("videodb://a/b/c.avi"), True)
        self.assertEqual(vfs_utils.is_videodb("musicdb://a/b/c.mp3"), False)

    def test_is_pvr(self):

        self.assertEqual(vfs_utils.is_pvr("pvr://a/b/c.pvr"), True)
        self.assertEqual(vfs_utils.is_pvr("musicdb://a/b/c.mp3"), False)

    def test_is_pvr_channel(self):

        self.assertEqual(vfs_utils.is_pvr_channel(
            "pvr://channels/radio/12345/12345.pvr"), True)
        self.assertEqual(vfs_utils.is_pvr_channel(
            "pvr://recordsings/12345/12345.pvr"), False)

    def test_is_pvr_recording(self):

        self.assertEqual(vfs_utils.is_pvr_recording(
            "pvr://recordings/12345/12345.pvr"), True)
        self.assertEqual(vfs_utils.is_pvr_recording(
            "pvr://channels/radio/12345/12345.pvr"), False)

    def is_pvr_tv_channel(self):

        self.assertEqual(vfs_utils.is_pvr_tv_channel(
            "pvr://channels/tv/madtv.pvr"), True)
        self.assertEqual(vfs_utils.is_pvr_tv_channel(
            "pvr://channels/radio/radio.pvr"), False)

    def test_is_pvr_radio_channel(self):

        self.assertEqual(vfs_utils.is_pvr_radio_channel(
            "pvr://channels/radio/radio.pvr"), True)
        self.assertEqual(vfs_utils.is_pvr_radio_channel(
            "pvr://channels/tv/madtv.pvr"), False)

    def test_is_supported_media(self):

        pass

    def test_get_media_type(self):

        pass

    def test_build_path_to_ressource(self):

        self.assertEqual(vfs_utils.build_path_to_ressource(
            "musicdb://a/b/c/", "file.mp3"), "musicdb://file.mp3")
        self.assertEqual(vfs_utils.build_path_to_ressource(
            "videodb://a/b/c/", "file.avi"), "videodb://file.avi")
        self.assertEqual(vfs_utils.build_path_to_ressource(
            "/home/user/a/b/c/", "file.avi"), "/home/user/a/b/c/file.avi")

    def test_get_file_extension(self):

        self.assertEqual(vfs_utils.get_file_extension(
            "plugin://test/1/2/4.jpg"), ".jpg")
        self.assertEqual(vfs_utils.get_file_extension(
            "plugin://test/1/2/"), None)

    def test_get_longest_common_path(self):

        files = ["plugin://test/1/2/3.jpg", "plugin://test/1/2/4.jpg",
                 "plugin://test/1/2/2/6.jpg", "plugin://test/1/2/6.jpg"]
        s = vfs_utils.get_longest_common_path(files)
        self.assertEqual(s, "plugin://test/1/2/")

    def test_is_uri(self):

        self.assertEqual(vfs_utils.is_uri("plugin://test/1/2/3.jpg"), True)

        path = "A:/a/b/c/".replace("/", os.sep)
        self.assertEqual(vfs_utils.is_uri(path), False)

    def test_is_external(self):

        self.assertEqual(vfs_utils.is_external("plugin://test/1/2/"), False)
        self.assertEqual(vfs_utils.is_external("http://test/1/2/"), True)
        self.assertEqual(vfs_utils.is_external("https://test/1/2/"), True)

    def test_is_favourites(self):

        self.assertEqual(vfs_utils.is_favourites(
            "favourites://PlayMedia(%22plugin%3a%2f%2fplugin.audio.radio_de%2fstation%2f3307%22)/"), True)
        self.assertEqual(vfs_utils.is_favourites("plugin://test/1/2/"), False)

    def test_get_favourites_target(self):

        target = vfs_utils.get_favourites_target(
            "favourites://PlayMedia(%22plugin%3a%2f%2fplugin.audio.radio_de%2fstation%2f3307%22)/")
        self.assertEqual(
            target, "plugin://plugin.audio.radio_de/station/3307")

    def test_is_script(self):

        self.assertEqual(vfs_utils.is_script("script://script.pasink/"), True)
        self.assertEqual(vfs_utils.is_script("plugin://script.pasink/"), True)
        self.assertEqual(vfs_utils.is_script("script.pasink/"), True)

        self.assertEqual(vfs_utils.is_script(
            "script://plugin.audio.radio/"), False)
        self.assertEqual(vfs_utils.is_script(
            "plugin://plugin.audio.radio/"), False)
        self.assertEqual(vfs_utils.is_script(
            "/home/user/music/song.mp3"), False)

    def test_get_file_name(self):

        self.assertEqual(vfs_utils.get_file_name(
            "script://script.pasink/media.mp3"), "media")
        self.assertEqual(vfs_utils.get_file_name(
            "/script.pasink/media.mp3"), "media")
        self.assertEqual(vfs_utils.get_file_name("/media.mp3"), "media")
        self.assertEqual(vfs_utils.get_file_name("media.mp3"), "media")
        self.assertEqual(vfs_utils.get_file_name("media"), "media")
        self.assertEqual(vfs_utils.get_file_name("script://path.ext/"), None)
