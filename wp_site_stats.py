#build site stats file with site owner info
import pandas as pd
import mysql.connector

#connect to db
#currently set to local db powered by MAMP which contains wp_blogs and all options tables
#ideally, this could be connected to a metrics-specific version of full wp db
#and it should work, although memory may need to be increased.
cnx = mysql.connector.connect(user='root', password='root', host='localhost', port=8889, database='wp')

#---------------Users info------------------
#load users from csv
users_df = pd.read_csv('wp_users_all.csv')

#cleaning users_df raw data
#clean up the division column as IDM has not standardized input. 
div_dict = {"Faculty of Arts and Science" : "College of Arts and Science",\
            "The Steinhardt School of Culture, Education, and Human Development" : "Steinhardt School",\
            "Steinhardt School of Culture, Education, and Human Development" : "Steinhardt School",\
            "Student Affairs" : "Office of the President",\
            "Polytechnic School of Engineering" : "Tandon School of Engineering",\
            "Leonard N Stern School of Business" : "Stern School of Business",\
            "University Enrollment Management" : "Office of the President",\
            "Faculty of Arts & Science" : "College of Arts and Science",\
            "NYU Abu Dhabi" : "Abu Dhabi", "Academic Technology Systems" : "NYU IT",\
            "ATS Media Support" : "NYU IT", "Jeff Lehman / Yu Lizhong" : "Shanghai",\
            "NYU - Global" : "Office of the President", "Abu Dhabi NY Campus" : "Abu Dhabi",\
            "Global Technology Services" : "NYU IT", "Information Technology Services" : "NYU IT",\
            "Global Programs" : "Office of the President",\
            "NYU Tandon School of Engineering" : "Tandon School of Engineering",\
            "Institute for Public Knowledge" : "Office of the President",\
            "Robert F. Wagner Graduate School of Public Service" : "Robert F Wagner Graduate School of Public Service",\
            "Office of the Provost" : "Office of the President",\
            "NYU - Florence" : "Florence",\
            "Office of the Vice Provost for Research and Faculty Affairs" : "Office of the President",\
            "Faculty of Arts & Science / Liberal Studies" : "College of Arts and Science",\
            "Office of the Vice Provost for Faculty, Arts, Humanities & Diversity" : "Office of the President",\
            "Office of the NYU President" : "Office of the President",\
            "Office of the Executive Vice President" : "Office of the President",\
            "Office of the Vice Chancellor, University Life and Global Programs" : "Office of the President",\
            "Abu Dhabi Campus" : "Abu Dhabi", "Rory Meyers College of Nursing" : "College of Nursing",\
            "Capital Projects and Facilities" : "Office of the President", "NYU - Buenos Aires" : "Buenos Aires",\
            "NYU Shanghai" : "Shanghai", "NYU - Shanghai" : "Shanghai", "NYU - Berlin" : "Berlin",\
            "NYU - Madrid" : "Madrid", "Systems & Svcs-Office of the Assoc VP" : "Office of the President",\
            "Office of the Chief of Staff" : "Office of the President",\
            "Steinhardt School of Culture, Education and Human Development" : "Steinhardt School",\
            "Office of the Senior Vice Provost for Research" : "Office of the President",\
            "NYU - London" : "NYU London", "CUSP" : "Center for Urban Science and Progress",\
            "Student Link" : "Office of the President", "NYU Florence" : "Florence",\
            "Office of the SVP Finance and Budget/Chief Financial Officer" : "Office of the President",\
            "Washington Square College" : "Office of the President",\
            "CDV-Office of the Controller" : "Office of the President",\
            "Internal Audit" : "Office of the President",\
            "Office of Budget and Financial Planning" : "Office of the President",\
            "Office of the President Emeritus III" : "Office of the President",\
            "Office of the Treasurer" : "Office of the President",\
            "Provost Fiscal Affairs" : "Office of the President", "University Deans" : "Office of the President",\
            "Investment Office" : "Office of the President",\
            "Financial Operations & Treasurer" : "Office of the President",\
            "Office of the Executive Vice President for Health" : "Office of the President",\
            "NYU - Paris" : "Paris", "College of Dentistry - Continuing Education" : "College of Dentistry",\
            "Office of the Vice Provost for Globalization & Multicultural Affairs" : "Office of the President",\
            "OFC VP FIN OPS AND TREASURY" : "Office of the President",\
            "Office of the Senior Vice Provost For Academic Affairs" : "Office of the President",\
            "ALI Admin" : "School of Professional Studies",\
            "CDV-Bursar/Student Financials" : "Office of the President",\
            "University Life" : "Office of the President", "NYU Prague" : "Prague",\
            "NYU - Prague" : "Prague", "Provostial Areas" : "Office of the President",\
            "NYU in DC" : "NYU DC", "Facilities and Construction Management" : "Office of the President",\
            "NYU Paris" : "Paris", "NYU London" : "London", }
