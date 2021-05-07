# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy.orm import sessionmaker
from .models import SenatorDB, db_connect, create_table

#class QuantocustaumsenadorPipeline:
#    def process_item(self, item, spider):
#        return item

class QuantocustaumsenadorPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()
        senatordb = SenatorDB()

        exists = bool(session.query(SenatorDB).filter_by(url=item["url"]).first())

        if not exists:
            senatordb.name = item["name"]
            senatordb.url = item["url"]
            senatordb.party = item["party"]
            senatordb.fu = item["fu"]
            senatordb.period = item["period"]
            senatordb.phones = item["phones"]
            senatordb.email = item["email"]
            senatordb.address = item["address"]

            try:
                session.add(senatordb)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item