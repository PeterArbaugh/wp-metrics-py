# Import pandas
import pandas as pd

#Load csv files
#Old data
old_df = pd.read_csv('OLD CSV FILENAME')

#New data
new_df = pd.read_csv('NEW CSV FILENAME')

# Drop unnecessary columns from old_df
old_cols = ['blog_id', 'privacy descr', 'current_theme', 'admin users']
old_df = old_df[old_cols]

# Rename columns
old_df.columns = ['blog_id', 'prior privacy', 'prior theme', 'prior admin users']

# Merge tables on blog_id
final_df = pd.merge(new_df, old_df, on='blog_id')

# Reorder columns so old and new data columns are adjacent
final_df = final_df[['blog_id',
 'blog_name',
 'blog_description',
 'siteurl',
 'blog_url',
 'prior privacy',
 'privacy descr',
 'has_accessibility_footer',
 'admin_email',
 'users_count',
 'active_plugins_count',
 'db_version',
 'prior theme',
 'current_theme',
 'custom_css',
 'registered',
 'last_updated',
 'archived',
 'posts_count',
 'pages_count',
 'comments_count',
 'attachments_count',
 'site_type',
 'owner',
 'site owner role',
 'prior admin users',
 'admin users',
 'template',
 'Google Drive embeds (count)',
 'Google Docs embeds (count)',
 'Google Sheets embeds (count)',
 'Google Slides embeds (count)',
 'Google Calendar embeds (count)',
 'Google Groups embeds (count)',
 'Google Hangouts embeds (count)',
 'Google Sites embeds (count)',
 'NYU Stream embeds (count)']]

# Export to csv
final_df.to_csv('WP_Accessibility_Diff.csv')
