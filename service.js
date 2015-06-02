var io = require( "socket.io-client" );
var TemperatureStream = require( "./system" ).TemperatureStream;
var SocketWriter = require( "./socket" ).SocketWriter;


var socketServerURL = process.env.SOCKET_SERVER_URL;
if ( !socketServerURL ) {
    console.log( "Environment variable 'SOCKET_SERVER_URL' must be defined" );
    process.exit( 1 );
}


if ( require.main === module ) {

    main();

}


function bailout () {
    process.exit( 1 );
}


function main () {
    var socketServer = io.connect( socketServerURL );
    socketServer.on( "connect", function () {

        var cpuTempMessageLabel = process.env.CPU_TEMP_MESSAGE_LABEL || "cpu_temp";
        var cpuTempReadInterval = process.env.CPU_TEMP_READ_INTERVAL || 5 * 60 * 1000;

        var temperature = new TemperatureStream();
        temperature.on( "error", bailout );

        var socket = new SocketWriter( socketServer, cpuTempMessageLabel, cpuTempReadInterval );
        socket.on( "error", bailout );

        temperature.pipe( socket );

    } );
}
