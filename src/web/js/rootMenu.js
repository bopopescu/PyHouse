<<<<<<< HEAD

// import Nevow.Athena

/*

// MyModule.MyWidget = Nevow.Athena.Widget.subclass('MyModule.MyWidget');

=======
/* 
 * Add a Twisted plugin which maps your module name onto your JavaScript source file:
 *
 * from nevow import athena
 *
 * myPackage = athena.JSPackage({
 *    'MyModule': '/absolute/path/to/mymodule.js',
 *     })
 *     
 *     
 * In the JavaScript source file (in this case, mymodule.js), import Nevow.Athena:
 */
// import Nevow.Athena


/*
 * Next, subclass the JavaScript Nevow.Athena.Widget class (notice the module name that was defined in the plugin file):
 * 
 * MyModule.MyWidget = Nevow.Athena.Widget.subclass('MyModule.MyWidget');
 */

MyModule.MyWidget = Nevow.Athena.Widget.subclass('MyModule.MyWidget');


/*
>>>>>>> origin/ajax

MyModule.MyWidget = Nevow.Athena.Widget.subclass('MyModule.MyWidget');

Nevow.Athena.Widget.subclass(EchoThing, 'EchoWidget').methods(

	function __XXinit__(self, node) {
        EchoThing.EchoWidget.upcall(self, "__init__", node);
        self.echoWidget = self.nodeByAttribute('name', 'echoElement');
        self.scrollArea = self.nodeByAttribute('name', 'scrollArea');
        self.message = self.nodeByAttribute('name', 'message');
    },  

    function XXdoSay(self) {
        self.callRemote("say", self.message.value);
        self.message.value = ""; 
        return false;
    },
 
    function XXaddText(self, text) {
        var newNode = document.createElement('div');
        newNode.appendChild(document.createTextNode(text));
        self.scrollArea.appendChild(newNode);
        document.body.scrollTop = document.body.scrollHeight;
    });

	function XXsay(self, msg) {
	    self.callRemote("say", msg);
	    // Now show the text to the user somehow...
	}

	function XXhear(self, avatarName, text) {
	    // Here, you'd show the user some text.
	}
*/
<<<<<<< HEAD
	
ChatRoom.MyWidget = Nevow.Athena.Widget.subclass('web_rootMenu.ChatRoom');
	
Nevow.Athena.Widget.subclass(ChatRoom, 'ChatterBox').methods(
=======

rootMenu.MyWidget = Nevow.Athena.Widget.subclass('rootMenu.MyWidget');

	
Nevow.Athena.Widget.subclass(DBKChatRoom, 'ChatterBox').methods(
>>>>>>> origin/ajax

    function __init__(self, node) {
        ChatThing.ChatterWidget.upcall(self, "__init__", node);
        self.chooseBox = self.nodeByAttribute('name', 'chooseBox');
        self.scrollArea = self.nodeByAttribute('name', 'scrollArea');
        self.sendLine = self.nodeByAttribute('name', 'sendLine');
        self.usernameField = self.nodeByAttribute('name', 'username');
        self.userMessage = self.nodeByAttribute('name', 'userMessage');
        self.loggedInAs = self.nodeByAttribute('name', 'loggedInAs');
    },

	function doSetUsername(self) {
        var username = self.usernameField.value;
        self.callRemote("setUsername", username).addCallback(
            function (result) {
                self.chooseBox.style.display = "none";
                self.sendLine.style.display = "block";
                self.loggedInAs.appendChild(document.createTextNode(username));
                self.loggedInAs.style.display = "block";
            });
        return false;
    },

    function doSay(self) {
        self.callRemote("say", self.userMessage.value);
        self.nodeByAttribute('name', 'userMessage').value = "";
        return false;
    },

    function displayMessage(self, message) {
        var newNode = document.createElement('div');
        newNode.appendChild(document.createTextNode(message));
        self.scrollArea.appendChild(newNode);
        document.body.scrollTop = document.body.scrollHeight;
    },

    function displayUserMessage(self, avatarName, text) {
        var msg = avatarName+': '+text;
        self.displayMessage(msg);
    });

<<<<<<< HEAD

// Create the "Class" 
var ChatRoom = {
=======
DBKChatRoom.getColorXX = Nevow.Athena.Widget.subclass('web_rootMenu.DBKChatRoom');

// Create the "Class" 
var DBKChatRoom = {
>>>>>>> origin/ajax
	    type: "macintosh",
	    color: "red",
	    getInfo: function () {
	        return this.color + ' ' + this.type + ' apple';
<<<<<<< HEAD
	    }
	}
=======
	    },

		getColor: function () {
			return this.color;
		}
	};
>>>>>>> origin/ajax
