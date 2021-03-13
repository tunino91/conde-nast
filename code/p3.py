import pandas as pd
import plotly as pl
import os
import datetime

import matplotlib.pyplot as plt
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors
import scipy.stats as stats
import warnings


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
	
def printmax(desk_count,mob_count,tab_count):
	new_l = [desk_count,mob_count,tab_count]
	maxpos = new_l.index(max(new_l))
	if maxpos == 0:
		print('Device type has the highest bounce rate is Desktop')
	if maxpos == 1:
		print('Device type has the highest bounce rate is Mobile')
	if maxpos == 2:
		print('Device type has the highest bounce rate is Tablet')

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
        plt.close()
    plt.show()

def hist_save(dist_arr, bins,title,label,xlabel,ylabel,fileName='file.png'):

    plt.hist(dist_arr,bins,histtype='bar',rwidth=0.8,label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(fileName)

def prepFolders():
	main_folders = ['q3_figures']
	q3_sub_folders = ['ctr_dist_after','ctr_dist_before','outlierClicks']
    # Create main folders:
	for folder in main_folders:
		if not os.path.exists(folder):
			os.makedirs(folder)
	# Create subfolders of q3:
	for folder in q3_sub_folders:
		if not os.path.exists(os.path.join(main_folders[0],folder)):
			os.makedirs(os.path.join(main_folders[0],folder))

if __name__ == '__main__':
    prepFolders()
    warnings.filterwarnings("ignore", category=UserWarning)
    ## CSV Reading into Pandas DataFrame ##
    main_folder = csv_folder()
    csv_path = find_csv_file(main_folder)
    df = pd.read_csv(filepath_or_buffer=csv_path)
    df = loadColumns(df=df,filterValue=['Brand','Market','User_Id','Event_Name','Component_Name','Site_Section'])

    # print('df.dtypes = ',df.dtypes)
    # Get Brand:Conde Nast Travel
    print(f'###################################')
    print(f'############ PART-III #############')
    print(f'###################################\n')
    print(f'Lets take a look at CTR% on Ads for Conde Nast Travelers')
    df = filterByColumnsValue(df=df,column=df['Brand'],filterValue=['Conde Nast Traveler'])

    # Get Event_Name:Adv
    df = filterByColumnsValue(df=df,column=df['Component_Name'],filterValue=['Advertisement'])

    # List of all the markets CNT in
    market_options_cnt = get_column_options(df_x=df,column='Market')
    print('Conde Nast Travler is active in: ')
    for m in market_options_cnt:
        print(m)
    
    print(f'Finding CTR% per market...Hold tight! This may take a while')
    ## Find ctr per market:
    avg_ctr_per_market = {}
    all_ctr_details = {}
    site_section_count_all_users = { 'Artists':0,
                                'Albums':0,
                                'Food':0,
                                'Entertainment':0,
                                'Homepage':0,
                                'Sports':0,
                                'Shopping':0,
                                'Fashion':0,
                                'Beautiy':0,
                                'Wellness':0,
                                'Self Care':0,
                                'Clean Eating':0,
                                'Fitness':0,
                                }
    for market_option in market_options_cnt:
        # Filter to the given market
        df_market = filterByColumnsValue(df=df,column=df['Market'],filterValue=[market_option])

        # List of all user ids in that sepcific market
        unique_users_ids = get_column_options(df_x=df,column='User_Id')
        
        # to hold the ctr of each user in each market
        user_ctr={}
        ctr_sum_all = 0
        true_user_count_with_outliers_per_mkt = 0 # so i don't include any people that has imp:0 clk:0 into my mean calculation
        ctr_count_per_mkt_perUser_list = [] # has the ctr values of each user in a specific market
        # For each User_Id in the list, filter the dataframe for that user and count #of clicks and #of impression and calculate ctr of that user
        for user in unique_users_ids:
            # Look at every user's clicks and impressions and count them
            df_user = filterByColumnsValue(df=df_market,column=df['User_Id'],filterValue=[user])
            df_clk = filterByColumnsValue(df=df_user,column=df_user['Event_Name'],filterValue=['Click'])
            df_imp = filterByColumnsValue(df=df_user,column=df_user['Event_Name'],filterValue=['Impression'])
            clk_count_per_user = df_clk.shape[0]
            imp_count_per_user = df_imp.shape[0]
            # print('clk_count_per_user = ',clk_count_per_user)
            # print('imp_count_per_user = ',imp_count_per_user)

            # Account for 0/0 (some users are not looking at ads at all)
            if imp_count_per_user != 0:
                ################################# SITE-SECTION ################################
                ############### Warning: Only exclusive to this part of the code ##############
                ### Don't copy it right away while making use of this section in the future ###
                ##  This part is responsible to understand each users site-section pref by  ###
            
                # Extract the list of single users' site-section list he/she clicked the adv for
                # print('df_usersite_sec =',list(df_clk['Site_Section'])) # Either a list like:['Entertainment', 'Food', 'Food', 'Entertainment', 'Entertainment', 'Food'] or :[]
                site_list = list(df_clk['Site_Section'])
                for site in site_list:
                    # Update all users' dictionary then print this info outside the for loops.
                    site_section_count_all_users[site] = site_section_count_all_users[site] + 1 
                #################################################################################
                #################################################################################

                true_user_count_with_outliers_per_mkt += 1
                ctr_per_user = clk_count_per_user/imp_count_per_user*100
                user_ctr[user]=ctr_per_user
                # ctr_count_per_mkt_perUser_list.append(user_ctr[user])
                ctr_sum_all += ctr_per_user
        all_ctr_details[market_option]=user_ctr # contains: Market_1->user1:value,user2:value.. Market2->user1:value,user2:value
        # print('ctr_sum_all = ',ctr_sum_all)
        avg_ctr_per_market[market_option] = ctr_sum_all/(true_user_count_with_outliers_per_mkt)
        # ctr_per_market[market_option]=user_ctr
    # print('all_ctr_details = ',all_ctr_details) # contains: Market_1->user1:value,user2:value.. Market2->user1:value,user2:value

    # print('ctr_per_market = ',ctr_per_market)
    print(f'Conde Nast Average CTR of Ads per Market:')
    for key,val in avg_ctr_per_market.items():
        print(f'{key}:{val:.2f}%')

    ## Find the site-section that has the highest CTR ##
    all_values = site_section_count_all_users.values()
    max_value = max(all_values) 
    max_key = max(site_section_count_all_users, key=site_section_count_all_users.get)
    #################################################################################

    #################################################################################
    ###### This is the result of further investigation part where we looked #########
    #########   at which site-section had the highest number of clicks ##############
    ############################ and plotting the results ###########################
    #################################################################################
    print(f'Let\'s see which site section gets the most number of advertisment clicks')
    print(f'Highest number of clicks on advertisements({max_value} of them) were obtained on {max_key} section of CNT')

    #################################################################################
    ############### PLOT ADVERTISEMENT CLICK COUNTS per SITE-SECTIONs ###############
    #################################################################################
    plt.title('NUMBER OF CLICKS ON ADVERTISEMENTS PER SITE-SECTION')
    plt.ylabel('Count')
    for site,count in site_section_count_all_users.items():
        plt.xlabel('Site Section')
        plt.bar(x='     ',height=count,label=site+f':{count}')
        plt.legend()
    
    ### Folder Prep ###
    folder_q3 = 'q3_figures'
    folder_q31 = 'ctr_dist_before'
    ### End Prep ###
    filen = os.path.join(os.getcwd(),folder_q3,folder_q31,'adClickCountnPerSiteSec.png')
    print(f'Saving a graph showing the number of clicks per site-section in Folder:{filen}')
    
    plt.savefig(filen)
    plt.close()
	#################################################################################
    #################################################################################
    ###### Plot the Histogram of CTR per parket ######
    f=os.path.join(os.getcwd(),folder_q3,folder_q31)
    print(f'Saving graphs that shows CTR per market in Folder:{f}')
    max_ctr=[]
    for market,value in all_ctr_details.items():
        ctr_dist=[]
        
        for user,ctr_value in all_ctr_details[market].items():
            ctr_dist.append(ctr_value)

        user_count = len(ctr_dist)
        
        max_ctr.append(max(ctr_dist))

        ##  Plot CTR distribution with histogram
        bins = [i for i in range(0,100)]
        title = 'CTR Distribution of ' + str(market)
        label = str(market) + ' Population:' + str(user_count) + "\n" + 'Avg CTR:'
        label = label + f'{avg_ctr_per_market[market]:.2f}%' 
        xlabel = 'CTR Count(%)'
        ylabel = 'Number of Users'

        ### Folder Prep ###
        folder_q3 = 'q3_figures'
        folder_q31 = 'ctr_dist_before'
        ### End Prep ###
        graphName=title+'.png'
        filen = os.path.join(os.getcwd(),folder_q3,folder_q31,graphName)
        hist_plt(dist_arr=ctr_dist, bins=bins,title=title,label=label,xlabel=xlabel,ylabel=ylabel,save=True,fileName=filen)
    
    end_bin = max(max_ctr)

    # How many users are there per market for cnt
    print(f'CNT Reader Count per Market: ')
    num_of_user_cnt_per_market = {}
    for market in market_options_cnt:
        ids = all_ctr_details[market].keys()
        reader_count_cnt_per_mkt = len(ids)
        num_of_user_cnt_per_market[market]=reader_count_cnt_per_mkt
        print(f'{market}:{reader_count_cnt_per_mkt}')
    # Total number of readers of CNT and sees an adv.
    tot_cnt_reader_count = sum(num_of_user_cnt_per_market.values())
    # print('CNT Reader Count per Market: ',num_of_user_cnt_per_market)

    ################################################
    ###### TAKE OUT THE OUTLIERS FROM THE DF: ######
    ################################################
    print(f'All CTR distributions seem to be similar from the graphs...Is this true?')
    print(f'Let\'s test this hypothesis!!! But first the distributions are not quite a reflection of normal distribution...')
    print(f'Unless... I take out the outliers from the distributions..')
    print(f'Let\'s see how many outliers we have in our datasets with CTR<1% & CTR>50%...')
    # First find the user_ids of the outliers 
    outlier_user_id_list = []
    outlier_user_id_list_low = []
    for market,value in all_ctr_details.items():

        for user,ctr_value in all_ctr_details[market].items():
            if ctr_value < 1:
                outlier_user_id_list.append(user)
                outlier_user_id_list_low.append(user)
            elif ctr_value > 50:
                outlier_user_id_list.append(user)
            
    # print('Outlier User_Ids: ',outlier_user_id_list)
    print(f'There are {len(outlier_user_id_list)} of outliers out of {tot_cnt_reader_count} readers')
    print(f'That\'s a quite high number of readers we are not considering..')
    #############################################
    ### PART WHERE WE GET RID OF THE OUTLIERS ###
    #############################################
    ## Get rid of all the rows from the df which was filtered as Brand:CNT,Component_Name:Adver
    ## This way now we can start to calculate the CNT per user again w/o the outliers
    df_no_outlier = df.copy()
    # print('shape of df_no_outlier AFTER outlier filter ',df_no_outlier.shape)
    for outlier_id in outlier_user_id_list:
        # get the names of indexes for
        indexNames = df_no_outlier[df_no_outlier['User_Id'] == int(outlier_id)].index
        df_no_outlier.drop(indexNames,inplace=True)
    # print('df_no_outlier = ',df_no_outlier)
    pure_pop_count_across_mkts = df_no_outlier.shape[0]
    print(f'Population count after the outlier exclusion:{pure_pop_count_across_mkts}')

    ##################################################
    ### THIS PART IS TAKEN FROM ABOVE,REPETITION #####
    ###### TO FIND THE CTR DIST PER MARKET AGAIN #####
    ### Only diff with above code that i subst df with df_no_outlier everywhere
    print(f'Now let\'s see whether CTR distribution per market changes after taking out the outliers...')
    # List of all the markets
    market_options_cnt = get_column_options(df_x=df_no_outlier,column='Market')
    # print('market_options_cnt = ',market_options_cnt)

    ## Find ctr per market:
    avg_ctr_per_market = {}
    all_ctr_details = {}
    for market_option in market_options_cnt:
        # Filter to the given market
        df_market = filterByColumnsValue(df=df_no_outlier,column=df_no_outlier['Market'],filterValue=[market_option])

        # List of all user ids
        unique_users_ids = get_column_options(df_x=df_no_outlier,column='User_Id')
        
        # to hold the ctr of each user in each market
        user_ctr={}
        ctr_sum_all = 0
        true_user_count_wo_outliers = 0 # so i don't include any people that has imp:0 clk:0 into my mean calculation
        ctr_count_per_mkt_perUser_list = [] # has the ctr values of each user in a specific market
        # For each User_Id in the list, filter the dataframe for that user and count #of clicks and #of impression and calculate ctr of that user
        for user in unique_users_ids:
            df_user = filterByColumnsValue(df=df_market,column=df['User_Id'],filterValue=[user])
            df_clk = filterByColumnsValue(df=df_user,column=df_user['Event_Name'],filterValue=['Click'])
            df_imp = filterByColumnsValue(df=df_user,column=df_user['Event_Name'],filterValue=['Impression'])
            clk_count_per_user = df_clk.shape[0]
            imp_count_per_user = df_imp.shape[0]
            # print('clk_count_per_user = ',clk_count_per_user)
            # print('imp_count_per_user = ',imp_count_per_user)
            ## account for 0/0,
            if imp_count_per_user != 0:
                true_user_count_wo_outliers += 1
                ctr_per_user = clk_count_per_user/imp_count_per_user*100
                user_ctr[user]=ctr_per_user
                # ctr_count_per_mkt_perUser_list.append(user_ctr[user])
                ctr_sum_all += ctr_per_user
        all_ctr_details[market_option]=user_ctr # contains: Market_1->user1:value,user2:value.. Market2->user1:value,user2:value
        # print('ctr_sum_all = ',ctr_sum_all)
        avg_ctr_per_market[market_option] = ctr_sum_all/(true_user_count_wo_outliers)
        # ctr_per_market[market_option]=user_ctr
    # print('all_ctr_details = ',all_ctr_details)

    # print('ctr_per_market = ',ctr_per_market)
    print('Average CTR per Market w/o Outliers:',avg_ctr_per_market)

    max_ctr=[]

    ## Plot the histogram of ctr per parket
    for market,value in all_ctr_details.items():
        ctr_dist=[]
        
        for user,ctr_value in all_ctr_details[market].items():
            ctr_dist.append(ctr_value)

        user_count = len(ctr_dist)
        max_ctr.append(max(ctr_dist))

        ##  Plot ctr distribution with histogram
        bins = [i for i in range(0,100)]
        title = 'CTR Distribution of ' + str(market) + '(No Outliers)'
        label = str(market) + ' Population:' + str(user_count) + "\n" + 'Avg CTR:'
        label = label + f'{avg_ctr_per_market[market]:.2f}%' 
        xlabel = 'CTR Count(%)'
        ylabel = 'Number of Users'
        ### Folder Prep ###
        folder_q3 = 'q3_figures'
        folder_q31 = 'ctr_dist_after'
        ### End Prep ###
        graphName=title+'.png'
        filen = os.path.join(os.getcwd(),folder_q3,folder_q31,graphName)
        hist_plt(dist_arr=ctr_dist, bins=bins,title=title,label=label,xlabel=xlabel,ylabel=ylabel,save=True,fileName=filen)
    
    end_bin = max(max_ctr)

    # How many users are there per market for cnt
    print(f'CNT Reader Count per Market: ')
    num_of_user_cnt_per_market_no_oliers = {}
    for market in market_options_cnt:
        ids = all_ctr_details[market].keys()
        reader_count_cnt_per_mkt = len(ids)
        num_of_user_cnt_per_market_no_oliers[market]=reader_count_cnt_per_mkt
        print(f'{market}:{reader_count_cnt_per_mkt}')
    # Total number of readers of CNT and sees an adv.
    tot_cnt_reader_count = sum(num_of_user_cnt_per_market_no_oliers.values())
    # print('CNT Reader Count per Market: ',num_of_user_cnt_per_market_no_oliers)

    ##################################################
    ################### ANOVA ########################
    ##################################################
    print(f'After taking out the outliers, the distributions look much closer to gaussian...\nAnd I know that these are independent sets... ')
    print(f'Running ANOVA Test to see if these values are in fact similar')
    me_list = list(all_ctr_details['Middle East'].values())
    sp_list = list(all_ctr_details['Spain'].values())
    us_list = list(all_ctr_details['U.S.'].values())
    it_list = list(all_ctr_details['Italy'].values())
    in_list = list(all_ctr_details['India'].values())
    ch_list = list(all_ctr_details['China'].values())
    uk_list = list(all_ctr_details['U.K.'].values())
    f_val,p_val = stats.f_oneway(me_list, sp_list, us_list, it_list, in_list,ch_list,uk_list)
    print(f'f-val:{f_val:.2f},p-val:{p_val:.2f}')
    if p_val>0.05:
        print(f'Since p-value is greater than 0.05 we can say that means of CTR% of all CNT Advertisement are similar!')
    else:
        print(f'Since p-value is less than 0.05 we can say that means of CTR% of all CNT Averstisement are NOT similar!')
    ####################################################################################
    ############ WHAT ARE THOSE OUTLIERS WITH <1% ARE CLICKING ON ACTUALLY? ############
    ####################################################################################
    site_section_count_outlier_users = { 'Artists':0,
                                'Albums':0,
                                'Food':0,
                                'Entertainment':0,
                                'Homepage':0,
                                'Sports':0,
                                'Shopping':0,
                                'Fashion':0,
                                'Beautiy':0,
                                'Wellness':0,
                                'Self Care':0,
                                'Clean Eating':0,
                                'Fitness':0,
                                }

    for low_outlier in outlier_user_id_list_low:
        # Get single outliers' data frame
        df_one_outlier = filterByColumnsValue(df=df,column=df['User_Id'],filterValue=[low_outlier])
        # Find the clicks
        df_one_outlier_clk = filterByColumnsValue(df=df_one_outlier,column=df['Event_Name'],filterValue=['Click'])
        # Get which site-section reader was clicking
        one_outlier_site_list = get_column_options(df_x=df_one_outlier_clk,column='Site_Section')
        
        for site in site_section_count_outlier_users:
            # Update all users' dictionary then print this info outside the for loops.
            site_section_count_outlier_users[site] = site_section_count_outlier_users[site] + 1

    ## Find the site-section that has the highest CTR ##
    all_values = site_section_count_outlier_users.values() 
    max_value = max(all_values)  ### Turns out all of the values are exactly same inside all_values list
    max_key = max(site_section_count_all_users, key=site_section_count_all_users.get)
    print(f'Remember those outliers whos CTR% were less than 1%...{len(outlier_user_id_list)} of them')
    print(f'They were clicking to all sections of the site equally,exactly {max_value} clicks per section...')
    #############################################################################
    #### PLOT ADVERTISEMENT CLICK COUNTS per SITE-SECTIONs (OUTLIERS:CTR<1%) ####
    #############################################################################
    plt.title('NUMBER OF CLICKS ON ADVERTISEMENTS PER SITE-SECTION FOR (OUTLIERS:CTR<1%)')
    plt.ylabel('Count')
    for site,count in site_section_count_outlier_users.items():
        plt.xlabel('Site Section')
        plt.bar(x='     ',height=count,label=site+f':{count}')
        plt.legend()
    
    ### Folder Prep ####
    folder_q3 = 'q3_figures'
    folder_q32 = 'ctr_dist_after'
    filen = os.path.join(os.getcwd(),folder_q3,folder_q32,'adClickCountnPerSiteSecOutliers.png')
    ### Folder Ready ####
    plt.savefig(filen)
    plt.close()
	#################################################################################
    #################################################################################