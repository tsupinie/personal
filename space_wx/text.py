import numpy as np
import smtplib
from urllib import urlopen
import datetime
from email.mime.text import MIMEText
import string
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

def mail(to, subject, text):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

def file_recent(url_obj, last_run_date):
    i = url_obj.info()
    last_mod_date = i.getdate('last-modified')
    print last_mod_date
    print last_run_date

    if last_mod_date > last_run_date:
        return True
    else:
        return False

def send_text(phone_number, subject, msg):
    from_line = "Space Wx Alert Prgm"
    mail(str(phone_number) + '@txt.att.net', subject, msg)

def read_url_text(url_obj):
    data = url_obj.readlines()
    return data

def get_acedata_table(file_lines):
    table = []
    for l in file_lines:
        split = l.split()
        try:
            float(split[0])
        except:
            continue
        table.append(split)
    table = np.asarray(table)
    return table

def geomagstorm_occuring(file_lines):
    line = ""
    for l in file_lines:
        if "Geomagnetic storms reaching the " in l:
            G = int(l.split(' ')[4][1])
            return G
    return None

def geomagstorm_expected(file_lines):
    line = ""
    for l in file_lines:
        if "Geomagnetic storms reaching the " in l:
             G = int(l.split(' ')[4][1])
             return G
    return None

def get_Kp_index(file_lines):
    line = ""
    for l in file_lines:
        if "The estimated planetary K-index" in l:
            kp = int(l.split(' ')[11][0])
            return kp

def isKp_above_treshold(obs_kp):
    return obs_kp >= KP_TRESH

def is_G_above_treshold(obs_G):
    return obs_G >= GEOMAG_TRESH

def is_BS_above_threshold(obs_BS):    
    return obs_BS >= SOLAR_WIND_TRESH

def is_IMF_above_threshold(obs_IMF):
    return obs_IMF <= IMF_MEAN_TRESH

gmail_user = "aurora.alerts@gmail.com"
gmail_pwd = "qu3uswE3"

KP_TRESH = 7
GEOMAG_TRESH = 3
SOLAR_WIND_TRESH = 500 #km/s
IMF_MEAN_TRESH = -10 #nT

phone_no = [2403287819, 3167085076]

last_run_dict = np.load('last_run.npz')
last_date_1 = tuple(last_run_dict['wwv'])
last_date_2 = tuple(last_run_dict['ace_swe'])
last_date_3 = tuple(last_run_dict['ace_mag'])

#last_run_dict = {}
#early_date = datetime.datetime.utctimetuple(datetime.datetime.utcnow())
#last_date_1 = early_date
#last_date_2 = early_date
#last_date_3 = early_date
#print last_date_3
new_last_run_dict = {}

#PARSE GEOPHYSICAL ALERT MESSAGE FOR NECESSARY DATA
obj = urlopen('http://www.swpc.noaa.gov/ftpdir/latest/wwv.txt')

if 'ob_kp_last' in last_run_dict:
	ob_kp_last = last_run_dict['ob_kp_last']
else:
	ob_kp_last = 0

if 'g_occ_last' in last_run_dict:
	g_occ_last = last_run_dict['g_occ_last']
else:
	g_occ_last = 0

if 'g_exp_last' in last_run_dict:
	g_exp_last = last_run_dict['g_exp_last']
else:
	g_exp_last = 0

if 'bs_last' in last_run_dict:
	bs_last = last_run_dict['bs_last']
else:
	bs_last = 0

if 'bs_avg_last' in last_run_dict:
	bs_avg_last = last_run_dict['bs_avg_last']
else:
	bs_avg_last = 0

if 'bz_last' in last_run_dict:
	bz_last = last_run_dict['bz_last']
else:
	bz_last = 0

if 'bz_avg_last' in last_run_dict:
	bz_avg_last = last_run_dict['bz_avg_last']
else:
	bz_avg_last = 0

