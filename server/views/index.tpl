<html>
	<body>
		<ul>
  			% for item in stocks:
    			<li>Symobl:{{item['symbol']}} {{item['Bid']}} change:{{item['Change']}}</li>
  			% end
		</ul>
	</body>
</html>