from sqlalchemy import Column, Integer, String
from database import Base, db_session

class Regular(Base):
    
    __tablename__ = 'regulars'
    
    id = Column(Integer, primary_key=True)
    project = Column(String)
    field = Column(String)
    action = Column(String)
    field_to = Column(String)
    value = Column(String)
    data = None
    def __init__(self, project=None,name=None):
        self.project = project
        if name:
            this_name=self.query.filter_by(value=name).filter_by(field='name').first()
            if this_name:
                project=this_name.project
                
        if project:
            this_project = self.get_project_setting(project)
            if this_project:
                for key in this_project:
                    setattr(self, key, this_project[key])
         
    def get_project_setting(self, project_name):
        if project_name:
            values = self.query.filter_by(project=project_name).all()
            if len(values):
                self.data=values
                return dict((v.field, v.value) for v in values)
            return None
    
    def get_parse_setting(self,action=None):
        if not action:
            action='parse'
        _data=[]
        for data in self.data:
            if data.action==action:
                _data.append(data)
        for d in _data:
            yield d
            
    @classmethod
    def copy_project_to(cls, from_project, to_project):
        if from_project.lower() == to_project.lower():
            return None
        else:
            if len(from_project.strip(' ')) == 0:
                _from_project=cls.query.order_by(cls.id.desc()).first()
                if _from_project:
                    from_project=_from_project.project
            
                if len(cls.query.filter_by(project=to_project).all())>0:
                    print 'Project :%s exist!' % to_project
                    return None
                            
            from_projects = cls.query.filter_by(project=from_project).all()
            if from_projects:
                for fp in from_projects:
                    new_project=Regular()
                    new_project.project=to_project
                    new_project.field=fp.field
                    new_project.action=fp.action
                    new_project.field_to=fp.field_to
                    new_project.value=fp.value
                    db_session.add(new_project)
                db_session.commit()
                print 'Copied: %s ===>>> %s' % (from_project,to_project)
            
    @classmethod
    def get_all_projects(cls):
        projects = cls.query.distinct(cls.project).group_by(cls.project).all()
        if projects:
            return [p for p in projects]
    
