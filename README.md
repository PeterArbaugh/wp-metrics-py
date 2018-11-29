# wp-metrics-py

This is an expanding collection of scripts I wrote to deal with data from a very large WordPress multisite instance.

## wp_accessibility_diff.py

This is a simple script for data wrangling and can be used to compare data from multiple WP metrics reports in the same csv.

## wp_site_stats.py

The WordPress multisite database is a pain to pull metrics from.  While there are a few tables which pull all the different sites together (such as `wp_blogs`), most information about each site is stored on a series of site specific tables.  To get information about plugin usage on NYU Web Publishing directly from the database, I wrote this script to cycle through relelvant options tables, pull information from each one, and join to `wp_blogs` for data analysis and visualization.

This script has been replaced by a new process which can give us more complete data on a regular basis.

## AY 2018 Report - Public

This is the code used to produce metrics and visualizations for the yearly Web Publishing Product report.  No dataframes are visualized in this report for reasons of privacy.

## Inaccessible site count

A notebook to pull basic numbers about inaccessible sites in the system.  Recycles a lot of code used in the AY2018 Report.

## Plugins mail merge

A sample script to build list of plugins activated (on some site) by a given site owner.  Built for input into Lyris. This was complicated by the fact that users have varying numbers of plugins they need to be aware of.
