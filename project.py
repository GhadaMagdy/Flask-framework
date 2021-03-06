from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.pool import SingletonThreadPool, NullPool,StaticPool



app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread':False},poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def specificMenuJSON(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    return jsonify(MenuItems=[item.serialize])

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant,items=items)

# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/new/',methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    targetItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            targetItem.name=request.form['name']
            session.add(targetItem)
            session.commit()
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id,menu_id=menu_id,item=targetItem)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    targetItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(targetItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id,menu_id=menu_id,item=targetItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=9874)