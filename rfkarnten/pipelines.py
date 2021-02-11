# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class RfkarntenPipeline:
    # Database setup
    conn = sqlite3.connect('RaiffeisenKarnten.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute("""CREATE TABLE IF NOT EXISTS articles
                 (title text, link text, content text)""")

    def process_item(self, item, spider):
        self.c.execute("""SELECT * FROM articles WHERE title = ? """,
                       (item.get('title'), ))
        duplicate = self.c.fetchall()
        if len(duplicate):
            return item
        print(f"New entry added at {item['link']}")

        # Insert values
        self.c.execute("INSERT INTO articles (title, link, content)"
                       "VALUES (?,?,?)", (item.get('title'), item.get('link'), item.get('content')))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()