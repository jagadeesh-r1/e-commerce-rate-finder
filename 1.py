
# DESCRIPTIOP OF THE TABLES
################################################################################
# charges:                                                                     #
# 'domestic_shipping_charge', 'int(11)', 'NO', '', NULL, ''                    #
# 'dtp_charges', 'int(11)', 'NO', '', NULL, ''                                 #
# 'exchange_surcharge', 'int(11)', 'NO', '', NULL, ''                          #
# 'fuel_surcharge', 'int(11)', 'NO', '', NULL, ''                              #
# 'gst', 'int(11)', 'NO', '', NULL, ''                                         #
# 'id', 'int(11)', 'NO', 'PRI', NULL, 'auto_increment'                         #
# 'logistic_id', 'int(11)', 'NO', '', NULL, ''                                 #
# 'premium', 'int(11)', 'NO', '', NULL, ''                                     #
################################################################################
# logistics_names:                                                             #
# 'id', 'int(11)', 'NO', 'PRI', NULL, 'auto_increment'                         #
# 'logistics_name', 'varchar(1000)', 'NO', '', NULL, ''                        #
# 'timeline', 'varchar(1000)', 'NO', '', NULL, ''                              #
################################################################################
# logistics_zone:                                                              #
# 'id', 'int(11)', 'NO', 'PRI', NULL, 'auto_increment'                         #
# 'logistics_id', 'int(11)', 'NO', '', NULL, ''                                #
# 'country', 'varchar(45)', 'NO', '', NULL, ''                                 #
# 'zone', 'varchar(45)', 'NO', '', NULL, ''                                    #
################################################################################
# rate_card:                                                                   #
# 'id', 'int(11)', 'NO', 'PRI', NULL, 'auto_increment'                         #
# 'logistics_id', 'varchar(45)', 'NO', '', NULL, ''                            #
# 'zone', 'varchar(45)', 'NO', '', NULL, ''                                    #
# 'weight', 'double', 'NO', '', NULL, ''                                       #
# 'price', 'double', 'NO', '', NULL, ''                                        #
################################################################################



import _mysql

count=raw_input("Enter country to be shipped : ")
weight=int(raw_input("Enter Weight in gms : "))
height=int(raw_input("Enter Height(cm) : "))
lenght=int(raw_input("Enter Lenght(cm) : "))
breadth=int(raw_input("Enter Breadth(cm) : "))

weight=(float)(float(weight)/1000)

vol_w=(height*lenght*breadth)

vol_w=(float)(float(vol_w)/5000)

#print vol_w,weight
print
print

print "Carrier \t Price \t Timeline\t \tWeight Considered"
db = _mysql.connect("kluniversity-cluster.cluster-cefcziwk2pxu.ap-south-1.rds.amazonaws.com","kluniversity","kluniversity_123","exam_database" )


#db.query("""select * from logistics_zone""")
db.query("select logistics_id from logistics_zone where country like '%s'"%count)


r=db.store_result()

data_country=r.fetch_row(maxrows=0)

for log_id in data_country:
	id=log_id[0]
	#print "the id of the country %s is %s"% (count,id) 
	#db.query("DESCRIBE logistics_names")
	db.query("select domestic_shipping_charge,dtp_charges,exchange_surcharge,fuel_surcharge,gst,premium from charges where logistic_id=%s"% id)
	charges_data=db.store_result()
	charges=charges_data.fetch_row(maxrows=0)
	for k in charges:
		dsc=k[0]
		dtp=k[1]
		exs=k[2]
		fuel=k[3]
		gst=k[4]
		prem=k[5]

	db.query("select logistics_name,timeline from logistics_names where id=%s"% id)
	name_time=db.store_result()
	data=name_time.fetch_row(maxrows=0)
	for log_name in data:
		del_name=log_name[0]
		time=log_name[1]
		if(del_name == "'DHL Ecommerce'" or del_name == "'Indiapost'"):
			final_weight=weight
		else:
			if(vol_w>weight):
				final_weight=vol_w
			else:
				final_weight=weight
		db.query("select price from rate_card where logistics_id=%s and weight=%f"% (id,final_weight))
		price_data=db.store_result()
		price=price_data.fetch_row(maxrows=0)
###***here actually we need to saperate countries into zones as USA,lattinamerica,Africa,AsiaPasific but didnt do it because i was so sleepy. Sorry.
		min=10000
		for i in price:
			#print i[0]
			if int(i[0]) < min :
				min = int(i[0])
		final_price=min
		prem=(float)(float(prem)/100)*final_price
		fuel=(float)(float(fuel)/100)*final_price
		gst=(float)(float(gst)/100)*final_price
		exs=(float)(float(exs)/100)*final_price
		final_price=final_price+prem+fuel+gst+exs+(float)(dtp)+(float)(dsc)
		#print final_price

		print " %s    \t   %0.2f  \t    %s   \t  %0.2f "%(del_name,final_price,time,final_weight)








db.close()
