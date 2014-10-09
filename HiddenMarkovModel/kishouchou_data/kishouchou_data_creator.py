# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib

####################################################################################################################################
#※データ取得したい地域、年ごとにURLが違うので、それに応じて22行目の作成するファイル名、114行目、116行目のurl変数、122行目のextractで指定する部分をいじる必要がある。
#※閏年の場合は57行目range内は366、その他365にする。
####################################################################################################################################

def extract( text, start, end ):
    # textからstartで始まりendで終わる文字を切り抜き
    # 切り抜かれた文字(startとendを含む)と切り抜いた文字(startとendの間)を返す
    s = text.find( start )
    e = text.find( end )
    if s == -1 or e == -1:
        return -1, -1
    e += len(end)
    remain = text[ :s ] + text[ e: ]  # 切り抜かれた文字(startとendを含む)
    return remain, text[ s:e ]

def TSVoutput(output_data):
	output_tsv=open('kishouchou_Alldata_2012Tokyo.txt', 'w') ######################作成するファイル名。ファイル名が同じだとこのプログラムを実行する度に上書きされていくため、複数地域についてデータ取得する場合、ファイル名を毎回変えて実行する##############
	print output_tsv	
	
	for line in range(len(output_data)):
		for column in range(len(output_data[0])):
			output_tsv.write('%s\t' % output_data[line][column])
		output_tsv.write('\n') 			

	
def DataSplit_do(weatherinfo_list):
	output_data = [['' for m in range(22)] for n in range(367)]
	
	output_data[0][0]='Month'
	output_data[0][1]='Date'
	output_data[0][2]='Mean station level air pressure (hPa)'
	output_data[0][3]='Mean sea level air pressure (hPa)'
	output_data[0][4]='Total rainfall (mm)'
	output_data[0][5]='Maximum rainfall per hour (mm)'
	output_data[0][6]='Maximum rainfall per 10 minutes (mm)'
	output_data[0][7]='Mean air temperature (℃)'
	output_data[0][8]='Maximum temperature　(℃)'
	output_data[0][9]='Minimum temperature　(℃)'
	output_data[0][10]='Mean relative humidity　(%)'
	output_data[0][11]='Minimum relative humidity (%)'
	output_data[0][12]='Mean wind speed (m/s)'
	output_data[0][13]='Maximum wind speed (m/s)'
	output_data[0][14]='Direction of Maximum wind speed'
	output_data[0][15]='Maximum instantaneous wind speed (m/s)'
	output_data[0][16]='Direction of Maximum instantaneous wind speed'
	output_data[0][17]='Sunshine duration (h)'
	output_data[0][18]='Total snowfall (cm)'
	output_data[0][19]='Maximum depth of snow cover (cm)'
	output_data[0][20]='Meteorological summary 6:00-18:00'
	output_data[0][21]='Meteorological summary 18:00- next day 6:00'	

	for z in range(366):  #################←閏年の場合は366にする################################################################

		Month=weatherinfo_list[z*22+0]
		Day=weatherinfo_list[z*22+1]
		Mean_station_level_air_pressure=weatherinfo_list[z*22+2]
		Mean_sea_level_air_pressure=weatherinfo_list[z*22+3]
		Total_rainfall=weatherinfo_list[z*22+4]
		Maximum_rainfall_per_hour=weatherinfo_list[z*22+5]
		Maximum_rainfall_per_10_minutes=weatherinfo_list[z*22+6]
		Mean_air_temperature=weatherinfo_list[z*22+7]
		Maximum_temperature=weatherinfo_list[z*22+8]
		Minimum_temperature=weatherinfo_list[z*22+9]
		Mean_relative_humidity=weatherinfo_list[z*22+10]
		Minimum_relative_humidity=weatherinfo_list[z*22+11]
		Mean_wind_speed=weatherinfo_list[z*22+12]
		Maximum_wind_speed=weatherinfo_list[z*22+13]
		Directon_of_Maximum_wind_speed=weatherinfo_list[z*22+14]
		Maximum_instantaneous_wind_speed=weatherinfo_list[z*22+15]
		Direction_of_Maximum_instantaneous_wind_speed=weatherinfo_list[z*22+16]
		Sunshine_duration=weatherinfo_list[z*22+17]
		Total_snowfall=weatherinfo_list[z*22+18]
		Maximum_depth_of_snow_cover=weatherinfo_list[z*22+19]
		Meteorological_summary_0600_1800=weatherinfo_list[z*22+20]
		Meteorological_summary_1800_next_day_0600=weatherinfo_list[z*22+21]
		
	
		output_data[z+1][0]=Month
		output_data[z+1][1]=Day
		output_data[z+1][2]=Mean_station_level_air_pressure
		output_data[z+1][3]=Mean_sea_level_air_pressure
		output_data[z+1][4]=Total_rainfall
		output_data[z+1][5]=Maximum_rainfall_per_hour
		output_data[z+1][6]=Maximum_rainfall_per_10_minutes
		output_data[z+1][7]=Mean_air_temperature
		output_data[z+1][8]=Maximum_temperature
		output_data[z+1][9]=Minimum_temperature
		output_data[z+1][10]=Mean_relative_humidity
		output_data[z+1][11]=Minimum_relative_humidity
		output_data[z+1][12]=Mean_wind_speed
		output_data[z+1][13]=Maximum_wind_speed
		output_data[z+1][14]=Directon_of_Maximum_wind_speed
		output_data[z+1][15]=Maximum_instantaneous_wind_speed
		output_data[z+1][16]=Direction_of_Maximum_instantaneous_wind_speed
		output_data[z+1][17]=Sunshine_duration
		output_data[z+1][18]=Total_snowfall
		output_data[z+1][19]=Maximum_depth_of_snow_cover
		output_data[z+1][20]=Meteorological_summary_0600_1800
		output_data[z+1][21]=Meteorological_summary_1800_next_day_0600
		

	#print 'output_data',output_data
	return output_data


