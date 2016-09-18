from scrapy.dupefilters import RFPDupeFilter
from model.config import DBSession
from model.item import Item

class DeepFilter(RFPDupeFilter):
    
    def __init__(self, path=None, debug=False):
        self.db=DBSession()
        super(DeepFilter,self).__init__(path, debug)
    
    def request_seen(self, request):
        _item = self.db.query(Item).filter(Item.from_url == request.url).first()
        if _item:
            return True
        else:
            return super(DeepFilter, self).request_seen(request)