users_df = users_df.replace(div_dict)

#clean and standardize affiliate subtype.  
#We are focused on student/faculty/staff and at this point don't need all of the smaller groups.
as_dict = {"administrator" : "staff", "student employee" : "student", "degree" : "student",\
           "adjunct faculty" : "faculty", "account_sponsored_staff" : "staff", "office staff" : "staff",\
           "program_affiliate_other" : "staff", "nondegree sps" : "student", "contractor" : "staff",\
           "prospective_employee" : "staff", "technical staff" : "staff", "som_faculty" : "faculty",\
           "som_employee" : "staff", "retired employee" : "retired", "retired faculty" : "retired",\
           "program_affiliate_scholar" : "faculty", "casual employee" : "staff",\
           "global_employee" : "staff", "special_service_account" : "staff",\
           "research assistant" : "researcher", "nondegree" : "student", "service staff" : "staff",\
           "student_applicant" : "student", "admitted_student" : "student", "noncredit tandon" : "student",\
           "nyumc_affiliate" : "staff", "nondegree sps ali" : "staff", "nyuhc_employee" : "staff",\
           "graduate assistant" : "student", "nondegree cert" : "student",\
           "account_sponsored_student" : "student", "visiting_scholar" : "faculty",\
           "noncredit steinhardt" : "student", "visiting_academic_other" : "faculty",\
           "som_voluntary_faculty" : "faculty", "emeritus faculty" : "faculty", "employee_temp" : "staff",\
           "field_instructor" : "faculty", "general_id_other" : "staff", "sh_employee" : "staff",\
           "poly_applicant" : "student", "nondegree sps cert" : "student", "noncredit silver" : "student",\
           "teaching assistant" : "student", "trustee_law" : "trustee", "som_house_staff" : "staff",\
           "nondegree dental" : "student", "college_preview" : "student", "noncredit cas" : "student",\
           "nondegree sps diploma" : "student", "summer_associate" : "staff",\
           "ad_executive_authority" : "staff", "special_student" : "student", "ad_contingent" : "staff",\
           "nondegree dental intl" : "student", "admin_account" : "staff", "noncredit shanghai" : "student",\
           "global_building_resident" : "staff"}
users_df = users_df.replace(as_dict)


#clean affiliation. only current faculty, students, and staff can access the service, so we group all others.
users_df = users_df.replace(['former affiliate', 'former employee', 'former student', 'no_affiliation_info',\
                        'recent employee', 'recent student', 'current alumni', 'recent affiliate', ''],'access removed')

#drop first and last name from users_df
users_df = users_df.drop(['Last Name', 'First Name'], axis=1)

#at this point you have a clean version of user data provided by IDM.
#users_df can be downloaded for visualization or analyzed further
#users_df.to_csv('processed_user_data')

#-----------Plugins, site owner, and Jetpack info-----------------
#get info from wpdev options tables
#Options tables in WP contain information about plugins and the admin email by default.
#Some plugins, such as Jetpack, also store data in the options tables.

#connection is set above
#Step 1: get a list of all options tables and create new df
cur = cnx.cursor(buffered=True)
query = ("SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%_options'")
cur.execute(query)
df = pd.DataFrame(cur.fetchall())
cur.close()

#step 2: get raw plugins information from each options table, append to df
cur2 = cnx.cursor()
def getPlugins(tname):
    query2 = ("SELECT option_value FROM %s WHERE option_name='active_plugins'") % tname
    cur2.execute(query2)
    return cur2.fetchone()

df['raw_plugins'] = df.apply(lambda row: getPlugins(row[0]), axis=1)
cur2.close()

#step 3: get admin email for each site from options table and append to df
cur3 = cnx.cursor()
def getSiteAdmins(tname):
    query3 = ("SELECT option_value FROM %s WHERE option_name='admin_email'") % tname
    cur3.execute(query3)
    return cur3.fetchone()

df['admin_email'] = df.apply(lambda row: getSiteAdmins(row[0]), axis=1)
cur3.close()

#step 4: get jetpack module info
cur4 = cnx.cursor()
def getJetpack(tname):
    query4 = ("SELECT option_value FROM %s WHERE option_name='jetpack_active_modules'") % tname
    cur4.execute(query4)
    return cur4.fetchone()

df['jetpack_raw'] = df.apply(lambda row: getJetpack(row[0]), axis=1)
cur4.close()

