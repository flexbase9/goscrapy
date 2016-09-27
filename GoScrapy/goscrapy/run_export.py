from model.config import DBSession
from model.item import Item
from model.rule import Regular
import sys, os, csv

print 'Start Export ...'
if __name__ == "__main__":
    db=DBSession()
    export_path=os.path.dirname(os.path.abspath(__file__))
    site_name=sys.argv[1]
    all_items = db.query(Item).filter(Item.site_name==site_name).all()
    item_confg=db.query(Regular).filter(Regular.name==site_name).first()
    export_fields=None
    if item_confg:
        export_fields=item_confg.export_fields.split(',')
        
    if all_items:        
        with open('%s/export/%s.csv' % (export_path ,site_name ),'wb') as csvfile:
            wr = csv.writer(csvfile,quoting=csv.QUOTE_ALL)
            if export_fields:
                line_title=[('%s' % i).encode('utf-8').replace('_',' ').title() for i in export_fields if i in all_items[0].__dict__.keys() ]
            else:
                line_title=[('%s' % i).encode('utf-8').title() for i in all_items[0].__dict__.keys() if i!='_sa_instance_state']
            wr.writerow(line_title)
            for item in all_items:
                dict_item = item.__dict__
                if export_fields:
                    line_value=[' '.join(('%s' % dict_item[k]).encode('utf-8').split()) for k in export_fields if k in dict_item.keys() ]
                else:
                    line_value=[' '.join(('%s' % i).encode('utf-8').split()) for i in dict_item.values() if not ('sqlalchemy.orm.state.InstanceState' in '%s' % i)]
                wr.writerow(line_value)
    print 'Save to %s/export/%s.csv' % (export_path ,site_name )