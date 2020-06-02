基本概念
* dag
* task
* execution_date
* operator
* sensor

* hook
  是接口，用来通向外部数据库，与外部数据库沟通
* conn
  连接，保存连接的信息，比如用户名，密码，主机地址等
* plugin
  插件
  
1. 插件开发
可以通过引入插件，给airflow增加hook，operator，sensor，以及web管理界面

web管理界面支持flask_admin开发，也支持flask app builder开发

a. flask_admin
   增加要给Model
   """
   from sqlalchemy import Boolean, Column, String, Index, Text
   import sqlalchemy as db
   from airflow.models.base import Base, ID_LEN
   from airflow.utils.sqlalchemy import UtcDateTime

   class CheckRuleModel(Base):
       __tablename__ = 'check_rules'           #定义所用的表名
       rule_no = db.Column(db.Integer, primary_key=True)
       rule_desc = db.Column(db.String(500))
       check_table = db.Column(db.String(200))
       check_sql = db.Column(db.String(1000))
       check_type = db.Column(db.Integer)
       check_result = db.Column(db.Integer)
       check_action = db.Column(db.Integer)
       diagnose_sql = db.Column(db.String(1000))
       def __repr__(self):
           return str((
               self.rule_no, self.check_table, self.check_sql))

   """
   增加一个ModelView
   """
   from flask_admin.contrib import sqla

  class CheckRuleModelView(sqla.ModelView):
     #定义要显示的列
     column_list =['rule_no','rule_desc','check_table','check_sql','check_type','check_result','check_action','diagnose_sql']
  """
  
  生成视图
  from check_rule_model import CheckRuleModel 
  from check_rule_model_view import CheckRuleModelView 
  #生成对应模型的视图，该视图赋值给airflow plugin将在后台显示
  vCheckView = CheckRuleModelView(CheckRuleModel,Session,name="check rule",category = "Rules")
  

  

