import unittest

from processors.google_drive_media import GoogleDriveMediaFolder


class _UpdateRequest:
    def __init__(self, response):
        self.response = response

    def execute(self):
        return self.response


class _FilesResource:
    def __init__(self):
        self.update_kwargs = None

    def update(self, **kwargs):
        self.update_kwargs = kwargs
        return _UpdateRequest(
            {
                "id": kwargs["fileId"],
                "name": "track.mp3",
                "webViewLink": "https://drive.example.test/file",
                "parents": [kwargs["addParents"]],
            }
        )


class _DriveService:
    def __init__(self):
        self.files_resource = _FilesResource()

    def files(self):
        return self.files_resource


class GoogleDriveMediaFolderTests(unittest.TestCase):
    def test_move_source_to_completed_reparents_file_from_active_inbox(self):
        folder = GoogleDriveMediaFolder(credentials=object(), folder_id="active-inbox")
        service = _DriveService()
        folder._service_instance = service
        folder.completed_folder_id = lambda name: "completed-folder"

        result = folder.move_source_to_completed({"id": "audio-id", "name": "track.mp3"})

        self.assertEqual(
            service.files_resource.update_kwargs,
            {
                "fileId": "audio-id",
                "addParents": "completed-folder",
                "removeParents": "active-inbox",
                "fields": "id,name,webViewLink,parents",
                "supportsAllDrives": True,
            },
        )
        self.assertEqual(result["file_id"], "audio-id")
        self.assertEqual(result["folder_name"], "upload_완료")


if __name__ == "__main__":
    unittest.main()
