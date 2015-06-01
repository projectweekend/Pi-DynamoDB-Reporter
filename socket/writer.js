var util = require( "util" );
var Writable = require( "stream" ).Writable;


module.exports = SocketWriter;


function SocketWriter ( socket, label, interval ) {

    Writable.call( this, { objectMode: true } );

    this._socket = socket;
    this._label = label;
    this._interval = interval;

}

util.inherits( SocketWriter, Writable );

SocketWriter.prototype._write = function( data, enc, next ) {

    try {
        this._socket.emit( this._label, data );
    } catch ( e ) {
        return next( e );
    }

    if ( this._interval ) {
        return setTimeout( next, this._interval );
    }

};
