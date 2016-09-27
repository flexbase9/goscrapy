from scrapy.dupefilters import RFPDupeFilter
from model.config import DBSession
from model.item import Item
from model.common_item import CommonItem

class DeepFilter(RFPDupeFilter):
    
    def __init__(self, path=None, debug=False):
        self.db = DBSession()
        super(DeepFilter, self).__init__(path, debug)
    
    def request_seen(self, request):
        _item = self.db.query(Item).filter(Item.from_url == request.url).filter(Item.name != None).first()
        if _item:
            return True
        else:
            return super(DeepFilter, self).request_seen(request)

class CommonFilter(RFPDupeFilter):
    
    count = 0
    
    def request_seen(self, request):
        item = CommonItem.query.filter_by(from_url=request.url).first()
        self.count+=1
        
        if item and item.items and len(item.items) > 0:
            print 'Skipped %s: %s' % (self.count, request.url)
            return True
        else:
            return super(CommonFilter, self).request_seen(request)
