
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# This class is used to process the items scraped by the spider.
class RobotoPipeline:
    def process_item(self, item, spider):
        return item
