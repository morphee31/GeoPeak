# GeoPeak

GeoPeak is a simple web service for storing and retrieving moutain peaks. 

It uses the **python** web framework **Django** and a database **PostgreSQL**.

It implements the following features:
- models/db tables for storing a peak location and attribute: lat, lon, altitude, name
- REST api endpoints to :
    * create/read/update/delete a peak
    * retrieve a list of peaks in a given geographical bounding box
- add an api/docs url to allow viewing the documentation of the api and send requests on endpoints
- add an html/javascript page to view the peaks on a map (use opensource packages : **[Plotly](https://plotly.com/)**)
- deploy all this stack using docker and docker-compose
- 
## Deployment 



### Get project
```
git clone https://github.com/morphee31/GeoPeak.git
```


### Development server
To deploy and run development server :
```docker
cd MFI_GeoPeak
docker-compose up -d --build
```

To display server logs : 
```docker
docker-compose logs -f
```

URL server : [localhost:8000](http://localhost:8000)

### Production server

Config server file : [.env.dev]()
To deploy and run production server :
```docker
cd MFI_GeoPeak
docker-compose -f docker-compose.prod.yml up -d --build
```

To display server logs : 
```docker
docker-compose -f docker-compose.prod.yml logs -f
```

URL server : [localhost:1337](http://localhost:1337)
