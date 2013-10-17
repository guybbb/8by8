from bottle import route, run, response, hook, static_file, get, redirect, PasteServer, request, abort, template
#import yql
import sqlite3
from ledbridge import sendtogrid

#configuration
con = sqlite3.connect('stocks.db')
con.execute("CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY, symbol char(100) NOT NULL, purchase_price INTEGER NOT NULL)")
server_port = 80
demo = False
stocks_price = [32.74,22.78,888.79,23.92,174.83,40.26,51.12,14.66]
stocks_price.reverse()

@hook('after_request')
def enable_cors():
    '''
       Allow cross-site calls
    '''   
    response.headers['Access-Control-Allow-Origin'] = '*'

# Static Routes
@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='../public/js')

@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='../public/css')

@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='../public/images')

@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='../public/fonts')

@get('/<filename:re:.*\.html>')
def html(filename):
    return static_file(filename, root='../public/html')


# Dynamic Routes

@route('/')
def index():
    '''
       redirect to index.html
    '''
    redirect("/index.html")

@route('/quote')
def get_quote():
	y = yql.Public()
	query = 'select * from yahoo.finance.quotes where symbol in ("YHOO","AAPL","GOOG","MSFT")'
	res = y.execute(query, env="store://datatables.org/alltableswithkeys")

	return template('index',stocks=res.rows)

@route('/stocks', method='PUT')
def update_quotes():
	
	response.content_type = 'application/json'
	#get list of stocks from JSON object

	print request.json
	user_price = []
	for stock in request.json:
		print stock['symbol'], stock['price']
		user_price.append(int(stock['price']))
	out = {'status':'ok'}

	print user_price
	if not(demo):
		user_price.reverse()
		sendtogrid(stocks_price, user_price, 5)
	return out

run(host='0.0.0.0', port=server_port, reloader=True, debug=True)

