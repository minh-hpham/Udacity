#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
#
# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#
#
# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    if restaurants == []:
        flash('You currently have no restaurants')
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash('New restaurant added!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editRestaurant.name = request.form['name']
        session.add(editRestaurant)
        session.commit()
        flash('Your Restaurant is edited')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',restaurant_id=restaurant_id, restaurant = editRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash('Your Restaurant is deleted')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=deletedRestaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(id=restaurant_id)
    if items == []:
        flash('You currently have no menu item')
    return render_template('menu.html',restaurant=restaurant, items=items,restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'],
            course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('new menu item %s is created'% newItem.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['form']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['course']:
            editedItem.course = request.form['course']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('This item is edited')
        return redirect('showMenu', restaurant_id=restaurant_id)
    else:
        return render_template(
            'editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id,item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        session.delete(deletedItem)
        session.commit()
        flash('This item is deleted')
        return redirect(url_for('menu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',item = deletedItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