#step 5: get theme info
cur5 = cnx.cursor()
def getTheme(tname):
    query5 = ("SELECT option_value FROM %s WHERE option_name='stylesheet'") % tname
    cur5.execute(query5)
    return cur5.fetchone()

df['theme'] = df.apply(lambda row: getTheme(row[0]), axis=1)
cur5.close()

#data cleaning
#get clean admin email
df['admin_email'] = df['admin_email'].astype(str)
df['admin_email'] = df['admin_email'].str[2:-3]

#create NetID column
df['NetID'] = df['admin_email'].str[:-8]

#get site ID from the table name. (for joining tables later)
def getID(tn):
    tn = str(tn)
    return tn[3:-8]
    
#a func for each plugin. to check the active_plugins output stored in raw_plugins    
def attachmentImporter(s):
    s = str(s)
    if 'attachment-importer/index.php' in s:
        return 1
    else:
        return 0
    
def aesop(s):
    s = str(s)
    if 'aesop-story-engine/aesop-core.php' in s:
        return 1
    else:
        return 0
    
def autoblog(s):
    s = str(s)
    if 'autoblog/autoblogpremium.php' in s:
        return 1
    else:
        return 0
    
def bbPress(s):
    s = str(s)
    if 'bbpress/bbpress.php' in s:
        return 1
    else:
        return 0
    
def videoGallery(s):
    s = str(s)
    if 'contus-video-gallery/hdflvvideoshare.php' in s:
        return 1
    else:
        return 0
    
def customSidebars(s):
    s = str(s)
    if 'custom-sidebars/customsidebars.php' in s:
        return 1
    else:
        return 0
    
def displayPostsShortcode(s):
    s = str(s)
    if 'display-posts-shortcode/display-posts-shortcode.php' in s:
        return 1
    else:
        return 0
    
def duplicatePost(s):
    s = str(s)
    if 'duplicate-post/duplicate-post.php' in s:
        return 1
    else:
        return 0
    
def emailUsers(s):
    s = str(s)
    if 'email-users/email-users.php' in s:
        return 1
    else:
        return 0
    
def embedWebmap(s):
    s = str(s)
    if 'embed-webmap/embed-webmap.php' in s:
        return 1
    else:
        return 0
    
def enableMediaReplace(s):
    s = str(s)
    if 'enable-media-replace/enable-media-replace.php' in s:
        return 1
    else:
        return 0

def everyCalendar(s):
    s = str(s)
    if 'every-calendar-1/ecp1-plugin.php' in s:
        return 1
    else:
        return 0
    
def feedWordPress(s):
    s = str(s)
    if 'feedwordpress/feedwordpress.php' in s:
        return 1
    else:
        return 0
    
def gDocEmbed(s):
    s = str(s)
    if 'google-document-embedder/gviewer.php' in s:
        return 1
    else:
        return 0
    
def iframe(s):
    s = str(s)
    if 'iframe/iframe.php' in s:
        return 1
    else:
        return 0
    
def imageWall(s):
    s = str(s)
    if 'image-wall/image-wall.php' in s:
        return 1
    else:
        return 0
    
def importUsers(s):
    s = str(s)
    if 'import-users-from-csv/import-users-from-csv.php' in s:
        return 1
    else:
        return 0
    
def jetpack(s):
    s = str(s)
    if 'jetpack/jetpack.php' in s:
        return 1
    else:
        return 0
    
def leaflet(s):
    s = str(s)
    if 'leaflet-maps-marker/leaflet-maps-marker.php' in s:
        return 1
    else:
        return 0
    
def legacyCSS(s):
    s = str(s)
    if 'legacy-jetpack-custom-css-editor/legacy-jetpack-custom-css-editor.php' in s:
        return 1
    else:
        return 0
    
def nextGen(s):
    s = str(s)
    if 'nextgen-gallery/nggallery.php' in s:
        return 1
    else:
        return 0
    
def pvgm(s):
    s = str(s)
    if 'photo-video-gallery-master/photo-video-gallery-master.php' in s:
        return 1
    else:
        return 0
    
def pintrest(s):
    s = str(s)
    if 'pinterest-rss-widget/pinterest-rss-widget.php' in s:
        return 1
    else:
        return 0
    
def postTypeSwitcher(s):
    s = str(s)
    if 'post-type-switcher/post-type-switcher.php' in s:
        return 1
    else:
        return 0
    
def simpleMathjax(s):
    s = str(s)
    if 'simple-mathjax/simple-mathjax.php' in s:
        return 1
    else:
        return 0
    
