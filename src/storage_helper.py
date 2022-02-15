import os
import pathlib
import shutil


class StorageHelper:
    DATA_DIRECTORY: str = 'scraped_data'
    IMG_DIRECTORY: str = 'images'
    CSV_DIRECTORY: str = 'csv'
    PARENT_DIRECTORY: str = '..'

    def __init__(self):
        self.current_path: str = self._get_current_path()
        self.data_directory_full_path: str = os.path.join(
            self.current_path,
            StorageHelper.PARENT_DIRECTORY,
            StorageHelper.DATA_DIRECTORY,
        )
        self.img_storage_path: str = os.path.join(
                                             self.data_directory_full_path,
                                             StorageHelper.IMG_DIRECTORY
                                             )
        self.csv_storage_path: str = os.path.join(
                                             self.data_directory_full_path,
                                             StorageHelper.CSV_DIRECTORY
                                             )

    def _get_current_path(self)  -> str:
        return pathlib.Path(__file__).parent.absolute()

    def _create_scraped_data_directories(self) -> None:
        shutil.rmtree(self.data_directory_full_path, ignore_errors=True)
        os.makedirs(self.img_storage_path)
        os.makedirs(self.csv_storage_path)
        print(f'\nWhere your data is stored ?\nIMG: {self.img_storage_path}\nCSV: {self.csv_storage_path}\n')

    def init_storage(self) -> None:
        self._create_scraped_data_directories()
