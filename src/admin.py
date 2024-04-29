import os
from flask_admin import Admin
from models import db, User,Characters,Planets,Vehicles,FavoriteCharacter,FavoritePlanet,FavoriteVehicle
from flask_admin.contrib.sqla import ModelView


#para que aparezca en la tabla, hay que escribir en el admin.add...
class MyFavoritesView(ModelView):
        column_list= ("usuario_id", "people_id")
        form_columns = ("usuario_id", "people_id")

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(ModelView(FavoriteCharacter, db.session))
    admin.add_view(ModelView(FavoritePlanet, db.session))
    admin.add_view(ModelView(FavoriteVehicle, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))