def subscribeByEmail(s):
    s = str(s)
    if 'subscribe-by-email/subscribe-by-email.php' in s:
        return 1
    else:
        return 0
    
def guestPostSubmit(s):
    s = str(s)
    if 'tt-guest-post-submit/tt-guest-post-submit.php' in s:
        return 1
    else:
        return 0
    
def tumblr(s):
    s = str(s)
    if 'tumblr-widget-for-wordpress/tumblr-widget.php' in s:
        return 1
    else:
        return 0
    
def usp(s):
    s = str(s)
    if 'user-submitted-posts/user-submitted-posts.php' in s:
        return 1
    else:
        return 0
    
def accessibility(s):
    s = str(s)
    if 'wp-accessibility/wp-accessibility.php' in s:
        return 1
    else:
        return 0
    
def proQuiz(s):
    s = str(s)
    if 'wp-pro-quiz/wp-pro-quiz.php' in s:
        return 1
    else:
        return 0
    
def recaptcha(s):
    s = str(s)
    if 'wp-recaptcha/wp-recaptcha.php' in s:
        return 1
    else:
        return 0
    
def postVotes(s):
    s = str(s)
    if 'wpmu-dev-post-votes/wpmu-dev-post-votes.php' in s:
        return 1
    else:
        return 0
    
def googleMaps(s):
    s = str(s)
    if 'wpmu_dev_maps_plugin/wpmu_dev_maps_plugin.php' in s:
        return 1
    else:
        return 0
    
def yopPoll(s):
    s = str(s)
    if 'yop-poll/yop_poll.php' in s:
        return 1
    else:
        return 0
    
def zotPress(s):
    s = str(s)
    if 'zotpress/zotpress.php' in s:
        return 1
    else:
        return 0

#make a column with blog ID so we can join to a df of wp_blogs    
df['blog_id'] = df.apply(lambda row: getID(row[0]), axis=1)

#create a new column for each plugin and check if active on raw_plugins list
df['Attachment-Importer'] = df.apply(lambda row: attachmentImporter(row[1]), axis=1)
df['Aesop-Story-Engine'] = df.apply(lambda row: aesop(row[1]), axis=1)
df['Autoblog'] = df.apply(lambda row: autoblog(row[1]), axis=1)
df['bbPress'] = df.apply(lambda row: bbPress(row[1]), axis=1)
df['Video-Gallery'] = df.apply(lambda row: videoGallery(row[1]), axis=1)
df['Custom-Sidebars'] = df.apply(lambda row: customSidebars(row[1]), axis=1)
df['Display-Posts-Shortcode'] = df.apply(lambda row: displayPostsShortcode(row[1]), axis=1)
df['Email-Users'] = df.apply(lambda row: emailUsers(row[1]), axis=1)
df['Embed-Webmap'] = df.apply(lambda row: embedWebmap(row[1]), axis=1)
df['Enable-Media-Replace'] = df.apply(lambda row: enableMediaReplace(row[1]), axis=1)
df['Every-Calendar'] = df.apply(lambda row: everyCalendar(row[1]), axis=1)
df['Feed-WordPress'] = df.apply(lambda row: feedWordPress(row[1]), axis=1)
df['G-Doc-Embedder'] = df.apply(lambda row: gDocEmbed(row[1]), axis=1)
df['iFrame'] = df.apply(lambda row: iframe(row[1]), axis=1)
df['Image-Wall'] = df.apply(lambda row: imageWall(row[1]), axis=1)
df['Bulk-Import-Users'] = df.apply(lambda row: importUsers(row[1]), axis=1)
df['Jetpack'] = df.apply(lambda row: jetpack(row[1]), axis=1)
df['Leaflet-Maps-Marker'] = df.apply(lambda row: leaflet(row[1]), axis=1)
df['Legacy-Custom-CSS'] = df.apply(lambda row: legacyCSS(row[1]), axis=1)
df['NextGen'] = df.apply(lambda row: nextGen(row[1]), axis=1)
df['PVGM'] = df.apply(lambda row: pvgm(row[1]), axis=1)
df['Pintrest'] = df.apply(lambda row: pintrest(row[1]), axis=1)
df['Post-Type-Switcher'] = df.apply(lambda row: postTypeSwitcher(row[1]), axis=1)
df['Simple-Mathjax'] = df.apply(lambda row: simpleMathjax(row[1]), axis=1)
df['Subscribe-By-Email'] = df.apply(lambda row: subscribeByEmail(row[1]), axis=1)
df['Guest-Post-Submit'] = df.apply(lambda row: guestPostSubmit(row[1]), axis=1)
df['Tumblr'] = df.apply(lambda row: tumblr(row[1]), axis=1)
df['User-Submitted-Posts'] = df.apply(lambda row: usp(row[1]), axis=1)
df['Accessiblity'] = df.apply(lambda row: accessibility(row[1]), axis=1)
df['Pro-Quiz'] = df.apply(lambda row: proQuiz(row[1]), axis=1)
df['Recaptcha'] = df.apply(lambda row: recaptcha(row[1]), axis=1)
df['Post-Votes'] = df.apply(lambda row: postVotes(row[1]), axis=1)
df['Google-Maps'] = df.apply(lambda row: googleMaps(row[1]), axis=1)
df['YOP-Poll'] = df.apply(lambda row: yopPoll(row[1]), axis=1)
df['Zotpress'] = df.apply(lambda row: zotPress(row[1]), axis=1)