if file_recent(obj, last_date_1):
	 
	text = read_url_text(obj)
	ob_kp = get_Kp_index(text)
	g_exp = geomagstorm_expected(text)
	g_occ = geomagstorm_occuring(text)

	msg = ""
	if isKp_above_treshold(ob_kp) and not isKp_above_treshold(ob_kp_last):
	    msg = 'K-index @ ' + str(ob_kp)

	if g_occ is not None:
	    if is_G_above_treshold(g_occ) and not is_G_above_treshold(g_occ_last):
	        msg += "\nG%d Storm Occurred." % g_occ

	if g_exp is not None:
	    if is_G_above_treshold(g_exp) and not is_G_above_treshold(g_exp_last):
	        msg += "\nG%d Storm Expected." % g_exp

	if msg is not "":
	    for no in phone_no:
	        send_text(no, "GeoPhys Alert Msg", msg)

	new_last_run_dict['wwv'] = np.asarray(datetime.datetime.utctimetuple(datetime.datetime.utcnow()))
	new_last_run_dict['ob_kp_last'] = ob_kp
	new_last_run_dict['g_occ_last'] = g_occ
	new_last_run_dict['g_exp_last'] = g_exp
else:
	new_last_run_dict['wwv'] = np.asarray(last_date_1)
	new_last_run_dict['ob_kp_last'] = ob_kp_last
	new_last_run_dict['g_occ_last'] = g_occ_last
	new_last_run_dict['g_exp_last'] = g_exp_last
#PARSE ACE DATA FOR NECSSARY INFORMATION

obj = urlopen('http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_swepam_1m.txt')

if file_recent(obj, last_date_2):

	text = read_url_text(obj)
	table = get_acedata_table(text)
	bulk_speed = []
	ace_msg = ""
	table = table.T
	for S,bs in zip(table[6], table[8]):
	    if int(S) == 0:
	        bulk_speed.append(float(bs))
	bulk_speed = np.asarray(bulk_speed)

	avg_bs = np.mean(bulk_speed)

	if is_BS_above_threshold(bulk_speed[-1]) and not is_BS_above_threshold(bs_last):
	    ace_msg = "Solar Wind @ %.1f km/s" % bulk_speed[-1]

	if is_BS_above_threshold(avg_bs) and not is_BS_above_threshold(bs_avg_last):
	    if ace_msg != "":
	        ace_msg += "\n"

	     ace_msg += "Solar Wind 2 hr Avg @ %.1f km/s" % avg_bs  

	if ace_msg is not "":
	    for no in phone_no:
	        send_text(no, "Solar Wind Alert", ace_msg)

	new_last_run_dict['ace_swe'] = np.asarray(datetime.datetime.utctimetuple(datetime.datetime.utcnow()))
	new_last_run_dict['bs_last'] = bulk_speed[-1]
	new_last_run_dict['bs_avg_last'] = avg_bs
else:
	new_last_run_dict['ace_swe'] = np.asarray(last_date_2)
	new_last_run_dict['bs_last'] = bs_last
	new_last_run_dict['bs_avg_last'] = bs_avg_last
#BZ Data
#PARSE ACE DATA FOR NECSSARY INFORMATION

obj = urlopen('http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_mag_1m.txt')

if file_recent(obj, last_date_3):

	text = read_url_text(obj)
	table = get_acedata_table(text)
	bz_array = []
	ace_msg = ""
	table = table.T
	for S,bz in zip(table[6], table[9]):
	    if int(S) == 0:
	        bz_array.append(float(bz))
	bz_array = np.asarray(bz_array)
	avg_bz = np.mean(bz_array)

	if is_IMF_above_threshold(bz_array[-1]) and not is_IMF_above_threshold(bz_last):
	    ace_msg = "Bz @ %.1f nT" % bz_array[-1]

	if is_IMF_above_threshold(avg_bs) and not is_IMF_above_threshold(bz_avg_last):
	    if ace_msg != "":
	        ace_msg += "\n"

	    ace_msg += "Bz 2 hr Avg @ %.1f nT" % avg_bz

	if ace_msg is not "":
	    for no in phone_no:
	        #print 'Sending text: Bz Alert'
	        send_text(no, "Bz Alert", ace_msg)

	new_last_run_dict['ace_mag'] = np.asarray(datetime.datetime.utctimetuple(datetime.datetime.utcnow()))
	new_last_run_dict['bz_last'] = bz_array[-1]
	new_last_run_dict['bz_avg_last'] = avg_bz
else:
	new_last_run_dict['ace_mag'] = np.asarray(last_date_3)
	new_last_run_dict['bz_last'] = bz_last
	new_last_run_dict['bz_avg_last'] = bz_avg_last

last_run_dict = new_last_run_dict
np.savez('last_run.npz', **last_run_dict)
