import pandas as pd
import plotly as pl
import os
import datetime
import math

import matplotlib.pyplot as plt
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors
import numpy as np
from numpy.random import seed
from numpy.random import rand
import scipy.stats as stats


## Please make sure both the .csv file and main.py are in the same folder
## Input: N/A
## Output: path of the current folder
def csv_folder():
	csv_folder = os.getcwd()
	return csv_folder

## Input: Path to the main folder where all files reside
## Output: Full path to the .csv file in the given folder.(Finds by extension)
def find_csv_file(path):
	for file in os.listdir(str(path)):
		if file.endswith(".csv"):
			csv_path = os.path.join(str(path), file)
	return csv_path

## Input: 
## Output: 
def loadColumns(df,filterValue):
	df_page_view = df[filterValue]
	return df_page_view

def filterByColumnsValue(df,column,filterValue):
	return df[column.isin(filterValue)]
	
def returnmax(desk_count,mob_count,tab_count):
	new_l = [desk_count,mob_count,tab_count]
	maxpos = new_l.index(max(new_l))
	if maxpos == 0:
		return 'Desktop',desk_count
	if maxpos == 1:
		return 'Mobile',mob_count
	if maxpos == 2:
		return 'Tablet',tab_count
	

## Returns the unique options in a given column of a dataframe
## type(df)= dataFrame type(column)=string
def get_column_options(df_x,column):
    df_x = df_x.drop_duplicates(column)
    options = [item for item in df_x[column]]
    return options

