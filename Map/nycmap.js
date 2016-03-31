// This javascript is used by nycmap.html
// This article in Chinese gives some explanations:
// http://newtoypia.blogspot.tw/2014/08/osm-mashup.html

$( function () {
 //AirNow PM10 Map
  var NoiseStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({
        color: 'rgba(72, 61, 139, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [128, 255, 255, 1],
        width: 1
      })
    })
  });

  var NoiseSource = new ol.source.Vector({
    url:'data/Noise.geojson',
    format: new ol.format.GeoJSON()
  });

  var NoiseVector = new ol.layer.Vector({
    title: "Noise Source",
    source: NoiseSource,
    style: NoiseStyle
  });


  //AirNow PM10 Map
  var AN_PM10Style = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 3,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [128, 255, 255, 1],
        width: 1
      })
    })
  });

  var AN_PM10Source = new ol.source.Vector({
    url:'data/AirNow_PM10.geojson',
    format: new ol.format.GeoJSON()
  });

  var AN_PM10Vector = new ol.layer.Vector({
    title: "AN_PM10 Stations",
    source: AN_PM10Source,
    style: AN_PM10Style
  });

  //Air Now PM2.5 Map
  var AN_PM2_5Style = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 4,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [102, 102, 102, 1],
        width: 1
      })
    })
  });

  var AN_PM2_5Source = new ol.source.Vector({
    url:'data/AirNow_PM2_5.geojson',
    format: new ol.format.GeoJSON()
  });

  var AN_PM2_5Vector = new ol.layer.Vector({
    title: "AN_PM2.5 Stations",
    source: AN_PM2_5Source,
    style: AN_PM2_5Style
  });

  //PM2.5 Map
  var AQS_PM2_5Style = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [102,0, 102,1],
        width: 1
      })
    })
  });

  var AQS_PM2_5Source = new ol.source.Vector({
    url:'data/AQS_PM2_5.geojson',
    format: new ol.format.GeoJSON()
  });

  var AQS_PM2_5Vector = new ol.layer.Vector({
    title: "AQS_PM2.5 Stations",
    source: AQS_PM2_5Source,
    style: AQS_PM2_5Style
  });

  //POI Map
  var POIStyle = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [0.5, 46],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      opacity: 0.95,
      src: 'data/poi.png'
    })),
    stroke: new ol.style.Stroke({
      color: [128,255,255,1],
      width: 1
    })
  });

  var POISource = new ol.source.Vector({
    url:'data/POI.geojson',
    format: new ol.format.GeoJSON()
  });

  var POIVector = new ol.layer.Vector({
    title: "POI Stations",
    source: POISource,
    style: POIStyle
  });

  //Bike Map
  var BikeStyle = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [0.5, 46],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      opacity: 0.95,
      src: 'data/bike.png'
    })),
    stroke: new ol.style.Stroke({
      color: [102,102,102,1],
      width: 1
    })
  });

  var BikeSource = new ol.source.Vector({
    url:'data/bike.geojson',
    format: new ol.format.GeoJSON()
  });

  var BikeVector = new ol.layer.Vector({
    title: "Bike Stations",
    source: BikeSource,
    style: BikeStyle
  });