#TODO: sum of activated plugins for each site

#parse jetpack modules to get active modules
df['jetpack_raw'] = df['jetpack_raw'].astype(str)

#check if jetpack is active and record to new column
def jetpackActive(s):
    if s == 'None':
        return 1
    else:
        return 0

df['jetpack-active'] = df.apply(lambda row: jetpackActive(row[3]), axis=1)

#check if each module is active

def tg(s):
    if 'tiled-gallery' in s:
        return 1
    else:
        return 0
    
df['tiled-gallery'] = df.apply(lambda row: tg(row[3]), axis=1)

def sd(s):
    if 'sharedaddy' in s:
        return 1
    else:
        return 0

df['sharing'] = df.apply(lambda row: sd(row[3]), axis=1)

def wg(s):
    if 'widgets' in s:
        return 1
    else:
        return 0
    
df['widgets'] = df.apply(lambda row: wg(row[3]), axis=1)

def lx(s):
    if 'latex' in s:
        return 1
    else:
        return 0
    
df['latex'] = df.apply(lambda row: lx(row[3]), axis=1)

def gh(s):
    if 'gravatar-hovercards' in s:
        return 1
    else:
        return 0

df['gravatar'] = df.apply(lambda row: gh(row[3]), axis=1)

def cr(s):
    if 'carousel' in s:
        return 1
    else:
        return 0

df['carousel'] = df.apply(lambda row: cr(row[3]), axis=1)

def wv(s):
    if 'widget-visibility' in s:
        return 1
    else:
        return 0

df['widgets'] = df.apply(lambda row: wv(row[3]), axis=1)

def css(s):
    if 'custom-css' in s:
        return 1
    else:
        return 0

df['custom-css'] = df.apply(lambda row: css(row[3]), axis=1)

def inf(s):
    if 'infinite-scroll' in s:
        return 1
    else: 
        return 0

df['infinite-scroll'] = df.apply(lambda row: inf(row[3]), axis=1)

def sc(s):
    if 'shortcodes' in s:
        return 1
    else:
        return 0
    
df['shortcodes'] = df.apply(lambda row: sc(row[3]), axis=1)

def cf(s):
    if 'contact-form' in s:
        return 1
    else: 
        return 0
    
df['contact-form'] = df.apply(lambda row: cf(row[3]), axis=1)

def cct(s):
    if 'custom-content-types' in s:
        return 1
    else:
        return 0

df['custom-content'] = df.apply(lambda row: cct(row[3]), axis=1)

def sm(s):
    if 'sitemaps' in s:
        return 1
    else:
        return 0

df['sitemaps'] = df.apply(lambda row: sm(row[3]), axis=1)

def md(s):
    if 'markdown' in s:
        return 1
    else:
        return 0
    
df['markdown'] = df.apply(lambda row: md(row[3]), axis=1)

def vt(s):
    if 'verfication-tools' in s:
        return 1
    else:
        return 0
    
df['verification'] = df.apply(lambda row: vt(row[3]), axis=1)

#drop unnecessary rows
df = df.drop(df.columns[0], axis=1) #this deals with the row created when the df is first declared


#--------------Get blogs info----------------

#load copy of wp_blogs table from localdb
all_sites = pd.read_sql('SELECT * FROM wp_blogs', con=cnx)

#---------------JOIN all the dfs----------------
all_sites['blog_id'] = all_sites['blog_id'].astype(str) #data types need to match
df['blog_id'] = df['blog_id'].astype(str)

#the actual join
site_stats = pd.merge(all_sites, df, how='left', on='blog_id')


site_stats['NetID'] = site_stats['NetID'].astype(str)#data types need to match
users_df['NetID'] = users_df['NetID'].astype(str)
site_stats = pd.merge(site_stats, users_df, how='left', on='NetID')

#-------------Download as CSV---------------
site_stats.to_csv('site_stats_92017')