def hist_plt(dist_arr, bins,title,label,xlabel,ylabel,save=False,fileName='file.png'):

    plt.hist(dist_arr,bins,histtype='bar',rwidth=0.8,label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    if save==True:
        plt.savefig(fileName)
    plt.show()

def hist_save(dist_arr, bins,title,label,xlabel,ylabel,fileName='file.png'):
	rand_n = rand(1)
	plt.hist(dist_arr,bins,histtype='bar',rwidth=0.8,label=label)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend()
	plt.figure(rand_n)
	plt.savefig(fileName)

def bar_plt(x_values,y_values,title,label,xlabel,ylabel,save=False,fileName='file.png'):
	# rand_n = rand(1)
	plt.bar(x=x_values,height=y_values,label=label)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend()
	# plt.figure(rand_n)
	if save==True:
		plt.savefig(fileName)
	plt.show()

def bar_save(x_values,y_values,label,title='',xlabel='',ylabel='',fileName='file.png',color=['#42ACFE']):
	plt.bar(x=x_values,height=y_values,label=label,linewidth=1,color=color)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend()
	plt.savefig(fileName)
	plt.close()

# def returnMatches(a, b):
#     return [[x for x in a if x in b], [x for x in b if x in a]]

def returnMatches(x, y):
    return frozenset(x).intersection(y)

def prepFolders():
	main_folders = ['q1_figures','q2_figures','q3_figures']
	q1_sub_folders = ['q10','q11','q12']
	q2_sub_folders = ['q21','q22','q23']
	q3_sub_folders = ['ctr_dist_after','ctr_dist_before','outlierClicks']
	# Create main folders:
	for folder in main_folders:
		if not os.path.exists(folder):
			os.makedirs(folder)
	# Create subfolders of q1:
	for folder in q1_sub_folders:
		if not os.path.exists(os.path.join(main_folders[0],folder)):
			os.makedirs(os.path.join(main_folders[0],folder))
	# Create subfolders of q2:
	for folder in q2_sub_folders:
		if not os.path.exists(os.path.join(main_folders[1],folder)):
			os.makedirs(os.path.join(main_folders[1],folder))
	# Create subfolders of q3:
	for folder in q3_sub_folders:
		if not os.path.exists(os.path.join(main_folders[2],folder)):
			os.makedirs(os.path.join(main_folders[2],folder))
if __name__ == '__main__':
	prepFolders()
	## CSV Reading into Pandas DataFrame ##
	main_folder = csv_folder()
	csv_path = find_csv_file(main_folder)
	df = pd.read_csv(filepath_or_buffer=csv_path)

	# print('Shape of dataset = ',df.shape)
	# print('df.dtypes',df.dtypes)
	########### DATASET INFORMATION ###########
	'''
	Shape:(375799, 10)
	Brand             object
	Market            object
	User_Id            int64
	Session_Id         int64
	Date              object
	Device            object
	Event_Name        object
	Component_Name    object
	Site_Section      object
	Event_Order        int64 
	'''
	print(f'############# PART-I #############')
	print(f'##################################')
	############################################
	## DataFrame prep to understand pageview count of Glamour in Aug.
	filter_q11 = ['Brand','Date','Event_Name']
	df_q1 = loadColumns(df,filter_q11)
	# print('Shape of df_q1 = ',df_q1.shape)
	# print('pageview_head = ',df_q1.head())
	#############################################

	## Input: 
	## Output: Extract August & Convert 'Date' Column to type: datatime
	pd.set_option('mode.chained_assignment', None)
	df_q1['Date'] = pd.to_datetime(df_q1['Date'])
	df_q1_aug = df_q1[df_q1['Date'].dt.month == 8]
	# print('Shape of df_q1_aug = ',df_q1_aug.shape)
	# print('df_q1_aug = ',df_q1_aug.head())
	################################################################
	################################################################
	
	## Input: DataFrame Filter: 'Date':August
	## Output:DataFrame Filter: 'Date':August & 'Brand':Glamour
	df_q1_aug_glam = filterByColumnsValue(df=df_q1_aug,column=df_q1_aug.Brand,filterValue=['Glamour'])
	# print('Shape of df_q1_aug_glam',df_q1_aug_glam.shape)
	# print('df_q1_aug_glam = ',df_q1_aug_glam.head())
	################################################################
	################################################################

	## Input: DataFrame Filter: 'Date':August & 'Brand':Glamour
	## Output:DataFrame Filter: 'Date':August & 'Brand':Glamour & 'Event_Name':Pageview
	df_q1_aug_glam_pv = filterByColumnsValue(df=df_q1_aug_glam,column=df_q1_aug_glam.Event_Name,filterValue=['Pageview'])
	glmAugPv = df_q1_aug_glam_pv.shape[0]
	print(f'Q1.1) Glamour had {glmAugPv} number of Pageviews in August')
	print(f'Saving graph in {os.path.join(os.getcwd(),"q1_figures","q10")}...')
	# print('Shape of df_q1_aug_glam_pv',df_q1_aug_glam_pv.shape)
	# print('df_q1_aug_glam_pv = ',df_q1_aug_glam_pv.head())

	######### PLOT # OF PAGEVIEWS IN AUG FOR GLAMOUR #########
	months = [i for i in range(1,13)]
	bar_save(x_values=months,y_values=[0,0,0,0,0,0,0,glmAugPv,0,0,0,0],title='Number of Pageviews in August for Glamour', \
		label='Glamour'+'\n'+'Count:'+str(glmAugPv),xlabel='Months',ylabel='PageView Count', \
		fileName=os.path.join(os.getcwd(),'q1_figures','q10','GlmAugPv.png'))
	################################################################
	################################################################
	##################### END OF Q1.0 ##############################
	################################################################
	################################################################
	## Input: Whole DataFrame
	## Output:Frames with only Columns=Brand,User_Id,Event_Name
	df_q11 = loadColumns(df=df,filterValue=['Brand','User_Id','Event_Name'])
	# print('Shape of df_q11',df_q11.shape)
	# print('df_q11 = ',df_q11.head())
	################################################################
	################################################################
	
	## Input: DataFrame - Rows with only columns: 'Brand','User_Id','Event_Name'
	## Output:DataFrame - 'Brand':CNT
	df_q11_CNT = filterByColumnsValue(df=df_q11,column=df_q11.Brand,filterValue=['Conde Nast Traveler'])
	# print('Shape of df_q11_CNT = ',df_q11_CNT.shape)
	# print('df_q11_CNT = ',df_q11_CNT.head())
	################################################################
	################################################################

	## Input: DataFrame - Rows with column 'Brand':CNT
	## Output:DataFrame - Rows with column 'Brand':CNT & 'Event_Name':Impressions
	df_q11_CNT_impr = filterByColumnsValue(df=df_q11_CNT,column=df_q11_CNT.Event_Name,filterValue=['Impression'])
	# print('Shape of df_q11_CNT_impr = ',df_q11_CNT_impr.shape)
	# print('df_q11_CNT_impr = ',df_q11_CNT_impr.head())
	################################################################
	################################################################

	## Input: DataFrame - Rows with column 'Brand':CNT & 'Event_Name':Impressions
	## Output:DataFrame - Duplicate rows dropped referencing 'User_Id' column
	df_q11_CNT_impr_nodupes = df_q11_CNT_impr.drop_duplicates('User_Id')
	# print('Shape of df_q11_CNT_impr_nodupes = ',df_q11_CNT_impr_nodupes.shape)
	# print('df_q11_CNT_impr_nodupes = ',df_q11_CNT_impr_nodupes.head())
	################################################################
	################################################################

	## Input: DataFrame - Unique rows referencing 'User_Id' column
	## Output:Number of Users who watched video on CNT
	video_count_cnt = df_q11_CNT_impr_nodupes.shape[0]
	print(f'Q1.2) {video_count_cnt} users watch Video on CNT')
	print(f'Saving graph in {os.path.join(os.getcwd(),"q1_figures","q11")}...')
	################ PLOT VIDEO VIEW COUNT FOR CNT ################
	bar_save(x_values=['CNT'],y_values=[video_count_cnt],title='CNT Video Views', \
		label='CNT'+'\n'+'Count:'+str(video_count_cnt),xlabel='Companies',ylabel='Video View Count', \
		fileName=os.path.join(os.getcwd(),'q1_figures','q11','cnt_views.png'),color='#42ACFE')
	################################################################
	################################################################
	##################### END OF Q1.1 ##############################
	################################################################
	################################################################
	## Input: Whole DataFrame
	## Output: DataFrame with only Columns=Brand,Session_Id,Device,Event_Name
	df_q12 = loadColumns(df=df,filterValue=['Brand','Session_Id','Device','Event_Name'])
	# print('Shape of df_q12',df_q12.shape)
	# print('df_q12 = ',df_q12.head())
	################################################################
	################################################################
	
	## Input: DataFrame - Rows with only columns: 'Brand','User_Id','Event_Name'
	## Output:DataFrame - 'Brand':SELF
	df_q12_self = filterByColumnsValue(df=df_q12,column=df_q12.Brand,filterValue=['Self'])
	# print('Shape of df_q12_self = ',df_q12_self.shape)
	# print('df_q12_self = ',df_q12_self.head())
	################################################################
	################################################################

	## Input: DataFrame - 'Brand':SELF
	## Output:Total number of sessions for Brand:'Self' # 37021
	session_cnt_self = df_q12_self['Session_Id'].shape[0]
	# print('Total number of Sessions for Brand:Self = ',session_cnt_self)
	
	## Input:
	## Output:Number of unique session_ids. to have a list of session_ids: 9845
	df_q12_self_nodupes = df_q12_self.drop_duplicates('Session_Id')
	# print('Total Number of Sessions = ',df_q12_self_nodupes['Session_Id'].shape[0])

	## Input:
	## Output:
	unique_sess_ids = []
	[unique_sess_ids.append(id_) for id_ in df_q12_self_nodupes['Session_Id']]
	bouncers = []
	device_names_per_session_id = {}
	for id_ in unique_sess_ids:
		# Output: DataFrame - dataframe for each uniquely identified session_ids for 'Brand':Self
		df_of_one_sess_id = filterByColumnsValue(df=df_q12_self,column=df_q12_self.Session_Id,filterValue=[id_])
		# print('df_of_one_sess_id = ',df_of_one_sess_id)

		# Input: dataframe per session_id for 'Brand':Self
		# Output: DataFrame - It has only the 'Brand':Self & 'Event_Name':Page for every unique session_id
		df_of_one_sess_id_pageView = filterByColumnsValue(df=df_of_one_sess_id,column=df_of_one_sess_id['Event_Name'],filterValue=['Pageview'])
		# print('df_of_one_sess_id_pageView = ',df_of_one_sess_id_pageView)
		# print('pageview_count = ',df_of_one_sess_id_pageView.shape[0])


		if df_of_one_sess_id_pageView.shape[0]==1: # This means that the filtered dataframe only had one Pageview and that's why df must only have one row.
			bouncers.append(id_)
			
			# print('session_id that bounces = ',df_of_one_sess_id_pageView['Session_Id'].iloc[0])
			# dummy.append(df_of_one_sess_id_pageView['Session_Id'].iloc[0])

			## create an entry in the dictionary with the name of this session as key and assign the DeviceName as the its value
			device_names_per_session_id[df_of_one_sess_id_pageView['Session_Id'].iloc[0]] = str(df_of_one_sess_id_pageView['Device'].iloc[0])
	
	# How many of them are 'Mobile' how many are 'Desktop' how many are 'Tablet'
	# Highest number of device will have the highest bounce rate
	desk_count=0
	mob_count=0
	tab_count=0
	for key,value in device_names_per_session_id.items():
		if value == 'Desktop':
			desk_count += 1
		elif value == 'Mobile':
			mob_count += 1
		elif value == 'Tablet':
			tab_count += 1
		else:
			misc_count += 1
	# print('device type has the highest bounce rate = ',max([desk_count,mob_count,tab_count]))
	# print('device_names_per_session_id = ',device_names_per_session_id)
	bouncer_count = len(bouncers)
	# print(f'Number of bouncers of SELF is {bouncer_count}')
	
	# print(f'Number of device is {len(device_names_per_session_id)}')
	desk_bounce_rate = desk_count/bouncer_count*100
	mob_bounce_rate = mob_count/bouncer_count*100
	tab_bounce_rate = tab_count/bouncer_count*100
	device_name,high_br = returnmax(desk_bounce_rate,mob_bounce_rate,tab_bounce_rate)
	self_bounce_rate = bouncer_count/session_cnt_self*100
	print(f'Q1.3) {(self_bounce_rate):.2f}% of SELF’s sessions are bounces:')
	print(f'      Desktop Bounce Rate: {desk_bounce_rate:.2f}%')
	print(f'      Mobile Bounce Rate: {mob_bounce_rate:.2f}%')
	print(f'      Tablet Bounce Rate: {tab_bounce_rate:.2f}%')
	print(f'{device_name} has the highest bounce rate of {high_br:.2f}%')

	############### PLOTTING SELF BOUNCE RATE #####################
	print(f'Saving graph in {os.path.join(os.getcwd(),"q1_figures","q12")}...')
	label = 'Self' + "\n" + 'Bounce Rate:' + f'{self_bounce_rate:.2f}%' + "\n" + 'Highest Bounce Rate Device:' + f'{device_name}:{high_br:.2f}%'
	bar_save(x_values=['','','','','SELF','','','',''],y_values=[0,0,0,0,self_bounce_rate,0,0,0,0], \
		title='SELF Bounce Rate',label=label,xlabel='Company',ylabel='Bounce Rate(%)',fileName=os.path.join(os.getcwd(),'q1_figures','q12','slf_br.png'))
	################################################################
	################################################################
	##################### END OF Q1.2 ##############################
	################################################################
	################################################################

	################################################################
	################################################################
	#####################   PART II   ##############################
	################################################################
	################################################################
	print(f'###################################')
	print(f'############# PART-II #############')
	print(f'###################################\n')
	df_q21 = loadColumns(df=df,filterValue=['Brand','Market','User_Id','Session_Id','Event_Name'])
	# print('df_q21 = ',df_q21)

	## Have only Brand:CNT
	df_q21_cnt = filterByColumnsValue(df=df_q21 ,column=df_q21['Brand'] ,filterValue=['Conde Nast Traveler'])
	# print('df only cnt = ',df_q21_cnt)
	
	## Give me a list of all the markets:
	df_q21_cnt_nodupes_in_market = df_q21_cnt.drop_duplicates('Market')
	# print('df_q21_cnt_nodupes_in_market = ',df_q21_cnt_nodupes_in_market)
	unique_cnt_markets = []
	[unique_cnt_markets.append(market) for market in df_q21_cnt_nodupes_in_market['Market']]
	print(f'Q2.1) Subscription Rates per Market')
	print(f'CNT is currently active in:')
	for i in range(0,len(unique_cnt_markets)):
		print(unique_cnt_markets[i])
	# print(f'      CNT is active in {unique_cnt_markets} markets')

	#### Finding Subs % per market for CNT ####
	## Create dict to hold each markets' subscription rate
	subs_rate_per_mkt = {}
	## For each market that CNT is in:
	##   Generate a new dataframe for only "that market" from df_q21_cnt(only has rows with Brand:CNT)
	##   Count how many unique users there are in that market for CNT
	##   Filter the new dataframe to have Event_Name:Subscription
	##   Count how many users are on the filtered df from prev. step
	##   Calculate rate
	##   Add the rate for that market to the dictionary
	print(f'Lets look at the statistics one market at a time...')
	for market in unique_cnt_markets:
		## Generate a new dataframe for only "that market" from df_q21_cnt(only has rows with Brand:CNT)
		df_q21_cnt_per_mkt = filterByColumnsValue(df=df_q21_cnt,column=df_q21_cnt['Market'],filterValue=[market])
		# print('df_q21_cnt_per_mkt = ',df_q21_cnt_per_mkt)

		## Count how many unique users there are in that market for CNT
		df_q21_cnt_per_mkt_nodupes = df_q21_cnt_per_mkt.drop_duplicates('User_Id')
		unique_num_of_users = df_q21_cnt_per_mkt_nodupes.shape[0]
		
		# print(f'There are a total of {unique_num_of_users} readers of CNT in {market}')
		print(f'#####{market}#####')
		print(f'Reader Count:{unique_num_of_users}')

		## Filter the new dataframe to have Event_Name:Subscription
		df_q21_cnt_per_mkt_subs = filterByColumnsValue(df=df_q21_cnt_per_mkt,column=df_q21_cnt_per_mkt['Event_Name'],filterValue=['Subscription'])
		## Count how many users are on the filtered df from prev. step
		subscribers_count = df_q21_cnt_per_mkt_subs['User_Id'].shape[0]
		print(f'Subsciber Count:{subscribers_count}')

		## Calculate rate, subs_rate_per_mkt dictionary holds all the subs.% values for each market:
		subs_rate_per_mkt[market] = (subscribers_count/unique_num_of_users)*100
		print(f'Subscription Rate: {subs_rate_per_mkt[market]:.2f}%')
		print('################')
	
	######## IDEA: RANK THESE MARKETS FROM TOP TO BOTTOM ########
	####### What might you say to a stakeholder to contextualize these results? ####
	## All the markets and their rates: subs_rate_per_mkt
	subs_rate_per_mkt_sourted_list = sorted(subs_rate_per_mkt.values())
	# print('subs_rate_per_mkt_sourted_list = ',subs_rate_per_mkt_sourted_list)
	most_successful_subs_rate_markets = ''
	for key,value in subs_rate_per_mkt.items():
		if value==subs_rate_per_mkt_sourted_list[-1]:
			most_successful_subs_rate_market = key
	## ANSWER TO THE PART II is most_successful_subs_rate_market:most succesful market
	print(f'Highest Subscription Rate Market is {most_successful_subs_rate_market}:{subs_rate_per_mkt[most_successful_subs_rate_market]:.2f}%')
	############ PLOT SUBSCRIPTION RATE FOR EACH OF CNT'S MARKET ############
	folder_q2 = 'q2_figures'
	folder_q21 = 'q21'
	filen = os.path.join(os.getcwd(),folder_q2,folder_q21,'subsRateCNT.png')
	print(f'Saving graph in {filen}... ')
	label = f'Highest Subscription Rate:{most_successful_subs_rate_market}:{subs_rate_per_mkt[most_successful_subs_rate_market]:.2f}%'
	bar_save(x_values=list(subs_rate_per_mkt.keys()), \
		y_values=list(subs_rate_per_mkt.values()), \
		title='CNT Subscription Rates per Market',label=label, \
		xlabel='Market',ylabel='Subscription %',fileName=filen \
		)
	###########################################################################
	### What might you say to a stakeholder to contextualize these results?:###
	## Bundle Subs Price in the U.S. is the lowest, following that is CA.######
	############ Other destinations is the highest subs at:$39.97  ############
	############ Online is the cheapest:$19.99. We should check for: ##########
	## Ravenue per market to better understand the true return of investment ##
	########################### END OF Q2.1 ###################################
	###########################################################################
	## Load only necessary columns
	df_q22 = loadColumns(df=df,filterValue=['Brand','Date','Event_Name','Component_Name','User_Id'])
	## filter to the 'Brand':Glamour
	df_q22_glm = filterByColumnsValue(df=df_q22,column=df_q22['Brand'],filterValue=['Glamour'])
	## Filter by date - before/after 09/01/2020
	pd.set_option('mode.chained_assignment', None)
	df_q22_glm['Date'] = pd.to_datetime(df_q22_glm['Date'])
	date = '2019-09-01'
	mask_before = (df_q22_glm['Date'] < date)
	mask_after = (df_q22_glm['Date'] >= date)
	df_q22_glm_before = df_q22_glm.loc[mask_before]
	df_q22_glm_after = df_q22_glm.loc[mask_after]
	# print('df_q22_glm_before = ',df_q22_glm_before)
	# print('Shape of df_q22_glm_before = ',df_q22_glm_before.shape)
	# print('df_q22_glm_after = ',df_q22_glm_after)
	# print('Shape of df_q22_glm_after = ',df_q22_glm_after.shape)

	## Show only Component_Name:'Ads'
	df_q22_glm_before_ads = filterByColumnsValue(df=df_q22_glm_before,column=df_q22_glm_before['Component_Name'],filterValue=['Advertisement'])
	df_q22_glm_after_ads = filterByColumnsValue(df=df_q22_glm_after,column=df_q22_glm_after['Component_Name'],filterValue=['Advertisement'])

	## Count number of clicks for before and after the campaign
	## Then get the list of all the unique users(uniq_users_glm_before/after) who has click 
	## to later see if particularly these unique users' ctr is higher or not
	df_q22_glm_before_clk = filterByColumnsValue(df=df_q22_glm_before_ads,column=df_q22_glm_before_ads['Event_Name'],filterValue=['Click'])
	clk_count_before = df_q22_glm_before_clk.shape[0]
	uniq_users_glm_before = list(df_q22_glm_before_clk.drop_duplicates('User_Id')['User_Id'])
	# print('All unique glm user ids before = ',uniq_users_glm_before)

	df_q22_glm_after_clk = filterByColumnsValue(df=df_q22_glm_after_ads,column=df_q22_glm_after_ads['Event_Name'],filterValue=['Click'])
	clk_count_after = df_q22_glm_after_clk.shape[0]
	uniq_users_glm_after = list(df_q22_glm_after_clk.drop_duplicates('User_Id')['User_Id'])
	# print('All unique glm user ids after = ',uniq_users_glm_after)
	
	## Count number of impressions for before and after the campaign
	df_q22_glm_before_impr = filterByColumnsValue(df=df_q22_glm_before_ads,column=df_q22_glm_before_ads['Event_Name'],filterValue=['Impression'])
	impr_count_before = df_q22_glm_before_impr.shape[0]

	df_q22_glm_after_impr = filterByColumnsValue(df=df_q22_glm_after_ads,column=df_q22_glm_after_ads['Event_Name'],filterValue=['Impression'])
	impr_count_after = df_q22_glm_after_impr.shape[0]

	ctr_before_campaign = clk_count_before/impr_count_before*100
	ctr_afer_campaign = clk_count_after/impr_count_after*100
	print(f'Q2.2) Campaign Performance of Glamour:')
	print(f'      CTR Before Campaign: {ctr_before_campaign:.2f}%')
	print(f'      CTR After Campaign: {ctr_afer_campaign:.2f}%')
	print(f'Lets see whatelse we can find from this data...')
	# bar_save(x_values=[ctr_before_campaign,ctr_afer_campaign],y_values=['Before','After'],label=,title=,xlabel=,ylabel=,fileName='ctr_glm.png')
	label_bef = 'CTR:' + f'{ctr_before_campaign:.2f}%' + "\n" + 'Population:' + str(len(uniq_users_glm_before))
	plt.bar(x='Before',height=ctr_before_campaign,label=label_bef,linewidth=1,color='#42ACFE')
	plt.xlabel('Campaign')
	plt.ylabel('CTR(%)')
	plt.title('CTR Before/After Campaign for Glamour')
	plt.legend()
	label_af = 'CTR:' + f'{ctr_afer_campaign:.2f}%' + "\n" + 'Population:' + str(len(uniq_users_glm_after))
	plt.bar(x='After',height=ctr_afer_campaign,label=label_af,linewidth=1,color='#FE6342')
	plt.legend()
	### Folder Prep ####
	folder_q2 = 'q2_figures'
	folder_q22 = 'q22'
	filen = os.path.join(os.getcwd(),folder_q2,folder_q22,'ctr_glm.png')
	### Folder Ready ####
	plt.savefig(filen)
	plt.close()
	################################################################
	##################### END OF Q2.2 ##############################
	#The campaign seems to be unsuccesful but need to investigate further:
	##### maybe in some devices there is significant increase  #####
	################################################################

	################################################################
	################ FURTHER INVESTIGATION OF Q2.2 #################
	################################################################
	loyal_ids = list(returnMatches(uniq_users_glm_before,uniq_users_glm_after))
	print(f'{len(loyal_ids)} many readers were visiting Glamour site before & after the campaing...')
	print(f'Let\'s see how the campaigned performed on our loyal customers...')
	## For all loyal ids see how the ctr changes ##
	ctr_loyal_before_after = {} # is a dict with key:loyal_id,value:[before,after]
	for loyal_id in loyal_ids:

		# Get rows of loyal ids in before and after dfs
		df_loyal_before = filterByColumnsValue(df=df_q22_glm_before_ads,column=df_q22_glm_before_ads['User_Id'],filterValue=[loyal_id])
		df_loyal_after = filterByColumnsValue(df=df_q22_glm_after_ads,column=df_q22_glm_after_ads['User_Id'],filterValue=[loyal_id])

		# Get click count of loyal ids in before and after dfs
		df_loyal_before_clk = filterByColumnsValue(df=df_loyal_before,column=df_loyal_before['Event_Name'],filterValue=['Click'])
		loyal_clk_count_before = df_loyal_before_clk.shape[0]
		df_loyal_after_clk = filterByColumnsValue(df=df_loyal_after,column=df_loyal_after['Event_Name'],filterValue=['Click'])
		loyal_clk_count_after = df_loyal_after_clk.shape[0]

		# Get impression count of loyal ids in before and after dfs
		df_loyal_before_imp = filterByColumnsValue(df=df_loyal_before,column=df_loyal_before['Event_Name'],filterValue=['Impression'])
		loyal_imp_count_before = df_loyal_before_imp.shape[0]
		df_loyal_after_imp = filterByColumnsValue(df=df_loyal_after,column=df_loyal_after['Event_Name'],filterValue=['Impression'])
		loyal_imp_count_after = df_loyal_after_imp.shape[0]

		# Calculate the ctr of the loyal users before and after the campaign and store it in ctr_loyal_before_after dict
		ctr_loyal_before_campaign = loyal_clk_count_before/loyal_imp_count_before*100
		ctr_loyal_afer_campaign = loyal_clk_count_after/loyal_imp_count_after*100
		ctr_loyal_before_after[loyal_id] = [ctr_loyal_before_campaign,ctr_loyal_afer_campaign]

	# print(f'Loyal CTR:{ctr_loyal_before_after}')
	####### Find the increasing and decreasing CTR% ########
	#### of the same users before and after the campaign ###
	loyal_increasing_ctr = []
	loyal_decreasing_ctr = []
	loyal_flat_ctr = []
	for val in ctr_loyal_before_after.values():
		if val[0]<val[1]:
			loyal_increasing_ctr.append(val[1]-val[0])
		elif val[0]>val[1]:
			loyal_decreasing_ctr.append(val[0]-val[1])
		else:
			loyal_flat_ctr.append(val[0])
	
	mean_increasing_loyal = sum(loyal_increasing_ctr)/len(loyal_increasing_ctr)
	mean_decreasing_loyal = sum(loyal_decreasing_ctr)/len(loyal_decreasing_ctr)
	print(f'CTR% has increased {mean_increasing_loyal:.2f}% but also decreased by {mean_decreasing_loyal:.2f}% on avg.')
	# label_bef = 'Before CTR:' + f'{ctr_before_campaign:.2f}%' + "\n" + 'Population:' + str(len(uniq_users_glm_before))
	# plt.bar(x='Before',height=ctr_before_campaign,label=label_bef,linewidth=1,color='b')
	# plt.xlabel('Campaign')
	# plt.ylabel('CTR(%)')
	# plt.title('CTR Before/After Campaign for Glamour')
	# plt.legend()
	# plt.savefig('ctr')
	# plt.close()

	################################################################
	################# T-TEST CTR DISTRIBUTION ######################
	################################################################
	print(f'Hmmm...These numbers are all good but are they significantly different from each other?')
	print(f'We can check the p-value of these 2 groups through t-test...')
	print(f'Testing...')
	t_ctr,p_ctr = stats.ttest_ind(loyal_increasing_ctr,loyal_decreasing_ctr)
	print(f't-value:{t_ctr:.2f}, p-value:{p_ctr:.2f}')
	if p_ctr>0.05:
		print(f'Since p-value is greater than 0.05 we can say that 2 means of CTR% of Loyal Readers Before and After the Campaign are similar!')
	else:
		print(f'Since p-value is less than 0.05 we can say that 2 means of CTR% of Loyal Readers Before and After the Campaign are NOT similar!')
	################################################################
	################## PLOT CTR DISTRIBUTION #######################
	################################################################
	low = math.ceil(min(loyal_increasing_ctr))
	high = math.ceil(max(loyal_increasing_ctr))
	bin_inc = [i for i in range(low,high,1)]
	fig, axs = plt.subplots(2,1,constrained_layout=True)
	lab_inc = f'Mean Increase:{mean_increasing_loyal:.2f}%'+"\n"+f'Population:{len(loyal_increasing_ctr)}'
	axs[0].hist(loyal_increasing_ctr,bin_inc,histtype='bar',rwidth=0.8,label=lab_inc,color='#42ACFE')
	axs[0].set_title(f'CTR Increasing Population')
	axs[0].set_xlabel('CTR %')
	axs[0].set_ylabel('Reader Count')

	lab_dec = f'Mean Decrease:{mean_decreasing_loyal:.2f}%'+"\n"+f'Population:{len(loyal_decreasing_ctr)}'
	axs[1].hist(loyal_decreasing_ctr,bin_inc,histtype='bar',rwidth=0.8,label=lab_dec,color='#FE6342')
	axs[1].set_title('CTR Decreasing Population')
	axs[1].set_xlabel('CTR %')
	axs[1].set_ylabel('Reader Count')
	
	fig.suptitle(f'CTR Dist of Loyal Glamour Readers (p:{p_ctr:.2f})')
	### Folder Prep ###
	folder_q2 = 'q2_figures'
	folder_q22 = 'q22'
	filen = os.path.join(os.getcwd(),folder_q2,folder_q22,'ctr_dist_loyal_bef_after.png')
	### End Prep ###
	print(f'Saving the graph showing CTR distributions of the loyal readers before and after the campaign in Folder:{filen}')
	fig.savefig(filen)
	plt.close()

	################################################################
	#################### END OF Q2.2 INVESTIG ######################
	################################################################

	#################################################################
	######################## COHORT ANALYSIS ########################
	#################################################################
	print('#################################################################')
	print('######################## RETENTION GRAPH ########################')
	print('#################################################################\n')
	print(f'Q2.3) Monthly Cohort Retention Graph for Pitchfork is being generated...')
	df_q23 = loadColumns(df=df,filterValue=['Brand','Date','User_Id'])
	df_q23_Pfork = filterByColumnsValue(df=df_q23,column=df_q23['Brand'],filterValue=['Pitchfork'])
	# print('df_q23_Pfork = ',df_q23_Pfork)

	pd.set_option('mode.chained_assignment', None)
	df_q23_Pfork['Date'] = pd.to_datetime(df_q23_Pfork['Date'])
	df_q23_Pfork['visit_month'] = df_q23_Pfork['Date'].dt.to_period('M')
	# print(df_q23_Pfork)

	df_q23_Pfork['cohort'] = df_q23_Pfork.groupby('User_Id')['Date'].transform('min').dt.to_period('M')
	# print(df_q23_Pfork.head(30))

	# Group by cohort, then visit_month, sum all the unique user ids
	df_cohort = df_q23_Pfork.groupby(['cohort', 'visit_month']) \
              .agg(n_customers=('User_Id', 'nunique')) \
              .reset_index(drop=False)

	df_cohort['period_number'] = (df_cohort.visit_month - df_cohort.cohort).apply(attrgetter('n'))

	cohort_pivot = df_cohort.pivot_table(index = 'cohort',
                                     columns = 'period_number',
                                     values = 'n_customers')
	
	cohort_size = cohort_pivot.iloc[:,0]
	retention_matrix = cohort_pivot.divide(cohort_size, axis = 0)

	with sns.axes_style("white"):
		fig, ax = plt.subplots(1, 2, figsize=(12, 8), sharey=True, gridspec_kw={'width_ratios': [1, 11]})
		
		# retention matrix
		sns.heatmap(retention_matrix, 
					mask=retention_matrix.isnull(), 
					annot=True, 
					fmt='.0%', 
					cmap='RdYlGn', 
					ax=ax[1])
		ax[1].set_title('Pitchfork Monthly Cohorts: User Retention', fontsize=16)
		ax[1].set(xlabel='# of months',
				ylabel='')

		# cohort size
		cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: 'cohort_size'})
		white_cmap = mcolors.ListedColormap(['white'])
		sns.heatmap(cohort_size_df, 
					annot=True, 
					cbar=False, 
					fmt='g', 
					cmap=white_cmap, 
					ax=ax[0])

		fig.tight_layout()
		### Folder Prep ###
		folder_q2 = 'q2_figures'
		folder_q23 = 'q23'
		### End Prep ###
		filen = os.path.join(os.getcwd(),folder_q2,folder_q23,'cohort.png')
		print(f'Monthly Cohort Retention Graph is saved in Folder:{filen} ')
		fig.savefig(filen)
		plt.close()
	################################################################
	######################## END OF Q2.3 ###########################
	################################################################