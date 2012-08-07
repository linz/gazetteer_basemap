// Assumes that OpenLayers and jquery are loaded before the init function is run.

var gazmap = gazmap || {};

gazmap.config = gazmap.config || 
{
    mapDiv: 'map',
    proxyHost: "",
    mapProjection: "EPSG:3857",
    displayProjection: "EPSG:4326",
    backgroundColor: "#D0E6F4",
    basemapUrl: "http://topobasemap.koordinates.co.nz/v2/gazetteer_basemap/${z}/${x}/${y}.png", 
    labelWfsUrl: "http://wfs.data.linz.govt.nz/3e78150f9b2645228602e113fbc2a586/v/x1154/wfs",
    labelWfsFeatureNS: "http://data.linz.govt.nz/ns/v",
    labelWfsFeatureType: "x1154",
    
    mapCentre: [173,-41],
    mapRestrictedExtent: [[165.5,-48],[179.5,-33.5]],
    mapMinZoom: 5,
    mapMaxZoom: 14,

    basemapOptions: 
    {
        // attribution: "Tiles &copy; LINZ",
        sphericalMercator: true,
        wrapDateLine: false,
        transitionEffect: "resize",
        buffer: 1,
        numZoomLevels: 15
    },

    labelBaseStyle:
    {
        label : "${label}",
        fontColor: "black",
        fontSize: "12px",
        fontFamily: "Arial, helvetica, sans",
        fontWeight: "normal",
        labelOutlineColor: "white",
        labelOutlineWidth: 1
    },

    labelStyleLookup: 
    {
        TWN1: { fontSize: "12px" },
        TWN2: { fontSize: "14px" },
        TWN3: { fontSize: "16px" },
        HYD1: { fontColor: "blue", fontSize: "12px" },
        HYD2: { fontColor: "blue", fontSize: "14px" },
        HYD3: { fontColor: "blue", fontSize: "16px" }
    },

};


gazmap.init = function()
{
    // Read in any extra configuration, loaded by the configuration

    var config=gazmap.config;

    if( 'extra' in config )
    {
        for( k in config.extra )
        { 
            config[k] = config.extra[k];
        }
    }

    // Proxy host - required for the WFS layer
    
    if( config.proxyHost )
    {
        OpenLayers.ProxyHost=config.proxyHost;
    }

    // Coordinate systems

    gazmap.mapProjection = new OpenLayers.Projection(config.mapProjection);
    gazmap.displayProjection = new OpenLayers.Projection(config.displayProjection);

    // Create the basemap layer
    
    // Resolutions and server resolutions to constrain the range of zoom levels:
    
    var baseopts = config.basemapOptions;
    var resolutions=[];
    var serverResolutions=[];
    var res = 156543.03390625;
    for( var zoom = 0; zoom < baseopts.numZoomLevels; zoom++, res /= 2 )
    {
        serverResolutions.push(res);
        if( zoom >= config.mapMinZoom && zoom <= config.mapMaxZoom )
        {
            resolutions.push(res);
        }
    }

    config.basemapOptions.serverResolutions=serverResolutions;
    config.basemapOptions.resolutions=resolutions;

    gazmap.basemap_layer = new OpenLayers.Layer.XYZ (
        "Basemap",
        [config.basemapUrl], 
        config.basemapOptions
    );

    gazmap.zoomOffset = config.mapMinZoom;

    // Create the label layer
    // Labels are styled using the using the base style, with values overridden for
    // each feature based on looking up the style attribute in labelStyleLookup
    
    gazmap.label_style = new OpenLayers.StyleMap( config.labelBaseStyle );
    gazmap.label_style.addUniqueValueRules( 'default', 'style', config.labelStyleLookup );
    
    gazmap.label_wfs = new OpenLayers.Protocol.WFS({
            version: '1.1.0',
            srsName: 'EPSG:3857',
            url: config.labelWfsUrl,
            featureNS: config.labelWfsFeatureNS,
            featureType: config.labelWfsFeatureType
            });
    gazmap.label_filter = new OpenLayers.Filter.Comparison({
        type: OpenLayers.Filter.Comparison.EQUAL_TO,
        property: "zoom_level",
        value: config.mapMinZoom,
        });
    gazmap.label_layer = new OpenLayers.Layer.Vector( "Labels",{
        strategies: [new OpenLayers.Strategy.BBOX()],
        protocol: gazmap.label_wfs,
        filter: gazmap.label_filter,
        wrapDateLine: false,
        styleMap: gazmap.label_style
        });
    var layer = gazmap.label_layer;
    layer.events.register('moveend', layer, function( event ){
        if( event.zoomChanged )
        {
            var zoom = parseInt(layer.map.getZoom())+config.mapMinZoom;
            gazmap.label_filter.value = zoom;
            gazmap.label_layer.refresh({force:true});
        }
    });

    //  Initiallize the map

    gazmap.controls = [
        new OpenLayers.Control.Attribution(),
        new OpenLayers.Control.Navigation({
            dragPanOptions: {
               enableKinetic: true
            }
        }),
        new OpenLayers.Control.PanZoom(),
        new OpenLayers.Control.Permalink({anchor: true}),
        new OpenLayers.Control.LayerSwitcher({'ascending':false})
        ];

    var convertXy=function(xy)
    {
        var pt = new OpenLayers.LonLat(xy);
        return pt.transform(gazmap.displayProjection,gazmap.mapProjection);
    };
    var centrePoint = convertXy( config.mapCentre );
    var extentsBL = convertXy(config.mapRestrictedExtent[0]);
    var extentsTR = convertXy(config.mapRestrictedExtent[1]);
    var mapRestrictedExtent = [extentsBL.lon,extentsBL.lat,extentsTR.lon,extentsTR.lat];

    // Set up the map options
    var gazmapopts = config.mapopts || {};
    gazmapopts.div = config.mapDiv;
    gazmapopts.layers = [gazmap.basemap_layer, gazmap.label_layer];
    gazmapopts.center = centrePoint;
    gazmapopts.zoom = 0;
    gazmapopts.projection = gazmap.mapProjection;
    gazmapopts.displayProjection = gazmap.displayProjection;
    gazmapopts.restrictedExtent=mapRestrictedExtent;
    
    // Create the map
    var map = new OpenLayers.Map(gazmapopts);
    gazmap.map = map;

    gazmap.mapZoomLevel = function()
    {
        return map.getZoom()+gazmap.zoomOffset;
    }

    // Set the map background colour - uses jQuery
    $('.olMap').css({'background-color': config.backgroundColor});
}

