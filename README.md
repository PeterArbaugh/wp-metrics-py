# wp-metrics-py

The WordPress multisite database is a pain to pull metrics from.  While there are a few tables which pull all the different sites together (such as `wp_blogs`), most information about each site is stored on a series of site specific tables.  To get information about plugin usage on NYU Web Publishing directly from the database, I wrote this script to cycle through relelvant options tables, pull information from each one, and join to `wp_blogs` for data analysis and visualization.

