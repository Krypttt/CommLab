var portNumber = 3000;
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var socketArray = [];
var memberList = [];
// define a dict to map member to id
var memberToId = {};

// return index.html as displaying page whenever connects to server from browser
app.get('/',function(req, res){
    res.sendFile(__dirname + '/index.html');
});

// set the server to listen on port 3000
http.listen(portNumber,function(){
    console.log('listening on *:' + portNumber);
});


// io --> socket manager on server
io.on('connection',function(socket){
    // set the nickname and link the nickname to id
    socket.on('set nickname', function(nickname) {
        console.log("nickname set: " + nickname)
        socket.nickname = nickname;
        memberToId[socket.nickname] = socket.id
        console.log(nickname + ' just connected!');
        if (memberList.indexOf(socket.nickname) == -1) {
            memberList[memberList.length] = socket.nickname
	    }
	    io.emit('member list', memberList)
	    console.log(memberList);
	    io.emit('show message on screen', socket.nickname+" has entered the chat")
    });
    // append socket to the socket list
    socketArray[socketArray.length] = socket;
    console.log('socket count: ' + socketArray.length);
    // define a listener for user send out message events
    socket.on('user send out message', function(msg){          
        //only send message back to the client of this socket ( with event string 'show message on screen' )
        //socket.emit('show message on screen', '== server got your message == : '+ msg);
        // to the sender
        socket.emit('show message on screen', msg);
        
        //broadcast to everyone include the client of this socket ( with event string 'event string' ), you can define 'event string' your self
        //io.emit('event string', '== server to every client == ' + msg);
        
        //broadcast to everyone except for the client of this socket ( with event string 'event string' ), you can define 'event string' your self
        // to everyone else
        socket.broadcast.emit('event string', msg);
    });
    // define a private message listener
    socket.on('private message',function(to, from, msg){
        // if the member is not in the server, throw error back to the sender
	    if (memberToId[to] == undefined){
	  	    socket.emit("show message on screen", "Member Not Found!Check again.")
	    }
	    else{
	  	    // to self
	  	    socket.emit("show message on screen", "PM to " + to + ": " + msg);
	  	    // to target
	  	    socket.broadcast.to(memberToId[to]).emit("show message on screen", "Message from " + from + ": " + msg);
	    }
	});
    // define a disconnect listener
    // cannot put the removal process outside of the if statement or else the member list would be chaotic
    socket.on('disconnect',function(){
		var socketIndex;
		var nicknameIndex;
		for (var i = 0; i < socketArray.length; i++) {
		    //remove the disconnected socket from socketArray
            if (socketArray[i] == socket) {
                socketIndex = i;
				socketArray.splice(socketIndex, 1);
				console.log('socket count: ' + socketArray.length);
			}
            //remove the disconnected member from memberList
			if (memberList[i] == socket.nickname) {
				nicknameIndex = i;
				memberList.splice(nicknameIndex, 1);
				console.log(memberList)
				io.emit("show message on screen", socket.nickname + " has left the chat")
                //update all clients' member list
				io.emit('member list', memberList);
			}
		}
	});
});