/*
  //ASOS Precipitation Map
  var ASOS_PreciStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 3,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [139, 58, 58, 1],
        width: 1
      })
    })
  });

  var ASOS_PreciSource = new ol.source.Vector({
    url:'data/ASOS_Preci.geojson',
    format: new ol.format.GeoJSON()
  });

  var ASOS_PreciVector = new ol.layer.Vector({
    title: "ASOS_Precitation Stations",
    source: ASOS_PreciSource,
    style: ASOS_PreciStyle
  });
*/
  //GSOD Weather Map
  var GSOD_WeatherStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 3,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [255, 255, 0, 1],
        width: 1
      })
    })
  });

  var GSOD_WeatherSource = new ol.source.Vector({
    url:'data/GSOD_obs.geojson',
    format: new ol.format.GeoJSON()
  });

  var GSOD_WeatherVector = new ol.layer.Vector({
    title: "GSOD_Weather Stations",
    source: GSOD_WeatherSource,
    style: GSOD_WeatherStyle
  });

  //QCLCD Weather Map
  var QCLCD_WeatherStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 4,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [139, 0, 0, 1],
        width: 1
      })
    })
  });

  var QCLCD_WeatherSource = new ol.source.Vector({
    url:'data/QCLCD_obs.geojson',
    format: new ol.format.GeoJSON()
  });

  var QCLCD_WeatherVector = new ol.layer.Vector({
    title: "QCLCD_Weather_ Stations",
    source: QCLCD_WeatherSource,
    style: QCLCD_WeatherStyle
  });

  //Thermometer
  var ThermoStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 2,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [102,0,102,1],
        width: 1
      })
    })
  });

  var ThermoSource = new ol.source.Vector({
    url:'data/thermometer.geojson',
    format: new ol.format.GeoJSON()
  });

  var ThermoVector = new ol.layer.Vector({
    title: "Thermometer",
    source: ThermoSource,
    style: ThermoStyle
  });

  //Hygrometer
  var HygroStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 3,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [0,102,102,1],
        width: 1
      })
    })
  });

  var HygroSource = new ol.source.Vector({
    url:'data/hygrometer.geojson',
    format: new ol.format.GeoJSON()
  });

  var HygroVector = new ol.layer.Vector({
    title: "Hygrometer",
    source: HygroSource,
    style: HygroStyle
  });

  //Anemometer
  var AnemoStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 4,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [0,0,255,1],
        width: 1
      })
    })
  });

  var AnemoSource = new ol.source.Vector({
    url:'data/anemometer.geojson',
    format: new ol.format.GeoJSON()
  });

  var AnemoVector = new ol.layer.Vector({
    title: "Anemometer",
    source: AnemoSource,
    style: AnemoStyle
  });

  //Barometer
  var BaroStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 1)'
      }),
      stroke: new ol.style.Stroke({
        color: [128,0,0,1],
        width: 1
      })
    })
  });

  var BaroSource = new ol.source.Vector({
    url:'data/barometer.geojson',
    format: new ol.format.GeoJSON()
  });

  var BaroVector = new ol.layer.Vector({
    title: "Barometer",
    source: BaroSource,
    style: BaroStyle
  });

  //Defualt Style for Bundary
  var Bunstyle = new ol.style.Style({
    fill: new ol.style.Fill({
      color: 'rgba(255, 255, 255, 0.1)'
    }),
    stroke: new ol.style.Stroke({
      color: '#000000',
      width: 1
    })
  });

  //New York Boundary
  var BunSource = new ol.source.Vector({
    url:'data/nyc_boundary.geojson',
    format: new ol.format.GeoJSON()
  });

  var BunVector = new ol.layer.Vector({
    title: "NYC_Boundary",
    source: BunSource,
    style: Bunstyle
  });

  //New York District
  var DistSource = new ol.source.Vector({
    url:'data/nyccb2015.geojson',
    format: new ol.format.GeoJSON()
  });

  var DistVector = new ol.layer.Vector({
    title: "NYC_District",
    source: DistSource,
    style: Bunstyle
  });

    //Base Map
  var osm =  new ol.layer.Tile({ 
    title: 'BaseMap',
    source: new ol.source.MapQuest({layer: 'osm'}
  )});

  var map = new ol.Map({
    target: "nyc_canvas", 
    layers: [osm, BunVector, DistVector, POIVector, NoiseVector, BikeVector, BaroVector, AnemoVector, HygroVector, ThermoVector, QCLCD_WeatherVector, GSOD_WeatherVector, AQS_PM2_5Vector, AN_PM2_5Vector,AN_PM10Vector],
    view: new ol.View({
        center: ol.proj.fromLonLat([-74.0059,40.7127]),
        zoom: 10
    })  
    // eventListeners: {
    //   featureover: onHoverMarker,
    //   featureout: onLeaveMarker,
    //   featureclick: onClickMarker
    // }
  });

  // Define the usage of layerSwitcher
  var layerSwitcher = new ol.control.LayerSwitcher({
    tipLabel: 'SwitchLayer'
  });
  map.addControl(layerSwitcher);  

  console.log(vectorSource.getKeys())

// ll_proj = new OpenLayers.Projection('EPSG:4326'); 
// osm_proj = map.getProjectionObject();
// function ll2osm(lon, lat) {
//     return new OpenLayers.LonLat(lon,lat).transform(ll_proj, osm_proj);
// }
// function pt2osm(lon, lat) {
//     return new OpenLayers.Geometry.Point(lon,lat).transform(ll_proj, osm_proj);
// }

// map.setCenter(ll2osm(120.97, 23.7), 7);
// $.ajax({
//   url: "../data/airports.json",
//   async: false,
//   success: function(data, textStatus) { airport_db = data; },
//   error: function() { alert("json file '../data/airports.json' read error or format error"); }
// });

// marker_layer = map.getLayersByName("Markers")[0];
// console.log("airport_db length: " + airport_db.length);
// for (i=0; i<airport_db.length; ++i) {
//   one_airport = airport_db[i];
//   coord = pt2osm(one_airport.lon, one_airport.lat),
//   one_airport.marker = new OpenLayers.Feature.Vector(coord,
//     { airport_info: one_airport },
//     { externalGraphic: '../data/airports.png', graphicHeight: 30, graphicWidth: 30,
//       graphicXOffset:-15, graphicYOffset:-15  }
//   );
//   marker_layer.addFeatures(one_airport.marker);
// }

// function onHoverMarker(e) {
//   marker = e.feature;
//   marker.renderIntent = "select";
//   marker.layer.drawFeature(marker);
//   one_airport = marker.attributes.airport_info;
//   html_info = one_airport.name + " 代號 <i>"
//     + one_airport.id + "</i>";
//   marker.attributes.popup = new OpenLayers.Popup.FramedCloud(
//     one_airport.id,
//     marker.geometry.getBounds().getCenterLonLat(),
//     new OpenLayers.Size(100,100), html_info,
//     null, true, null
//   );
//   map.addPopup(marker.attributes.popup, true);
// }

// function onLeaveMarker(e) {
//   marker = e.feature;
//   marker.renderIntent = "default";
//   marker.layer.drawFeature(marker);
//   marker.attributes.popup.destroy();
// }

// function onClickMarker(e) {
//   marker = e.feature;
//   one_airport = marker.attributes.airport_info;
//   html_info = 
//     "<strong>機場代號</strong>:" + one_airport.id +
//     "<br /><strong>機場名稱</strong>:" + one_airport.name +
//     "<br /><strong>所在城市</strong>:" + one_airport.city +
//     "<br /><strong>所在國家</strong>:" + one_airport.country;
//   $("#details").html(html_info);
// }


});

