from scraper import Scraper
from image_helper import ImageHelper
from storage_helper import StorageHelper

storage_helper: StorageHelper = StorageHelper()
storage_helper.init_storage()

image_helper: ImageHelper = ImageHelper(storage_helper)

scraper: Scraper = Scraper(storage_helper, image_helper)
scraper.run()
