import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'..','..'))

from flask import Flask
from goscrapy.model.regular import Regular
from goscrapy.model.common_item import CommonItem,CommonItemLine

def create_app(config_filename): 
    app=Flask(__name__,static_folder='static')
    app.config.from_object(config_filename)
    
    from flask import render_template, send_from_directory
    
    @app.route('/export')
    def export():
        return render_template('export.html')
    
    @app.route('/<path:filename>')
    def thefile(filename):
        return send_from_directory(os.path.join(app.root_path,'templates'), filename)
    
    @app.route('/')
    def index():
        projects = Regular.query.distinct(Regular.project).group_by(Regular.project).all()
        
        return render_template('index.html',projects=projects)  
  
    return app