def autoread_html(): #気象庁のデータベースから全データを検索して weatherinfo_list に格納する
	day_data=[]
	for i in range(1,13):
		if i<10:
			url='http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2012&month=0' + str(i) +'&day=&view=p1' ##############他の地域や年についてデータを取得したい場合ここをいじる#################
		else:
			url='http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2012&month=' + str(i) +'&day=&view=p1' ###############他の地域や年についてデータを取得したい場合ここをいじる#################
		
		g = urllib.urlopen(url)
		print "Reading from" + url # +"Content-type: text/html; \n\n"
		toriaezu=g.read()
		for j in range(0,31):
			toriaezu, remaintsv = extract( toriaezu, '<a href="hourly_s1.php?prec_no=44&block_no=47662&year=2012', '</td></tr>') ######################他の地域や年についてデータを取得したい場合ここをいじる##################

			if remaintsv == -1: # startstart endend タグがなかったら抜ける
				break
			remaintsv= "".join(remaintsv)
			day_data.append('>' +str(i) +'<') #月の情報を加える
			day_data.append(remaintsv)
	print 'len(day_data)'
	print day_data
	print len(day_data)
	
	weatherinfo_list=[]

	for k in range(len(day_data)):
		#print day_data[k]
		#print 'day_data[k]'
		day_data[k] = day_data[k].replace('<a href=','').replace('/td></tr>','').replace('><','')
		#print day_data[k] 
		for l in range(22):
			day_data[k], weatherinfo = extract( day_data[k], '>', '<' )
			print weatherinfo
			if weatherinfo == -1: # startstart endend タグがなかったら抜ける
				break
			weatherinfo = weatherinfo.replace('<','').replace('>','')

			#print 'weatherinfo',weatherinfo
			weatherinfo= "".join(weatherinfo)
			weatherinfo_list.append(weatherinfo)
		
	print 'weatherinfo_list',weatherinfo_list,len(weatherinfo_list)
	return weatherinfo_list
			
		

if __name__ == '__main__':
	TSVoutput(DataSplit_do(autoread_html()))
	