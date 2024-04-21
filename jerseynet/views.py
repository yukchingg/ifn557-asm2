from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Team, Jersey, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    teams = Team.query.order_by(Team.name).all()
    return render_template('index.html', teams=teams)

@main_bp.route('/jerseys/<int:teamid>')
def teamjerseys(teamid):
    jerseys = Jersey.query.filter(Jersey.team_id==teamid).all()
    return render_template('teamjerseys.html', jerseys=jerseys)

@main_bp.route('/itemdetails/<int:jerseyid>')
def itemdetails(jerseyid):
    jersey = Jersey.query.get_or_404(jerseyid)
    return render_template('itemdetails.html', jersey=jersey)

@main_bp.route('/jerseys/')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    jerseys = Jersey.query.filter(Jersey.name.like(search)).all()
    return render_template('teamjerseys.html', jerseys = jerseys)

# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST','GET'])
def order():
    jersey_id = request.values.get('jersey_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='',surname='', address='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for jersey in order.jerseys:
            totalprice = totalprice + jersey.price
    
    # are we adding an item?
    if jersey_id is not None and order is not None:
        jersey = Jersey.query.get(jersey_id)
        if jersey not in order.jerseys:
            try:
                order.jerseys.append(jersey)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, totalprice=totalprice)

# Delete specific basket items
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        jersey_to_delete = Jersey.query.get(id)
        try:
            order.jerseys.remove(jersey_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.address = form.address.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for jersey in order.jerseys:
                totalcost = totalcost + jersey.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our awesome team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)




