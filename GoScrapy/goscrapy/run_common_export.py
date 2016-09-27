from model.common_item import CommonItem, CommonItemLine
from model.regular import Regular
import sys, os, csv

print 'Start Export ...'
if __name__ == "__main__":
    export_path = os.path.dirname(os.path.abspath(__file__))
    site_name = sys.argv[1]
    item_confg = Regular(name=site_name)
    if item_confg.data:
        all_items = CommonItem.query.filter_by(site_name=item_confg.name).all()
        try:
            export_fields = item_confg.export_fields.split(',')
        except AttributeError:
            export_fields = None
        if len(all_items):        
            with open('%s/export/%s.csv' % (export_path , site_name), 'wb') as csvfile:
                wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                if export_fields:
                    line_title = [('%s' % i).encode('utf-8').replace('_', ' ').title() for i in export_fields ]
                else:
                    line_title = [('%s' % i).encode('utf-8').title() for i in all_items[0].__dict__.keys() if i != '_sa_instance_state']
                    
                wr.writerow(line_title)
                
                for item in all_items:
                    _item=dict()
                    for i in item.__dict__:
                        if isinstance(getattr(item, i), (str,unicode,basestring,int,float)):
                            _item[i]=getattr(item, i)
                    if len(item.items):
                        for _i in item.items:
                            _item[_i.field]=_i.value
                            
                    if export_fields:
                        line_value = [' '.join(('%s' % _item[k]).encode('utf-8').split()) for k in export_fields if k in _item.keys() ]
                    else:
                        line_value = [' '.join(('%s' % i).encode('utf-8').split()) for i in _item.values() if not ('sqlalchemy.orm.state.InstanceState' in '%s' % i)]
                    wr.writerow(line_value)
    print 'Save to %s/export/%s.csv' % (export_path , site_name)