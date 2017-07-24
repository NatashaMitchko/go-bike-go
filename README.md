# Go Bike Go

Inspired by the app [WABA](https://itunes.apple.com/us/app/where-a-bike-at-citibike-nyc/id689093812?mt=8) (where a bike at?), Go Bike Go allows users to quikly find Citibikes on their commute. Users create a profile with their home and work addresses and can easily see bike and dock availability at the endpoints of their commute.

## Setting up the database

The database that is connected to the server is a postgreSQL database with the geospatial extension postGIS. This allows the server to ask questions like "what are the 5 closest bike docks available to me that have bikes available?". Enabling postGIS for this project was as simple as making sure the extension is installed, creating a postgreSQL database and enabling the extension in that database.

```
$ createdb go_bike_go
$ psql go_bike_go
go_bike_go=# CREATE EXTENSION postgis;
```

