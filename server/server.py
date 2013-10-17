from bottle import route, run, response, hook, static_file, get, redirect, PasteServer, request, abort, template
import yql
import sqlite3
from ledbridge import sendtogrid

#configuration
con = sqlite3.connect('stocks.db')
con.execute("CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY, symbol char(100) NOT NULL, purchase_price INTEGER NOT NULL)")
server_port = 80
demo = False

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
	for stock in request.json:
		print stock['symbol'], stock['price']
	out = {'status':'ok'}

	if not(demo):
		sendtogrid([500,300,200,100], [498, 301, 202, 99], 5)
	return out

run(host='0.0.0.0', port=server_port, reloader=True, debug=True)

