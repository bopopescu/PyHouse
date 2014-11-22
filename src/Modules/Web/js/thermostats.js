/**
 * @name: PyHouse/src/Modules/Web/js/thermostats.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Sep 03, 2014
 * @summary: Displays the thermostat element
 *
 */


helpers.Widget.subclass(thermostats, 'ThermostatsWidget').methods(

    function __init__(self, node) {
        thermostats.ThermostatsWidget.upcall(self, "__init__", node);
    },



 // ============================================================================
    /**
     * Place the widget in the workspace.
	 *
	 * @param self is    <"Instance" of undefined.thermostats.ThermostatsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			self.hideWidget2(self);
		}
		function eb_widgetready(p_reason) {
			Divmod.debug('---', 'ERROR thermostats.eb_widgetready() - ' + p_reason);
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		l_defer.addErrback(eb_widgetready);
		return l_defer;
	},
	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function startWidget(self) {
		Divmod.debug('---', 'thermostats.startWidget() was called.');
		showSelectionButtons(self);
		hideDataEntry(self);
		self.fetchHouseData();
	},



// ============================================================================
	/**
	 * Build a screen full of buttons - One for each room and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_thermostat_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Thermostats, 'handleSelectButtonOnClick');
		var l_html = build_lcars_top('Thermostats', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_thermostat_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the Thermostat data from the server.
	 * The server calls displayThermostatButtons with the Thermostat info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'thermostats.eb_fetchHouseData() was called. ERROR: ' + res);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_thermostat.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},
	/**
	 * Event handler for Thermostat selection buttons.
	 * 
	 * The user can click on a room button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleSelectButtonOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ThermostatIx = l_ix;
		globals.House.ThermostatName = l_name;
		if (l_ix <= 1000) {  // One of the Thermostat buttons.
			var l_obj = globals.House.HouseObj.Thermostats[l_ix];
			globals.House.ThermostatObj = l_obj;
			globals.House.Self = self;
			showDataEntry(self);
			hideSelectionButtons(self);
			self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
		} else if (l_ix == 10001) {  // The "Add" button
			showDataEntry(self);
			hideSelectionButtons(self);
			var l_ent = self.createEntry();
			self.buildLcarDataEntryScreen(l_ent, 'handleDataOnClick');
		} else if (l_ix == 10002) {  // The "Back" button
			self.hideWidget2(self);
			self.showWidget2('HouseMenu');
		}
	},



// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildBasicPart(self, p_thermostat, p_html, p_onchange){
		Divmod.debug('---', 'thermostats.buildBasicPart() was called.');
		p_html += buildLcarTextWidget(self, 'Name', 'Thermostat Name', p_thermostat.Name);
		p_html += buildLcarTextWidget(self, 'Key', 'Index', p_thermostat.Key, 'disable');
		p_html += buildLcarTrueFalseWidget(self, 'ThermostatActive', 'Active ?', p_thermostat.Active);
		p_html += buildLcarTextWidget(self, 'UUID', 'UUID', p_thermostat.UUID, 'disable');
		p_html += buildLcarHvacSliderWidget(self, 'CoolSetting', 'Cool', p_thermostat.CoolSetPoint, 'handleSliderChangeCool');
		p_html += buildLcarHvacSliderWidget(self, 'HeatSetting', 'Heat', p_thermostat.HeatSetPoint, 'handleSliderChangeHeat');
		p_html += buildLcarFamilySelectWidget(self, 'ControllerFamily', 'Family', p_thermostat.ControllerFamily, p_onchange);
		return p_html
	},
	function handleSliderChangeCool(p_event){
		Divmod.debug('---', 'thermostats.handleSliderChangeCool() was called.');
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'CoolSetting');
		updateSliderBoxValue(l_self, 'CoolSetting', l_level);
	},
	function handleSliderChangeHeat(p_event){
		Divmod.debug('---', 'thermostats.handleSliderChangeHeat() was called.');
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'HeatSetting');
		updateSliderBoxValue(l_self, 'HeatSetting', l_level);
	},
	function buildInsteonPart(self, p_thermostat, p_html) {
		Divmod.debug('---', 'thermostats.buildInsteonPart() was called.');
		p_html += buildLcarTextWidget(self, 'InsteonAddress', 'Insteon Address', p_thermostat.InsteonAddress);
		p_html += buildLcarTextWidget(self, 'DevCat', 'Dev Cat', p_thermostat.DevCat);
		p_html += buildLcarTextWidget(self, 'GroupNumber', 'Group Number', p_thermostat.GroupNumber);
		p_html += buildLcarTextWidget(self, 'GroupList', 'Group List', p_thermostat.GroupList);
		p_html += buildLcarTrueFalseWidget(self, 'Master', 'Master ?', p_thermostat.IsMaster);
		p_html += buildLcarTrueFalseWidget(self, 'Controller', 'Controller ?', p_thermostat.IsController);
		p_html += buildLcarTrueFalseWidget(self, 'Responder', 'Responder ?', p_thermostat.IsResponder);
		p_html += buildLcarTextWidget(self, 'ProductKey', 'Product Key', p_thermostat.ProductKey);
		return p_html;
	},
	function buildUpbPart(self, p_thermostat, p_html) {
		Divmod.debug('---', 'thermostats.buildUpbPart() was called.');
		p_html += buildLcarTextWidget(self, 'UPBAddress', 'UPB Address', p_thermostat.UPBAddress);
		p_html += buildLcarTextWidget(self, 'Password', 'UPB Password', p_thermostat.UPBPassword);
		p_html += buildLcarTextWidget(self, 'NetworkID', 'UPB Network', p_thermostat.UPBNetworkID);
		return p_html;
	},
	function buildAllParts(self, p_thermostat, p_html, p_handler, p_onchange) {
		Divmod.debug('---', 'thermostats.buildAllParts() was called - family: ' + p_thermostat.ControllerFamily);
		p_html = self.buildBasicPart(p_thermostat, p_html, p_onchange);
		if (p_thermostat.ControllerFamily == 'Insteon') {
			p_html = self.buildInsteonPart(p_thermostat, p_html);
		}
        if (p_thermostat.ControllerFamily == 'UPB') {
        	p_html = self.buildUpbPart(p_thermostat, p_html);
        }
		p_html += buildLcarEntryButtons(p_handler);
		return p_html;
	},
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		var l_thermostat = arguments[1];
		Divmod.debug('---', 'thermostats.buildLcarDataEntryScreen() was called.');
		console.log("thermostats.buildLcarDataEntryScreen() - Thermo = %O", l_thermostat);
		var l_html = "";
		var l_data_html = "";
		l_data_html = self.buildAllParts(l_thermostat, l_data_html, p_handler, 'familyChanged');
		var l_html = build_lcars_top('Thermostat Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(25, l_data_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function familyChanged() {
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		Divmod.debug('---', 'thermostats.familyChanged was called !!!');
		// console.log("thermostats.buildLcarDataEntryScreen() - light %O", l_obj);
		// console.log("thermostats.buildLcarDataEntryScreen() - l_self %O", l_self);
		var l_family = fetchSelectWidget(l_self, 'LightFamily');
		l_obj.ControllerFamily = l_family;
		l_self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
	},



// ============================================================================
	function fetchEntry(self) {
        var l_data = {
            Name      : fetchTextWidget(self, 'Name'),
            Key       : fetchTextWidget(self, 'Key'),
			Active    : fetchTrueFalseWidget(self, 'ThermostatActive'),
			UUID      : fetchTextWidget(self, 'UUID'),
			ControllerFamily : fetchSelectWidget(self, 'ControllerFamily'),
			CoolSetPoint : fetchSliderWidget(self, 'CoolSetting'),
			HeatSetPoint : fetchSliderWidget(self, 'HeatSetting'),
			Delete : false
            };
        if (l_data.ControllerFamily === 'Insteon') {
        	l_data = self.fetchInsteonEntry(l_data);
        }
        if (l_data.ControllerFamily === 'UPB') {
        	l_data = self.fetchUpbEntry(l_data);
        }
		return l_data;
	},
	function fetchInsteonEntry(self, p_data) {
        p_data.InsteonAddress = fetchTextWidget(self, 'InsteonAddress');
        p_data.DevCat = fetchTextWidget(self, 'DevCat');
        p_data.GroupNumber = fetchTextWidget(self, 'GroupNumber');
        p_data.GroupList = fetchTextWidget(self, 'GroupList');
        p_data.IsMaster = fetchTrueFalseWidget(self, 'Master');
        p_data.IsResponder = fetchTrueFalseWidget(self, 'Responder');
        p_data.IsController = fetchTrueFalseWidget(self, 'Controller');
        p_data.ProductKey = fetchTextWidget(self, 'ProductKey');
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
        p_data.UPBAddress = fetchTextWidget(self, 'UPBAddress');
        p_data.UPBPassword = fetchTextWidget(self, 'Password');
        p_data.UPBNetworkID = fetchTextWidget(self, 'NetworkID');
		return p_data;
	},
	function createEntry(self, p_ix) {
		var l_key = 0;
		if (globals.House.HouseObj.Thermostats !== 'undefined')
			l_key = Object.keys(globals.House.HouseObj.Thermostats).length;
        var l_Data = {
    			Name : 'Change Me',
    			Key : l_key,
    			Active : false,
    			CoolSetPoint : 80,
    			HeatSetPoint : 65,
    			ControllerFamily : 'Insteon',
    			InsteonAddress :	'99.88.77',
    			DevCat :			'0',
    			Delete : false
                };
		return l_Data;
	},



// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'thermostats.cb_handleDataOnClick() was called.');
			// self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'thermostats.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		var l_defer;
		var l_json;
		//Divmod.debug('---', 'thermostats.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	l_json = JSON.stringify(self.fetchEntry());
	        l_defer = self.callRemote("saveThermostatsData", l_json);  // @ web_thermostat
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideDataEntry();
			self.showSelectionButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
	        l_defer = self.callRemote("saveThermostatsData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			break;
		}
        return false;  // false stops the chain.
	}
);
// Divmod.debug('---', 'thermostats.startWidget() was called.');
// console.log("thermostats.handleSelectButtonOnClick() - l_obj = %O", l_obj);
//### END DBK
