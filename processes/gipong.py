from pywps.Process import WPSProcess  
from osgeo import ogr
import os
import StringIO
import logging
import geojson

class Process(WPSProcess):


    def __init__(self):

        ##
        # Process initialization
        WPSProcess.__init__(self,
            identifier = "gipong",
            title="gipong process",
            abstract="""This is demonstration process of PyWPS, convert geojson to kml.""",
            version = "1.0",
            storeSupported = True,
            statusSupported = True)

        ##
        # Adding process inputs
        
        self.dataIn = self.addComplexInput(identifier="data",
                    title="Input geojson data",
                    formats = [{
                        'mimeType': 'text/plain',
                        'encoding': 'iso-8859-2',
                        'schema': None
                        }])

        #self.textIn = self.addLiteralInput(identifier="text",
        #            title = "Some width")

        ##
        # Adding process outputs

        self.dataOut = self.addComplexOutput(identifier="output",
                title="Output geojson data",
                formats =  [{'mimeType':'text/xml'}])

        #self.textOut = self.addLiteralOutput(identifier = "text",
        #        title="Output literal data")

    ##
    # Execution part of the process
    def execute(self):
        geojsonFile = self.dataIn.getValue()
        geojsonData = open(geojsonFile, 'r')

        f = open('/var/www/testfile1117.geojson', 'w')
        f.write(geojsonData.read())
        f.close()

        f = open('/var/www/testfile1117.geojson', 'r')
        feature = geojson.loads(f.read())
        geometry = feature['geometry']
        featureType = geometry['type']
        geoinfo = ''
        if featureType == "Point":
            geoinfo = '\
            <Point>\
              <coordinates>'+str(geometry['coordinates'][0])+','+str(geometry['coordinates'][1])+'</coordinates>\
            </Point>'

        if featureType == "LineString":
            coordinates = ''
            for i in range(len(geometry['coordinates'])):
                coordinates += (str(geometry['coordinates'][i][0])+','+str(geometry['coordinates'][i][1])+' ')
            geoinfo = '\
            <LineString>\
              <coordinates>'+coordinates+'</coordinates>\
            <LineString>'

        if featureType == "Polygon":
            coordinates = ''
            for i in range(len(geometry['coordinates'])):
                coordinates += (str(geometry['coordinates'][i][0])+','+str(geometry['coordinates'][i][1])+' ')
            geoinfo = '\
            <Polygon>\
              <coordinates>'+coordinates+'</coordinates>\
            </Polygon>'
        
        f.close()
        kmltemplate = '\
        <?xml version="1.0" encoding="UTF-8"?>\
        <kml xmlns="http://www.opengis.net/kml/2.2">\
          <Placemark>\
            <name>wps output test</name>\
            <description>geojson to kml test</description>\
            '+geoinfo+'\
          </Placemark>\
        </kml>'
        f2 = open('/var/www/testfile1117_1.kml', 'w')
        f2.write(kmltemplate)
        f2.close()


        
        # just copy the input values to output values
        self.dataOut.setValue(StringIO.StringIO(kmltemplate))
        #self.dataOut.setValue(self.dataIn.getValue())

        return

    