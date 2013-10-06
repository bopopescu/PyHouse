/* rooms.js
 * 
 * Displays the rooms
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * 	
 */

helpers.Widget.subclass(rooms, 'RoomsWidget').methods(

	function __init__(self, node) {
		//Divmod.debug('---', 'rooms.__init__() was called. - self=' + self + "  node=" + node);
		rooms.RoomsWidget.upcall(self, '__init__', node);
		globals.Rooms.Selected = {};
	},

	/**
	 * @param self is    <"Instance" of undefined.rooms.RoomsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'rooms.cb_widgready() was called. self = ' + self);
			self.hideWidget();
		}
		//Divmod.debug('---', 'rooms.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		Divmod.debug('---', 'rooms.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchRoomData(self, globals.SelectedHouse.Ix);
	},
	function showButtons(self) {
		Divmod.debug('---', 'rooms.showButtons() was called. ');
		self.nodeById('RoomButtonsDiv').style.display = 'block';	
	},
	function hideButtons(self) {
		Divmod.debug('---', 'rooms.hideButtons() was called. ');
		self.nodeById('RoomButtonsDiv').style.display = 'none';		
	},
	function showEntry(self) {
		Divmod.debug('---', 'rooms.showEntry() was called. ');
		self.nodeById('RoomEntryDiv').style.display = 'block';		
	},
	function hideEntry(self) {
		Divmod.debug('---', 'rooms.hideEntry() was called. ');
		self.nodeById('RoomEntryDiv').style.display = 'none';		
	},

	// ============================================================================
	/**
	 * This triggers getting the room data from the server.
	 * The server calls displayRoomButtons with the room info.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchRoomData(self, p_houseIndex) {
		function cb_fetchData(p_json) {
			Divmod.debug('---', 'room.cb_fetchData() was called. ');
			globals.Rooms.Obj = JSON.parse(p_json);
			var l_tab = buildTable(globals.Rooms.Obj, 'handleMenuOnClick', '');
			self.nodeById('RoomTableDiv').innerHTML = l_tab;
		}
		function eb_fetchData(self, p1, p2) {
			//Divmod.debug('---', 'rooms.eb_fetchData() was called. ' + p1 + ' ' + p2);
		}
		//Divmod.debug('---', 'rooms.fetchRoomData() was called.');
        var l_defer = self.callRemote("getRoomData", globals.SelectedHouse.Ix);  // call server @ web_rooms.py
		l_defer.addCallback(cb_fetchData);
		l_defer.addErrback(eb_fetchData);
        return false;
	},

	/**
	 * Event handler for room selection buttons.
	 * 
	 * The user can click on a room button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.Rooms.Selected.Ix = l_ix;
		globals.Rooms.Selected.Name = l_name;
		if (l_ix <= 1000) {
			// One of the rooms buttons.
			var l_obj = globals.Rooms.Obj[l_ix];
			globals.Rooms.Selected.RoomObj = l_obj;
			//Divmod.debug('---', 'rooms.doHandleOnClick(1) was called. ' + l_ix + ' ' + l_name);
			//console.log("rooms.doHandleOnClick() - l_obj = %O", l_obj);
			self.showEntry(self);
			self.hideButtons(self);
			self.fillEntry(self, l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			self.showEntry(self);
			self.hideButtons(self);
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget(self);
		}
	},
	
	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[2];
		//Divmod.debug('---', 'schedules.fillEntry() was called. ' + sched);
		self.nodeById('Name').value = sched.Name;
		self.nodeById('Key').value = sched.Key;
		self.nodeById('Active').innerHTML = buildActiveWidget(sched.Active);
		self.nodeById('Comment').value = sched.Comment;
		self.nodeById('Corner').value = sched.Corner;
		self.nodeById('Size').value = sched.Size;
	},
	function fetchEntry(self) {
        var l_roomData = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : fetchActive('Active'),
			Comment : self.nodeById('Comment').value,
			Corner : self.nodeById('Corner').value,
			Size : self.nodeById('Size').value,
			HouseIx : globals.SelectedHouse.Ix
            }
		return l_roomData;
	},

	/**
	 * Event handler for rooms buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 * 
	 * @param self is   <"Instance" of undefined.rooms.RoomsWidget>
	 * @param p_formNode is the form node
	 */
	function handleDataOnClick(self, p_formNode) {
		function cb_doHandleSubmit(p_json) {
			//Divmod.debug('---', 'rooms.cb_doHandleSubmit() was called.');
			self.showWidget(self);
		}
		function eb_doHandleSubmit(res){
			Divmod.debug('---', 'rooms.eb_doHandleSubmit() was called. res=' + res);
		}
		Divmod.debug('---', 'rooms.doHandleSubmit(1) was called. Self:' + self + '  Node:' + p_formNode);
		console.log('rooms.doHandleSubmit(3) Node=%O', p_formNode);
    	var l_json = JSON.stringify(self.fetchEntry(self));
		Divmod.debug('---', 'rooms.doHandleSubmit(2) was called. JSON:' + l_json);

		// Here we need to find out which submit key was pressed.
		// then dispatch to the proper routine

        var l_defer = self.callRemote("saveRoomData", l_json);  // @ web_schedule
		l_defer.addCallback(cb_doHandleSubmit);
		l_defer.addErrback(eb_doHandleSubmit);
		// return false stops the resetting of the server.
        return false;
	}
);
