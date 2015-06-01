var exec = require( "child_process" ).exec;
var util = require( "util" );
var Readable = require( "stream" ).Readable;


module.exports = TemperatureStream;


var TemperatureStream = function () {

    Readable.call( this, { objectMode: true } );

};

util.inherits( TemperatureStream, Readable );


TemperatureStream.prototype._read = function () {

    var _this = this;

    function onData ( err, data ) {

        if ( err ) {
            throw err;
        }

        _this.push( data );

    }

    _this._readCPUTemperature( onData );

};

TemperatureStream.prototype._readCPUTemperature = function( done ) {

    exec( "vcgencmd measure_temp", function ( err, stdout ) {

        if ( err ) {
            return done( err );
        }

        var match = stdout.match(/\d+\.\d+|\d+/);
        if ( !match ) {
            return done( new Error( "No temp in stdout: " + stdout ) );
        }

        var tempC = parseFloat( match[ 0 ] );
        var tempF = tempC * (9/5) + 32;

        return done( null, {
            celsius: tempC,
            fahrenheit: tempF
        } );

    } );

};
